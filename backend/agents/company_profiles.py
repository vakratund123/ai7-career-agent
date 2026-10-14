"""
Comprehensive Company Intelligence Profiles & Tailored Outreach Generator for V. Jagannath.
Maps all 45 target employers to their signature Dubai/UAE assets, corporate strategy,
and crafts bespoke, company-profile-grounded Email Pitches and LinkedIn Notes.
"""

from typing import Dict, Any, Optional

COMPANY_PROFILES: Dict[str, Dict[str, str]] = {
    # ----------------- PRIME DEVELOPERS -----------------
    "Emaar Properties": {
        "sector": "Prime Developer",
        "signature_assets": "Downtown Dubai, Dubai Mall, Dubai Hills Estate, and Dubai Creek Harbour",
        "corporate_focus": "driving premier retail and commercial asset yields across master-planned lifestyle communities",
        "jagannath_hook": "directing commercial leasing and asset strategies across 800,000 sq. ft. of flagship mixed-use space (including One Za'abeel) within an AED 800M portfolio",
        "value_prop": "commercial leasing governance, high-value tenant acquisition, and master-plan yield optimization",
        "linkedin_angle": "Emaar's iconic Downtown and master community retail footprint"
    },
    "Aldar Properties": {
        "sector": "Prime Developer",
        "signature_assets": "Yas Island, Saadiyat Cultural District, and accelerated Dubai commercial/logistics expansion",
        "corporate_focus": "scaling prime commercial, retail, and logistics asset platforms across Abu Dhabi and Dubai",
        "jagannath_hook": "20+ years of UAE commercial leasing, negotiating 2,500+ commercial transactions and steering multi-asset commercialization",
        "value_prop": "strategic portfolio expansion, RERA governance, and tenant relationship stewardship across UAE markets",
        "linkedin_angle": "Aldar's strategic commercial asset expansion across Dubai and the Northern Emirates"
    },
    "Wasl Asset Management Group": {
        "sector": "Prime Developer / Master Asset Manager",
        "signature_assets": "Over 50,000 residential and commercial units, Wasl Tower, and prime hospitality assets across Dubai",
        "corporate_focus": "managing one of Dubai's largest and most diversified government real estate portfolios",
        "jagannath_hook": "overseeing an AED 800M commercial and mixed-use portfolio with 2,500+ lease negotiations executed under institutional governance",
        "value_prop": "large-scale leasing operations, tenant retention, CAPEX efficiency, and long-term asset value enhancement",
        "linkedin_angle": "Wasl's extensive Dubai property portfolio and landmark developments like Wasl Tower"
    },
    "Nakheel": {
        "sector": "Prime Developer",
        "signature_assets": "Palm Jumeirah, Dubai Islands, Nakheel Mall, and waterfront community commercial centers",
        "corporate_focus": "reimagining waterfront retail and community commercial assets to capture expanding GCC demographic growth",
        "jagannath_hook": "evaluating 300+ commercial locations through demographic catchment modeling and directing high-footfall retail leasing",
        "value_prop": "retail curation, footfall-to-turnover revenue optimization, and master-community asset stewardship",
        "linkedin_angle": "Nakheel's transformative Dubai Islands and master community retail developments"
    },
    "Dubai Holding / Meraas": {
        "sector": "Prime Developer",
        "signature_assets": "Bluewaters, City Walk, JBR, Madinat Jumeirah, and Dubai Creek Harbour",
        "corporate_focus": "delivering Dubai's most vibrant lifestyle, urban retail, and commercial destinations",
        "jagannath_hook": "leading commercial leasing at Ithra Dubai / ICD across luxury retail and B2B commercial space (including One Za'abeel and Deira Enrichment)",
        "value_prop": "luxury brand placement, urban retail lease structuring, and destination asset management",
        "linkedin_angle": "Dubai Holding / Meraas's signature lifestyle and urban retail portfolio"
    },
    "Majid Al Futtaim": {
        "sector": "Prime Developer / Mall Operator",
        "signature_assets": "Mall of the Emirates, City Centre regional shopping malls, and Tilal Al Ghaf mixed-use community",
        "corporate_focus": "setting the benchmark for integrated lifestyle destinations and destination shopping malls across MENA",
        "jagannath_hook": "2,500+ lease agreements successfully negotiated with top-tier international and regional retail brands",
        "value_prop": "turnover rent structuring, base rent indexation, tenant covenant protection, and retail asset performance",
        "linkedin_angle": "Majid Al Futtaim's regional shopping mall network and Tilal Al Ghaf community assets"
    },
    "DAMAC Properties": {
        "sector": "Prime Developer",
        "signature_assets": "DAMAC Hills 1 & 2, Business Bay commercial towers, and luxury branded residences across Dubai",
        "corporate_focus": "accelerating luxury property development and maximizing commercial asset operational yields",
        "jagannath_hook": "directing asset management and leasing operations across AED 800M+ in commercial/mixed-use properties",
        "value_prop": "rapid tenant acquisition, occupancy optimization, and commercial lease administration",
        "linkedin_angle": "DAMAC's prime commercial assets and master community developments in Dubai"
    },
    "Sobha Realty": {
        "sector": "Prime Developer",
        "signature_assets": "Sobha Hartland 1 & 2, Sobha Seahaven, and luxury commercial/retail developments in MBR City",
        "corporate_focus": "crafting ultra-luxury, backward-integrated residential and commercial master communities",
        "jagannath_hook": "driving premium commercial asset strategy, high-finish retail leasing, and luxury tenant curation",
        "value_prop": "high-net-worth tenant engagement, commercial lease governance, and asset lifecycle enhancement",
        "linkedin_angle": "Sobha's ultra-luxury developments across Sobha Hartland and Dubai water canal"
    },

    # ----------------- SOVEREIGN WEALTH & GOVERNMENT -----------------
    "Investment Corporation of Dubai": {
        "sector": "Sovereign Wealth",
        "signature_assets": "Ithra Dubai, One Za'abeel, ICD Brookfield Place, and strategic state real estate holdings",
        "corporate_focus": "stewarding the Government of Dubai's primary commercial asset and strategic infrastructure holdings",
        "jagannath_hook": "proven institutional track record as Leasing Lead at Ithra Dubai LLC, directing 800,000 sq. ft. of space across One Za'abeel and Deira Enrichment within an AED 800M portfolio",
        "value_prop": "immediate institutional continuity, ICD-entity governance familiarity, and deep landlord-tenant leasing mastery",
        "linkedin_angle": "ICD's landmark portfolio, building upon my direct leadership with Ithra Dubai on One Za'abeel"
    },
    "Mubadala Investment Company": {
        "sector": "Sovereign Wealth",
        "signature_assets": "Al Maryah Island (ADGM), Grade A institutional office towers, and global real estate platforms",
        "corporate_focus": "deploying long-term sovereign capital into high-conviction, resilient commercial and real assets",
        "jagannath_hook": "managing an AED 800M diversified portfolio under institutional ICD governance with 2,500+ commercial lease executions",
        "value_prop": "institutional asset underwriting, yield defense, covenant analysis, and disciplined landlord stewardship",
        "linkedin_angle": "Mubadala's institutional real estate and commercial asset management strategy in the UAE"
    },
    "Dubai World Trade Centre": {
        "sector": "Government Business Hub",
        "signature_assets": "One Central, DWTC Free Zone, and premier commercial office buildings hosting multinational HQs",
        "corporate_focus": "powering Dubai's global business and exhibition infrastructure with prime commercial real estate",
        "jagannath_hook": "leading commercial leasing across One Za'abeel and Deira Enrichment, negotiating with Fortune 500 corporate occupiers",
        "value_prop": "Grade A commercial leasing, free zone tenant acquisition, lease administration, and occupancy maximization",
        "linkedin_angle": "DWTC's One Central commercial district and prime free zone office assets"
    },

    # ----------------- INSTITUTIONAL ASSET MANAGEMENT & PE -----------------
    "Brookfield Asset Management": {
        "sector": "Institutional Real Estate & PE",
        "signature_assets": "ICD Brookfield Place in DIFC and premier Grade A commercial real estate platforms globally",
        "corporate_focus": "delivering premier institutional asset management and premium workspace experiences in the GCC",
        "jagannath_hook": "managing an AED 800M portfolio with ICD-ecosystem leadership (Ithra Dubai / One Za'abeel) and 2,500+ commercial lease negotiations",
        "value_prop": "Grade A landlord representation, premium corporate tenant retention, and disciplined asset yield governance",
        "linkedin_angle": "Brookfield's institutional Grade A asset management and ICD Brookfield Place excellence"
    },
    "Blackstone": {
        "sector": "Institutional Real Estate & PE",
        "signature_assets": "Global logistics networks, premier Grade A commercial offices, and hospitality asset platforms",
        "corporate_focus": "accelerating direct real estate investment and opportunistic asset management across the Middle East",
        "jagannath_hook": "directing asset management and leasing for an AED 800M commercial and mixed-use portfolio in Dubai",
        "value_prop": "asset yield optimization, CAPEX governance, tenant covenant restructuring, and institutional portfolio stewardship",
        "linkedin_angle": "Blackstone's Middle East real estate expansion and high-yield commercial asset strategy"
    },
    "BlackRock": {
        "sector": "Institutional Asset Management",
        "signature_assets": "Real Assets and Infrastructure equity platforms operating through ADGM and DIFC hubs",
        "corporate_focus": "scaling institutional real estate equity, sustainable assets, and long-term tenant value retention in the GCC",
        "jagannath_hook": "20 years of UAE commercial asset management, executing 2,500+ commercial leases under institutional standards",
        "value_prop": "institutional portfolio governance, ESG compliance, lease yield protection, and disciplined tenant underwriting",
        "linkedin_angle": "BlackRock's GCC Real Assets platform and institutional property investment strategy"
    },
    "Goldman Sachs": {
        "sector": "Investment Banking & Real Estate",
        "signature_assets": "Real Estate Principal Investment Area (REPIA) and DIFC regional investment operations",
        "corporate_focus": "identifying opportunistic commercial asset investments and optimizing corporate real estate portfolios in the GCC",
        "jagannath_hook": "AED 800M portfolio track record, feasibility modeling across 300+ locations, and 2,500+ executed lease transactions",
        "value_prop": "commercial underwriting, yield enhancement, lease negotiation strategy, and stakeholder alignment",
        "linkedin_angle": "Goldman Sachs's real estate investment activities and corporate property footprint in the GCC"
    },
    "Morgan Stanley": {
        "sector": "Investment Banking & Real Estate",
        "signature_assets": "Real Estate Investing (MSREI) and regional wealth/corporate advisory in DIFC",
        "corporate_focus": "structuring prime real estate asset acquisitions and maximizing asset value across GCC core markets",
        "jagannath_hook": "leading leasing and asset strategy across 800,000 sq. ft. of prime space within an AED 800M portfolio",
        "value_prop": "asset yield enhancement, covenant evaluation, RERA regulatory alignment, and institutional lease execution",
        "linkedin_angle": "Morgan Stanley's Middle East real estate investment and asset advisory mandate"
    },
    "J.P. Morgan Asset Management": {
        "sector": "Institutional Asset Management",
        "signature_assets": "Global Real Estate (GRE) platform and DIFC executive operations",
        "corporate_focus": "deploying institutional capital into Grade A commercial properties and mixed-use real estate in prime hubs",
        "jagannath_hook": "managing an AED 800M mixed-use portfolio with 2,500+ commercial lease negotiations completed",
        "value_prop": "disciplined landlord stewardship, corporate occupier relations, and portfolio cash-flow optimization",
        "linkedin_angle": "J.P. Morgan Asset Management's real estate and commercial property platform in Dubai"
    },
    "KKR": {
        "sector": "Private Equity & Real Estate",
        "signature_assets": "Real Estate Equity & Credit strategies expanding across the GCC via DIFC/ADGM",
        "corporate_focus": "acquiring high-quality commercial assets and driving operational transformation to optimize cash yield",
        "jagannath_hook": "proven operational turnaround and leasing direction for 800,000 sq. ft. of luxury commercial/retail assets",
        "value_prop": "hands-on operational asset enhancement, leasing speed, and institutional capital discipline",
        "linkedin_angle": "KKR's real estate private equity initiatives and commercial property investments in the region"
    },
    "Apollo Global Management": {
        "sector": "Private Equity & Real Assets",
        "signature_assets": "Real Estate Credit and opportunistic commercial equity platforms across MENA",
        "corporate_focus": "partnering with regional developers and institutions to structure high-yield real estate investments",
        "jagannath_hook": "AED 800M portfolio leadership, 2,500+ leases negotiated, and ICD entity governance track record",
        "value_prop": "commercial lease restructuring, risk-mitigated asset management, and tenant yield maximization",
        "linkedin_angle": "Apollo's real estate credit and commercial asset investment strategy in the UAE"
    },
    "The Carlyle Group": {
        "sector": "Private Equity & Real Estate",
        "signature_assets": "Global Real Estate funds investing across commercial, logistics, and mixed-use sectors",
        "corporate_focus": "generating long-term value through active asset management and strategic tenant repositioning",
        "jagannath_hook": "20 years of UAE commercial leasing, overseeing landmark ICD-backed developments like One Za'abeel",
        "value_prop": "value-add leasing strategy, high-retention tenant curation, and commercial performance enhancement",
        "linkedin_angle": "Carlyle's real estate private equity and asset value creation initiatives in the GCC"
    },
    "Invesco": {
        "sector": "Asset Management",
        "signature_assets": "Global Real Estate investment solutions managed through regional DIFC hub",
        "corporate_focus": "optimizing commercial property allocations and delivering resilient income streams for institutional clients",
        "jagannath_hook": "managing AED 800M in commercial and mixed-use assets with disciplined leasing governance",
        "value_prop": "steady-yield tenant management, commercial lease enforcement, and portfolio risk mitigation",
        "linkedin_angle": "Invesco's real estate asset management platform and regional property investments"
    },
    "Fidelity": {
        "sector": "Asset Management",
        "signature_assets": "Institutional real estate securities and direct GCC corporate operations",
        "corporate_focus": "driving investment excellence in commercial real estate and sustainable infrastructure across MENA",
        "jagannath_hook": "20-year UAE track record in asset enhancement, lease negotiations, and RERA compliance",
        "value_prop": "commercial property lifecycle governance, tenant underwriting, and portfolio performance analysis",
        "linkedin_angle": "Fidelity's institutional real estate and property investment initiatives in the GCC"
    },
    "Vanguard": {
        "sector": "Asset Management",
        "signature_assets": "Global real estate index and active portfolios serving GCC institutional sovereign investors",
        "corporate_focus": "providing institutional-grade asset allocation and low-cost, resilient real estate investment vehicles",
        "jagannath_hook": "deep operational mastery of UAE commercial leasing, managing an AED 800M portfolio under rigorous audit governance",
        "value_prop": "cost governance, institutional compliance, and long-term commercial lease stability",
        "linkedin_angle": "Vanguard's institutional investment strategy and real estate asset advisory in the region"
    },

    # ----------------- GLOBAL TECH & MULTINATIONAL CORPORATE REAL ESTATE (CRE) -----------------
    "Amazon": {
        "sector": "Global Tech / Corporate Real Estate",
        "signature_assets": "MENA Regional HQ in Dubai Internet City, extensive fulfillment centers, and corporate office portfolio",
        "corporate_focus": "optimizing corporate real estate operations, multi-site lease acquisitions, and workplace infrastructure across MENA",
        "jagannath_hook": "20 years of UAE commercial leasing, negotiating 2,500+ commercial and corporate occupier lease contracts",
        "value_prop": "corporate occupier leasehold negotiations, landlord relationship governance, CAPEX oversight, and RERA compliance",
        "linkedin_angle": "Amazon's MENA corporate real estate operations and facilities expansion"
    },
    "Google": {
        "sector": "Global Tech / Corporate Real Estate",
        "signature_assets": "MENA Headquarters at Dubai Internet City and regional innovation workplaces",
        "corporate_focus": "designing sustainable, innovative, and employee-centric corporate real estate environments across MENA",
        "jagannath_hook": "managing prime commercial spaces across One Za'abeel and Dubai's premier business corridors",
        "value_prop": "landlord lease negotiations, prime workspace strategy, commercial terms governance, and facilities coordination",
        "linkedin_angle": "Google's MENA workplace and corporate real estate strategy in Dubai"
    },
    "Microsoft": {
        "sector": "Global Tech / Corporate Real Estate",
        "signature_assets": "MENA Regional Headquarters at Dubai Internet City and regional commercial hubs",
        "corporate_focus": "expanding sustainable corporate workplaces and cloud infrastructure across the UAE and Gulf",
        "jagannath_hook": "directing commercial leasing and corporate asset strategy across AED 800M in prime Dubai developments",
        "value_prop": "corporate lease administration, green building governance, commercial terms optimization, and landlord partnership",
        "linkedin_angle": "Microsoft's regional corporate real estate and sustainable workplace strategy in Dubai"
    },
    "Visa": {
        "sector": "Fintech / Corporate Real Estate",
        "signature_assets": "CEMEA Headquarters at Dubai Media/Internet City and regional innovation centers",
        "corporate_focus": "managing corporate facilities, long-term commercial office leaseholds, and workplace agility across CEMEA",
        "jagannath_hook": "overseeing commercial portfolio leasing, RERA legal frameworks, and tenant-landlord agreements across 2,500+ deals",
        "value_prop": "commercial lease governance, lease renewal optimization, corporate facilities compliance, and tenant advocacy",
        "linkedin_angle": "Visa's CEMEA corporate real estate portfolio and workplace operations in Dubai"
    },
    "Mastercard": {
        "sector": "Fintech / Corporate Real Estate",
        "signature_assets": "EEMEA Regional Headquarters at Dubai Internet City and tech hub facilities",
        "corporate_focus": "delivering premier corporate office infrastructure and flexible workspace portfolios across EEMEA",
        "jagannath_hook": "20+ years in UAE commercial real estate, managing AED 800M assets and institutional developer relationships",
        "value_prop": "corporate leasehold negotiations, tenant rights governance, operational cost control, and facilities alignment",
        "linkedin_angle": "Mastercard's regional corporate real estate footprint and Dubai headquarters strategy"
    },
    "Etihad Airways": {
        "sector": "Aviation & Corporate Property",
        "signature_assets": "Zayed International Airport hub, global ticketing/lounge facilities, and extensive residential staff compounds",
        "corporate_focus": "optimizing commercial property portfolios, retail airport concessions, and corporate facilities across the UAE",
        "jagannath_hook": "negotiating 2,500+ commercial and retail leases, evaluating 300+ locations, and managing an AED 800M portfolio",
        "value_prop": "commercial concession lease restructuring, corporate property management, and operational expenditure control",
        "linkedin_angle": "Etihad Airways's commercial property portfolio, airport concessions, and facilities strategy"
    },

    # ----------------- LUXURY & RETAIL CONGLOMERATES -----------------
    "Chalhoub Group": {
        "sector": "Luxury Retail Conglomerate",
        "signature_assets": "700+ luxury retail boutiques, beauty concept stores, and flagship concessions in Dubai Mall, MOE, and across GCC",
        "corporate_focus": "driving luxury brand expansion and securing prime mall and high-street real estate for global iconic fashion houses",
        "jagannath_hook": "20+ years of UAE retail leasing leadership, negotiating 2,500+ leases with premier landlords (Emaar, Nakheel, MAF, ICD)",
        "value_prop": "prime retail store acquisition, turnover rent vs. base rent optimization, landlord concession negotiations, and mall relationships",
        "linkedin_angle": "Chalhoub Group's luxury retail store portfolio and prime mall flagship real estate strategy"
    },
    "GMG": {
        "sector": "Retail Conglomerate",
        "signature_assets": "Sun & Sand Sports, Supercare Pharmacy, Nike concept stores, and 500+ retail stores across GCC shopping malls",
        "corporate_focus": "expanding sports, health, and consumer retail store networks across premier regional malls and urban centers",
        "jagannath_hook": "evaluating 300+ locations through footfall and feasibility modeling; directing leasing for 800,000 sq. ft. of flagship space",
        "value_prop": "retail store expansion strategy, commercial leasehold negotiations, rental indexation management, and landlord partnerships",
        "linkedin_angle": "GMG's retail store network expansion across major UAE shopping malls and commercial districts"
    },
    "Landmark Group": {
        "sector": "Retail Conglomerate",
        "signature_assets": "Centrepoint, Max, Babyshop, Home Centre, and Landmark Tower in Dubai Marina",
        "corporate_focus": "operating mega-scale anchor retail footprints and optimizing commercial leaseholds across the Middle East",
        "jagannath_hook": "managing an AED 800M portfolio, negotiating 2,500+ commercial transactions, and master-plan retail asset stewardship",
        "value_prop": "anchor tenant lease structuring, occupancy cost containment, demographic catchment analysis, and mall lease renewals",
        "linkedin_angle": "Landmark Group's retail real estate network and major anchor store leasing strategy"
    },
    "Al-Futtaim Group": {
        "sector": "Diversified Retail & Real Estate",
        "signature_assets": "Dubai Festival City Mall, Cairo Festival City, automotive showrooms, and IKEA mega-stores across GCC",
        "corporate_focus": "managing mixed-use retail destinations and expanding premier retail brand store footprints across MENA",
        "jagannath_hook": "directing commercial leasing and asset strategy across One Za'abeel and Deira Enrichment within an AED 800M scope",
        "value_prop": "large-format retail leasing, mixed-use asset management, tenant mix optimization, and commercial lease governance",
        "linkedin_angle": "Al-Futtaim Group's mixed-use developments like Dubai Festival City and retail asset portfolio"
    },

    # ----------------- REAL ESTATE CONSULTANCIES & BROKERAGES -----------------
    "Cushman & Wakefield Core": {
        "sector": "Commercial Real Estate Advisory",
        "signature_assets": "Leading commercial transaction advisory, landlord & tenant representation, and capital markets across Dubai & UAE",
        "corporate_focus": "providing institutional landlords and corporate occupiers with premier commercial leasing and asset advisory services",
        "jagannath_hook": "20 years of hands-on landlord leasing leadership in Dubai, managing an AED 800M portfolio and 2,500+ completed transactions",
        "value_prop": "landlord representation, institutional commercial agency leasing, deep UAE occupier network, and lease transaction closing",
        "linkedin_angle": "Cushman & Wakefield Core's institutional commercial agency and landlord advisory excellence"
    },
    "Savills Middle East": {
        "sector": "Commercial Real Estate Advisory",
        "signature_assets": "Prime commercial office leasing, strategic landlord representation, and property management across GCC",
        "corporate_focus": "delivering institutional real estate advisory and agency leasing for Grade A commercial and mixed-use developments",
        "jagannath_hook": "overseeing leasing across 800,000 sq. ft. of flagship ICD-backed commercial space (including One Za'abeel)",
        "value_prop": "Grade A commercial agency leasing, occupier relationship management, institutional valuation, and deal execution",
        "linkedin_angle": "Savills Middle East's prime commercial leasing and strategic asset management services"
    },
    "Knight Frank Middle East": {
        "sector": "Commercial Real Estate Advisory",
        "signature_assets": "Prime commercial agency, institutional investment advisory, and luxury asset management across UAE & Saudi Arabia",
        "corporate_focus": "advising sovereign wealth funds, institutional investors, and premier landlords on flagship commercial real estate",
        "jagannath_hook": "AED 800M portfolio scope, 2,500+ commercial leases negotiated, and leadership across One Za'abeel and Deira Enrichment",
        "value_prop": "institutional landlord advisory, high-value commercial leasing transactions, and occupier placement strategy",
        "linkedin_angle": "Knight Frank's prime commercial real estate and institutional asset advisory in Dubai"
    },

    # ----------------- EXECUTIVE RECRUITMENT & TALENT FIRMS -----------------
    "Michael Page Middle East": {
        "sector": "Executive Search & Recruitment",
        "signature_assets": "Premier real estate and property executive search practice in UAE and Saudi Arabia",
        "corporate_focus": "connecting GCC master developers, sovereign wealth funds, and global funds with top-tier real estate leaders",
        "jagannath_hook": "ready-to-deploy Senior Asset Manager & Leasing Director with 15+ years in Dubai, verified AED 800M portfolio, and One Za'abeel track record",
        "value_prop": "proven bilingual-aligned leader with 2,500+ executed leases, RERA governance mastery, and immediate UAE availability",
        "linkedin_angle": "your executive real estate recruitment practice and leadership mandates in the UAE"
    },
    "Charterhouse Middle East": {
        "sector": "Executive Search & Recruitment",
        "signature_assets": "Leading specialist recruitment consultancy placing senior property and asset management executives across the GCC",
        "corporate_focus": "placing high-impact C-suite, Directors, and Senior Managers across prime developers and institutional landlords",
        "jagannath_hook": "demonstrated leadership directing 800,000 sq. ft. of commercial space across One Za'abeel and Deira Enrichment for Ithra Dubai",
        "value_prop": "verified executive profile: AED 800M portfolio, 2,500+ leases, 300+ location feasibilities, and impeccable institutional references",
        "linkedin_angle": "Charterhouse's property & asset management executive search mandates in Dubai"
    },
    "Hays Middle East": {
        "sector": "Executive Search & Recruitment",
        "signature_assets": "Global recruitment powerhouse specializing in construction, property, and asset management in UAE & GCC",
        "corporate_focus": "supplying premier regional developers and property firms with seasoned real estate and leasing directors",
        "jagannath_hook": "20 years of continuous UAE real estate leadership with verified AED 800M portfolio stewardship and ICD entity experience",
        "value_prop": "proven asset performance leader, immediate Dubai residency/availability, and flawless commercial leasing execution",
        "linkedin_angle": "Hays Middle East's property and real estate leadership recruitment across the UAE"
    },
    "Cooper Fitch": {
        "sector": "Executive Search & Recruitment",
        "signature_assets": "Premier recruitment and HR advisory consultancy placing senior executives across UAE, Saudi Arabia, and GCC",
        "corporate_focus": "advising sovereign wealth funds and master developers on strategic real estate leadership appointments",
        "jagannath_hook": "15+ years managing AED 800M+ assets, negotiating 2,500+ leases, and directing leasing at One Za'abeel (Ithra Dubai / ICD)",
        "value_prop": "institutional-grade executive ready for Director of Asset Management or Head of Commercial Leasing mandates",
        "linkedin_angle": "Cooper Fitch's executive search assignments in UAE real estate and asset management"
    },

    # ----------------- STRATEGY & BIG 4 CONSULTANCIES -----------------
    "McKinsey & Company": {
        "sector": "Strategy Consulting",
        "signature_assets": "Real Estate & Infrastructure Practice advising GCC sovereign developers and ministries",
        "corporate_focus": "guiding mega-project commercialization, real estate portfolio turnaround, and sovereign asset optimization",
        "jagannath_hook": "grounded operational mastery: 800,000 sq. ft. of commercial leasing, AED 800M portfolio management, and 300+ feasibility models",
        "value_prop": "operational reality testing for real estate strategies, tenant demand analysis, and commercial asset turnaround",
        "linkedin_angle": "McKinsey's Real Estate Practice and GCC mega-project advisory mandates"
    },
    "Deloitte": {
        "sector": "Big 4 Advisory",
        "signature_assets": "Middle East Real Estate & Infrastructure Advisory practice based in Dubai & Riyadh",
        "corporate_focus": "delivering commercial asset feasibility, portfolio valuation, and developer strategy across the GCC",
        "jagannath_hook": "20 years of UAE commercial leasing, RERA governance, and directing One Za'abeel asset strategy",
        "value_prop": "real estate market reality, lease feasibility verification, tenant covenant analysis, and asset optimization",
        "linkedin_angle": "Deloitte Middle East's Real Estate & Construction advisory practice"
    },
    "PwC": {
        "sector": "Big 4 Advisory",
        "signature_assets": "Real Estate Advisory and Capital Projects & Infrastructure practice in UAE & Middle East",
        "corporate_focus": "advising governments, master developers, and family offices on real estate monetization and asset efficiency",
        "jagannath_hook": "managing an AED 800M commercial/mixed-use portfolio with 2,500+ commercial transactions completed",
        "value_prop": "commercial leasing execution, asset yield optimization, and public-private developer governance",
        "linkedin_angle": "PwC Middle East's Real Estate and Capital Projects practice in Dubai"
    },
    "KPMG": {
        "sector": "Big 4 Advisory",
        "signature_assets": "Real Estate, Construction, and Infrastructure advisory practice across UAE and Lower Gulf",
        "corporate_focus": "providing market feasibility, lease audit, and asset management optimization for UAE landlords",
        "jagannath_hook": "overseeing leasing for 800,000 sq. ft. of prime space with 300+ location feasibilities evaluated",
        "value_prop": "lease governance, audit compliance, commercial yield protection, and operational asset management",
        "linkedin_angle": "KPMG Lower Gulf's Real Estate & Infrastructure advisory team"
    },
    "EY": {
        "sector": "Big 4 Advisory",
        "signature_assets": "Real Estate, Hospitality & Construction (RHC) Strategy & Transactions practice in MENA",
        "corporate_focus": "guiding institutional M&A, asset portfolio carve-outs, and commercial repositioning across the GCC",
        "jagannath_hook": "AED 800M portfolio stewardship, 2,500+ leases negotiated, and leadership at Ithra Dubai (One Za'abeel)",
        "value_prop": "practical asset underwriting, tenant covenant risk mitigation, and commercial lease turnaround",
        "linkedin_angle": "EY MENA's Real Estate and Transaction Advisory practice in Dubai"
    }
}


