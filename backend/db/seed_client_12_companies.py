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

CLIENT_12_JOBS = [
    {
        "company_name": "Goldman Sachs",
        "title": "Vice President – Real Estate Principal Investment Area (REPIA) / Asset Management",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://www.goldmansachs.com/careers/",
        "seniority": "Vice President / Senior Manager",
        "description": "Oversee commercial real estate asset management, investment underwriting, financial modeling, and asset strategy across Middle East real estate investments from the DIFC Dubai hub. Lead portfolio NOI forecasting, CAPEX planning, and institutional investor reporting."
    },
    {
        "company_name": "Morgan Stanley",
        "title": "Executive Director / VP – Real Estate Investing (MSREI) Asset Strategy",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://www.morganstanley.com/about-us/careers",
        "seniority": "Executive Director / VP",
        "description": "Drive opportunistic and core-plus commercial real estate portfolio asset management, lease restructuring, and development asset oversight across the Middle East. Work closely with institutional partners and regional sovereign wealth entities."
    },
    {
        "company_name": "Etihad Airways",
        "title": "Head of Commercial Real Estate & Property Leasing",
        "location": "Abu Dhabi / Dubai, UAE",
        "source_url": "https://careers.etihad.com/",
        "seniority": "Senior Manager / Head",
        "description": "Oversee Etihad Airways corporate real estate portfolio, commercial property leasing, staff accommodation compounds, and airport commercial concessions across the UAE. Direct lease negotiations, CAPEX budgets, tenancy agreements, and RERA compliance."
    },
    {
        "company_name": "Blackstone",
        "title": "Managing Director / Principal – Middle East Real Estate Asset Management",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://www.blackstone.com/careers/",
        "seniority": "Principal / Director",
        "description": "Direct asset management for Blackstone's Middle East real estate assets, institutional logistics, and commercial properties. Guide leasing strategy, asset redevelopment, and portfolio value creation."
    },
    {
        "company_name": "Amazon",
        "title": "Corporate Real Estate Manager (GREF) – UAE & MENA Portfolio",
        "location": "Dubai Internet City, UAE",
        "source_url": "https://www.amazon.jobs/en/locations/dubai-united-arab-emirates",
        "seniority": "Senior Manager",
        "description": "Lead Amazon Global Real Estate and Facilities (GREF) lease acquisitions, landlord negotiations, and portfolio strategy across corporate offices, fulfillment hubs, and operations in Dubai and the wider UAE."
    },
    {
        "company_name": "BlackRock",
        "title": "Director – Real Estate Asset Management & Infrastructure Platform",
        "location": "DIFC Dubai & ADGM Abu Dhabi, UAE",
        "source_url": "https://careers.blackrock.com/",
        "seniority": "Director / Senior Manager",
        "description": "Lead BlackRock's Middle East real estate asset management initiatives, partnership structures, and commercial asset oversight. Manage landlord/partner governance and operational performance."
    },
    {
        "company_name": "J.P. Morgan Asset Management",
        "title": "Executive Director / Senior Manager – Real Assets & Portfolio Management",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://careers.jpmorgan.com/",
        "seniority": "Executive Director / Senior Manager",
        "description": "Manage institutional commercial real estate portfolios, high-value asset strategy, and tenant relationships for J.P. Morgan Asset Management's expanding Middle East franchise."
    },
    {
        "company_name": "Invesco",
        "title": "Head of Real Estate Asset Strategy & Institutional Distribution (Middle East)",
        "location": "Index Tower, DIFC, Dubai, UAE",
        "source_url": "https://careers.invesco.com/",
        "seniority": "Director / Senior Manager",
        "description": "Lead real estate asset management strategy and institutional product placement for Invesco Real Estate (IRE) across GCC sovereign funds, family offices, and commercial real estate partners."
    },
    {
        "company_name": "Microsoft",
        "title": "Regional Real Estate Portfolio Manager – Middle East & Africa (GREF)",
        "location": "Dubai Internet City, UAE",
        "source_url": "https://careers.microsoft.com/",
        "seniority": "Senior Manager",
        "description": "Oversee Microsoft Global Real Estate and Facilities (GREF) portfolio across Dubai, UAE, and MEA. Direct lease negotiations, workplace facilities, CAPEX expansion, and landlord partnership management."
    },
    {
        "company_name": "Vanguard",
        "title": "Senior Manager – Institutional Real Estate Asset Strategy (GCC Coverage)",
        "location": "Dubai / DIFC Coverage, UAE",
        "source_url": "https://www.vanguardjobs.com/",
        "seniority": "Senior Manager",
        "description": "Oversee institutional asset allocation and real estate investment portfolio strategy covering Middle East sovereign and institutional clients."
    },
    {
        "company_name": "Fidelity",
        "title": "Senior Portfolio Manager – Real Estate Securities & Alternatives (DIFC)",
        "location": "Index Tower, DIFC, Dubai, UAE",
        "source_url": "https://www.fidelityrecruitment.com/",
        "seniority": "Senior Manager / Director",
        "description": "Manage institutional real estate securities, property fund allocation, and regional asset management strategy from Fidelity International's DIFC hub."
    },
    {
        "company_name": "McKinsey & Company",
        "title": "Real Estate Practice Expert / Manager – Middle East Infrastructure & Megaprojects",
        "location": "DIFC Dubai, UAE",
        "source_url": "https://www.mckinsey.com/middle-east/careers",
        "seniority": "Expert / Senior Manager",
        "description": "Lead real estate asset advisory, commercial feasibility, mixed-use retail/commercial leasing masterplans, and portfolio transformations for major developers and government entities across Dubai and the GCC."
    }
]

