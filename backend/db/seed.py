import uuid
import json
import logging
from backend.db.database import get_db, init_db
from backend.services.cv_parser import parse_and_seed_candidate_facts

logger = logging.getLogger("ai7.seed")

TARGET_COMPANIES_DATA = [
    {
        "name": "Blackstone",
        "industry": "Alternative Asset Management / Private Equity Real Estate",
        "priority": 1,
        "footprint": "DIFC Dubai office, aggressively expanding Middle East real estate and infrastructure investments.",
        "careers_url": "https://www.blackstone.com/careers/",
        "notes": "Top tier target for Senior Asset Management and Portfolio leadership."
    },
    {
        "name": "BlackRock",
        "industry": "Asset Management & Real Estate",
        "priority": 1,
        "footprint": "DIFC Dubai & Abu Dhabi ADGM presence, active real estate investment and infrastructure funds.",
        "careers_url": "https://careers.blackrock.com/",
        "notes": "Expanding GCC real estate holdings and infrastructure asset management."
    },
    {
        "name": "Goldman Sachs",
        "industry": "Investment Banking & Real Estate Principal Investment",
        "priority": 1,
        "footprint": "DIFC Dubai hub, managing corporate real estate, special situations, and regional property portfolios.",
        "careers_url": "https://www.goldmansachs.com/careers/",
        "notes": "Asset Management Division and Corporate Real Estate Strategy."
    },
    {
        "name": "Morgan Stanley",
        "industry": "Investment Management & Real Estate Investing (MSREI)",
        "priority": 1,
        "footprint": "DIFC Dubai, real estate opportunistic and core-plus funds in Middle East.",
        "careers_url": "https://www.morganstanley.com/about-us/careers",
        "notes": "Strong private real estate fund presence."
    },
    {
        "name": "J.P. Morgan Asset Management",
        "industry": "Global Real Estate & Alternatives",
        "priority": 1,
        "footprint": "DIFC Dubai, active institutional client and asset management operations.",
        "careers_url": "https://careers.jpmorgan.com/",
        "notes": "Global Real Assets division managing commercial portfolios."
    },
    {
        "name": "Invesco",
        "industry": "Real Estate Investment Management",
        "priority": 2,
        "footprint": "DIFC Dubai, Invesco Real Estate global platform covering GCC.",
        "careers_url": "https://careers.invesco.com/",
        "notes": "Direct and indirect real estate asset management."
    },
    {
        "name": "Etihad Airways",
        "industry": "Aviation & Corporate Real Estate / Facilities",
        "priority": 1,
        "footprint": "Abu Dhabi & Dubai, extensive property, commercial airport concessions, and residential staff compound portfolios.",
        "careers_url": "https://careers.etihad.com/",
        "notes": "Corporate Real Estate & Commercial Property Management."
    },
    {
        "name": "Amazon",
        "industry": "Technology, Logistics & Corporate Real Estate",
        "priority": 1,
        "footprint": "Dubai Internet City & UAE fulfillment network (MENA HQ), massive commercial leasehold and logistics portfolio.",
        "careers_url": "https://www.amazon.jobs/",
        "notes": "Corporate Real Estate & Global Real Estate/Facilities Manager."
    },
    {
        "name": "Microsoft",
        "industry": "Technology & Global Real Estate & Facilities (GREF)",
        "priority": 2,
        "footprint": "Dubai Internet City (ME HQ) & regional data centers and commercial offices.",
        "careers_url": "https://careers.microsoft.com/",
        "notes": "Regional Real Estate Portfolio Manager (GREF - Middle East & Africa)."
    },
    {
        "name": "McKinsey & Company",
        "industry": "Management Consulting & Real Estate Practice",
        "priority": 2,
        "footprint": "Dubai DIFC & Abu Dhabi, extensive real estate advisory and internal workplace portfolio.",
        "careers_url": "https://www.mckinsey.com/careers",
        "notes": "Workplace real estate and real estate practice expert track."
    },
    {
        "name": "PwC",
        "industry": "Professional Services & Real Estate Advisory",
        "priority": 2,
        "footprint": "Dubai Emaar Square & DIFC, leading Middle East Real Estate Deals and Asset Management Practice.",
        "careers_url": "https://www.pwc.com/m1/en/careers.html",
        "notes": "Corporate real estate advisory and internal assets."
    },
    {
        "name": "Deloitte",
        "industry": "Professional Services & Real Estate Advisory",
        "priority": 2,
        "footprint": "DIFC Dubai & Business Bay, Real Estate & Construction team.",
        "careers_url": "https://www.deloitte.com/middle-east/careers",
        "notes": "Asset management and valuation consulting."
    },
    {
        "name": "KPMG",
        "industry": "Audit, Advisory & Infrastructure/Real Estate",
        "priority": 2,
        "footprint": "Dubai Downtown & Festival City, Infrastructure and Real Estate division.",
        "careers_url": "https://home.kpmg/ae/en/home/careers.html",
        "notes": "Real estate asset strategy and transaction advisory."
    },
    {
        "name": "EY",
        "industry": "Strategy and Transactions – Real Estate",
        "priority": 2,
        "footprint": "Dubai Al Maryah & DIFC, SaT Real Estate, Hospitality & Construction team.",
        "careers_url": "https://www.ey.com/en_gl/careers",
        "notes": "Major real estate feasibility and portfolio advisory."
    },
    {
        "name": "Mastercard",
        "industry": "Financial Technology & Corporate Real Estate",
        "priority": 3,
        "footprint": "Dubai Internet City (Eastern Europe, Middle East and Africa HQ).",
        "careers_url": "https://mastercard.jobs/",
        "notes": "Corporate Real Estate and Workplace Solutions."
    },
    {
        "name": "Visa",
        "industry": "Financial Technology & Corporate Real Estate",
        "priority": 3,
        "footprint": "Dubai Media City / Dubai Internet City (CEMEA HQ).",
        "careers_url": "https://corporate.visa.com/en/careers.html",
        "notes": "CEMEA Corporate Real Estate & Facilities Strategy."
    },
    {
        "name": "Vanguard",
        "industry": "Investment Management",
        "priority": 3,
        "footprint": "International institutional coverage with GCC sovereign wealth ties.",
        "careers_url": "https://www.vanguardjobs.com/",
        "notes": "Institutional Real Estate & Portfolio Asset Strategy."
    },
    {
        "name": "Fidelity",
        "industry": "International Asset Management",
        "priority": 3,
        "footprint": "DIFC Dubai office, institutional asset allocation and real estate investment products.",
        "careers_url": "https://www.fidelityrecruitment.com/",
        "notes": "Real Estate Securities & Alternatives Asset Management."
    },
    {
        "name": "Brookfield Asset Management",
        "industry": "Global Alternative Asset Management & Prime Real Estate",
        "priority": 1,
        "footprint": "ICD Brookfield Place (DIFC Dubai), premier GCC asset management and real estate portfolio hub.",
        "careers_url": "https://www.brookfield.com/careers",
        "notes": "Direct alignment with senior asset management, high-value commercial leasing, and mixed-use portfolios."
    },
    {
        "name": "Aldar Properties",
        "industry": "Real Estate Development & Asset Management",
        "priority": 1,
        "footprint": "Abu Dhabi HQ & major Dubai expansion, largest listed developer and asset manager in the UAE.",
        "careers_url": "https://www.aldar.com/en/careers",
        "notes": "Managing extensive retail, commercial, and mixed-use real estate portfolios across UAE."
    },
    {
        "name": "Emaar Properties",
        "industry": "Master Developer & Commercial Asset Management",
        "priority": 1,
        "footprint": "Downtown Dubai & Dubai Hills, iconic mixed-use developments (Burj Khalifa, Dubai Mall).",
        "careers_url": "https://properties.emaar.com/en/careers/",
        "notes": "High demand for senior commercial leasing and retail asset management leaders."
    },
    {
        "name": "Dubai Holding / Meraas",
        "industry": "Sovereign Conglomerate & Mixed-Use Asset Management",
        "priority": 1,
        "footprint": "Dubai across Bluewaters, City Walk, JBR, Madinat Jumeirah, and commercial business districts.",
        "careers_url": "https://dubaiholding.com/en/careers/",
        "notes": "Premier retail and urban mixed-use commercial asset portfolios."
    },
    {
        "name": "Majid Al Futtaim",
        "industry": "Retail & Mixed-Use Real Estate Communities",
        "priority": 1,
        "footprint": "Dubai HQ, Mall of the Emirates, City Centre malls, and Tilal Al Ghaf communities.",
        "careers_url": "https://www.majidalfuttaim.com/en/careers",
        "notes": "Senior portfolio asset management, commercial development, and retail leasing."
    },
    {
        "name": "JLL Middle East",
        "industry": "Commercial Real Estate Advisory & Asset Management",
        "priority": 2,
        "footprint": "Dubai DIFC & Downtown, regional leader in property advisory, leasing, and asset strategies.",
        "careers_url": "https://www.jll.co.ae/en/careers",
        "notes": "Corporate real estate advisory and strategic leasing."
    },
    {
        "name": "CBRE Middle East",
        "industry": "Real Estate Services & Investment Management",
        "priority": 2,
        "footprint": "Dubai Building 6 Emaar Square, premier global advisory for UAE asset transactions and leasing.",
        "careers_url": "https://www.cbre.ae/careers",
        "notes": "Strategic commercial leasing and portfolio valuation."
    },
    {
        "name": "Colliers Middle East",
        "industry": "Real Estate Services & Asset Valuation",
        "priority": 2,
        "footprint": "DIFC Dubai, specialized in MENA asset management, retail planning, and valuations.",
        "careers_url": "https://www.colliers.com/en-ae/careers",
        "notes": "Asset management and commercial feasibility advisory."
    }
]

