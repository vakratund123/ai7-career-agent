import logging
from datetime import datetime
from typing import Dict, Any, Tuple

logger = logging.getLogger("ai7.security")

# Action classifications
# AUTO: Executes automatically without user prompt
# CONFIGURABLE: Depends on candidate's chosen Autonomy Level (1, 2, or 3)
# HUMAN: Always requires explicit human confirmation (cannot be automated)
ACTION_POLICIES = {
    "READ_PUBLIC_JOB": "AUTO",
    "RESEARCH_COMPANY": "AUTO",
    "GENERATE_RESUME": "AUTO",
    "GENERATE_MESSAGE": "AUTO",
    "UPDATE_CRM": "AUTO",
    "PREPARE_APPLICATION": "AUTO",
    "SEND_RECRUITER_MESSAGE": "CONFIGURABLE",
    "SUBMIT_APPLICATION": "CONFIGURABLE",
    "SEND_EMAIL": "CONFIGURABLE",
    "SALARY_NEGOTIATION": "HUMAN",
    "LEGAL_DECLARATION": "HUMAN",
    "CONTRACT_ACCEPTANCE": "HUMAN"
}

class SecurityPolicyEngine:
    """
    Centralized permissions, compliance, rate limiting, and anti-spam engine.
    """
    def __init__(self):
        # Company-level contact tracking: {company_name: [timestamp_sent]}
        self.company_outreach_history: Dict[str, list] = {}
        # Contact-level outreach count: {contact_id: count}
        self.contact_outreach_count: Dict[str, int] = {}
        # Unsubscribed or negative contacts: set of emails/names
        self.suppression_list: set = set()

    def check_permission(self, action_name: str, autonomy_level: int = 2) -> Tuple[bool, str]:
        """
        Evaluates whether an agent action is permitted or requires human escalation.
        Returns (is_permitted, reason_or_escalation_type)
        """
        policy = ACTION_POLICIES.get(action_name, "HUMAN")

        if policy == "AUTO":
            return True, "Permitted: Routine autonomous action"

        if policy == "HUMAN":
            return False, f"Escalate to human: {action_name} involves material commitments, legal, or sensitive decisions."

        if policy == "CONFIGURABLE":
            if autonomy_level == 1:
                # Level 1 Copilot: Human approves all external actions
                return False, f"Human approval required: Autonomy is Level 1 (Copilot) for {action_name}"
            elif autonomy_level == 2:
                # Level 2 AI-First (Default): Routine communications permitted if within anti-spam rules
                return True, "Permitted: Level 2 AI-First routine operation with safety guardrails"
            elif autonomy_level == 3:
                # Level 3 High Autonomy: Automated execution permitted
                return True, "Permitted: Level 3 High Autonomy"

        return False, "Action requires human confirmation by default"

    def check_outreach_safety(self, company: str, contact_id: str, contact_email: str) -> Tuple[bool, str]:
        """Anti-spam guardrails checking frequency, cooldown, and suppression."""
        if contact_email in self.suppression_list:
            return False, "Recipient is on the suppression/unsubscribe list. STOP."

        count = self.contact_outreach_count.get(contact_id, 0)
        if count >= 3:
            return False, f"Maximum touchpoints (3) reached for contact {contact_id}. Cooldown active."

        company_touches = self.company_outreach_history.get(company, [])
        # Max 4 active outreaches per company across entire pipeline to prevent spamming
        if len(company_touches) >= 4:
            return False, f"Company-level outreach cap (4) reached for {company}. Waiting for response or cooldown."

        return True, "Safe for personalized outreach."

    def record_outreach(self, company: str, contact_id: str):
        self.contact_outreach_count[contact_id] = self.contact_outreach_count.get(contact_id, 0) + 1
        if company not in self.company_outreach_history:
            self.company_outreach_history[company] = []
        self.company_outreach_history[company].append(datetime.utcnow().isoformat())

    def add_to_suppression(self, identifier: str):
        self.suppression_list.add(identifier)
        logger.info(f"Added {identifier} to suppression list.")

security_engine = SecurityPolicyEngine()
