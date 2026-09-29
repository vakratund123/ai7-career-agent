import logging
import asyncio
import uuid
import json
from typing import Dict, Any, List
from backend.db.database import get_db
from backend.core.event_bus import event_bus
from backend.agents.career_brain import career_brain_agent
from backend.agents.job_discovery import job_discovery_agent
from backend.agents.company_intelligence import company_intelligence_agent
from backend.agents.fit_match import job_fit_agent
from backend.agents.resume_tailor import resume_tailor_agent
from backend.agents.application_agent import application_agent
from backend.agents.contact_intelligence import contact_intelligence_agent
from backend.agents.outreach_agent import outreach_agent
from backend.agents.follow_up import follow_up_agent
from backend.agents.email_inbox import email_inbox_agent
from backend.agents.interview_intel import interview_intel_agent
from backend.agents.crm_pipeline import crm_pipeline_agent
from backend.agents.learning_agent import learning_agent
from backend.agents.compliance_agent import compliance_agent
from backend.agents.human_escalation import human_escalation_agent

logger = logging.getLogger("ai7.agent.orchestrator")

class OrchestratorAgent:
    """
    Orchestrator Agent (Agent A):
    The central reasoning and task-management brain of AI7.
    Dispatches workflows across the 16 multi-agent team, manages state transitions,
    and guarantees that the candidate acts purely as an exception handler.
    """
    def __init__(self):
        self._setup_event_listeners()

    def _setup_event_listeners(self):
        """Wires reactive event subscriptions between agents."""
        event_bus.subscribe("JOB_DISCOVERED", self._handle_job_discovered)
        event_bus.subscribe("JOB_QUALIFIED", self._handle_job_qualified)
        event_bus.subscribe("APPLICATION_READY", self._handle_application_ready)

    async def _handle_job_discovered(self, payload: dict):
        job_id = payload.get("job_id")
        logger.info(f"Orchestrator reacting to JOB_DISCOVERED: {job_id}")
        # Run fit analysis
        fit_report = job_fit_agent.evaluate_job(job_id)
        if fit_report.get("overall_fit_label") in ["STRONG_FIT", "MODERATE_FIT"]:
            await event_bus.publish("JOB_QUALIFIED", {"job_id": job_id, "fit": fit_report})

    async def _handle_job_qualified(self, payload: dict):
        job_id = payload.get("job_id")
        logger.info(f"Orchestrator reacting to JOB_QUALIFIED: {job_id}")
        # Prepare application packet & tailored resume
        app_packet = application_agent.prepare_application_packet(job_id)
        await event_bus.publish("APPLICATION_READY", {"job_id": job_id, "application": app_packet})

    async def _handle_application_ready(self, payload: dict):
        job_id = payload.get("job_id")
        logger.info(f"Orchestrator reacting to APPLICATION_READY: {job_id}")
        # Discover contacts and prepare outreach
        contacts = contact_intelligence_agent.get_contacts_by_job(job_id)
        if contacts:
            contact = contacts[0]
            outreach_draft = outreach_agent.generate_outreach_draft(job_id, contact["id"])
            # In Level 2 (AI-First), if permitted, dispatch or queue
            outreach_agent.send_outreach(outreach_draft["outreach_id"])

    def run_full_pipeline_cycle(self) -> Dict[str, Any]:
        """
        Runs an end-to-end autonomous cycle:
        Scouts new jobs -> Analyzes Company Intel -> Evaluates Fit ->
        Prepares Tailored Resumes & Cover Letters -> Discovers Contacts ->
        Prepares Outreach -> Updates CRM.
        """
        cycle_id = str(uuid.uuid4())[:8]
        logger.info(f"Starting autonomous pipeline cycle [{cycle_id}]")

        # 1. Discover jobs
        new_jobs = job_discovery_agent.discover_opportunities()

        # 2. Get active jobs to process
        all_jobs = job_discovery_agent.get_all_jobs()
        processed_count = 0
        qualified_count = 0
        applications_prepared = 0
        outreaches_created = 0

        for job in all_jobs:
            job_id = job["id"]

            # Step A: Evaluate fit if not yet evaluated
            match_report = job_fit_agent.get_match_report(job_id)
            if not match_report:
                match_report = job_fit_agent.evaluate_job(job_id)

            if match_report.get("overall_fit_label") in ["STRONG_FIT", "MODERATE_FIT"]:
                qualified_count += 1

                # Step B: Research company
                dossier = company_intelligence_agent.get_company_dossier(job["company_name"])

                # Step C: Prepare application & tailored resume if not yet done
                with get_db() as conn:
                    app_exists = conn.execute("SELECT id FROM applications WHERE job_id = ?", (job_id,)).fetchone()
                if not app_exists:
                    app_packet = application_agent.prepare_application_packet(job_id)
                    applications_prepared += 1

                # Step D: Contact discovery & outreach
                contacts = contact_intelligence_agent.get_contacts_by_job(job_id)
                if contacts:
                    contact = contacts[0]
                    with get_db() as conn:
                        outreach_exists = conn.execute("SELECT id FROM outreach_campaigns WHERE job_id = ? AND contact_id = ?", (job_id, contact["id"])).fetchone()
                    if not outreach_exists:
                        draft = outreach_agent.generate_outreach_draft(job_id, contact["id"])
                        if "outreach_id" in draft:
                            outreach_agent.send_outreach(draft["outreach_id"])
                            outreaches_created += 1

            processed_count += 1

        # Audit log for the cycle
        with get_db() as conn:
            conn.execute("""
                INSERT INTO audit_logs (id, agent_name, action, entity_id, reasoning_summary, evidence, confidence)
                VALUES (?, 'orchestrator_agent', 'run_cycle', ?, ?, ?, 1.0)
            """, (str(uuid.uuid4()), cycle_id, f"Completed autonomous loop. Scouted {len(new_jobs)} jobs, qualified {qualified_count}, prepared {applications_prepared} applications, dispatched {outreaches_created} outreaches.", f"Jobs processed: {processed_count}", ))

        return {
            "cycle_id": cycle_id,
            "jobs_scouted": len(new_jobs),
            "jobs_evaluated": processed_count,
            "jobs_qualified": qualified_count,
            "applications_prepared": applications_prepared,
            "outreaches_dispatched": outreaches_created,
            "status": "COMPLETED"
        }

    def get_agent_activity_feed(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns structured audit log stream for the live UI."""
        with get_db() as conn:
            rows = conn.execute("""
                SELECT * FROM audit_logs
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]

orchestrator = OrchestratorAgent()
