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

SOVEREIGN_AND_PE_JOBS = [
    {
        "company_name": "Investment Corporation of Dubai",
        "title": "Director / Senior Asset Manager – Real Estate & Hospitality Portfolio",
        "location": "DIFC & Downtown Dubai, UAE",
        "source_url": "https://www.icd.gov.ae/",
        "seniority": "Director / Senior Manager",
        "description": "Provide strategic asset oversight, leasing performance governance, and portfolio ROI optimization across ICD's landmark commercial, mixed-use, and hospitality subsidiaries (including Ithra Dubai, One Za'abeel, and Brookfield joint-ventures). Lead financial reviews, tenant mix strategy, and capital allocation."
    },
    {
        "company_name": "Mubadala Investment Company",
        "title": "Executive Director / Senior Manager – Real Assets & Commercial Portfolio",
        "location": "Abu Dhabi & Dubai, UAE",
        "source_url": "https://www.mubadala.com/en/careers",
        "seniority": "Director / Senior Manager",
        "description": "Drive commercial real estate asset management, property joint ventures, and capital investments across the UAE and global markets. Oversee multi-asset leasing, development milestones, and strategic partner negotiations."
    },
    {
        "company_name": "KKR",
        "title": "Principal / Director – Middle East Real Estate & Infrastructure Investments",
        "location": "DIFC Dubai & ADGM Abu Dhabi, UAE",
        "source_url": "https://www.kkr.com/careers",
        "seniority": "Principal / Director",
        "description": "Direct asset management, portfolio performance reviews, and commercial lease restructuring across KKR's Middle East real estate and infrastructure holdings. Evaluate asset acquisitions, financial underwriting, and capital expenditure programs."
    },
    {
        "company_name": "Apollo Global Management",
        "title": "Principal / Senior Manager – Real Estate Asset Management & Developer JVs",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://www.apollo.com/careers",
        "seniority": "Principal / Senior Manager",
        "description": "Oversee commercial real estate assets, institutional joint-venture partnerships (including Aldar Properties platform), and large-scale mixed-use investments in the UAE. Formulate asset value creation plans and leasing yield strategies."
    },
    {
        "company_name": "The Carlyle Group",
        "title": "Managing Director / Director – Middle East Real Assets & Investor Strategy",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://www.carlyle.com/careers",
        "seniority": "Director / Managing Director",
        "description": "Lead real estate asset strategy, institutional portfolio governance, and investor relations for The Carlyle Group's Middle East operations based out of DIFC Gate Village."
    },
    {
        "company_name": "Google",
        "title": "Real Estate and Workplace Services (REWS) Manager – MENA Portfolio",
        "location": "Dubai Internet City, UAE",
        "source_url": "https://www.google.com/about/careers/applications/jobs/results/?location=Dubai",
        "seniority": "Senior Manager",
        "description": "Manage Google's commercial real estate leasehold portfolio, facility operations, space planning, and landlord relations across Dubai, UAE, and MENA regional hubs. Direct multi-million dollar CAPEX facility improvements."
    },
    {
        "company_name": "Savills Middle East",
        "title": "Director – Commercial Real Estate Agency & Strategic Asset Consultancy",
        "location": "Al Sa'ada Tower, DIFC Dubai, UAE",
        "source_url": "https://www.savills.ae/",
        "seniority": "Director",
        "description": "Lead strategic commercial real estate leasing advisory, landlord representation, and asset management consultancy for sovereign wealth funds, master developers, and corporate tenants across Dubai."
    },
    {
        "company_name": "Knight Frank Middle East",
        "title": "Partner / Head of Commercial Real Estate Agency & Asset Advisory",
        "location": "ICD Brookfield Place, DIFC Dubai, UAE",
        "source_url": "https://www.knightfrank.ae/careers",
        "seniority": "Partner / Director",
        "description": "Lead commercial office and retail leasing mandates, developer asset positioning, and tenant representation across premier Dubai commercial real estate hubs (DIFC, Downtown, One Za'abeel)."
    }
]