def get_company_profile(company_name: str) -> Dict[str, str]:
    """Retrieves or synthesizes a bespoke corporate intelligence profile for any company."""
    if company_name in COMPANY_PROFILES:
        return COMPANY_PROFILES[company_name]
    
    # Fuzzy match check
    for key, val in COMPANY_PROFILES.items():
        if key.lower() in company_name.lower() or company_name.lower() in key.lower():
            return val
            
    # Fallback contextual profile for commercial real estate in UAE
    return {
        "sector": "Commercial Real Estate & Investment",
        "signature_assets": f"premier commercial, residential, and mixed-use developments across Dubai and the UAE",
        "corporate_focus": f"optimizing commercial property operations, tenant retention, and portfolio yield",
        "jagannath_hook": "managing an AED 800M commercial and mixed-use portfolio, executing 2,500+ leases, and directing leasing at One Za'abeel for Ithra Dubai",
        "value_prop": "commercial leasing governance, high-value tenant acquisition, and portfolio revenue optimization",
        "linkedin_angle": f"{company_name}'s commercial real estate footprint in the UAE"
    }


def generate_tailored_email(contact: Dict[str, Any], job: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Generates a bespoke email pitch precisely grounded in the company's verified profile
    and Jagannath's tailored value proposition.
    """
    company = contact.get("company_name", "").strip() or (job.get("company_name", "") if job else "your organization")
    prof = get_company_profile(company)
    contact_name = contact.get("full_name", "").strip()
    first_name = contact_name.split()[0] if contact_name else "Leader"
    job_title = (job.get("title") if job else None) or "Senior Asset Manager / Commercial Portfolio Director"
    role_category = contact.get("role_category", "department_leader")

    # Tailored Subject Lines based on Company & Role
    if role_category == "recruiter":
        subject = f"V. Jagannath - Application for {job_title} | {company} ({prof['sector']})"
    else:
        subject = f"V. Jagannath - Senior Asset Management & Leasing Leadership | {company} Alignment"

    # Contextual Opening Paragraph tailored to Company
    if role_category == "recruiter":
        intro = (
            f"Dear {first_name},\n\n"
            f"I noticed {company}'s strategic talent search for a {job_title} in Dubai and wanted to formally introduce my executive profile.\n\n"
            f"With {company} focused on {prof['corporate_focus']}, my 15+ years of UAE commercial leasing and asset management experience offer direct, immediate alignment."
        )
    else:
        intro = (
            f"Dear {first_name},\n\n"
            f"I hope this note finds you well.\n\n"
            f"I follow {company}'s growth across {prof['signature_assets']} with great respect. As {company} continues {prof['corporate_focus']}, I am writing to introduce my leadership background for senior asset management and commercial portfolio opportunities."
        )

    # Core Accomplishments tailored to Company type
    core_body = (
        f"Over the past 15+ years in Dubai, I have managed commercial, retail, and mixed-use portfolios exceeding AED 800M in asset value and successfully executed over 2,500 lease transactions.\n\n"
        f"Most notably, {prof['jagannath_hook']}. In this capacity, I directed tenant curation, base and turnover rent structuring, RERA regulatory compliance, and cross-functional operations across Grade A office and luxury retail destinations.\n\n"
        f"Given {company}'s market standing, I bring immediate expertise in {prof['value_prop']} to protect and enhance net operating income (NOI)."
    )

    # Professional Call to Action
    closing = (
        f"My executive ATS resume and verified deal dossier are prepared for your review. I would welcome the opportunity for a brief introductory conversation to explore how my track record can support {company}'s strategic milestones.\n\n"
        f"Best regards,\n\n"
        f"Vanganur Jagannath\n"
        f"Senior Manager – Real Estate Asset Management & Commercial Leasing\n"
        f"Dubai, United Arab Emirates\n"
        f"Phone: +971 50 5099065\n"
        f"Email: v.jagannath3@gmail.com\n"
        f"LinkedIn: https://www.linkedin.com/in/v-jagannath-re"
    )

    full_body = f"{intro}\n\n{core_body}\n\n{closing}"
    return {
        "subject": subject,
        "body": full_body
    }


def generate_tailored_linkedin(contact: Dict[str, Any], job: Optional[Dict[str, Any]] = None) -> str:
    """
    Generates a concise, high-impact LinkedIn outreach note tailored specifically
    to the target company and recipient.
    """
    company = contact.get("company_name", "").strip() or (job.get("company_name", "") if job else "your organization")
    prof = get_company_profile(company)
    contact_name = contact.get("full_name", "").strip()
    first_name = contact_name.split()[0] if contact_name else "Colleague"

    # Crisp, punchy LinkedIn connection / InMail note
    return (
        f"Hi {first_name}, I follow {company}'s developments across {prof['linkedin_angle']} with great admiration.\n\n"
        f"With 15+ years directing UAE real estate asset management (AED 800M portfolio, 2,500+ leases, and leasing lead on One Za'abeel under Ithra Dubai / ICD), "
        f"I specialize in {prof['value_prop']}.\n\n"
        f"I would welcome connecting to explore synergies with {company}'s commercial milestones in Dubai.\n\n"
        f"Best regards,\n"
        f"V. Jagannath (+971 50 5099065)"
    )
