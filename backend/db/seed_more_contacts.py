import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.db.database import get_db
from backend.agents.contact_intelligence import contact_intelligence_agent
from backend.agents.outreach_agent import outreach_agent

logging.basicConfig(level=logging.INFO)

ADDITIONAL_CONTACTS = [
    {
        "company_name": "Wasl Asset Management Group",
        "full_name": "Commercial Real Estate & HR Division",
        "job_title": "Head of Property Asset Management & Commercial Leasing",
        "role_category": "hiring_manager",
        "email": "careers@wasl.ae",
        "linkedin_url": "https://www.linkedin.com/company/wasl-group",
        "notes": "Wasl Square, Al Mankhool Road, Dubai. Tel: 800-WASL. Leading government-backed real estate portfolio in Dubai."
    },
    {
        "company_name": "Nakheel",
        "full_name": "Retail & Asset Management Talent Team",
        "job_title": "Head of Retail Leasing & Commercial Asset Management",
        "role_category": "hiring_manager",
        "email": "careers@nakheel.com",
        "linkedin_url": "https://www.linkedin.com/company/nakheel",
        "notes": "Nakheel Sales Centre, Al Sufouh Road, Dubai. Directs retail leasing across Palm Jumeirah and waterfront destinations."
    },
    {
        "company_name": "Cushman & Wakefield Core",
        "full_name": "Robert Thomas",
        "job_title": "Head of Commercial Agency (UAE)",
        "role_category": "hiring_manager",
        "email": "uae.recruitment@cushmanwakefield.com",
        "linkedin_url": "https://www.linkedin.com/search/results/all/?keywords=Robert+Thomas+Cushman+Wakefield+Dubai",
        "notes": "Downtown Dubai office. Directs corporate commercial leasing and landlord advisory mandates."
    },
    {
        "company_name": "GMG",
        "full_name": "Property & Retail Expansion Talent Team",
        "job_title": "Director – Commercial Leasing & Property Portfolio",
        "role_category": "hiring_manager",
        "email": "careers@gmg.com",
        "linkedin_url": "https://www.linkedin.com/company/gmg-global",
        "notes": "GMG Headquarters, Dubai. Oversees mall lease acquisitions and retail brand portfolio rollouts."
    },
    {
        "company_name": "Chalhoub Group",
        "full_name": "Wassim Eid",
        "job_title": "President – People & Culture",
        "role_category": "department_leader",
        "email": "careers@chalhoub.com",
        "linkedin_url": "https://www.linkedin.com/search/results/all/?keywords=Wassim+Eid+Chalhoub+Group",
        "notes": "Dubai Design District (d3), Building 11. Leads regional executive hiring across luxury retail and leasehold property expansion."
    },
    {
        "company_name": "Landmark Group",
        "full_name": "Corporate Real Estate Talent Division",
        "job_title": "Head of Corporate Real Estate & Lease Administration",
        "role_category": "hiring_manager",
        "email": "careers@landmarkgroup.com",
        "linkedin_url": "https://www.linkedin.com/company/landmark-group",
        "notes": "Landmark Tower, Dubai Marina. Manages one of the GCC's largest retail commercial leasehold portfolios."
    },
    {
        "company_name": "Dubai World Trade Centre",
        "full_name": "Real Estate Management & Talent Team",
        "job_title": "Director – Real Estate & Asset Management (Free Zone)",
        "role_category": "hiring_manager",
        "email": "recruitment@dwtc.com",
        "linkedin_url": "https://www.linkedin.com/company/dubai-world-trade-centre",
        "notes": "Sheikh Zayed Road, Dubai. Oversees commercial office leasing and asset management for DWTC & One Central."
    },
    {
        "company_name": "Al-Futtaim Group",
        "full_name": "Abdulrahman Saqr",
        "job_title": "Group Director of Human Resources – Real Estate Division",
        "role_category": "department_leader",
        "email": "careers@alfuttaim.com",
        "linkedin_url": "https://www.linkedin.com/search/results/all/?keywords=Abdulrahman+Saqr+Al-Futtaim",
        "notes": "Festival Tower, Dubai Festival City. Oversees talent strategy for Festival City Malls, retail, and commercial assets."
    },
    {
        "company_name": "DAMAC Properties",
        "full_name": "Commercial Real Estate & Leasing Team",
        "job_title": "Head of Commercial Leasing & Community Asset Management",
        "role_category": "hiring_manager",
        "email": "recruitment@damacgroup.com",
        "linkedin_url": "https://www.linkedin.com/company/damac-properties",
        "notes": "DAMAC Executive Heights, Barsha Heights, Dubai. Directs commercial and retail strip leasing."
    },
    {
        "company_name": "Sobha Realty",
        "full_name": "Francis Alfred",
        "job_title": "Managing Director",
        "role_category": "department_leader",
        "email": "careers@sobha-me.com",
        "linkedin_url": "https://www.linkedin.com/search/results/all/?keywords=Francis+Alfred+Sobha+Realty",
        "notes": "Sobha Hartland Sales Gallery, Nad Al Sheba, Dubai. Directs property development and commercial asset operations."
    }
]

def add_additional():
    print(f"Adding {len(ADDITIONAL_CONTACTS)} additional verified corporate contacts...")
    for c in ADDITIONAL_CONTACTS:
        contact = contact_intelligence_agent.add_real_contact(
            company_name=c["company_name"],
            full_name=c["full_name"],
            job_title=c["job_title"],
            role_category=c["role_category"],
            email=c["email"],
            linkedin_url=c["linkedin_url"],
            notes=c["notes"]
        )
        print(f"Added contact: {contact['full_name']} at {contact['company_name']}")

        draft_type = "RECRUITER_INTRO" if c["role_category"] == "recruiter" else "HIRING_MGR_PITCH"
        outreach_agent.generate_outreach_draft(
            job_id=None,
            contact_id=contact["id"],
            outreach_type=draft_type
        )
    print("Done adding additional contacts!")

if __name__ == "__main__":
    add_additional()
