import logging
import uuid
from typing import Dict, Any, List
from backend.db.database import get_db

logger = logging.getLogger("ai7.agent.email_inbox")

EMAIL_CATEGORIES = [
    "JOB_OPPORTUNITY",
    "RECRUITER",
    "INTERVIEW",
    "APPLICATION_UPDATE",
    "REJECTION",
    "REQUEST_FOR_INFORMATION",
    "SALARY_DISCUSSION",
    "NETWORKING",
    "SPAM",
    "OTHER"
]

class EmailInboxAgent:
    """
    Email / Inbox Agent (Agent K):
    Classifies incoming communications into 9 categories.
    Enforces automatic handling for routine updates, and immediate Human Escalation
    for salary negotiations, interview schedules, and legal/contractual terms.
    """
    def __init__(self):
        pass

    def classify_and_process_email(self, sender: str, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """Classifies an incoming email and determines if escalation is required."""
        text_lower = (subject + " " + body).lower()

        # Classification logic
        classification = "OTHER"
        escalate = False
        reason = None

        if any(w in text_lower for w in ["interview", "invitation to speak", "video call", "zoom", "teams"]):
            classification = "INTERVIEW"
            escalate = True
            reason = "Interview detected: Candidate confirmation and time selection required."
        elif any(w in text_lower for w in ["salary", "compensation", "package", "remuneration", "benefits"]):
            classification = "SALARY_DISCUSSION"
            escalate = True
            reason = "Salary/compensation negotiation requires human judgment."
        elif any(w in text_lower for w in ["contract", "offer letter", "formal offer"]):
            classification = "APPLICATION_UPDATE"
            escalate = True
            reason = "Formal offer / contract detected: Requires candidate review."
        elif any(w in text_lower for w in ["regret to inform", "other candidates", "not moving forward", "unsuccessful"]):
            classification = "REJECTION"
            escalate = False
        elif any(w in text_lower for w in ["recruiter", "talent acquisition", "headhunter", "executive search"]):
            classification = "RECRUITER"
            escalate = False
        elif any(w in text_lower for w in ["provide more details", "documents needed", "work authorization status"]):
            classification = "REQUEST_FOR_INFORMATION"
            escalate = True
            reason = "Employer requested additional documents/credentials."
        elif any(w in text_lower for w in ["lottery", "crypto", "inheritance", "viagra", "click here"]):
            classification = "SPAM"
            escalate = False

        email_id = f"eml_{str(uuid.uuid4())[:8]}"

        with get_db() as conn:
            conn.execute("""
                INSERT INTO emails (id, sender, recipient, subject, body_snippet, classification, confidence, requires_human_escalation, escalation_reason)
                VALUES (?, ?, ?, ?, ?, ?, 1.0, ?, ?)
            """, (email_id, sender, recipient, subject, body[:250], classification, int(escalate), reason))

            if escalate:
                conn.execute("""
                    INSERT INTO approvals (id, action_type, title, description, payload, status)
                    VALUES (?, 'INBOX_ESCALATION', ?, ?, ?, 'PENDING')
                """, (str(uuid.uuid4()), f"Inbox Alert: {classification} from {sender}", reason, body[:400]))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'email_inbox_agent', 'classified_email', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), email_id, f"Classified email as {classification} (Escalate: {escalate})", subject, ))

        return {
            "email_id": email_id,
            "classification": classification,
            "requires_human_escalation": escalate,
            "escalation_reason": reason
        }

    def get_recent_emails(self, limit: int = 20) -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM emails ORDER BY processed_at DESC LIMIT ?", (limit,)).fetchall()
            return [dict(r) for r in rows]

email_inbox_agent = EmailInboxAgent()