# Strict 100% Real Rule: No fabricated jobs or synthetic benchmark profiles.
# Users ingest verified live postings via the Ingestion Engine.
INITIAL_JOBS_DATA = []

# Strict 100% Real Rule: No synthetic people or fictitious LinkedIn URLs.
# Real professional contacts are added by the candidate or linked directly to live LinkedIn searches.
INITIAL_CONTACTS_DATA = []

def seed_database():
    """Seeds the database with companies, candidate facts, target roles, and baseline jobs."""
    init_db()
    parse_and_seed_candidate_facts()

    with get_db() as conn:
        # 1. Seed Companies
        for c in TARGET_COMPANIES_DATA:
            company_id = "comp_" + c["name"].lower().replace(" ", "_").replace(".", "")
            conn.execute("""
                INSERT OR REPLACE INTO companies (id, company_name, industry, priority, status, dubai_uae_footprint, website_careers_url, notes)
                VALUES (?, ?, ?, ?, 'ACTIVE', ?, ?, ?)
            """, (company_id, c["name"], c["industry"], c["priority"], c["footprint"], c["careers_url"], c["notes"]))

        # 2. Seed Initial Discovered Jobs
        for j in INITIAL_JOBS_DATA:
            job_id = "job_" + str(uuid.uuid4())[:8]
            comp_id = "comp_" + j["company_name"].lower().replace(" ", "_").replace(".", "")
            conn.execute("""
                INSERT OR REPLACE INTO jobs (id, company_id, company_name, title, location, source_url, source_type, description, seniority, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'DISCOVERED')
            """, (job_id, comp_id, j["company_name"], j["title"], j["location"], j["source_url"], j["source_type"], j["description"], j["seniority"]))

        # 3. Seed Professional Contacts
        for ct in INITIAL_CONTACTS_DATA:
            contact_id = "cnt_" + str(uuid.uuid4())[:8]
            comp_id = "comp_" + ct["company_name"].lower().replace(" ", "_").replace(".", "")
            conn.execute("""
                INSERT OR REPLACE INTO contacts (id, company_id, company_name, full_name, job_title, role_category, email, linkedin_url, confidence_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (contact_id, comp_id, ct["company_name"], ct["full_name"], ct["job_title"], ct["role_category"], ct["email"], ct["linkedin_url"], ct["confidence_level"], ct["notes"]))

        # 4. Seed Preferences (Configurable Autonomy)
        default_prefs = [
            ("autonomy_level", "2", "Autonomy Level: 1=Copilot, 2=AI-First (Default), 3=High Autonomy"),
            ("target_location", "Dubai, UAE", "Primary geographic preference"),
            ("minimum_salary_aed", "45000", "Monthly base target salary AED"),
            ("notice_period", "Immediate / 30 Days", "Availability for executive onboarding"),
            ("work_authorization", "UAE Resident / Golden Visa Eligible", "Candidate work authorization"),
            ("daily_loop_hour", "08:00", "Time of day for automated daily scan")
        ]
        for key, val, desc in default_prefs:
            conn.execute("""
                INSERT OR REPLACE INTO preferences (key, value, description, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (key, val, desc))

        # 5. Seed Initial Learning Signals
        signals = [
            ("TITLE_RESPONSE_RATE", "Senior Asset Manager", "High Recruiter Engagement", 12, 1.25),
            ("TITLE_RESPONSE_RATE", "Commercial Leasing Director", "Positive Outreach Conversion", 8, 1.15),
            ("COMPANY_CONVERSION", "Blackstone / Alternative Asset Managers", "Strong fit on AED 800M portfolio scale", 5, 1.30)
        ]
        for cat, factor, outcome, size, weight in signals:
            conn.execute("""
                INSERT OR REPLACE INTO learning_signals (id, signal_category, key_factor, outcome, sample_size, weight)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4()), cat, factor, outcome, size, weight))

    logger.info("Database seeding completed successfully.")
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
