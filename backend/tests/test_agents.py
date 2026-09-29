import os
import unittest
from pathlib import Path
from backend.db.database import init_db
from backend.db.seed import seed_database
from backend.agents.orchestrator import orchestrator
from backend.agents.resume_tailor import resume_tailor_agent
from backend.agents.application_agent import application_agent
from backend.agents.interview_intel import interview_intel_agent
from backend.agents.human_escalation import human_escalation_agent
from backend.agents.crm_pipeline import crm_pipeline_agent
from backend.agents.job_discovery import job_discovery_agent

class TestMultiAgentSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_database()
        if not job_discovery_agent.get_all_jobs():
            job_discovery_agent.ingest_job(
                title="Senior Asset Manager – Real Estate",
                company_name="Brookfield Asset Management",
                location="Dubai, UAE",
                source_url="https://www.brookfield.com/careers",
                description="Brookfield Real Estate is seeking an experienced Senior Asset Manager in Dubai to oversee commercial leasing, portfolio NOI optimization, and CAPEX planning. Requires 15+ years experience, large portfolio management (AED 500M+), commercial lease negotiation, and UAE RERA compliance.",
                seniority="Senior Manager / Director-track"
            )

    def test_pdf_resume_generation(self):
        jobs = job_discovery_agent.get_all_jobs()
        job = jobs[0]
        res = resume_tailor_agent.generate_tailored_resume(job["id"])
        self.assertIn("pdf_path", res)
        self.assertTrue(os.path.exists(res["pdf_path"]))
        self.assertTrue(res["pdf_path"].endswith(".pdf"))
        self.assertGreater(os.path.getsize(res["pdf_path"]), 1000)

    def test_application_preparation_and_exception_handling(self):
        jobs = job_discovery_agent.get_all_jobs()
        job = jobs[0]
        packet = application_agent.prepare_application_packet(job["id"])
        self.assertIn("cover_letter", packet)
        self.assertIn("V. Jagannath", packet["cover_letter"])
        self.assertIn("One Za'abeel", packet["cover_letter"])
        self.assertIn("qa_answers", packet)
        self.assertIsInstance(packet["exceptions_flagged"], list)

    def test_interview_intel_dossier(self):
        jobs = job_discovery_agent.get_all_jobs()
        job = jobs[0]
        dossier = interview_intel_agent.prepare_interview_dossier(job["id"])
        self.assertIn("dossier", dossier)
        prep = dossier["dossier"]
        self.assertIn("star_stories", prep)
        self.assertGreater(len(prep["star_stories"]), 0)
        self.assertIn("technical_domain_questions", prep)

    def test_full_pipeline_orchestration(self):
        result = orchestrator.run_full_pipeline_cycle()
        self.assertEqual(result["status"], "COMPLETED")
        self.assertGreater(result["jobs_evaluated"], 0)

        # Check CRM overview
        overview = crm_pipeline_agent.get_pipeline_overview()
        self.assertIn("stages", overview)
        self.assertGreater(sum(overview["counts"].values()), 0)

    def test_daily_executive_briefing(self):
        briefing = human_escalation_agent.generate_daily_executive_briefing()
        self.assertIn("briefing_text", briefing)
        self.assertIn("Jagannath", briefing["candidate_name"])
        self.assertIn("action_required", briefing)
        self.assertIn("metrics", briefing)

if __name__ == "__main__":
    unittest.main()
