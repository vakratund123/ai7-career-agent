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

NEW_JOBS = [
    {
        "company_name": "PwC",
        "title": "Director / Senior Manager – Real Estate Deals & Asset Advisory",
        "location": "Emaar Square, Dubai, UAE",
        "source_url": "https://www.pwc.com/m1/en/careers.html",
        "seniority": "Director / Senior Manager",
        "description": "Lead real estate deals advisory, commercial due diligence, asset valuation, and portfolio restructuring for sovereign wealth funds, master developers, and family offices in the UAE and GCC. Advise on capital projects, retail/commercial tenant mix, and NOI optimization."
    },
    {
        "company_name": "Deloitte",
        "title": "Director / Senior Manager – Infrastructure & Real Estate Advisory",
        "location": "DIFC & Downtown Dubai, UAE",
        "source_url": "https://www.deloitte.com/middle-east/careers",
        "seniority": "Director / Senior Manager",
        "description": "Direct commercial real estate feasibility, asset management strategies, and large-scale master development advisory. Evaluate tenant leasing structures, financial models, and property portfolio ROI for premier UAE clients."
    },
    {
        "company_name": "KPMG",
        "title": "Partner / Director – Real Estate, Infrastructure & Asset Advisory",
        "location": "Dubai Festival City & DIFC, UAE",
        "source_url": "https://home.kpmg/ae/en/home/careers.html",
        "seniority": "Director / Senior Manager",
        "description": "Lead KPMG Lower Gulf real estate and construction advisory mandates. Guide clients through commercial property valuations, leasehold transactions, feasibility studies, and operational asset performance across Dubai."
    },
    {
        "company_name": "EY",
        "title": "Senior Manager – Strategy and Transactions (SaT) Real Estate & Hospitality",
        "location": "ICD Brookfield Place, DIFC, Dubai, UAE",
        "source_url": "https://www.ey.com/en_gl/careers",
        "seniority": "Senior Manager",
        "description": "Provide transaction and strategic asset advice to leading regional property developers and sovereign entities. Formulate master development leasing strategies, commercial feasibility models, and asset restructuring solutions."
    },
    {
        "company_name": "Mastercard",
        "title": "Regional Manager – Corporate Real Estate & Workplace Solutions (EEMEA)",
        "location": "Dubai Internet City, UAE",
        "source_url": "https://mastercard.jobs/",
        "seniority": "Senior Manager",
        "description": "Oversee corporate real estate portfolio, facilities management, and leasehold strategy across Mastercard's Eastern Europe, Middle East, and Africa (EEMEA) headquarters and regional offices. Negotiate commercial lease agreements and oversee CAPEX facility enhancements."
    },
    {
        "company_name": "Visa",
        "title": "Director – Regional Real Estate, Facilities & Workplace Strategy (CEMEA)",
        "location": "Dubai Internet City, UAE",
        "source_url": "https://www.visa.com/careers",
        "seniority": "Director / Senior Manager",
        "description": "Direct corporate real estate, facility operations, and master leasehold agreements across Visa's 100,000 sq. ft. CEMEA headquarters in Dubai and regional hubs. Oversee landlord relationships, tenant space planning, and budget administration."
    }
]

