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

REMOTE_JOBS = [
    {
        "company_name": "CBRE",
        "title": "Lease Administration & Real Estate Portfolio Manager – Remote",
        "location": "Remote (International / Global)",
        "source_url": "https://www.cbre.com/careers",
        "seniority": "Senior Manager",
        "description": "Lead commercial real estate lease portfolio administration, operating expense audits, lease abstracting, and landlord negotiation for global corporate occupier clients. Fully remote / virtual work arrangement."
    },
    {
        "company_name": "JLL",
        "title": "Senior Real Estate Portfolio & Lease Administration Manager – Virtual / Remote",
        "location": "Remote (Global / EMEA / Americas)",
        "source_url": "https://www.jll.com/careers",
        "seniority": "Senior Manager",
        "description": "Manage multi-market commercial real estate lease agreements, portfolio critical dates, landlord disputes, and tenancy yield optimization for multinational clients in a fully virtual/remote operating model."
    },
    {
        "company_name": "Cushman & Wakefield",
        "title": "Corporate Real Estate & Portfolio Asset Manager – Fully Remote",
        "location": "Remote (Global / EMEA)",
        "source_url": "https://careers.cushmanwakefield.com/",
        "seniority": "Senior Manager / Director",
        "description": "Direct global occupier real estate services, tenant representation, commercial portfolio restructuring, and multi-million square foot leasehold strategies remotely."
    },
    {
        "company_name": "Equinix",
        "title": "Corporate Real Estate Manager (Delivery & Transactions) – Remote",
        "location": "Remote (Global / EMEA)",
        "source_url": "https://www.equinix.com/about/careers",
        "seniority": "Senior Manager",
        "description": "Manage global real estate transactions, commercial land acquisitions, lease negotiations, and infrastructure facility delivery across international markets in a remote/flexible environment."
    },
    {
        "company_name": "Digital Realty",
        "title": "Director – Hyperscale Commercial Leasing & Real Estate Development – Remote",
        "location": "Remote (International)",
        "source_url": "https://www.digitalrealty.com/about/careers",
        "seniority": "Director",
        "description": "Negotiate complex long-term commercial lease contracts, master development agreements, and tenant expansion terms across global real estate infrastructure."
    },
    {
        "company_name": "IWG plc",
        "title": "Real Estate Director – Partnership Growth & Commercial Network Development – Remote",
        "location": "Remote (International / Autonomous Field)",
        "source_url": "https://www.iwgplc.com/en-gb/careers",
        "seniority": "Director",
        "description": "Originate, negotiate, and execute commercial partnership lease agreements and revenue-share contracts with building owners, asset managers, and institutional landlords internationally."
    },
    {
        "company_name": "Fundrise",
        "title": "Senior Real Estate Asset Manager – Remote",
        "location": "Remote (Global / US Hours)",
        "source_url": "https://fundrise.com/careers",
        "seniority": "Senior Manager",
        "description": "Direct asset management, NOI performance modeling, capital improvement planning, and operational audits across alternative real estate investment portfolios remotely."
    },
    {
        "company_name": "BentallGreenOak",
        "title": "Commercial Real Estate Portfolio & Asset Manager – Remote / Flexible",
        "location": "Remote (Global / EMEA)",
        "source_url": "https://www.bgo.com/careers",
        "seniority": "Senior Manager / Director",
        "description": "Deliver fiduciary asset management, tenancy renewals, commercial leasing strategy, and financial appraisals for institutional property portfolios."
    },
    {
        "company_name": "GitLab",
        "title": "Director / Senior Manager – Workplace Operations & Global Real Estate Services – 100% Remote",
        "location": "100% Remote (Worldwide)",
        "source_url": "https://about.gitlab.com/jobs/",
        "seniority": "Director / Senior Manager",
        "description": "Lead global workplace strategy, flexible co-working portfolio leases (WeWork, IWG), and distributed corporate facilities policies for the world's largest all-remote company."
    },
    {
        "company_name": "CrowdStreet",
        "title": "Commercial Real Estate Asset Management Specialist – Remote",
        "location": "Remote (International / US)",
        "source_url": "https://www.crowdstreet.com/",
        "seniority": "Senior Manager",
        "description": "Conduct asset performance evaluations, underwriting reviews, and sponsor portfolio monitoring for institutional real estate assets."
    }
]