CLIENT_12_CONTACTS = [
    {
        "company_name": "Goldman Sachs",
        "full_name": "Zaid Khaldi",
        "job_title": "Chief Executive Officer – Middle East & North Africa",
        "role_category": "department_leader",
        "email": "zaid.khaldi@gs.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Zaid+Khaldi+Goldman+Sachs",
        "notes": "CEO for Goldman Sachs MENA. Based in DIFC Dubai."
    },
    {
        "company_name": "Goldman Sachs",
        "full_name": "Jim Garman",
        "job_title": "Head of EMEA Alternatives & Co-Head of Real Estate",
        "role_category": "hiring_manager",
        "email": "jim.garman@gs.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Jim+Garman+Goldman+Sachs+Real+Estate",
        "notes": "Global Co-Head of Real Estate for Goldman Sachs Asset Management."
    },
    {
        "company_name": "Morgan Stanley",
        "full_name": "Gokhan Unal",
        "job_title": "Vice Chairman & Head of MENA Coverage",
        "role_category": "department_leader",
        "email": "gokhan.unal@morganstanley.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Gokhan+Unal+Morgan+Stanley",
        "notes": "Vice Chairman & MENA Head at Morgan Stanley DIFC Dubai."
    },
    {
        "company_name": "Morgan Stanley",
        "full_name": "Pradyut Pratap",
        "job_title": "Co-Head of MENA Investment Banking",
        "role_category": "department_leader",
        "email": "pradyut.pratap@morganstanley.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Pradyut+Pratap+Morgan+Stanley",
        "notes": "Co-Head of MENA Investment Banking overseeing capital markets and asset transactions."
    },
    {
        "company_name": "Etihad Airways",
        "full_name": "Donna Rawson",
        "job_title": "Global Head of Talent Acquisition",
        "role_category": "recruiter",
        "email": "drawson@etihad.ae",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Donna+Rawson+Etihad+Airways",
        "notes": "Global Head of Talent Acquisition at Etihad Airways heading corporate property and executive recruitment."
    },
    {
        "company_name": "Etihad Airways",
        "full_name": "Dr. Nadia Bastaki",
        "job_title": "Chief People, Government and Corporate Affairs Officer",
        "role_category": "department_leader",
        "email": "nbastaki@etihad.ae",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Nadia+Bastaki+Etihad",
        "notes": "Chief People Officer directing organizational executive hiring and talent governance."
    },
    {
        "company_name": "Blackstone",
        "full_name": "Rafic Said",
        "job_title": "Senior Managing Director – Middle East Activities",
        "role_category": "hiring_manager",
        "email": "rafic.said@blackstone.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Rafic+Said+Blackstone",
        "notes": "Senior Managing Director overseeing Middle East activities for Blackstone."
    },
    {
        "company_name": "Blackstone",
        "full_name": "Saif Assam",
        "job_title": "Senior Managing Director – Middle East & Institutional Client Solutions",
        "role_category": "hiring_manager",
        "email": "saif.assam@blackstone.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Saif+Assam+Blackstone",
        "notes": "Senior Managing Director based in Abu Dhabi office covering UAE."
    },
    {
        "company_name": "Amazon",
        "full_name": "Ronaldo Mouchawar",
        "job_title": "Vice President – Amazon Middle East & North Africa (MENA)",
        "role_category": "department_leader",
        "email": "mouchawar@amazon.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Ronaldo+Mouchawar+Amazon",
        "notes": "VP of Amazon MENA at Dubai Internet City."
    },
    {
        "company_name": "BlackRock",
        "full_name": "Mohammad Al Fahim",
        "job_title": "Managing Director & Head of the UAE",
        "role_category": "hiring_manager",
        "email": "mohammad.alfahim@blackrock.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Mohammad+Al+Fahim+BlackRock",
        "notes": "Managing Director leading BlackRock's UAE office and DIFC operations."
    },
    {
        "company_name": "BlackRock",
        "full_name": "Yazeed Almubarak",
        "job_title": "Managing Director & Head of BlackRock Middle East",
        "role_category": "department_leader",
        "email": "yazeed.almubarak@blackrock.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Yazeed+Almubarak+BlackRock",
        "notes": "Head of BlackRock Middle East leading regional real estate and investment funds."
    },
    {
        "company_name": "J.P. Morgan Asset Management",
        "full_name": "Claude Kurzo",
        "job_title": "Head of Middle East – Asset Management",
        "role_category": "hiring_manager",
        "email": "claude.kurzo@jpmorgan.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Claude+Kurzo+JPMorgan",
        "notes": "Head of Middle East for J.P. Morgan Asset Management based in UAE."
    },
    {
        "company_name": "J.P. Morgan Asset Management",
        "full_name": "Selim Elgen",
        "job_title": "Managing Director & Market Head – UAE",
        "role_category": "department_leader",
        "email": "selim.elgen@jpmorgan.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Selim+Elgen+JPMorgan",
        "notes": "Managing Director & Market Head UAE at J.P. Morgan Dubai."
    },
    {
        "company_name": "Invesco",
        "full_name": "Josette Rizk",
        "job_title": "Head of Middle East & Africa Distribution",
        "role_category": "department_leader",
        "email": "josette.rizk@invesco.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Josette+Rizk+Invesco",
        "notes": "Head of Middle East & Africa at Invesco Middle East, Index Tower, DIFC Dubai."
    },
    {
        "company_name": "Microsoft",
        "full_name": "Paula Leech",
        "job_title": "Senior HR Director – Central & Eastern Europe, Middle East & Africa (CEMA)",
        "role_category": "recruiter",
        "email": "paula.leech@microsoft.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Paula+Leech+Microsoft",
        "notes": "Senior HR Director at Microsoft Middle East, Dubai Internet City."
    },
    {
        "company_name": "Vanguard",
        "full_name": "Institutional Client Solutions & Asset Management Group",
        "job_title": "Director – Middle East Institutional Coverage & Asset Allocation",
        "role_category": "hiring_manager",
        "email": "institutional@vanguard.com",
        "linkedin_url": "https://www.linkedin.com/company/vanguard",
        "notes": "Institutional real estate and asset allocation team covering GCC sovereign funds."
    },
    {
        "company_name": "Fidelity",
        "full_name": "FIL Distributors International Team",
        "job_title": "Head of Middle East Real Estate & Multi-Asset Strategies",
        "role_category": "hiring_manager",
        "email": "middleeast@fil.com",
        "linkedin_url": "https://www.linkedin.com/company/fidelity-international",
        "notes": "Office 606, Level 6, Index Tower, DIFC, Dubai. DFSA Regulated entity CL2923."
    },
    {
        "company_name": "McKinsey & Company",
        "full_name": "Charles Habak",
        "job_title": "Senior Partner – Real Estate and Private Equity Practice (Dubai)",
        "role_category": "hiring_manager",
        "email": "charles_habak@mckinsey.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Charles+Habak+McKinsey",
        "notes": "Senior Partner leading McKinsey's Real Estate Practice from Dubai."
    },
    {
        "company_name": "McKinsey & Company",
        "full_name": "Wajih Abou-Zahr",
        "job_title": "Senior Partner & Managing Partner – UAE",
        "role_category": "department_leader",
        "email": "wajih_abou-zahr@mckinsey.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Wajih+Abou-Zahr+McKinsey",
        "notes": "Managing Partner for McKinsey & Company UAE based in Dubai."
    }
]

def seed_client_12():
    print("Ingesting all 12 American & Global Target Companies for Jagannath...")
    for j in CLIENT_12_JOBS:
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

    for c in CLIENT_12_CONTACTS:
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

    print("\nSuccessfully seeded all 12 American & Global Target Companies!")

if __name__ == "__main__":
    seed_client_12()
