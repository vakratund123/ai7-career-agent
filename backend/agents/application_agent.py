import logging
import uuid
import json
from typing import Dict, Any, Optional
from backend.db.database import get_db
from backend.agents.career_brain import career_brain_agent
from backend.agents.resume_tailor import resume_tailor_agent

logger = logging.getLogger("ai7.agent.application")

class ApplicationAgent:
    """
    Application Agent (Agent G):
    Prepares end-to-end application packages: tailored cover letters, corporate Q&A answers,
    and document attachments.
    Crucial Safety Rule: Never guess. Flags sensitive or missing data for Human Escalation.
    """
    def __init__(self):
        pass

    def prepare_application_packet(self, job_id: str) -> Dict[str, Any]:
        """Prepares a full application dossier for a qualified job."""
        with get_db() as conn:
            job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not job:
                return {"error": f"Job {job_id} not found."}

        profile = career_brain_agent.get_candidate_profile()
        target_company = job["company_name"]
        target_role = job["title"]

        # 1. Generate or retrieve tailored resume
        tailored_resume = resume_tailor_agent.generate_tailored_resume(job_id)

        # 2. Prepare tailored executive cover letter
        cover_letter = self._draft_cover_letter(profile, target_company, target_role)

        # 3. Prepare corporate questionnaire answers
        qa_answers, exceptions_flagged = self._prepare_qa_answers(profile, target_company)

        app_id = f"app_{str(uuid.uuid4())[:8]}"

        status = "PENDING_APPROVAL" if exceptions_flagged else "READY"

        with get_db() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO applications (id, job_id, company_name, role_title, tailored_resume_id, cover_letter, qa_answers, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (app_id, job_id, target_company, target_role, tailored_resume["document_id"], cover_letter, json.dumps(qa_answers), status))

            # Update job status to APPLICATION_READY
            conn.execute("UPDATE jobs SET status = 'APPLICATION_READY' WHERE id = ?", (job_id,))

            # If exceptions flagged, queue in approvals
            if exceptions_flagged:
                for exc in exceptions_flagged:
                    conn.execute("""
                        INSERT INTO approvals (id, action_type, title, description, payload, status)
                        VALUES (?, 'SUBMIT_APPLICATION', ?, ?, ?, 'PENDING')
                    """, (str(uuid.uuid4()), f"Confirm details for {target_company} application", exc["question"], json.dumps(exc)))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'application_agent', 'prepare_packet', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), app_id, f"Prepared application packet for {target_company}", f"Exceptions flagged: {len(exceptions_flagged)}", ))

        return {
            "application_id": app_id,
            "job_id": job_id,
            "company_name": target_company,
            "role_title": target_role,
            "status": status,
            "resume_version": tailored_resume["version"],
            "pdf_path": tailored_resume["pdf_path"],
            "cover_letter": cover_letter,
            "qa_answers": qa_answers,
            "exceptions_flagged": exceptions_flagged
        }

    def _draft_cover_letter(self, profile: dict, company: str, role: str) -> str:
        letter = f"""V. Jagannath
Dubai, UAE | +971 50 5099065 | v.jagannath3@gmail.com

Hiring Committee & Leadership Team
{company}
Dubai, United Arab Emirates

Subject: Application for {role}

Dear Hiring Team,

I am writing to express my strong interest in the {role} position at {company}. With over 20 years of dedicated real estate asset management, commercial leasing, and portfolio development experience in the UAE, I have developed a rigorous, commercially disciplined approach to maximizing asset yield, driving high-occupancy commercial leasing, and executing complex stakeholder transactions.

During my tenure as Leasing Lead at Ithra Dubai (Investment Corporation of Dubai), I had the privilege of directing retail and commercial asset management across flagship mixed-use developments including One Za'abeel, Deira Enrichment Project, The Plaza – Deira, and Waterfront Market. In this capacity, I oversaw commercial and luxury retail leasing across approximately 800,000 sq. ft., managing an AED 800M portfolio while structuring lease agreements with major regional and global corporate occupiers.

Throughout my career, I have negotiated over 2,500 commercial leases, conducted demographic and footfall feasibility evaluations for 300+ locations, and cultivated an executive network of over 6,000 regional decision-makers. My background combines deep familiarity with Dubai RERA regulatory frameworks, robust financial modeling and CAPEX allocation, and proven capability in aligning operational reality with long-term asset value.

Given {company}'s strategic footprint and expansion in the UAE and wider GCC, I would welcome the opportunity to discuss how my commercial leadership, institutional leasing background, and regional network can contribute to your portfolio objectives.

Sincerely,

V. Jagannath
Senior Manager – Asset Management & Portfolio Development"""
        return letter

    def _prepare_qa_answers(self, profile: dict, company: str):
        answers = {
            "Full Legal Name": "V. Jagannath",
            "Current Location": "Dubai, United Arab Emirates",
            "Email": "v.jagannath3@gmail.com",
            "Phone": "+971 50 5099065",
            "Total Years of Real Estate Experience": "20+ Years in UAE and India",
            "Current / Most Recent Employer": "Ithra Dubai LLC / Investment Corporation of Dubai (ICD)",
            "Notice Period": "Immediate / 30 Days",
            "Work Authorization (UAE)": "UAE Resident / Golden Visa Eligible",
            "Key Real Estate Metric": "AED 800M Real Estate Portfolio; 2,500+ commercial leases negotiated",
            "Regulatory / Licensing": "RERA Certified (2011–2016), Certified Retail Management Expert (2026)"
        }
        exceptions = []

        # Example sensitive check: Salary expectation
        exceptions.append({
            "question": f"Confirm targeted compensation package for {company}",
            "context": "System default is configured at AED 45,000 - 65,000 monthly base plus executive benefits. Human confirmation required.",
            "field": "salary_expectation"
        })

        return answers, exceptions

application_agent = ApplicationAgent()
