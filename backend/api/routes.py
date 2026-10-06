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
from backend.agents.resume_tailor import resume_tailor_agent
from backend.core.config import EXPORTS_DIR

logger = logging.getLogger("ai7.api")

router = APIRouter(prefix="/api")

# Models
class JobIngestRequest(BaseModel):
    title: str
    company_name: str
    location: Optional[str] = "Dubai, UAE"
    source_url: str
    description: str
    seniority: Optional[str] = "Senior Manager / Director-track"

class ContactAddRequest(BaseModel):
    company_name: str
    full_name: str
    job_title: str
    role_category: Optional[str] = "hiring_manager"
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    target_job_id: Optional[str] = None
    notes: Optional[str] = None

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
    subject: Optional[str] = "Introduction: Real Estate Asset Management & Commercial Strategy — V. Jagannath"
    body: Optional[str] = (
        "Dear Colleague,\n\n"
        "I hope this note finds you well.\n\n"
        "I wanted to share a brief introduction to my background in UAE commercial asset management, retail leasing, and mixed-use portfolio development, having recently overseen 800,000 sq. ft. of prime space across One Za'abeel and the Deira Enrichment Project within an AED 800M portfolio mandate.\n\n"
        "Please feel free to reach out if you would like to discuss strategic opportunities or review my full dossier.\n\n"
        "Best regards,\n"
        "V. Jagannath\n"
        "+971 50 5099065 | v.jagannath3@gmail.com"
    )

class DisconnectRequest(BaseModel):
    service_name: str # "GMAIL" or "LINKEDIN"

class LinkedInTestRequest(BaseModel):
    recipient_url: Optional[str] = "https://www.linkedin.com/in/uae-realestate-leader"
    subject: Optional[str] = "AI7 Career Agent Test Connection"
    message: Optional[str] = "Executive introduction from V. Jagannath."

class SimulateRequest(BaseModel):
    service_name: Optional[str] = None # None means both GMAIL and LINKEDIN


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

@router.post("/jobs/ingest")
def ingest_real_job(req: JobIngestRequest):
    """
    Ingests a 100% verified real job posting.
    Immediately evaluates match score, tailors ATS resume PDF, and prepares application.
    """
    if not req.title.strip() or not req.company_name.strip() or not req.description.strip():
        raise HTTPException(status_code=400, detail="Title, Company Name, and Description are required.")

    # 1. Ingest into database
    job = job_discovery_agent.ingest_job(
        title=req.title.strip(),
        company_name=req.company_name.strip(),
        location=req.location or "Dubai, UAE",
        source_url=req.source_url.strip(),
        description=req.description.strip(),
        seniority=req.seniority or "Senior Manager / Director-track"
    )
    job_id = job["id"]

    # 2. Evaluate fit against Jagannath's verified facts
    match_report = job_fit_agent.evaluate_job(job_id)

    # 3. Generate tailored ATS resume PDF
    resume_res = resume_tailor_agent.generate_tailored_resume(job_id)

    # 4. Prepare application packet (cover letter, Q&A)
    app_packet = application_agent.prepare_application_packet(job_id)

    return {
        "status": "ingested",
        "job": job,
        "match_report": match_report,
        "resume": resume_res,
        "application_packet": app_packet
    }