SOVEREIGN_AND_PE_CONTACTS = [
    {
        "company_name": "Investment Corporation of Dubai",
        "full_name": "Gabriel von Bonsdorff",
        "job_title": "Head of Real Estate & Hospitality",
        "role_category": "department_leader",
        "email": "gabriel.vonbonsdorff@icd.gov.ae",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Gabriel+von+Bonsdorff+ICD",
        "notes": "Directs Real Estate & Hospitality for Investment Corporation of Dubai (ICD), parent of Ithra Dubai."
    },
    {
        "company_name": "Investment Corporation of Dubai",
        "full_name": "Othmane Jabri",
        "job_title": "Director – Global Real Estate & Hospitality Investments",
        "role_category": "hiring_manager",
        "email": "othmane.jabri@icd.gov.ae",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Othmane+Jabri+ICD",
        "notes": "Director overseeing global and regional real estate investment implementations at ICD."
    },
    {
        "company_name": "Mubadala Investment Company",
        "full_name": "Khaled Al Shamlan Al Marri",
        "job_title": "Chief Executive Officer – Real Assets",
        "role_category": "department_leader",
        "email": "kmarri@mubadala.ae",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Khaled+Al+Shamlan+Al+Marri+Mubadala",
        "notes": "CEO of Real Assets overseeing Real Estate and Infrastructure investments across Mubadala."
    },
    {
        "company_name": "Mubadala Investment Company",
        "full_name": "Khadija Benzit",
        "job_title": "Director of Real Estate",
        "role_category": "hiring_manager",
        "email": "kbenzit@mubadala.ae",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Khadija+Benzit+Mubadala",
        "notes": "Director of Real Estate at Mubadala leading regional property assets."
    },
    {
        "company_name": "KKR",
        "full_name": "Julian Barratt-Due",
        "job_title": "Managing Director & Head of Middle East Investing",
        "role_category": "department_leader",
        "email": "julian.barratt-due@kkr.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Julian+Barratt-Due+KKR",
        "notes": "Managing Director leading KKR Middle East Investing from DIFC Dubai & ADGM."
    },
    {
        "company_name": "Apollo Global Management",
        "full_name": "Michael Maechling",
        "job_title": "Managing Director",
        "role_category": "department_leader",
        "email": "mmaechling@apollo.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Michael+Maechling+Apollo",
        "notes": "Managing Director at Apollo Global Management covering regional real estate investments."
    },
    {
        "company_name": "The Carlyle Group",
        "full_name": "Ani Khatri",
        "job_title": "Managing Director, Partner & Senior Relationship Manager",
        "role_category": "department_leader",
        "email": "ani.khatri@carlyle.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Ani+Khatri+Carlyle",
        "notes": "Gate Village, DIFC Dubai. Leads Middle East relations and institutional partnerships."
    },
    {
        "company_name": "Google",
        "full_name": "Charbel Sarkis",
        "job_title": "Regional Director – Google MENA",
        "role_category": "department_leader",
        "email": "csarkis@google.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Charbel+Sarkis+Google",
        "notes": "Regional Director at Google Dubai Internet City, Building 14."
    },
    {
        "company_name": "Savills Middle East",
        "full_name": "Richard Paul",
        "job_title": "Head of Professional Services & Strategic Consultancy Middle East",
        "role_category": "department_leader",
        "email": "richard.paul@savills.me",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Richard+Paul+Savills+Dubai",
        "notes": "Al Sa'ada Tower, DIFC Dubai. Leads strategic consultancy and asset advisory across Middle East."
    },
    {
        "company_name": "Savills Middle East",
        "full_name": "Toby Hall",
        "job_title": "Head of Commercial Agency (Middle East)",
        "role_category": "hiring_manager",
        "email": "toby.hall@savills.me",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Toby+Hall+Savills+Dubai",
        "notes": "Directs commercial real estate agency and corporate tenant leasing in Dubai."
    },
    {
        "company_name": "Knight Frank Middle East",
        "full_name": "Adam Wynne",
        "job_title": "Partner – Head of Commercial Agency (UAE)",
        "role_category": "hiring_manager",
        "email": "adam.wynne@me.knightfrank.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Adam+Wynne+Knight+Frank",
        "notes": "ICD Brookfield Place, Level 28, DIFC Dubai. Leads commercial agency and leasing advisory."
    },
    {
        "company_name": "Knight Frank Middle East",
        "full_name": "James Lewis",
        "job_title": "Managing Director – Middle East & Africa",
        "role_category": "department_leader",
        "email": "james.lewis@me.knightfrank.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=James+Lewis+Knight+Frank",
        "notes": "Managing Director directing Knight Frank's real estate business across Middle East."
    }
]

def seed_sovereign_and_pe():
    print("Ingesting Sovereign Wealth Funds, Global Private Equity & Corporate Real Estate Leaders...")
    for j in SOVEREIGN_AND_PE_JOBS:
        job = job_discovery_agent.ingest_job(
            title=j["title"],
            company_name=j["company_name"],
            location=j["location"],
            source_url=j["source_url"],
            description=j["description"],
            seniority=j["seniority"]
        )
        match = job_fit_agent.evaluate_job(job["id"])
        print(f"Ingested [{job['company_name']}] '{job['title']}' -> Match: {match['overall_fit_label']} ({match['match_score']:.2f})")

    for c in SOVEREIGN_AND_PE_CONTACTS:
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
        print(f"Added Contact & Generated Pitch: {contact['full_name']} at {contact['company_name']}")

    print("\nSuccessfully seeded Sovereign Wealth Funds and Global Real Estate Leaders!")

if __name__ == "__main__":
    seed_sovereign_and_pe()