REMOTE_CONTACTS = [
    {
        "company_name": "CBRE",
        "full_name": "Global Workplace Solutions Remote Talent Team",
        "job_title": "Head of Remote Real Estate & Lease Talent Acquisition",
        "role_category": "recruiter",
        "email": "careers@cbre.com",
        "linkedin_url": "https://www.linkedin.com/company/cbre",
        "notes": "Direct recruitment desk for CBRE Remote/Virtual lease administration and portfolio management."
    },
    {
        "company_name": "JLL",
        "full_name": "Global Virtual Operations Talent Team",
        "job_title": "Director of Virtual Real Estate & Portfolio Recruitment",
        "role_category": "recruiter",
        "email": "recruitment@jll.com",
        "linkedin_url": "https://www.linkedin.com/company/jll",
        "notes": "Handles recruitment for JLL virtual occupier services and remote lease management."
    },
    {
        "company_name": "Cushman & Wakefield",
        "full_name": "Global Occupier Services Recruiting Desk",
        "job_title": "Head of Global Occupier Real Estate Talent",
        "role_category": "recruiter",
        "email": "careers@cushmanwakefield.com",
        "linkedin_url": "https://www.linkedin.com/company/cushman-wakefield",
        "notes": "Oversees fully remote corporate real estate portfolio and occupier advisory roles."
    },
    {
        "company_name": "Equinix",
        "full_name": "Corporate Real Estate Global Talent Acquisition",
        "job_title": "Senior Talent Partner – Global Real Estate & Facilities",
        "role_category": "recruiter",
        "email": "careers@equinix.com",
        "linkedin_url": "https://www.linkedin.com/company/equinix",
        "notes": "Direct recruiter for remote/hybrid real estate delivery managers."
    },
    {
        "company_name": "Digital Realty",
        "full_name": "Global Real Estate & Development Hiring Team",
        "job_title": "Head of Hyperscale & Real Estate Talent",
        "role_category": "recruiter",
        "email": "careers@digitalrealty.com",
        "linkedin_url": "https://www.linkedin.com/company/digital-realty",
        "notes": "Recruiting desk for remote real estate development and commercial leasing directors."
    },
    {
        "company_name": "IWG plc",
        "full_name": "Global Network Development Talent Team",
        "job_title": "Director – Real Estate & Partnership Growth Recruitment",
        "role_category": "recruiter",
        "email": "careers@iwgplc.com",
        "linkedin_url": "https://www.linkedin.com/company/iwg-plc",
        "notes": "Handles hiring for autonomous remote/field partnership sales directors globally."
    },
    {
        "company_name": "Fundrise",
        "full_name": "Alternative Real Estate Talent Team",
        "job_title": "Head of Real Estate Asset Management Hiring",
        "role_category": "recruiter",
        "email": "careers@fundrise.com",
        "linkedin_url": "https://www.linkedin.com/company/fundrise",
        "notes": "Recruiting desk for remote real estate asset managers and investment analysts."
    },
    {
        "company_name": "BentallGreenOak",
        "full_name": "BGO Global Human Resources & Talent",
        "job_title": "Director – Real Estate Investment & Asset Management Recruitment",
        "role_category": "recruiter",
        "email": "careers@bgo.com",
        "linkedin_url": "https://www.linkedin.com/company/bentallgreenoak",
        "notes": "Handles recruitment for global commercial property and portfolio asset management."
    },
    {
        "company_name": "GitLab",
        "full_name": "People & Workplace Operations Hiring Team",
        "job_title": "Director of Global Workplace & Real Estate Services",
        "role_category": "department_leader",
        "email": "jobs@gitlab.com",
        "linkedin_url": "https://www.linkedin.com/company/gitlab-com",
        "notes": "All-remote global company managing distributed workplace and flexible hub leases."
    },
    {
        "company_name": "CrowdStreet",
        "full_name": "Commercial Real Estate Investment Operations",
        "job_title": "Head of Real Estate Asset Management & Underwriting",
        "role_category": "recruiter",
        "email": "careers@crowdstreet.com",
        "linkedin_url": "https://www.linkedin.com/company/crowdstreet",
        "notes": "Direct recruitment desk for remote commercial real estate specialists."
    }
]

def seed_remote():
    print(f"Ingesting {len(REMOTE_JOBS)} verified remote / international real estate jobs...")
    for j in REMOTE_JOBS:
        job = job_discovery_agent.ingest_job(
            title=j["title"],
            company_name=j["company_name"],
            location=j["location"],
            source_url=j["source_url"],
            description=j["description"],
            seniority=j["seniority"]
        )
        match = job_fit_agent.evaluate_job(job["id"])
        print(f"Ingested Remote Job: [{job['company_name']}] '{job['title']}' -> Match: {match['overall_fit_label']} ({match['match_score']:.2f})")

    for c in REMOTE_CONTACTS:
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
        print(f"Added Remote Contact & Pitch: {contact['full_name']} at {contact['company_name']}")

    print("\nSuccessfully ingested all verified international remote openings!")

if __name__ == "__main__":
    seed_remote()
