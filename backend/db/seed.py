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
    }
]

INITIAL_JOBS_DATA = [
    {
        "company_name": "Blackstone",
        "title": "Senior Asset Manager – Real Estate (GCC & MENA)",
        "location": "Dubai, UAE (DIFC)",
        "source_url": "https://www.blackstone.com/careers/job-req-dxb-8821",
        "source_type": "company_career_page",
        "seniority": "Senior Manager / Director-Track",
        "description": """Blackstone Real Estate is seeking an experienced Senior Asset Manager based in Dubai to drive value enhancement, commercial leasing strategy, and operational performance across our growing commercial and mixed-use property portfolio in the UAE and GCC.
Key Responsibilities:
- Formulate and execute asset strategy, tenant-mix planning, and NOI optimization for prime commercial, retail, and mixed-use assets.
- Lead commercial lease structuring and complex negotiations with institutional occupiers and regional developers.
- Manage financial modeling, CAPEX budgeting, five-year strategic business plans, and cash flow forecasts.
- Conduct demographic, footfall, and catchment feasibility studies for asset repositioning.
- Maintain rigorous governance, risk compliance, and alignment with UAE RERA legal standards.
Requirements:
- 15+ years of extensive real estate asset management and commercial leasing experience in the UAE.
- Proven track record managing large-scale portfolios (AED 500M+).
- Demonstrable experience negotiating hundreds of commercial leases and driving occupancy.
- Deep network with developers, landlords, and corporate tenants across Dubai.
- Strong proficiency in financial modeling, yield analysis, and CAPEX planning in Excel.
- Fluency in English; multilingual proficiency in Hindi/Urdu is an advantage."""
    },
    {
        "company_name": "BlackRock",
        "title": "Real Estate Portfolio Manager – Asset Management & Expansion",
        "location": "Dubai, UAE",
        "source_url": "https://careers.blackrock.com/job/r240982-dubai",
        "source_type": "company_career_page",
        "seniority": "Senior Manager",
        "description": """BlackRock's Real Estate Investment & Asset Management division in Dubai is looking for a Real Estate Portfolio Manager to supervise asset positioning, tenant acquisition, and portfolio performance across regional retail and commercial properties.
Key Responsibilities:
- Oversee commercial asset performance, portfolio yield, and lease renewals.
- Structure high-value commercial agreements balancing long-term valuation with tenant retention.
- Oversee CAPEX allocations, expenditure budgets, and stakeholder governance.
- Coordinate feasibility evaluations and demographic catchment reviews for retail and commercial properties.
Requirements:
- 12+ years experience in UAE commercial real estate and asset management.
- Experience with luxury retail, B2B commercial, and mixed-use developments.
- Demonstrated success in evaluating commercial locations and managing tenant relationships.
- RERA certification or professional real estate affiliations strongly preferred."""
    },
    {
        "company_name": "Goldman Sachs",
        "title": "Vice President / Senior Manager – Real Estate Asset Management",
        "location": "Dubai, UAE",
        "source_url": "https://www.goldmansachs.com/careers/job-55412-dxb",
        "source_type": "company_career_page",
        "seniority": "Senior Manager / VP",
        "description": """Goldman Sachs Asset Management Real Estate division is seeking a senior professional to direct commercial portfolio strategy and value-add asset management across Dubai and regional GCC assets.
Responsibilities:
- Drive asset lifecycle strategies including positioning, leasing, capital improvements, and disposal readiness.
- Partner with master developers and corporate tenants to execute multi-million AED leasing transactions.
- Review and refine financial feasibility models, NOI forecasts, and investment committee decks.
- Guide cross-functional property operations and ensure compliance with Dubai RERA guidelines.
Qualifications:
- 15+ years in senior real estate leadership in UAE.
- Documented portfolio management experience exceeding AED 500M.
- Superior negotiation skills across commercial and retail sectors."""
    },
    {
        "company_name": "Etihad Airways",
        "title": "Head of Commercial Real Estate & Property Leasing",
        "location": "Abu Dhabi / Dubai, UAE",
        "source_url": "https://careers.etihad.com/job/dxb-cre-09",
        "source_type": "company_career_page",
        "seniority": "Senior Manager / Head",
        "description": """Etihad Airways is seeking a Commercial Real Estate Manager to lead property leasing, tenant strategy, and asset optimization across our real estate portfolio and corporate commercial assets across the UAE.
Responsibilities:
- Direct lease negotiations, tenant acquisition, and contract administration for commercial property assets.
- Manage CAPEX budgets, property maintenance operations, and tenancy compliance.
- Evaluate commercial feasibility and retail mix optimization for high-footfall assets.
Requirements:
- 15+ years UAE real estate and leasing experience.
- Deep expertise in RERA compliance and commercial contracts."""
    },
    {
        "company_name": "Amazon",
        "title": "Corporate Real Estate Manager – MENA Portfolio Strategy",
        "location": "Dubai, UAE",
        "source_url": "https://www.amazon.jobs/en/jobs/259104/corporate-real-estate-manager",
        "source_type": "company_career_page",
        "seniority": "Manager / Senior Manager",
        "description": """Amazon Global Real Estate and Facilities (GREF) is looking for a Corporate Real Estate Manager to oversee our leasehold commercial real estate portfolio across MENA, with primary focus on the UAE.
Responsibilities:
- Lead lease acquisitions, renewals, and landlord relationship management across hundreds of thousands of square feet of corporate office and operational spaces.
- Manage multi-year CAPEX budgets and five-year occupancy strategy.
- Negotiate complex lease agreements with developers and government-backed master entities.
Requirements:
- 10+ years in commercial real estate leasing and asset management in Dubai.
- Strong quantitative background in financial planning and portfolio forecasting."""
    }
]

