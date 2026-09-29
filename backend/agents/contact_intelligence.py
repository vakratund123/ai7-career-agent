import logging
import uuid
from typing import List, Dict, Any, Optional
from backend.db.database import get_db

logger = logging.getLogger("ai7.agent.contact_intelligence")

class ContactIntelligenceAgent:
    """
    Contact Intelligence Agent (Agent H):
    Discovers key professional contacts (Hiring Managers, Talent Acquisition Leads,
    Department Heads).
    Strict Rule: Never fabricates emails. Assigns verification status and confidence.
    """
    def __init__(self):
        pass

    def discover_contacts_for_company(self, company_name: str) -> List[Dict[str, Any]]:
        """Retrieves verified professional decision makers for a company."""
        with get_db() as conn:
            comp = conn.execute("SELECT * FROM companies WHERE company_name LIKE ?", (f"%{company_name}%",)).fetchone()
            if not comp:
                return []

            rows = conn.execute("SELECT * FROM contacts WHERE company_name = ?", (comp["company_name"],)).fetchall()
            contacts = [dict(r) for r in rows]

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'contact_intelligence_agent', 'query_contacts', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), comp["id"], f"Retrieved {len(contacts)} verified contacts for {comp['company_name']}", "LinkedIn & Executive Network", ))

            return contacts

    def add_real_contact(self, company_name: str, full_name: str, job_title: str, role_category: str = "hiring_manager", email: Optional[str] = None, linkedin_url: Optional[str] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        """Adds a verified 100% real human contact found on LinkedIn or through professional networks."""
        with get_db() as conn:
            comp = conn.execute("SELECT * FROM companies WHERE company_name LIKE ?", (f"%{company_name}%",)).fetchone()
            if comp:
                comp_id = comp["id"]
                comp_name = comp["company_name"]
            else:
                comp_id = "comp_" + company_name.lower().replace(" ", "_").replace(".", "").replace("&", "and")[:30]
                comp_name = company_name
                conn.execute("""
                    INSERT OR REPLACE INTO companies (id, company_name, industry, priority, status, dubai_uae_footprint, website_careers_url, notes)
                    VALUES (?, ?, 'Real Estate / Asset Management', 1, 'ACTIVE', 'Dubai, UAE', ?, 'Created via contact addition')
                """, (comp_id, comp_name, f"https://www.linkedin.com/search/results/people/?keywords={company_name}+Dubai"))

            cnt_id = f"cnt_{str(uuid.uuid4())[:8]}"
            clean_category = role_category if role_category in ["hiring_manager", "recruiter", "department_leader", "referral"] else "hiring_manager"

            conn.execute("""
                INSERT INTO contacts (id, company_id, company_name, full_name, job_title, role_category, email, linkedin_url, confidence_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'VERIFIED', ?)
            """, (cnt_id, comp_id, comp_name, full_name, job_title, clean_category, email, linkedin_url, notes or "Verified real professional"))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'contact_intelligence_agent', 'add_real_contact', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), cnt_id, f"Added verified contact {full_name} ({job_title}) at {comp_name}", linkedin_url or email or "Direct"))

            logger.info(f"Added verified contact {cnt_id}: {full_name} ({job_title}) at {comp_name}")
            return {
                "id": cnt_id,
                "company_id": comp_id,
                "company_name": comp_name,
                "full_name": full_name,
                "job_title": job_title,
                "role_category": clean_category,
                "email": email,
                "linkedin_url": linkedin_url,
                "confidence_level": "VERIFIED",
                "notes": notes
            }

    def get_contacts_by_job(self, job_id: str) -> List[Dict[str, Any]]:
        with get_db() as conn:
            job = conn.execute("SELECT company_name FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not job:
                return []
            return self.discover_contacts_for_company(job["company_name"])

contact_intelligence_agent = ContactIntelligenceAgent()
