import logging
import uuid
import json
from typing import Dict, Any, Optional
from backend.db.database import get_db
from backend.agents.career_brain import career_brain_agent
from backend.agents.company_intelligence import company_intelligence_agent

logger = logging.getLogger("ai7.agent.interview_intel")

class InterviewIntelligenceAgent:
    """
    Interview Intelligence Agent (Agent L):
    Prepares candidate dossiers for interviews with company context,
    STAR stories mapped directly to verified candidate metrics,
    domain questions, and post-interview thank-you drafts.
    """
    def __init__(self):
        pass

    def prepare_interview_dossier(self, job_id: str, stage: str = "HIRING_MANAGER") -> Dict[str, Any]:
        """Creates an executive interview preparation briefing."""
        with get_db() as conn:
            job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not job:
                return {"error": "Job not found"}

        company_name = job["company_name"]
        role_title = job["title"]
        profile = career_brain_agent.get_candidate_profile()
        dossier_data = company_intelligence_agent.get_company_dossier(company_name)

        star_stories = [
            {
                "title": "Restructuring & Leasing One Za'abeel & ICD Flagship Portfolio",
                "situation": "Investment Corporation of Dubai (ICD) / Ithra Dubai portfolio comprising 800,000 sq.ft. of luxury retail and B2B commercial space requiring high-occupancy positioning.",
                "task": "Develop tenant strategy, structure institutional leases, and manage AED 800M portfolio performance while maintaining RERA governance standards.",
                "action": "Conducted catchment and demographic footfall analysis, led direct negotiations with regional developers and corporate brands, and balanced commercial concessions with long-term NOI.",
                "result": "Negotiated 2,500+ commercial leases across the portfolio, optimized rental yield, and positioned One Za'abeel as a premier Dubai commercial landmark.",
                "provenance": "Ithra Dubai / ICD (2020-2025) verified records"
            },
            {
                "title": "UAE Store Network Expansion Feasibility (Grandiose / Ghassan Aboud)",
                "situation": "Aggressive retail footprint expansion requiring rigorous site selection and CAPEX control across multiple UAE emirates.",
                "task": "Evaluate hundreds of candidate properties to select commercially viable locations.",
                "action": "Evaluated 300+ locations using catchment footfall analytics, demographic density modeling, and landlord negotiations across 35+ executed leases.",
                "result": "Delivered profitable store roll-outs under budget with high tenant retention.",
                "provenance": "Ghassan Aboud Group (2017-2019) verified records"
            }
        ]

        technical_questions = [
            "How do you approach tenant-mix optimization for prime mixed-use developments versus commercial office towers in Dubai?",
            "Can you walk us through your methodology for CAPEX prioritization and NOI modeling in an inflationary rate environment?",
            "How do you handle complex disputes or lease restructuring under Dubai RERA tenancy law?",
            "What strategies have you used to negotiate commercial terms with institutional landlords like ICD or Emaar?"
        ]

        questions_for_candidate_to_ask = [
            f"What are {company_name}'s capital deployment targets for commercial real estate in the GCC over the next 24-36 months?",
            "How is the asset management department structured between direct property operations and portfolio investment strategy?",
            "What is the single biggest operational or leasing challenge facing this specific portfolio right now?"
        ]

        interview_prep = {
            "company_brief": {
                "name": company_name,
                "industry": dossier_data.get("industry", "Asset Management"),
                "uae_presence": dossier_data.get("dubai_uae_footprint", "DIFC Dubai"),
                "strategic_initiatives": dossier_data.get("strategic_initiatives", [])
            },
            "role_brief": {
                "title": role_title,
                "seniority": dict(job).get("seniority", "Senior Manager"),
                "key_mandate": "Drive commercial leasing, tenant relationships, CAPEX budgeting, and portfolio performance."
            },
            "star_stories": star_stories,
            "technical_domain_questions": technical_questions,
            "questions_to_ask_interviewers": questions_for_candidate_to_ask,
            "checklist": [
                "Review One Za'abeel leasing metrics (800,000 sq.ft., AED 800M portfolio)",
                "Prepare specific examples of CAPEX allocation and yield enhancement",
                "Ensure familiarity with Dubai commercial RERA compliance frameworks",
                "Have the tailored PDF resume ready for screen sharing"
            ]
        }

        int_id = f"int_{str(uuid.uuid4())[:8]}"

        with get_db() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO interviews (id, job_id, company_name, role_title, interview_stage, prep_dossier, status)
                VALUES (?, ?, ?, ?, ?, ?, 'UPCOMING')
            """, (int_id, job_id, company_name, role_title, stage, json.dumps(interview_prep)))

            # Update job status to INTERVIEW
            conn.execute("UPDATE jobs SET status = 'INTERVIEW' WHERE id = ?", (job_id,))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'interview_intel_agent', 'prepared_interview_dossier', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), int_id, f"Created interview preparation dossier for {company_name}", f"Role: {role_title}", ))

        return {
            "interview_id": int_id,
            "company_name": company_name,
            "role_title": role_title,
            "dossier": interview_prep
        }

    def record_debrief_and_generate_thank_you(self, interview_id: str, candidate_notes: str) -> Dict[str, Any]:
        """Processes candidate feedback and generates an immediate personalized thank-you note."""
        with get_db() as conn:
            int_row = conn.execute("SELECT * FROM interviews WHERE id = ?", (interview_id,)).fetchone()
            if not int_row:
                return {"error": "Interview record not found"}

        company = int_row["company_name"]
        role = int_row["role_title"]

        thank_you = (
            f"Dear Interview Committee,\n\n"
            f"Thank you for the productive conversation today regarding the {role} role at {company}.\n\n"
            f"I greatly enjoyed discussing your commercial property strategy in Dubai and was particularly energized by your vision for portfolio expansion. "
            f"Our discussion reaffirmed that my 20 years of UAE commercial leasing, portfolio governance, and hands-on management of the AED 800M Ithra Dubai / ICD portfolio align directly with your objectives.\n\n"
            f"Please let me know if you need any additional documentation. I look forward to the next steps.\n\n"
            f"Best regards,\n"
            f"V. Jagannath"
        )

        with get_db() as conn:
            conn.execute("""
                UPDATE interviews
                SET candidate_notes = ?, thank_you_draft = ?, status = 'COMPLETED'
                WHERE id = ?
            """, (candidate_notes, thank_you, interview_id))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'interview_intel_agent', 'recorded_debrief', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), interview_id, f"Recorded debrief for {company} interview", candidate_notes[:100], ))

        return {
            "interview_id": interview_id,
            "thank_you_draft": thank_you,
            "status": "COMPLETED"
        }

interview_intel_agent = InterviewIntelligenceAgent()