NEW_CONTACTS = [
    {
        "company_name": "PwC",
        "full_name": "Martin Berlin",
        "job_title": "Partner & Global Deals Real Estate Leader (Dubai)",
        "role_category": "department_leader",
        "email": "martin.berlin@pwc.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Martin+Berlin+PwC+Dubai",
        "notes": "Emaar Square, Building 4, Downtown Dubai. Tel: +971 4 304 3100. Global Deals Real Estate Leader."
    },
    {
        "company_name": "PwC",
        "full_name": "Ahmed Saleh",
        "job_title": "Partner – Capital Projects & Real Estate Practice",
        "role_category": "hiring_manager",
        "email": "ahmed.saleh@pwc.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Ahmed+Saleh+PwC+Dubai",
        "notes": "Partner leading large-scale real estate and giga-project developments advisory in Dubai."
    },
    {
        "company_name": "Deloitte",
        "full_name": "Oliver Morgan",
        "job_title": "Partner & Real Estate Leader – Strategy & Transactions",
        "role_category": "department_leader",
        "email": "oliver.morgan@deloitte.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Oliver+Morgan+Deloitte+Middle+East",
        "notes": "Emaar Square Building 3, Downtown Dubai. Partner leading Real Estate Strategy & Transactions across Middle East."
    },
    {
        "company_name": "Deloitte",
        "full_name": "Dunia Joulani",
        "job_title": "Partner – Infrastructure & Real Estate",
        "role_category": "hiring_manager",
        "email": "dunia.joulani@deloitte.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Dunia+Joulani+Deloitte",
        "notes": "Partner in Deloitte Middle East Infrastructure & Real Estate team."
    },
    {
        "company_name": "KPMG",
        "full_name": "Sidharth Mehta",
        "job_title": "Partner & Head of Real Estate and Construction (KPMG Lower Gulf)",
        "role_category": "department_leader",
        "email": "sidharthmehta@kpmg.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Sidharth+Mehta+KPMG+Lower+Gulf",
        "notes": "KPMG Building, Dubai Festival City. Partner heading Real Estate and Construction practice across UAE."
    },
    {
        "company_name": "KPMG",
        "full_name": "Fahad Kazim",
        "job_title": "Partner – Head of Infrastructure & Real Estate Advisory",
        "role_category": "hiring_manager",
        "email": "fahadkazim@kpmg.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Fahad+Kazim+KPMG",
        "notes": "Partner leading Infrastructure & Real Estate Advisory at KPMG Lower Gulf."
    },
    {
        "company_name": "EY",
        "full_name": "Philippe Najjar",
        "job_title": "Partner – Real Estate, Hospitality & Tourism Practice (Dubai)",
        "role_category": "department_leader",
        "email": "philippe.najjar@ae.ey.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Philippe+Najjar+EY+Dubai",
        "notes": "ICD Brookfield Place, DIFC Dubai. Partner leading Real Estate & Customer Growth Consulting."
    },
    {
        "company_name": "EY",
        "full_name": "Brad Watson",
        "job_title": "Partner – EY-Parthenon MENA Strategy & Transactions Leader",
        "role_category": "hiring_manager",
        "email": "brad.watson@ae.ey.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Brad+Watson+EY-Parthenon",
        "notes": "Leads Real Estate and Infrastructure strategy & transactions across MENA."
    },
    {
        "company_name": "Mastercard",
        "full_name": "Dimitrios Dosis",
        "job_title": "President – Eastern Europe, Middle East and Africa (EEMEA)",
        "role_category": "department_leader",
        "email": "dimitrios.dosis@mastercard.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Dimitrios+Dosis+Mastercard",
        "notes": "President of Mastercard EEMEA Headquarters, Dubai Internet City."
    },
    {
        "company_name": "Mastercard",
        "full_name": "Corporate Real Estate & Facilities Division",
        "job_title": "Head of Corporate Real Estate & Workplace Solutions (EEMEA)",
        "role_category": "hiring_manager",
        "email": "careers@mastercard.com",
        "linkedin_url": "https://www.linkedin.com/company/mastercard",
        "notes": "Mastercard Purpose-Built LEED Gold Headquarters, Dubai Internet City."
    },
    {
        "company_name": "Visa",
        "full_name": "Andrew Torre",
        "job_title": "Regional President – Central & Eastern Europe, Middle East and Africa (CEMEA)",
        "role_category": "department_leader",
        "email": "andrew.torre@visa.com",
        "linkedin_url": "https://www.linkedin.com/search/results/people/?keywords=Andrew+Torre+Visa",
        "notes": "Regional President of Visa CEMEA Headquarters, Dubai Media / Internet City."
    },
    {
        "company_name": "Visa",
        "full_name": "Regional Workplace & Real Estate Division",
        "job_title": "Head of Regional Workplace & Real Estate (CEMEA)",
        "role_category": "hiring_manager",
        "email": "careers@visa.com",
        "linkedin_url": "https://www.linkedin.com/company/visa",
        "notes": "Visa 100,000 sq. ft. Headquarters facility, Dubai Internet City."
    }
]

def seed_big4_and_fintech():
    print("Ingesting Big 4 & Fintech Corporate Real Estate Opportunities...")
    for j in NEW_JOBS:
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

    for c in NEW_CONTACTS:
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

    print("\nSuccessfully seeded Big 4 and Global Fintech leaders!")

if __name__ == "__main__":
    seed_big4_and_fintech()
