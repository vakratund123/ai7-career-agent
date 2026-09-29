import logging
import json
import uuid
from typing import Dict, Any, List, Optional
from backend.db.database import get_db

logger = logging.getLogger("ai7.agent.career_brain")

class CareerBrainAgent:
    """
    Career Brain Agent (Agent B):
    Persistent candidate knowledge system maintaining verified facts,
    provenance tracking, career metrics, employment records, and skills.
    RULE: The AI must NEVER convert an inference into a fact.
    Every factual candidate claim must have provenance.
    """
    def __init__(self, candidate_id: str = "jagannath_v"):
        self.candidate_id = candidate_id

    def get_candidate_profile(self) -> Dict[str, Any]:
        """Retrieves verified candidate profile and summary metrics."""
        with get_db() as conn:
            cand = conn.execute("SELECT * FROM candidates WHERE id = ?", (self.candidate_id,)).fetchone()
            if not cand:
                return {}
            profile = dict(cand)

            facts = [dict(row) for row in conn.execute("SELECT * FROM candidate_facts WHERE candidate_id = ?", (self.candidate_id,)).fetchall()]
            experiences = [dict(row) for row in conn.execute("SELECT * FROM experiences WHERE candidate_id = ? ORDER BY start_date DESC", (self.candidate_id,)).fetchall()]
            achievements = [dict(row) for row in conn.execute("SELECT * FROM achievements WHERE candidate_id = ?", (self.candidate_id,)).fetchall()]
            skills = [dict(row) for row in conn.execute("SELECT * FROM skills WHERE candidate_id = ?", (self.candidate_id,)).fetchall()]

            # Decode achievements JSON strings in experiences
            for exp in experiences:
                if exp.get("achievements"):
                    try:
                        exp["achievements"] = json.loads(exp["achievements"])
                    except Exception:
                        pass

            profile["verified_facts"] = facts
            profile["experiences"] = experiences
            profile["achievements"] = achievements
            profile["skills"] = skills
            return profile

    def verify_claim(self, claim_text: str) -> Dict[str, Any]:
        """
        Anti-Hallucination Gate:
        Checks if a factual claim has verified evidence in Career Brain.
        If evidence is unavailable, returns UNKNOWN — candidate confirmation required.
        """
        with get_db() as conn:
            cursor = conn.execute("""
                SELECT fact_text, source, confidence FROM candidate_facts
                WHERE candidate_id = ? AND verified = 1
            """, (self.candidate_id,))
            facts = cursor.fetchall()

        matched_fact = None
        claim_lower = claim_text.lower()
        for f in facts:
            fact_str = f["fact_text"].lower()
            # Simple keyword overlap or exact phrase match
            if any(term in fact_str for term in claim_lower.split() if len(term) > 4):
                matched_fact = f
                break

        if matched_fact:
            return {
                "verified": True,
                "status": "VERIFIED_EVIDENCE",
                "source": matched_fact["source"],
                "confidence": matched_fact["confidence"],
                "evidence": matched_fact["fact_text"]
            }
        else:
            return {
                "verified": False,
                "status": "UNKNOWN — candidate confirmation required",
                "source": None,
                "confidence": 0.0,
                "evidence": None
            }

    def add_fact(self, category: str, fact_text: str, source: str, verified: bool = True, confidence: float = 1.0):
        """Adds a verified candidate fact with provenance."""
        fact_id = str(uuid.uuid4())
        with get_db() as conn:
            conn.execute("""
                INSERT INTO candidate_facts (id, candidate_id, category, fact_text, source, verified, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (fact_id, self.candidate_id, category, fact_text, source, int(verified), confidence))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'career_brain_agent', 'add_fact', ?, ?, ?, ?)
            """, (str(uuid.uuid4()), fact_id, f"Added {category} fact with source {source}", fact_text, confidence))
        return fact_id

career_brain_agent = CareerBrainAgent()
