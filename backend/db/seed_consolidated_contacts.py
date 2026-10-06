import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.db.database import get_db
from backend.agents.contact_intelligence import contact_intelligence_agent
from backend.agents.outreach_agent import outreach_agent

logging.basicConfig(level=logging.INFO)

from backend.db.seed_verified_contacts import VERIFIED_CONTACTS
from backend.db.seed_real_opportunities import RECRUITMENT_AGENCIES_DATA
from backend.db.seed_more_contacts import ADDITIONAL_CONTACTS

def seed_all_contacts():
    with get_db() as conn:
        conn.execute("DELETE FROM contacts")
        conn.execute("DELETE FROM outreach_campaigns")
    
    all_contacts = VERIFIED_CONTACTS + RECRUITMENT_AGENCIES_DATA + ADDITIONAL_CONTACTS
    print(f"Seeding all {len(all_contacts)} verified contacts and generating tailored outreach...")

    for c in all_contacts:
        contact = contact_intelligence_agent.add_real_contact(
            company_name=c["company_name"],
            full_name=c["full_name"],
            job_title=c["job_title"],
            role_category=c["role_category"],
            email=c["email"],
            linkedin_url=c["linkedin_url"],
            notes=c["notes"]
        )
        draft_type = "RECRUITER_INTRO" if c["role_category"] == "recruiter" else "HIRING_MGR_PITCH"
        outreach_agent.generate_outreach_draft(
            job_id=None,
            contact_id=contact["id"],
            outreach_type=draft_type
        )
        print(f"Added & Drafted: {contact['full_name']} at {contact['company_name']}")

    print(f"\nAll {len(all_contacts)} contacts active and drafts generated!")

if __name__ == "__main__":
    seed_all_contacts()