@router.get("/real-search-links")
def get_real_search_links():
    """Returns working live search URLs for UAE Real Estate and Asset Management roles."""
    return {
        "job_boards": [
            {
                "title": "LinkedIn Jobs: Senior Asset Manager (Dubai, UAE)",
                "url": "https://www.linkedin.com/jobs/search/?keywords=Senior%20Asset%20Manager&location=Dubai%2C%20United%20Arab%20Emirates",
                "badge": "LinkedIn Live",
                "icon": "linkedin"
            },
            {
                "title": "LinkedIn Jobs: Commercial Real Estate Manager (Dubai, UAE)",
                "url": "https://www.linkedin.com/jobs/search/?keywords=Commercial%20Real%20Estate%20Manager&location=Dubai%2C%20United%20Arab%20Emirates",
                "badge": "LinkedIn Live",
                "icon": "linkedin"
            },
            {
                "title": "LinkedIn Jobs: Retail Leasing Director (Dubai, UAE)",
                "url": "https://www.linkedin.com/jobs/search/?keywords=Retail%20Leasing%20Director&location=Dubai%2C%20United%20Arab%20Emirates",
                "badge": "LinkedIn Live",
                "icon": "linkedin"
            },
            {
                "title": "GulfTalent: Real Estate & Property Jobs (UAE)",
                "url": "https://www.gulftalent.com/uae/jobs/category/real-estate",
                "badge": "GulfTalent",
                "icon": "globe"
            },
            {
                "title": "Bayt.com: Asset Management Jobs (Dubai)",
                "url": "https://www.bayt.com/en/uae/jobs/asset-management-jobs/",
                "badge": "Bayt",
                "icon": "briefcase"
            },
            {
                "title": "Indeed UAE: Commercial Real Estate (Dubai)",
                "url": "https://ae.indeed.com/jobs?q=Commercial+Real+Estate&l=Dubai",
                "badge": "Indeed UAE",
                "icon": "search"
            }
        ]
    }

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
@router.get("/contacts")
def list_contacts():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT c.*, 
                   comp.dubai_uae_footprint,
                   o.id as outreach_id,
                   o.channel as outreach_channel,
                   o.subject as outreach_subject,
                   o.message_body as outreach_message_body,
                   o.status as outreach_status,
                   o.outreach_type as outreach_type,
                   o.sent_at as outreach_sent_at
            FROM contacts c
            LEFT JOIN companies comp ON c.company_name = comp.company_name
            LEFT JOIN outreach_campaigns o ON c.id = o.contact_id
            ORDER BY c.company_name ASC, c.full_name ASC
        """).fetchall()
        return [dict(r) for r in rows]

@router.post("/contacts/add")
def add_real_contact(req: ContactAddRequest):
    """
    Adds a verified 100% real human contact found on LinkedIn or in professional circles.
    Instantly drafts tailored executive pitch or recruiter intro.
    """
    if not req.full_name.strip() or not req.company_name.strip():
        raise HTTPException(status_code=400, detail="Full Name and Company Name are required.")

    contact = contact_intelligence_agent.add_real_contact(
        company_name=req.company_name.strip(),
        full_name=req.full_name.strip(),
        job_title=req.job_title.strip() if req.job_title else "Executive",
        role_category=req.role_category or "hiring_manager",
        email=req.email.strip() if req.email else None,
        linkedin_url=req.linkedin_url.strip() if req.linkedin_url else None,
        notes=req.notes
    )

    # Immediately generate tailored outreach draft
    draft = outreach_agent.generate_outreach_draft(
        job_id=req.target_job_id,
        contact_id=contact["id"],
        outreach_type="RECRUITER_INTRO" if contact["role_category"] == "recruiter" else "HIRING_MGR_PITCH"
    )

    return {
        "status": "added",
        "contact": contact,
        "outreach_draft": draft
    }

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

@router.post("/integrations/disconnect")
def disconnect_service(req: DisconnectRequest):
    from backend.services.dispatch_service import dispatch_service
    success, msg = dispatch_service.disconnect_service(req.service_name)
    return {"status": "disconnected", "detail": msg}

@router.post("/integrations/simulate")
def enable_simulated_mode(req: SimulateRequest):
    from backend.services.dispatch_service import dispatch_service
    success, msg = dispatch_service.enable_simulation_mode(req.service_name)
    return {"status": "simulated", "detail": msg}

@router.post("/integrations/linkedin/test")
def test_linkedin_dispatch(req: LinkedInTestRequest):
    from backend.services.dispatch_service import dispatch_service
    success, msg = dispatch_service.send_live_linkedin(req.recipient_url, req.subject, req.message)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "dispatched", "detail": msg}

