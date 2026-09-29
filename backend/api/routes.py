import os
import json
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.db.database import get_db
from backend.agents.career_brain import career_brain_agent
from backend.agents.orchestrator import orchestrator
from backend.agents.job_discovery import job_discovery_agent
from backend.agents.fit_match import job_fit_agent
from backend.agents.application_agent import application_agent
from backend.agents.contact_intelligence import contact_intelligence_agent
from backend.agents.outreach_agent import outreach_agent
from backend.agents.crm_pipeline import crm_pipeline_agent
from backend.agents.learning_agent import learning_agent
from backend.agents.human_escalation import human_escalation_agent
from backend.agents.compliance_agent import compliance_agent
from backend.agents.interview_intel import interview_intel_agent
from backend.core.config import EXPORTS_DIR

logger = logging.getLogger("ai7.api")

router = APIRouter(prefix="/api")

# Models
class FactCreateRequest(BaseModel):
    category: str
    fact_text: str
    source: str
    confidence: Optional[float] = 1.0

class ApprovalDecisionRequest(BaseModel):
    decision: str # "APPROVE" or "REJECT"

class AutonomyUpdateRequest(BaseModel):
    autonomy_level: int # 1, 2, or 3

class DebriefRequest(BaseModel):
    notes: str

class GmailConnectRequest(BaseModel):
    email: str
    app_password: str
    live_dispatch: Optional[bool] = True

class LinkedInConnectRequest(BaseModel):
    profile_url: str
    session_cookie: str
    live_dispatch: Optional[bool] = True

class TestEmailRequest(BaseModel):
    recipient: str
    subject: Optional[str] = "AI7 Career Agent Test Transmission"
    body: Optional[str] = "This is a verified test email dispatched autonomously by the AI7 Career Agent on behalf of V. Jagannath."

# Candidate & Career Brain
@router.get("/candidate")
def get_candidate():
    profile = career_brain_agent.get_candidate_profile()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return profile

@router.get("/career-brain")
def get_career_brain():
    return career_brain_agent.get_candidate_profile()

@router.post("/career-brain/facts")
def add_fact(req: FactCreateRequest):
    fact_id = career_brain_agent.add_fact(req.category, req.fact_text, req.source, verified=True, confidence=req.confidence)
    return {"status": "created", "fact_id": fact_id}

# Executive Briefing
@router.get("/briefing")
def get_executive_briefing():
    return human_escalation_agent.generate_daily_executive_briefing()

# Jobs & Discovery
@router.get("/jobs")
def get_jobs(status: Optional[str] = None):
    return job_discovery_agent.get_all_jobs(status=status)

@router.post("/jobs/search")
def run_job_search():
    discovered = job_discovery_agent.discover_opportunities()
    return {"discovered_count": len(discovered), "jobs": discovered}

@router.get("/jobs/{job_id}")
def get_job_detail(job_id: str):
    with get_db() as conn:
        job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        match_rep = job_fit_agent.get_match_report(job_id)
        contacts = contact_intelligence_agent.get_contacts_by_job(job_id)
        return {
            "job": dict(job),
            "match_report": match_rep,
            "contacts": contacts
        }

@router.post("/jobs/{job_id}/analyze")
def analyze_job(job_id: str):
    report = job_fit_agent.evaluate_job(job_id)
    return report

# Applications & Tailored Documents
@router.post("/applications/prepare")
def prepare_application(job_id: str):
    packet = application_agent.prepare_application_packet(job_id)
    return packet

@router.get("/applications/{job_id}")
def get_application(job_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM applications WHERE job_id = ?", (job_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Application not yet prepared")
        res = dict(row)
        if res.get("qa_answers"):
            res["qa_answers"] = json.loads(res["qa_answers"])
        return res

@router.get("/documents/download/{filename}")
def download_document(filename: str):
    file_path = EXPORTS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(file_path), filename=filename, media_type='application/pdf')

# Contacts & Outreach
@router.post("/contacts/discover")
def discover_contacts(company_name: str):
    return contact_intelligence_agent.discover_contacts_for_company(company_name)

@router.post("/outreach/generate")
def generate_outreach(job_id: str, contact_id: str, outreach_type: str = "HIRING_MGR_PITCH"):
    draft = outreach_agent.generate_outreach_draft(job_id, contact_id, outreach_type=outreach_type)
    return draft

