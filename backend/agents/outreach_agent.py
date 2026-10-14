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

        # Generate bespoke email and LinkedIn outreach grounded in target company profile
        from backend.agents.company_profiles import generate_tailored_email, generate_tailored_linkedin
        email_data = generate_tailored_email(dict(contact), dict(job) if job else None)
        subject = email_data["subject"]
        body = email_data["body"]
        linkedin_note = generate_tailored_linkedin(dict(contact), dict(job) if job else None)

        outreach_id = f"out_{str(uuid.uuid4())[:8]}"

        clean_job_id = str(job_id).strip() if (job_id and str(job_id).strip()) else None
        with get_db() as conn:
            if clean_job_id:
                job_exists = conn.execute("SELECT 1 FROM jobs WHERE id = ?", (clean_job_id,)).fetchone()
                if not job_exists:
                    clean_job_id = None

            conn.execute("""
                INSERT OR REPLACE INTO outreach_campaigns (id, job_id, contact_id, company_name, channel, subject, message_body, linkedin_note, outreach_type, status)
                VALUES (?, ?, ?, ?, 'EMAIL', ?, ?, ?, ?, 'DRAFT')
            """, (outreach_id, clean_job_id, contact_id, company, subject, body, linkedin_note, outreach_type))

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

    def send_outreach(self, outreach_id: str, autonomy_level: Optional[int] = None) -> Dict[str, Any]:
        """Executes the outreach if permitted by security policy and transmits via live channels."""
        from backend.services.dispatch_service import dispatch_service

        with get_db() as conn:
            outreach = conn.execute("SELECT * FROM outreach_campaigns WHERE id = ?", (outreach_id,)).fetchone()
            if not outreach:
                return {"error": "Outreach campaign not found"}

            contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (outreach["contact_id"],)).fetchone()

            if autonomy_level is None:
                pref = conn.execute("SELECT value FROM preferences WHERE key = 'autonomy_level'").fetchone()
                effective_autonomy = int(pref["value"]) if pref else 1
            else:
                effective_autonomy = autonomy_level

        # Verify permission (Autonomy Level 1 requires explicit human approval)
        is_permitted, reason = security_engine.check_permission("SEND_RECRUITER_MESSAGE", effective_autonomy)
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
        recipient_email = contact["email"].strip() if (contact and contact["email"] and "@" in contact["email"]) else None
        # Only direct personal profile URLs (/in/) can receive InMail/messages
        recipient_linkedin = contact["linkedin_url"].strip() if (contact and contact["linkedin_url"] and "/in/" in contact["linkedin_url"]) else None
        live_result_msg = ""

        # Check integration status
        integrations = dispatch_service.get_integration_status()
        gmail_ready = integrations.get("gmail", {}).get("status") == "CONNECTED"
        linkedin_ready = integrations.get("linkedin", {}).get("status") == "CONNECTED"

        if recipient_email and gmail_ready:
            sent_live, live_msg = dispatch_service.send_live_email(recipient_email, outreach["subject"], outreach["message_body"])
            if sent_live:
                dispatch_status = "SENT_LIVE_GMAIL"
                live_result_msg = f"Delivered live to {recipient_email} via Gmail SMTP"
            else:
                dispatch_status = "STAGED_AWAITING_ACCOUNT"
                live_result_msg = f"Staged in queue: {live_msg}"
        elif recipient_linkedin and linkedin_ready:
            sent_live, live_msg = dispatch_service.send_live_linkedin(recipient_linkedin, outreach["subject"], outreach["message_body"])
            if sent_live:
                dispatch_status = "SENT_LIVE_LINKEDIN"
                live_result_msg = f"Delivered live to LinkedIn profile ({recipient_linkedin})"
            else:
                dispatch_status = "STAGED_AWAITING_ACCOUNT"
                live_result_msg = f"Staged in queue: {live_msg}"
        elif recipient_email and not gmail_ready:
            dispatch_status = "STAGED_AWAITING_ACCOUNT"
            live_result_msg = "Staged in queue: Connect verified Gmail in Accounts & Live Dispatch to send."
        elif recipient_linkedin and not linkedin_ready:
            dispatch_status = "STAGED_AWAITING_ACCOUNT"
            live_result_msg = "Staged in queue: Connect verified LinkedIn session in Accounts & Live Dispatch to send."
        else:
            dispatch_status = "STAGED_AWAITING_VERIFIED_CONTACT"
            live_result_msg = "Outreach pitch prepared and preserved as draft. Awaiting verified direct corporate email or personal LinkedIn profile URL."

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
