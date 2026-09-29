import logging
from typing import Dict, Any, Tuple
from backend.core.security import security_engine, ACTION_POLICIES
from backend.db.database import get_db

logger = logging.getLogger("ai7.agent.compliance")

class ComplianceSafetyAgent:
    """
    Compliance / Safety Agent (Agent O):
    Central enforcement gate ensuring no agent action violates configured candidate autonomy,
    rate limits, or privacy policies.
    """
    def __init__(self):
        pass

    def evaluate_action(self, action_name: str, payload: dict = None) -> Tuple[bool, str]:
        """Evaluates whether an action is permitted under the candidate's current autonomy setting."""
        with get_db() as conn:
            pref = conn.execute("SELECT value FROM preferences WHERE key = 'autonomy_level'").fetchone()
            autonomy_level = int(pref["value"]) if pref else 2

        permitted, reason = security_engine.check_permission(action_name, autonomy_level)
        return permitted, reason

    def get_security_posture(self) -> Dict[str, Any]:
        """Returns the active permissions matrix and anti-spam status."""
        with get_db() as conn:
            pref = conn.execute("SELECT value FROM preferences WHERE key = 'autonomy_level'").fetchone()
            autonomy_level = int(pref["value"]) if pref else 2

        level_labels = {
            1: "Level 1 — Copilot (Human approves all outreach/applications)",
            2: "Level 2 — AI-First [Default] (Routine automated, exceptions escalated)",
            3: "Level 3 — High Autonomy (Full autonomy within strict guardrails)"
        }

        return {
            "current_autonomy_level": autonomy_level,
            "autonomy_label": level_labels.get(autonomy_level, "Level 2"),
            "action_policies": ACTION_POLICIES,
            "anti_spam_guardrails": {
                "max_contacts_per_company": 4,
                "max_touchpoints_per_person": 3,
                "cooldown_days": 6,
                "unsubscribed_count": len(security_engine.suppression_list)
            }
        }

compliance_agent = ComplianceSafetyAgent()
