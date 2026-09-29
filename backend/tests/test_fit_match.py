import unittest
from backend.db.database import init_db
from backend.db.seed import seed_database
from backend.agents.fit_match import job_fit_agent
from backend.agents.job_discovery import job_discovery_agent

class TestJobFitMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed_database()

    def test_evidence_based_matching(self):
        jobs = job_discovery_agent.get_all_jobs()
        self.assertGreater(len(jobs), 0)

        # Test Blackstone Senior Asset Manager job
        blackstone_job = next((j for j in jobs if "Blackstone" in j["company_name"]), jobs[0])
        report = job_fit_agent.evaluate_job(blackstone_job["id"])

        self.assertIn(report["overall_fit_label"], ["STRONG_FIT", "MODERATE_FIT"])
        self.assertGreater(len(report["match_areas"]), 0)

        # Verify evidence citations exist for matches
        all_evidence_combined = ""
        for m in report["match_areas"]:
            self.assertIn("requirement", m)
            self.assertIn("candidate_evidence", m)
            self.assertGreater(len(m["candidate_evidence"]), 10)
            self.assertIn(m["status"], ["Strong Evidence", "Partial Evidence", "Weak Evidence"])
            all_evidence_combined += " " + m["candidate_evidence"]

        # Ensure evidence references real metrics
        self.assertTrue(any(metric in all_evidence_combined for metric in ["800M", "2,500", "Ithra Dubai", "20+", "300+"]))

    def test_gap_analysis(self):
        jobs = job_discovery_agent.get_all_jobs()
        for j in jobs:
            report = job_fit_agent.evaluate_job(j["id"])
            self.assertIsInstance(report["gaps"], list)
            for g in report["gaps"]:
                self.assertIn("unmet_requirement", g)
                self.assertIn("recommendation", g)

if __name__ == "__main__":
    unittest.main()
