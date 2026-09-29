import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_candidate_endpoint(self):
        response = self.client.get("/api/candidate")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["full_name"], "V. Jagannath")
        self.assertIn("verified_facts", data)
        self.assertIn("experiences", data)

    def test_briefing_endpoint(self):
        response = self.client.get("/api/briefing")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("briefing_text", data)
        self.assertIn("action_required", data)
        self.assertIn("metrics", data)

    def test_jobs_endpoint(self):
        response = self.client.get("/api/jobs")
        self.assertEqual(response.status_code, 200)
        jobs = response.json()
        self.assertIsInstance(jobs, list)
        self.assertGreater(len(jobs), 0)

    def test_pipeline_endpoint(self):
        response = self.client.get("/api/pipeline")
        self.assertEqual(response.status_code, 200)
        pipeline = response.json()
        self.assertIn("stages", pipeline)
        self.assertIn("counts", pipeline)

    def test_approvals_endpoint(self):
        response = self.client.get("/api/approvals")
        self.assertEqual(response.status_code, 200)
        approvals = response.json()
        self.assertIsInstance(approvals, list)

    def test_settings_endpoint(self):
        response = self.client.get("/api/settings")
        self.assertEqual(response.status_code, 200)
        settings = response.json()
        self.assertIn("security_posture", settings)
        self.assertIn("target_companies", settings)

if __name__ == "__main__":
    unittest.main()
