import logging
import uuid
from typing import Dict, Any, List
from backend.db.database import get_db

logger = logging.getLogger("ai7.agent.crm_pipeline")

PIPELINE_STAGES = [
    "DISCOVERED",
    "QUALIFIED",
    "RESEARCHED",
    "APPLICATION_READY",
    "APPLIED",
    "OUTREACH",
    "FOLLOW_UP",
    "RESPONSE",
    "INTERVIEW",
    "FINAL_STAGE",
    "OFFER",
    "CLOSED"
]

class CRMPipelineAgent:
    """
    CRM / Career Pipeline Agent (Agent M):
    Maintains the 12-stage Career CRM, orchestrates status transitions,
    and constructs full historical audit timelines for every opportunity.
    """
    def __init__(self):
        pass

    def get_pipeline_overview(self) -> Dict[str, Any]:
        """Returns opportunities grouped by pipeline stage."""
        overview = {stage: [] for stage in PIPELINE_STAGES}

        with get_db() as conn:
            jobs = conn.execute("""
                SELECT j.*, c.industry, c.priority
                FROM jobs j
                JOIN companies c ON j.company_id = c.id
                ORDER BY j.discovered_at DESC
            """).fetchall()

            for job in jobs:
                stage = job["status"]
                if stage in overview:
                    overview[stage].append(dict(job))
                else:
                    overview["DISCOVERED"].append(dict(job))

        return {
            "stages": PIPELINE_STAGES,
            "counts": {stage: len(overview[stage]) for stage in PIPELINE_STAGES},
            "pipeline": overview
        }

    def transition_stage(self, job_id: str, new_stage: str, reason: str = "Automated agent progression") -> Dict[str, Any]:
        """Transitions an opportunity to a new pipeline stage with full audit logging."""
        if new_stage not in PIPELINE_STAGES:
            return {"error": f"Invalid stage: {new_stage}"}

        with get_db() as conn:
            conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_stage, job_id))

            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'crm_pipeline_agent', 'transition_stage', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), job_id, f"Transitioned job to {new_stage}", reason, ))

        logger.info(f"Transitioned job {job_id} to stage {new_stage}")
        return {"job_id": job_id, "new_stage": new_stage, "reason": reason}

    def get_opportunity_timeline(self, job_id: str) -> List[Dict[str, Any]]:
        """Constructs an end-to-end historical timeline of all actions taken on an opportunity."""
        with get_db() as conn:
            logs = conn.execute("""
                SELECT * FROM audit_logs
                WHERE entity_id = ? OR reasoning_summary LIKE ?
                ORDER BY timestamp ASC
            """, (job_id, f"%{job_id}%")).fetchall()
            return [dict(l) for l in logs]

crm_pipeline_agent = CRMPipelineAgent()
