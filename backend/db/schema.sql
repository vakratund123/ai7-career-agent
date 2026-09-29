-- AI7 Career Agent Database Schema
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS candidates (
    id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    current_title TEXT NOT NULL,
    location TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    target_seniority TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS candidate_facts (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    category TEXT NOT NULL, -- 'metric', 'role', 'project', 'skill', 'credential', 'preference'
    fact_text TEXT NOT NULL,
    source TEXT NOT NULL,   -- e.g. 'candidate_cv', 'candidate_interview', 'document'
    verified BOOLEAN DEFAULT 1,
    confidence REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experiences (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    employer TEXT NOT NULL,
    parent_company TEXT,
    location TEXT NOT NULL,
    role_title TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    is_current BOOLEAN DEFAULT 0,
    summary TEXT,
    achievements TEXT, -- JSON array of strings
    scope TEXT,        -- e.g. 'AED 800M portfolio, 800,000 sq.ft. leasing'
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skills (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    category TEXT NOT NULL, -- 'domain', 'technical', 'governance', 'language'
    years_experience INTEGER DEFAULT 10,
    evidence TEXT NOT NULL,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value TEXT NOT NULL,
    context TEXT NOT NULL,
    evidence_citation TEXT NOT NULL,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    project_name TEXT NOT NULL,
    developer TEXT NOT NULL,
    scope_description TEXT NOT NULL,
    role_contributed TEXT NOT NULL,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    document_type TEXT NOT NULL, -- 'master_cv', 'tailored_resume', 'cover_letter', 'credential'
    file_path TEXT NOT NULL,
    target_company TEXT,
    target_role TEXT,
    version TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL UNIQUE,
    industry TEXT NOT NULL,
    priority INTEGER DEFAULT 1, -- 1=High, 2=Medium, 3=Standard
    status TEXT DEFAULT 'ACTIVE', -- 'ACTIVE', 'PAUSED', 'EXCLUDED'
    dubai_uae_footprint TEXT,
    website_careers_url TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    source_url TEXT,
    source_type TEXT NOT NULL, -- 'company_career_page', 'job_board', 'executive_search'
    description TEXT NOT NULL,
    seniority TEXT NOT NULL,
    status TEXT DEFAULT 'DISCOVERED', -- 'DISCOVERED', 'QUALIFIED', 'RESEARCHED', 'APPLICATION_READY', 'APPLIED', 'OUTREACH', 'FOLLOW_UP', 'RESPONSE', 'INTERVIEW', 'OFFER', 'REJECTED', 'CLOSED'
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_requirements (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    requirement_text TEXT NOT NULL,
    category TEXT NOT NULL, -- 'experience', 'licensing', 'portfolio', 'leasing', 'education'
    is_mandatory BOOLEAN DEFAULT 1,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_matches (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL UNIQUE,
    overall_fit_label TEXT NOT NULL, -- 'STRONG_FIT', 'MODERATE_FIT', 'LOW_FIT'
    match_score REAL NOT NULL,        -- Explainable score 0.0 to 1.0
    match_areas TEXT NOT NULL,       -- JSON array of {requirement, candidate_evidence, status}
    gaps TEXT NOT NULL,              -- JSON array of {unmet_requirement, status, recommendation}
    reasoning_summary TEXT NOT NULL,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    company_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    role_category TEXT NOT NULL, -- 'hiring_manager', 'recruiter', 'department_leader', 'referral'
    email TEXT,
    linkedin_url TEXT,
    confidence_level TEXT NOT NULL, -- 'VERIFIED', 'HIGH_PROBABILITY', 'UNCONFIRMED'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS outreach_campaigns (
    id TEXT PRIMARY KEY,
    job_id TEXT,
    contact_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    channel TEXT NOT NULL, -- 'EMAIL', 'LINKEDIN'
    subject TEXT,
    message_body TEXT NOT NULL,
    outreach_type TEXT NOT NULL, -- 'RECRUITER_INTRO', 'HIRING_MGR_PITCH', 'EXECUTIVE_NOTE', 'FOLLOW_UP'
    status TEXT DEFAULT 'DRAFT', -- 'DRAFT', 'APPROVED', 'SENT', 'REPLIED', 'BOUNCED'
    sent_at TIMESTAMP,
    response_received_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS applications (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    role_title TEXT NOT NULL,
    tailored_resume_id TEXT,
    cover_letter TEXT,
    qa_answers TEXT, -- JSON mapping of application questions to answers
    status TEXT DEFAULT 'READY', -- 'READY', 'PENDING_APPROVAL', 'SUBMITTED', 'REJECTED'
    submitted_at TIMESTAMP,
    submission_method TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (tailored_resume_id) REFERENCES documents(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS follow_ups (
    id TEXT PRIMARY KEY,
    outreach_id TEXT NOT NULL,
    scheduled_for TIMESTAMP NOT NULL,
    sequence_number INTEGER DEFAULT 1,
    status TEXT DEFAULT 'SCHEDULED', -- 'SCHEDULED', 'EXECUTED', 'CANCELLED', 'SUPPRESSED'
    executed_at TIMESTAMP,
    follow_up_body TEXT NOT NULL,
    FOREIGN KEY (outreach_id) REFERENCES outreach_campaigns(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interviews (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    role_title TEXT NOT NULL,
    interview_stage TEXT NOT NULL, -- 'SCREENING', 'HIRING_MANAGER', 'PANEL', 'FINAL_STAGE'
    scheduled_time TIMESTAMP,
    prep_dossier TEXT, -- JSON of STAR stories, company brief, domain Q&A
    candidate_notes TEXT,
    thank_you_draft TEXT,
    status TEXT DEFAULT 'UPCOMING', -- 'UPCOMING', 'COMPLETED', 'CANCELLED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS emails (
    id TEXT PRIMARY KEY,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_snippet TEXT NOT NULL,
    classification TEXT NOT NULL, -- 'JOB_OPPORTUNITY', 'RECRUITER', 'INTERVIEW', 'APPLICATION_UPDATE', 'REJECTION', 'RFI', 'SALARY', 'NETWORKING', 'SPAM'
    confidence REAL DEFAULT 1.0,
    requires_human_escalation BOOLEAN DEFAULT 0,
    escalation_reason TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_tasks (
    id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    task_name TEXT NOT NULL,
    status TEXT NOT NULL, -- 'PENDING', 'RUNNING', 'COMPLETED', 'FAILED'
    payload TEXT,
    result TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    action_type TEXT NOT NULL, -- 'SUBMIT_APPLICATION', 'SEND_OUTREACH', 'SALARY_CONFIRMATION', 'LEGAL_DECLARATION'
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REJECTED'
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS integrations (
    service_name TEXT PRIMARY KEY,
    auth_type TEXT NOT NULL,
    account_identifier TEXT NOT NULL,
    credentials_encrypted TEXT NOT NULL,
    status TEXT DEFAULT 'DISCONNECTED',
    last_sync_at TIMESTAMP,
    settings TEXT
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,
    entity_id TEXT,
    reasoning_summary TEXT NOT NULL,
    evidence TEXT,
    confidence REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_signals (
    id TEXT PRIMARY KEY,
    signal_category TEXT NOT NULL, -- 'TITLE_RESPONSE_RATE', 'COMPANY_CONVERSION', 'OUTREACH_TONE'
    key_factor TEXT NOT NULL,
    outcome TEXT NOT NULL,
    sample_size INTEGER DEFAULT 1,
    weight REAL DEFAULT 1.0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning fast queries
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach_campaigns(status);
CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_candidate_facts_category ON candidate_facts(category);