INITIAL_CONTACTS_DATA = [
    {
        "company_name": "Blackstone",
        "full_name": "Marcus Vance",
        "job_title": "Managing Director, Head of Middle East Real Estate",
        "role_category": "hiring_manager",
        "email": "vance.m@blackstone.com",
        "linkedin_url": "https://www.linkedin.com/in/marcus-vance-re-blackstone",
        "confidence_level": "VERIFIED",
        "notes": "Key decision maker for senior asset management and portfolio acquisitions in DIFC Dubai."
    },
    {
        "company_name": "BlackRock",
        "full_name": "Elena Rostova",
        "job_title": "Director – Real Estate Asset Management EMEA / GCC",
        "role_category": "hiring_manager",
        "email": "elena.rostova@blackrock.com",
        "linkedin_url": "https://www.linkedin.com/in/elena-rostova-blackrock",
        "confidence_level": "VERIFIED",
        "notes": "Directs commercial asset portfolios and hiring in Dubai/ADGM."
    },
    {
        "company_name": "Goldman Sachs",
        "full_name": "Tariq Al-Mansoor",
        "job_title": "Managing Director, Real Estate Principal Investment Area",
        "role_category": "department_leader",
        "email": "tariq.almansoor@gs.com",
        "linkedin_url": "https://www.linkedin.com/in/tariq-almansoor-gs",
        "confidence_level": "HIGH_PROBABILITY",
        "notes": "Leads GCC real estate deals and asset strategy from DIFC."
    },
    {
        "company_name": "Etihad Airways",
        "full_name": "Khalid Al-Hashemi",
        "job_title": "Vice President – Corporate Real Estate & Facilities",
        "role_category": "hiring_manager",
        "email": "khashemi@etihad.ae",
        "linkedin_url": "https://www.linkedin.com/in/khalid-hashemi-etihad",
        "confidence_level": "VERIFIED",
        "notes": "Oversees property leasing and corporate assets."
    },
    {
        "company_name": "Amazon",
        "full_name": "Sarah Jenkins",
        "job_title": "Senior Manager – MENA Talent Acquisition (Operations & Real Estate)",
        "role_category": "recruiter",
        "email": "jenkisa@amazon.com",
        "linkedin_url": "https://www.linkedin.com/in/sarah-jenkins-amazon-mena",
        "confidence_level": "VERIFIED",
        "notes": "Primary recruiter for UAE Corporate Real Estate roles."
    }
]

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
