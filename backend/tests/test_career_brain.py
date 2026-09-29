import unittest
from backend.db.database import init_db
from backend.services.cv_parser import parse_and_seed_candidate_facts
from backend.agents.career_brain import career_brain_agent

class TestCareerBrain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        parse_and_seed_candidate_facts()

    def test_candidate_profile_loaded(self):
        profile = career_brain_agent.get_candidate_profile()
        self.assertEqual(profile["full_name"], "V. Jagannath")
        self.assertEqual(profile["location"], "Dubai, UAE")
        self.assertIn("v.jagannath3@gmail.com", profile["email"])

    def test_core_metrics_provenance(self):
        profile = career_brain_agent.get_candidate_profile()
        achievements = profile["achievements"]
        metric_names = [a["metric_name"] for a in achievements]

        self.assertIn("Portfolio Scale", metric_names)
        self.assertIn("Lease Transactions", metric_names)
        self.assertIn("Flagship Leasing Scope", metric_names)

        # Verify exact documented values
        port_scale = next(a for a in achievements if a["metric_name"] == "Portfolio Scale")
        self.assertEqual(port_scale["metric_value"], "AED 800M")

        lease_txn = next(a for a in achievements if a["metric_name"] == "Lease Transactions")
        self.assertEqual(lease_txn["metric_value"], "2,500+ Leases")

    def test_anti_hallucination_verification(self):
        # 1. Valid verified claim
        valid_claim = "AED 800M real estate portfolio management"
        res_valid = career_brain_agent.verify_claim(valid_claim)
        self.assertTrue(res_valid["verified"])
        self.assertEqual(res_valid["status"], "VERIFIED_EVIDENCE")
        self.assertIsNotNone(res_valid["source"])

        # 2. Fabricated claim must be rejected as UNKNOWN
        fabricated_claim = "Ph.D. in Aerospace Nuclear Engineering from MIT"
        res_invalid = career_brain_agent.verify_claim(fabricated_claim)
        self.assertFalse(res_invalid["verified"])
        self.assertEqual(res_invalid["status"], "UNKNOWN — candidate confirmation required")

    def test_verified_employers(self):
        profile = career_brain_agent.get_candidate_profile()
        employers = [e["employer"] for e in profile["experiences"]]
        self.assertIn("Ithra Dubai LLC", employers)
        self.assertIn("Ghassan Aboud Group", employers)
        self.assertIn("Prime Hill Properties", employers)

if __name__ == "__main__":
    unittest.main()