@router.post("/outreach/{outreach_id}/send")
def send_outreach(outreach_id: str):
    res = outreach_agent.send_outreach(outreach_id)
    return res

# CRM & Pipeline
@router.get("/pipeline")
def get_pipeline():
    return crm_pipeline_agent.get_pipeline_overview()

@router.post("/pipeline/{job_id}/transition")
def transition_job_stage(job_id: str, stage: str):
    return crm_pipeline_agent.transition_stage(job_id, stage)

@router.get("/pipeline/{job_id}/timeline")
def get_timeline(job_id: str):
    return crm_pipeline_agent.get_opportunity_timeline(job_id)

# Interviews
@router.post("/interviews/dossier")
def prepare_interview(job_id: str, stage: str = "HIRING_MANAGER"):
    return interview_intel_agent.prepare_interview_dossier(job_id, stage=stage)

@router.post("/interviews/{interview_id}/debrief")
def record_interview_debrief(interview_id: str, req: DebriefRequest):
    return interview_intel_agent.record_debrief_and_generate_thank_you(interview_id, req.notes)

@router.get("/interviews")
def list_interviews():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM interviews ORDER BY created_at DESC").fetchall()
        res = []
        for r in rows:
            d = dict(r)
            if d.get("prep_dossier"):
                d["prep_dossier"] = json.loads(d["prep_dossier"])
            res.append(d)
        return res

# Approvals Queue (Human Escalation)
@router.get("/approvals")
def get_approvals():
    return human_escalation_agent.get_pending_approvals()

@router.post("/approvals/{approval_id}/resolve")
def resolve_approval(approval_id: str, req: ApprovalDecisionRequest):
    return human_escalation_agent.resolve_approval(approval_id, req.decision)

# Agent Activity & Autonomous Trigger
@router.get("/agent/activity")
def get_agent_activity():
    return orchestrator.get_agent_activity_feed()

@router.post("/agent/cycle/run")
def trigger_agent_cycle():
    result = orchestrator.run_full_pipeline_cycle()
    return result

# Analytics & Insights
@router.get("/analytics")
def get_analytics():
    return learning_agent.get_optimization_insights()

# Settings & Autonomy
@router.get("/settings")
def get_settings():
    posture = compliance_agent.get_security_posture()
    with get_db() as conn:
        companies = [dict(r) for r in conn.execute("SELECT * FROM companies ORDER BY priority ASC, company_name ASC").fetchall()]
        prefs = {r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM preferences").fetchall()}
    return {
        "security_posture": posture,
        "target_companies": companies,
        "preferences": prefs
    }

@router.post("/settings/autonomy")
def update_autonomy(req: AutonomyUpdateRequest):
    with get_db() as conn:
        conn.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES ('autonomy_level', ?)", (str(req.autonomy_level),))
    return {"status": "updated", "autonomy_level": req.autonomy_level}

# Accounts & Live Integrations
@router.get("/integrations")
def get_integrations():
    from backend.services.dispatch_service import dispatch_service
    return dispatch_service.get_integration_status()

@router.post("/integrations/gmail")
def connect_gmail(req: GmailConnectRequest):
    from backend.services.dispatch_service import dispatch_service
    success, msg = dispatch_service.connect_gmail(req.email, req.app_password, live_dispatch=req.live_dispatch)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "connected", "message": msg}

@router.post("/integrations/linkedin")
def connect_linkedin(req: LinkedInConnectRequest):
    from backend.services.dispatch_service import dispatch_service
    success, msg = dispatch_service.connect_linkedin(req.profile_url, req.session_cookie, live_dispatch=req.live_dispatch)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "connected", "message": msg}

@router.post("/integrations/sync-inbox")
def sync_inbox():
    from backend.services.dispatch_service import dispatch_service
    res = dispatch_service.sync_live_inbox()
    return res

@router.post("/integrations/test-email")
def test_email(req: TestEmailRequest):
    from backend.services.dispatch_service import dispatch_service
    success, msg = dispatch_service.send_live_email(req.recipient, req.subject, req.body)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "dispatched", "detail": msg}
