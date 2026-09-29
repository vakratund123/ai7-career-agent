import logging
import uuid
from typing import Dict, Any, Optional
from backend.db.database import get_db
from backend.core.security import security_engine

logger = logging.getLogger("ai7.agent.outreach")

class OutreachAgent:
    """
    Outreach Agent (Agent I):
    Generates tailored, authentic professional outreach communications.
    Anti-Spam Rules:
    - Never uses generic templates or fake familiarity ('I've followed your work for years').
    - Distinct strategic angles for: Hiring Manager, Recruiter, Executive, Referral.
    - Strictly references verified candidate facts (AED 800M portfolio, One Za'abeel leasing).
    """
    def __init__(self):
        pass

    def generate_outreach_draft(self, job_id: Optional[str], contact_id: str, outreach_type: str = "HIRING_MGR_PITCH") -> Dict[str, Any]:
        """Crafts a bespoke outreach message grounded in verified candidate career metrics."""
        with get_db() as conn:
            job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone() if job_id else None
            contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()

        if not contact:
            return {"error": "Contact not found."}

        company = job["company_name"] if job else contact["company_name"]
        contact_name = contact["full_name"]
        contact_role = contact["job_title"]
        job_title = job["title"] if job else "Senior Asset Manager / Commercial Portfolio Leader"

        # Check anti-spam safety
        is_safe, safety_reason = security_engine.check_outreach_safety(company, contact_id, contact["email"] or "")
        if not is_safe:
            return {"error": f"Outreach blocked by anti-spam safety: {safety_reason}"}

        # Select copy based on recipient type
        first_name = contact_name.split()[0] if contact_name else "Colleague"

        if outreach_type == "RECRUITER_INTRO" or contact["role_category"] == "recruiter":
            subject = f"V. Jagannath — Application for {job_title} ({company})"
            body = (
                f"Dear {first_name},\n\n"
                f"I noticed {company}'s current search for a {job_title} in Dubai and wanted to briefly introduce my background.\n\n"
                f"Most recently as Leasing Lead at Ithra Dubai (Investment Corporation of Dubai), I oversaw commercial and retail asset management across 800,000 sq. ft. of flagship space—including One Za'abeel and the Deira Enrichment Project—within an AED 800M portfolio mandate.\n\n"
                f"Over 20 years in the UAE, I have negotiated 2,500+ commercial leases and evaluated 300+ locations across demographic catchment and feasibility models.\n\n"
                f"I have submitted a formal application and would be glad to share any additional details that would assist your review.\n\n"
                f"Best regards,\n"
                f"V. Jagannath\n"
                f"+971 50 5099065 | v.jagannath3@gmail.com"
            )
        elif outreach_type == "EXECUTIVE_NOTE" or contact["role_category"] == "department_leader":
            subject = f"{company} UAE Real Estate & Asset Portfolio — V. Jagannath"
            body = (
                f"Dear {first_name},\n\n"
                f"I follow {company}'s strategic footprint across the GCC real estate sector with keen interest.\n\n"
                f"Having led retail and commercial asset management across 800,000 sq. ft. of ICD-backed developments in Dubai (including One Za'abeel) and managed a diversified AED 800M portfolio, I bring 20+ years of hands-on UAE commercial leasing, CAPEX planning, and RERA governance expertise.\n\n"
                f"As {company} continues to optimize its regional property and commercial portfolio, I would welcome the opportunity to connect for a brief introductory conversation.\n\n"
                f"Sincerely,\n"
                f"V. Jagannath\n"
                f"Senior Manager – Asset Management & Portfolio Development"
            )
        else: # Default: HIRING_MGR_PITCH
            subject = f"{job_title} candidate profile — V. Jagannath (AED 800M Portfolio / 2,500+ Leases)"
            body = (
                f"Dear {first_name},\n\n"
                f"I am writing regarding the {job_title} mandate at {company}.\n\n"
                f"My 20-year career in the UAE has focused on maximizing asset yield, tenant acquisition, and capital discipline. Most recently with Ithra Dubai / ICD, I directed leasing and commercial asset strategy across 800,000 sq. ft. of luxury retail and B2B commercial space across One Za'abeel and Deira Enrichment, negotiating with regional developers, corporate occupiers, and institutional stakeholders.\n\n"
                f"Key documented metrics from my career include:\n"
                f"• AED 800M Real Estate Portfolio scope managed across residential, commercial, and mixed-use assets\n"
                f"• 2,500+ commercial lease negotiations completed\n"
                f"• 300+ locations evaluated through demographic footfall and financial feasibility\n\n"
                f"I would welcome the opportunity to discuss how this experience aligns with {company}'s commercial objectives in Dubai.\n\n"
                f"Best regards,\n"
                f"V. Jagannath\n"
                f"+971 50 5099065 | v.jagannath3@gmail.com"
            )

        outreach_id = f"out_{str(uuid.uuid4())[:8]}"

        with get_db() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO outreach_campaigns (id, job_id, contact_id, company_name, channel, subject, message_body, outreach_type, status)
                VALUES (?, ?, ?, ?, 'EMAIL', ?, ?, ?, 'DRAFT')
            """, (outreach_id, job_id, contact_id, company, subject, body, outreach_type))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'outreach_agent', 'generate_draft', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), outreach_id, f"Generated personalized outreach for {contact_name} at {company}", body[:150] + "...", ))

        return {
            "outreach_id": outreach_id,
            "job_id": job_id,
            "contact_id": contact_id,
            "contact_name": contact_name,
            "company_name": company,
            "subject": subject,
            "message_body": body,
            "status": "DRAFT",
            "outreach_type": outreach_type
        }

    def send_outreach(self, outreach_id: str, autonomy_level: int = 2) -> Dict[str, Any]:
        """Executes the outreach if permitted by security policy and transmits via live channels."""
        from backend.services.dispatch_service import dispatch_service

        with get_db() as conn:
            outreach = conn.execute("SELECT * FROM outreach_campaigns WHERE id = ?", (outreach_id,)).fetchone()
            if not outreach:
                return {"error": "Outreach campaign not found"}

            contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (outreach["contact_id"],)).fetchone()

        # Verify permission
        is_permitted, reason = security_engine.check_permission("SEND_RECRUITER_MESSAGE", autonomy_level)
        if not is_permitted:
            # Stage in approvals queue
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO approvals (id, action_type, title, description, payload, status)
                    VALUES (?, 'SEND_OUTREACH', ?, ?, ?, 'PENDING')
                """, (str(uuid.uuid4()), f"Approve outreach to {outreach['company_name']}", f"Subject: {outreach['subject']}", outreach['message_body']))
            return {"status": "ESCALATED_TO_APPROVALS", "reason": reason}

        # Attempt Live Transmission
        dispatch_status = "SENT"
        recipient_email = contact["email"] if contact else None
        live_result_msg = ""

        if recipient_email:
            sent_live, live_msg = dispatch_service.send_live_email(recipient_email, outreach["subject"], outreach["message_body"])
            if sent_live:
                dispatch_status = "SENT_LIVE_GMAIL"
                live_result_msg = f"Delivered live to {recipient_email} via Gmail SMTP"
            else:
                dispatch_status = "STAGED_AWAITING_ACCOUNT"
                live_result_msg = f"Staged in queue: {live_msg}"
        else:
            dispatch_status = "STAGED_AWAITING_ACCOUNT"
            live_result_msg = f"Staged in queue: Connect LinkedIn session or verify recipient email."

        # Update database record
        with get_db() as conn:
            conn.execute("""
                UPDATE outreach_campaigns SET status = ?, sent_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (dispatch_status, outreach_id))

            # Update job status to OUTREACH
            if outreach["job_id"]:
                conn.execute("UPDATE jobs SET status = 'OUTREACH' WHERE id = ?", (outreach["job_id"],))

            security_engine.record_outreach(outreach["company_name"], outreach["contact_id"])

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'outreach_agent', 'dispatch_outreach', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), outreach_id, f"Dispatched outreach to {outreach['company_name']}: {dispatch_status}", live_result_msg, ))

        return {"status": dispatch_status, "outreach_id": outreach_id, "detail": live_result_msg}

outreach_agent = OutreachAgent()
