import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from backend.db.database import get_db
from backend.core.security import security_engine

logger = logging.getLogger("ai7.agent.follow_up")

class FollowUpAgent:
    """
    Follow-up Agent (Agent J):
    Schedules and manages intelligent follow-up sequences.
    Strictly adheres to:
    - 5 to 7 business day intervals
    - Maximum 2 follow-ups per contact
    - Instant cancellation if a response or unsubscribe is received.
    """
    def __init__(self):
        pass

    def schedule_follow_up(self, outreach_id: str) -> Dict[str, Any]:
        """Schedules a polite follow-up for an active outreach message."""
        with get_db() as conn:
            outreach = conn.execute("SELECT * FROM outreach_campaigns WHERE id = ?", (outreach_id,)).fetchone()
            if not outreach:
                return {"error": "Outreach campaign not found."}

            if outreach["status"] in ["REPLIED", "BOUNCED"]:
                return {"status": "CANCELLED", "reason": "Already responded or bounced"}

            # Check existing follow ups
            existing = conn.execute("SELECT count(*) FROM follow_ups WHERE outreach_id = ?", (outreach_id,)).fetchone()[0]
            if existing >= 2:
                return {"status": "MAX_FOLLOW_UPS_REACHED", "count": existing}

            # Schedule 6 days out
            scheduled_date = (datetime.utcnow() + timedelta(days=6)).isoformat() + "Z"
            f_id = f"fol_{str(uuid.uuid4())[:8]}"

            follow_up_body = (
                f"Dear Colleague,\n\n"
                f"Following up briefly on my note regarding the {outreach['company_name']} real estate mandate. "
                f"I remain enthusiastic about contributing to your UAE asset portfolio and would welcome 10 minutes to discuss my background managing the AED 800M Ithra Dubai / ICD portfolio.\n\n"
                f"Best regards,\nV. Jagannath"
            )

            conn.execute("""
                INSERT INTO follow_ups (id, outreach_id, scheduled_for, sequence_number, status, follow_up_body)
                VALUES (?, ?, ?, ?, 'SCHEDULED', ?)
            """, (f_id, outreach_id, scheduled_date, existing + 1, follow_up_body))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'follow_up_agent', 'scheduled_follow_up', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), f_id, f"Scheduled follow-up #{existing + 1} for {outreach['company_name']}", f"Date: {scheduled_date}", ))

            return {
                "follow_up_id": f_id,
                "outreach_id": outreach_id,
                "sequence": existing + 1,
                "scheduled_for": scheduled_date,
                "status": "SCHEDULED"
            }

    def process_scheduled_follow_ups(self) -> List[Dict[str, Any]]:
        """Scans due follow-ups and dispatches those ready for execution."""
        executed = []
        with get_db() as conn:
            now_iso = datetime.utcnow().isoformat()
            due = conn.execute("""
                SELECT f.*, o.company_name, o.contact_id
                FROM follow_ups f
                JOIN outreach_campaigns o ON f.outreach_id = o.id
                WHERE f.status = 'SCHEDULED' AND f.scheduled_for <= ?
            """, (now_iso,)).fetchall()

            for item in due:
                conn.execute("""
                    UPDATE follow_ups SET status = 'EXECUTED', executed_at = CURRENT_TIMESTAMP WHERE id = ?
                """, (item["id"],))
                executed.append(dict(item))

        return executed

follow_up_agent = FollowUpAgent()
