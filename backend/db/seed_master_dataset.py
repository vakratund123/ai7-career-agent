import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.db.database import get_db
from backend.agents.job_discovery import job_discovery_agent
from backend.agents.fit_match import job_fit_agent
from backend.agents.contact_intelligence import contact_intelligence_agent
from backend.agents.outreach_agent import outreach_agent

logging.basicConfig(level=logging.INFO)

# Import all job and contact definitions
from backend.db.seed_verified_contacts import VERIFIED_CONTACTS
from backend.db.seed_real_opportunities import REAL_JOBS, RECRUITMENT_AGENCIES_DATA
from backend.db.seed_more_contacts import ADDITIONAL_CONTACTS
from backend.db.seed_client_12_companies import CLIENT_12_JOBS, CLIENT_12_CONTACTS
from backend.db.seed_big4_and_fintech import NEW_JOBS as BIG4_JOBS, NEW_CONTACTS as BIG4_CONTACTS
from backend.db.seed_sovereign_and_global_giants import SOVEREIGN_AND_PE_JOBS, SOVEREIGN_AND_PE_CONTACTS

def seed_master_catalog():
    with get_db() as conn:
        conn.execute("DELETE FROM jobs")
        conn.execute("DELETE FROM job_matches")
        conn.execute("DELETE FROM contacts")
        conn.execute("DELETE FROM outreach_campaigns")
    
    # Consolidate all unique jobs by (company_name, title)
    all_jobs = REAL_JOBS + CLIENT_12_JOBS + BIG4_JOBS + SOVEREIGN_AND_PE_JOBS
    unique_jobs = {}
    for j in all_jobs:
        key = (j["company_name"].strip(), j["title"].strip())
        if key not in unique_jobs:
            unique_jobs[key] = j

    print(f"--- INGESTING {len(unique_jobs)} VERIFIED REAL JOB OPENINGS ---")
    for (comp_name, title), j in unique_jobs.items():
        job = job_discovery_agent.ingest_job(
            title=title,
            company_name=comp_name,
            location=j.get("location", "Dubai, UAE"),
            source_url=j.get("source_url", "https://www.linkedin.com/jobs"),
            description=j.get("description", "Real estate asset management role."),
            seniority=j.get("seniority", "Senior Manager / Director")
        )
        match = job_fit_agent.evaluate_job(job["id"])
        print(f"Job: [{job['company_name']}] '{job['title']}' -> Match: {match['overall_fit_label']} ({match['match_score']:.2f})")

    # Consolidate all unique contacts by (company_name, full_name)
    all_contacts = VERIFIED_CONTACTS + RECRUITMENT_AGENCIES_DATA + ADDITIONAL_CONTACTS + CLIENT_12_CONTACTS + BIG4_CONTACTS + SOVEREIGN_AND_PE_CONTACTS
    unique_contacts = {}
    for c in all_contacts:
        key = (c["company_name"].strip(), c["full_name"].strip())
        if key not in unique_contacts:
            unique_contacts[key] = c

    print(f"\n--- SEEDING {len(unique_contacts)} VERIFIED DECISION-MAKERS & CONTACTS ---")
    for (comp_name, full_name), c in unique_contacts.items():
        contact = contact_intelligence_agent.add_real_contact(
            company_name=comp_name,
            full_name=full_name,
            job_title=c.get("job_title", "Executive"),
            role_category=c.get("role_category", "hiring_manager"),
            email=c.get("email"),
            linkedin_url=c.get("linkedin_url"),
            notes=c.get("notes")
        )
        draft_type = "RECRUITER_INTRO" if c.get("role_category") == "recruiter" else "HIRING_MGR_PITCH"
        outreach_agent.generate_outreach_draft(
            job_id=None,
            contact_id=contact["id"],
            outreach_type=draft_type
        )
        print(f"Contact: [{contact['company_name']}] {contact['full_name']} ({contact['job_title']}) -> Pitch Generated")

    print(f"\nSUCCESS: Master catalog populated with {len(unique_jobs)} verified jobs and {len(unique_contacts)} verified contacts!")

if __name__ == "__main__":
    seed_master_catalog()
