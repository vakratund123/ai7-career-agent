// AI7 Career Agent Frontend Application
const API_BASE = '/api';

let currentCandidate = null;
let currentPipeline = null;
let currentJobs = [];
let currentApprovals = [];

document.addEventListener('DOMContentLoaded', () => {
  initApp();
  setInterval(refreshTelemetry, 15000);
});

async function initApp() {
  await Promise.all([
    loadBriefing(),
    loadCandidateProfile(),
    loadPipeline(),
    loadActivityStream(),
    loadSettings(),
    loadContacts(),
    loadInterviews(),
    loadApprovals(),
    loadIntegrationsStatus()
  ]);
}

async function refreshTelemetry() {
  await Promise.all([
    loadBriefing(),
    loadPipeline(),
    loadActivityStream(),
    loadContacts(),
    loadApprovals(),
    loadIntegrationsStatus()
  ]);
}

// Tab Switching
function switchTab(tabId) {
  document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));

  const targetTab = document.getElementById(tabId);
  if (targetTab) {
    targetTab.classList.add('active');
  }

  // Set active button
  const matchingBtn = Array.from(document.querySelectorAll('.tab-button')).find(btn => 
    btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(tabId)
  );
  if (matchingBtn) matchingBtn.classList.add('active');

  // Trigger tab-specific loads
  if (tabId === 'tab-matches') loadOpportunitiesRadar();
  if (tabId === 'tab-contacts') loadContacts();
  if (tabId === 'tab-resumes') loadTailoredResumes();
  if (tabId === 'tab-brain') loadCareerBrain();
  if (tabId === 'tab-interviews') loadInterviews();
  if (tabId === 'tab-approvals') loadApprovals();
  if (tabId === 'tab-integrations') loadIntegrationsStatus();
}


// 1. Executive Briefing
async function loadBriefing() {
  try {
    const res = await fetch(`${API_BASE}/briefing`);
    const data = await res.json();
    
    document.getElementById('briefing-text').innerHTML = data.briefing_text.replace(/\n/g, '<br/>');
    document.getElementById('action-required-text').textContent = data.action_required || 'No immediate action required';
    
    if (data.metrics) {
      document.getElementById('kpi-discovered').textContent = data.metrics.discovered || 0;
      document.getElementById('kpi-qualified').textContent = data.metrics.qualified || 0;
      document.getElementById('kpi-applications').textContent = data.metrics.applications_prepared || 0;
      document.getElementById('kpi-outreach').textContent = data.metrics.outreach_dispatched || 0;
      document.getElementById('kpi-interviews').textContent = data.metrics.interviews_active || 0;
      
      const apprvCount = data.metrics.pending_approvals_count || 0;
      document.getElementById('badge-approvals-count').textContent = apprvCount;
      if (apprvCount > 0) {
        document.getElementById('badge-approvals-count').style.background = 'rgba(245, 158, 11, 0.4)';
        document.getElementById('badge-approvals-count').style.color = '#F59E0B';
      }
    }
  } catch (err) {
    console.error('Failed to load briefing:', err);
  }
}

// 2. Candidate Profile
async function loadCandidateProfile() {
  try {
    const res = await fetch(`${API_BASE}/candidate`);
    currentCandidate = await res.json();
    
    document.getElementById('hdr-candidate-name').textContent = currentCandidate.full_name;
    document.getElementById('hdr-candidate-role').textContent = currentCandidate.current_title;
  } catch (err) {
    console.error('Failed to load candidate:', err);
  }
}

// 3. Pipeline Kanban
async function loadPipeline() {
  try {
    const res = await fetch(`${API_BASE}/pipeline`);
    currentPipeline = await res.json();
    
    const board = document.getElementById('kanban-board');
    board.innerHTML = '';
    
    // Six primary visual stages
    const displayStages = [
      { key: 'DISCOVERED', title: 'Discovered', icon: '📍' },
      { key: 'QUALIFIED', title: 'Qualified', icon: '✅' },
      { key: 'APPLICATION_READY', title: 'Application Ready', icon: '📑' },
      { key: 'OUTREACH', title: 'Outreach Active', icon: '✉️' },
      { key: 'INTERVIEW', title: 'Interview Stage', icon: '🎙️' },
      { key: 'OFFER', title: 'Offer / Closing', icon: '🏆' }
    ];
    
    let totalPipelineCount = 0;
    
    displayStages.forEach(st => {
      const col = document.createElement('div');
      col.className = 'kanban-column';
      
      const jobsInStage = currentPipeline.pipeline[st.key] || [];
      totalPipelineCount += jobsInStage.length;
      
      col.innerHTML = `
        <div class="column-header">
          <div class="column-title">${st.icon} ${st.title}</div>
          <span class="tab-count">${jobsInStage.length}</span>
        </div>
        <div class="column-cards" id="col-${st.key}"></div>
      `;
      
      const cardsContainer = col.querySelector('.column-cards');
      
      if (jobsInStage.length === 0) {
        cardsContainer.innerHTML = `<div style="font-size: 0.78rem; color: var(--text-muted); text-align: center; margin-top: 2rem;">No opportunities in this stage</div>`;
      } else {
        jobsInStage.forEach(job => {
          const card = document.createElement('div');
          card.className = 'job-card';
          card.onclick = () => openMatchInspector(job.id);
          
          card.innerHTML = `
            <div class="job-company">${job.company_name}</div>
            <div class="job-role-title">${job.title}</div>
            <div style="font-size: 0.76rem; color: var(--text-secondary); margin-bottom: 0.4rem;">${job.location}</div>
            <div class="job-meta-row">
              <span class="fit-badge ${job.status === 'DISCOVERED' ? 'fit-mod' : 'fit-strong'}">${job.status}</span>
              <span>${job.seniority ? job.seniority.split('/')[0] : 'Senior'}</span>
            </div>
          `;
          cardsContainer.appendChild(card);
        });
      }
      
      board.appendChild(col);
    });
    
    document.getElementById('badge-pipeline-count').textContent = totalPipelineCount;
  } catch (err) {
    console.error('Failed to load pipeline:', err);
  }
}

// 4. Live Multi-Agent Activity Stream
async function loadActivityStream() {
  try {
    const res = await fetch(`${API_BASE}/agent/activity`);
    const logs = await res.json();
    
    const stream = document.getElementById('activity-stream');
    if (!logs || logs.length === 0) {
      stream.innerHTML = `<div style="color: var(--text-muted); text-align: center; padding: 1.5rem;">No agent activities recorded yet.</div>`;
      return;
    }
    
    stream.innerHTML = logs.map(log => {
      const timeStr = new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      const agentInitials = log.agent_name.split('_').map(w => w[0].toUpperCase()).slice(0, 2).join('');
      
      return `
        <div class="activity-item">
          <div class="agent-avatar-badge">${agentInitials}</div>
          <div class="activity-content">
            <div class="activity-header">
              <span class="activity-agent-name">${formatAgentName(log.agent_name)}</span>
              <span class="activity-time">${timeStr}</span>
            </div>
            <div class="activity-summary">${log.reasoning_summary}</div>
            ${log.evidence ? `<div class="activity-evidence">${escapeHtml(log.evidence.substring(0, 180))}</div>` : ''}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Failed to load activity feed:', err);
  }
}

// 5. Settings & Target Companies
async function loadSettings() {
  try {
    const res = await fetch(`${API_BASE}/settings`);
    const data = await res.json();
    
    // Update autonomy dropdown
    if (data.security_posture) {
      document.getElementById('autonomy-selector').value = data.security_posture.current_autonomy_level;
      document.getElementById('safety-autonomy-mode').textContent = data.security_posture.autonomy_label;
    }
    
    // Render company chips
    if (data.target_companies) {
      const chipsContainer = document.getElementById('company-chips');
      chipsContainer.innerHTML = data.target_companies.map(c => `
        <span style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 6px; background: rgba(255,255,255,0.04); border: 1px solid var(--border-color); color: var(--text-primary);">
          ${c.company_name}
        </span>
      `).join('');
    }
  } catch (err) {
    console.error('Failed to load settings:', err);
  }
}

// 6. Opportunity & Evidence Radar
async function loadOpportunitiesRadar() {
  try {
    const res = await fetch(`${API_BASE}/jobs`);
    currentJobs = await res.json();
    
    const container = document.getElementById('matches-list');
    container.innerHTML = '';
    
    if (currentJobs.length === 0) {
      container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 2rem;">No jobs discovered yet. Run Career Scout Loop.</div>`;
      return;
    }
    
    for (const job of currentJobs) {
      const matchRes = await fetch(`${API_BASE}/jobs/${job.id}`);
      const jobDetail = await matchRes.json();
      const matchReport = jobDetail.match_report;
      
      const card = document.createElement('div');
      card.className = 'job-card';
      card.style.marginBottom = '1.25rem';
      
      let matchAreasHtml = '';
      if (matchReport && matchReport.match_areas) {
        matchAreasHtml = matchReport.match_areas.slice(0, 3).map(m => `
          <div style="font-size: 0.82rem; margin-bottom: 0.4rem; padding-left: 0.75rem; border-left: 2px solid var(--accent-emerald);">
            <div style="font-weight: 600; color: var(--text-primary);">${m.requirement}</div>
            <div style="color: var(--text-secondary); font-size: 0.78rem;">Evidence: ${m.candidate_evidence}</div>
          </div>
        `).join('');
      }
      
      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
          <div>
            <div class="job-company">${job.company_name}</div>
            <h4 style="font-size: 1.1rem; color: var(--text-primary);">${job.title}</h4>
            <div style="font-size: 0.8rem; color: var(--text-secondary);">${job.location} | Seniority: ${job.seniority}</div>
          </div>
          <span class="fit-badge ${matchReport && matchReport.overall_fit_label === 'STRONG_FIT' ? 'fit-strong' : 'fit-mod'}">
            ${matchReport ? matchReport.overall_fit_label : 'EVALUATING'}
          </span>
        </div>
        
        <div style="background: rgba(0,0,0,0.2); padding: 0.85rem; border-radius: 8px; margin-bottom: 0.85rem;">
          <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: var(--accent-gold); margin-bottom: 0.4rem;">
            Verified Evidence Citations:
          </div>
          ${matchAreasHtml || '<div style="color: var(--text-muted); font-size: 0.8rem;">Click to evaluate full evidence breakdown</div>'}
        </div>
        
        <div style="display: flex; gap: 0.6rem;">
          <button class="btn-secondary" onclick="openMatchInspector('${job.id}')">View Full Evidence Breakdown</button>
          <button class="btn-primary" onclick="prepareApplication('${job.id}')">Prepare Application Packet</button>
          <button class="btn-secondary" onclick="prepareInterview('${job.id}')">Prepare Interview Dossier</button>
        </div>
      `;
      
      container.appendChild(card);
    }
  } catch (err) {
    console.error('Failed to load opportunities radar:', err);
  }
}

// 7. Tailored Resumes Hub
async function loadTailoredResumes() {
  try {
    const res = await fetch(`${API_BASE}/jobs`);
    const jobs = await res.json();
    
    const container = document.getElementById('resumes-list');
    container.innerHTML = '';
    
    for (const job of jobs) {
      try {
        const appRes = await fetch(`${API_BASE}/applications/${job.id}`);
        if (appRes.ok) {
          const app = await appRes.json();
          const item = document.createElement('div');
          item.className = 'document-item';
          
          const filename = `Jagannath_${job.company_name.replace(/[^a-zA-Z0-9]/g, '')}_v1.pdf`;
          
          item.innerHTML = `
            <div>
              <div style="font-weight: 700; color: var(--text-primary); font-size: 1rem;">
                📄 Tailored Resume — ${job.company_name}
              </div>
              <div style="font-size: 0.8rem; color: var(--text-secondary);">
                Target Role: ${job.title} | Status: <span style="color: var(--accent-emerald); font-weight: 600;">${app.status}</span>
              </div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
              <button class="btn-secondary" onclick="viewApplicationPacket('${job.id}')">View Cover Letter & Q&A</button>
              <a href="${API_BASE}/documents/download/${filename}" target="_blank" class="btn-primary" style="text-decoration: none;">
                ⬇️ Download PDF Resume
              </a>
            </div>
          `;
          container.appendChild(item);
        }
      } catch (e) {
        // Application not yet generated for this job
      }
    }
    
    if (container.children.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; color: var(--text-muted); padding: 2rem;">
          No tailored resumes generated yet. Run the scout loop or click "Prepare Application Packet" on any qualified job.
        </div>
      `;
    }
  } catch (err) {
    console.error('Failed to load tailored resumes:', err);
  }
}

// 7B. Executive Contacts & Outreach Communications
window._allContacts = [];

async function loadContacts() {
  try {
    const res = await fetch(`${API_BASE}/contacts`);
    const contacts = await res.json();
    window._allContacts = contacts;

    const countBadge = document.getElementById('badge-contacts-count');
    if (countBadge) countBadge.textContent = contacts.length;

    renderContactsGrid(contacts);
  } catch (err) {
    console.error('Failed to load contacts:', err);
  }
}

function filterContacts(query) {
  if (!window._allContacts) return;
  const q = (query || '').toLowerCase().trim();
  if (!q) {
    renderContactsGrid(window._allContacts);
    return;
  }
  const filtered = window._allContacts.filter(c => 
    (c.full_name || '').toLowerCase().includes(q) ||
    (c.company_name || '').toLowerCase().includes(q) ||
    (c.job_title || '').toLowerCase().includes(q) ||
    (c.email || '').toLowerCase().includes(q)
  );
  renderContactsGrid(filtered);
}

function copyToClipboard(text, btnElement) {
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    if (btnElement) {
      const orig = btnElement.innerHTML;
      btnElement.innerHTML = '✓ Copied!';
      btnElement.style.borderColor = 'var(--accent-emerald)';
      setTimeout(() => {
        btnElement.innerHTML = orig;
        btnElement.style.borderColor = '';
      }, 2000);
    }
  }).catch(() => {
    prompt('Copy text:', text);
  });
}

function renderContactsGrid(contacts) {
  const grid = document.getElementById('contacts-grid');
  if (!grid) return;
  grid.innerHTML = '';

  if (!contacts || contacts.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 3rem; background: rgba(0,0,0,0.2); border-radius: 12px; border: 1px dashed var(--border-color);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
        <div style="font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">No contacts discovered yet</div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">Run the Career Scout Loop to automatically identify verified hiring managers and talent leaders.</div>
      </div>
    `;
    return;
  }

  contacts.forEach(c => {
    const card = document.createElement('div');
    card.style.cssText = `
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    `;

    const categoryColors = {
      'hiring_manager': { bg: 'rgba(245, 158, 11, 0.15)', text: '#F59E0B', label: 'Hiring Manager' },
      'recruiter': { bg: 'rgba(59, 130, 246, 0.15)', text: '#3B82F6', label: 'Talent Acquisition' },
      'department_leader': { bg: 'rgba(16, 185, 129, 0.15)', text: '#10B981', label: 'Department Head' },
      'referral': { bg: 'rgba(168, 85, 247, 0.15)', text: '#A855F7', label: 'Referral Contact' }
    };
    const cat = categoryColors[c.role_category] || { bg: 'rgba(255,255,255,0.1)', text: 'var(--text-secondary)', label: c.role_category || 'Contact' };

    const initials = (c.full_name || 'C').split(' ').filter(p => p).slice(0, 2).map(p => p[0]).join('').toUpperCase();

    let emailHtml = '';
    if (c.email) {
      emailHtml = `
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.6rem 0.85rem; gap: 0.5rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; overflow: hidden;">
            <span style="font-size: 0.95rem;">📧</span>
            <span style="font-family: monospace; font-size: 0.82rem; color: var(--accent-gold); word-break: break-all;">${escapeHtml(c.email)}</span>
          </div>
          <div style="display: flex; gap: 0.35rem; flex-shrink: 0;">
            <button class="btn-secondary" style="padding: 0.25rem 0.55rem; font-size: 0.72rem;" onclick="copyToClipboard('${escapeHtml(c.email)}', this)">📋 Copy</button>
            <a href="mailto:${escapeHtml(c.email)}?subject=${encodeURIComponent(c.outreach_subject || 'V. Jagannath — Executive Career Profile')}" class="btn-primary" style="padding: 0.25rem 0.55rem; font-size: 0.72rem; text-decoration: none; display: inline-flex; align-items: center;">✉️ Email</a>
          </div>
        </div>
      `;
    } else {
      emailHtml = `
        <div style="display: flex; align-items: center; gap: 0.5rem; background: rgba(255,255,255,0.02); border: 1px dashed var(--border-color); border-radius: 8px; padding: 0.55rem 0.85rem; font-size: 0.76rem; color: var(--text-muted);">
          <span>ℹ️</span> Direct corporate email unindexed; mapped to verified LinkedIn InMail channel.
        </div>
      `;
    }

    let linkedinHtml = '';
    if (c.linkedin_url) {
      linkedinHtml = `
        <a href="${escapeHtml(c.linkedin_url)}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.45rem 0.85rem; border-radius: 6px; background: rgba(10, 102, 194, 0.15); border: 1px solid rgba(10, 102, 194, 0.35); color: #0A66C2; font-size: 0.78rem; font-weight: 600; text-decoration: none;">
          <svg style="width: 13px; height: 13px; fill: currentColor;" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
          Open LinkedIn Profile ↗
        </a>
      `;
    }

    let outreachPreviewHtml = '';
    if (c.outreach_message_body) {
      outreachPreviewHtml = `
        <div style="border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: 0.25rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <div style="font-size: 0.76rem; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 0.35rem;">
              <span>📝</span> Prepared Outbound Pitch
              <span class="status-pill" style="font-size: 0.65rem; padding: 0.15rem 0.45rem;">${c.outreach_status || 'STAGED'}</span>
            </div>
            <button class="btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="copyToClipboard(decodeURIComponent('${encodeURIComponent(c.outreach_message_body)}'), this)">📋 Copy Pitch</button>
          </div>
          <div style="font-size: 0.74rem; color: var(--accent-gold); font-weight: 600; margin-bottom: 0.35rem; line-height: 1.3;">
            Subject: ${escapeHtml(c.outreach_subject || 'Executive Introduction — V. Jagannath')}
          </div>
          <details style="font-size: 0.76rem; color: var(--text-secondary); background: rgba(0,0,0,0.3); border-radius: 6px; padding: 0.5rem 0.75rem; border: 1px solid rgba(255,255,255,0.05);">
            <summary style="cursor: pointer; color: var(--accent-blue); font-weight: 600; font-size: 0.72rem; user-select: none;">
              Show Tailored Message (${(c.outreach_channel || 'EMAIL')})
            </summary>
            <div style="margin-top: 0.5rem; white-space: pre-wrap; font-family: monospace; font-size: 0.73rem; line-height: 1.5; color: var(--text-secondary); max-height: 200px; overflow-y: auto; padding-right: 0.4rem;">
${escapeHtml(c.outreach_message_body)}
            </div>
          </details>
        </div>
      `;
    }

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.75rem;">
        <div style="display: flex; gap: 0.75rem; align-items: center;">
          <div style="width: 42px; height: 42px; border-radius: 10px; background: linear-gradient(135deg, rgba(212,175,55,0.25), rgba(59,130,246,0.25)); border: 1px solid var(--accent-gold); display: flex; align-items: center; justify-content: center; font-weight: 700; color: var(--accent-gold); font-size: 0.95rem; flex-shrink: 0;">
            ${initials}
          </div>
          <div>
            <h4 style="font-size: 1rem; color: var(--text-primary); margin: 0; font-weight: 700;">${escapeHtml(c.full_name)}</h4>
            <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.15rem; line-height: 1.3;">${escapeHtml(c.job_title)}</div>
          </div>
        </div>
        <span style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; padding: 0.2rem 0.5rem; border-radius: 20px; background: ${cat.bg}; color: ${cat.text}; flex-shrink: 0;">
          ${cat.label}
        </span>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); border-radius: 6px; padding: 0.45rem 0.75rem; font-size: 0.76rem;">
        <span style="font-weight: 700; color: var(--accent-gold);">${escapeHtml(c.company_name)}</span>
        <span style="color: var(--text-muted); font-size: 0.72rem;">📍 Dubai / DIFC Presence</span>
      </div>

      ${emailHtml}

      <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
        ${linkedinHtml}
        <span style="font-size: 0.7rem; color: var(--accent-emerald); font-weight: 600; display: inline-flex; align-items: center; gap: 0.25rem;">
          ✓ ${c.confidence_level || 'VERIFIED'}
        </span>
      </div>

      ${outreachPreviewHtml}
    `;

    grid.appendChild(card);
  });
}


// 8. Career Brain Fact Graph
async function loadCareerBrain() {
  try {
    const res = await fetch(`${API_BASE}/career-brain`);
    const data = await res.json();
    
    const grid = document.getElementById('facts-grid');
    grid.innerHTML = '';
    
    if (data.verified_facts) {
      data.verified_facts.forEach(f => {
        const card = document.createElement('div');
        card.className = 'fact-card';
        
        card.innerHTML = `
          <span class="fact-category-tag tag-${f.category}">${f.category}</span>
          <div class="fact-text">${f.fact_text}</div>
          <div class="fact-provenance">
            <span class="verified-stamp">✓ Verified Ground Truth</span>
            <span>Source: ${f.source}</span>
          </div>
        `;
        grid.appendChild(card);
      });
    }
  } catch (err) {
    console.error('Failed to load Career Brain:', err);
  }
}

// 9. Interview Intelligence
async function loadInterviews() {
  try {
    const res = await fetch(`${API_BASE}/interviews`);
    const interviews = await res.json();
    
    const container = document.getElementById('interviews-list');
    container.innerHTML = '';
    
    if (interviews.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; color: var(--text-muted); padding: 2rem;">
          No interview records scheduled. You can generate an interview dossier for any target opportunity in the Opportunity Radar.
        </div>
      `;
      return;
    }
    
    interviews.forEach(inv => {
      const card = document.createElement('div');
      card.className = 'job-card';
      card.style.marginBottom = '1rem';
      
      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <div>
            <div class="job-company">${inv.company_name}</div>
            <h4 style="color: var(--text-primary); font-size: 1.05rem;">${inv.role_title}</h4>
            <div style="font-size: 0.8rem; color: var(--text-secondary);">Stage: ${inv.interview_stage} | Status: ${inv.status}</div>
          </div>
          <span class="status-pill">${inv.status}</span>
        </div>
        <div style="margin-top: 0.75rem;">
          <button class="btn-primary" onclick="openInterviewDossier('${inv.id}')">View STAR Stories & Briefing</button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to load interviews:', err);
  }
}

// 10. Approvals Queue (Human Escalation)
async function loadApprovals() {
  try {
    const res = await fetch(`${API_BASE}/approvals`);
    currentApprovals = await res.json();
    
    const container = document.getElementById('approvals-list');
    container.innerHTML = '';
    
    if (currentApprovals.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; color: var(--text-muted); padding: 2rem;">
          ✅ No pending exceptions. The autonomous agent is handling routine operations without requiring your intervention.
        </div>
      `;
      return;
    }
    
    currentApprovals.forEach(apprv => {
      const card = document.createElement('div');
      card.className = 'job-card';
      card.style.borderColor = 'rgba(245, 158, 11, 0.4)';
      card.style.marginBottom = '1rem';
      
      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
          <div>
            <span class="status-pill" style="background: rgba(245, 158, 11, 0.15); color: var(--accent-gold); border-color: rgba(245, 158, 11, 0.3);">
              ${apprv.action_type}
            </span>
            <h4 style="color: var(--text-primary); font-size: 1.1rem; margin-top: 0.4rem;">${apprv.title}</h4>
            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.25rem;">${apprv.description}</div>
          </div>
        </div>
        ${apprv.payload ? `<div style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 8px; font-size: 0.8rem; color: var(--text-muted); margin: 0.75rem 0; word-break: break-word;">${escapeHtml(apprv.payload)}</div>` : ''}
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn-primary" onclick="resolveApproval('${apprv.id}', 'APPROVE')">✓ Authorize Action</button>
          <button class="btn-secondary" onclick="resolveApproval('${apprv.id}', 'REJECT')">✕ Decline</button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to load approvals:', err);
  }
}

// Action Handlers
async function triggerAutonomousLoop() {
  const btn = document.getElementById('btn-run-cycle');
  const icon = document.getElementById('cycle-btn-icon');
  const text = document.getElementById('cycle-btn-text');
  
  btn.disabled = true;
  icon.className = 'spinner';
  icon.textContent = '';
  text.textContent = 'Agent Team Operating...';
  
  try {
    const res = await fetch(`${API_BASE}/agent/cycle/run`, { method: 'POST' });
    const data = await res.json();
    
    await refreshTelemetry();
    alert(`Autonomous Scout Loop Completed!\n• Evaluated: ${data.jobs_evaluated} jobs\n• Qualified: ${data.jobs_qualified}\n• Applications Prepared: ${data.applications_prepared}\n• Outreaches Dispatched: ${data.outreaches_dispatched}`);
  } catch (err) {
    alert('Failed to run autonomous cycle: ' + err.message);
  } finally {
    btn.disabled = false;
    icon.className = '';
    icon.textContent = '⚡';
    text.textContent = 'Run Career Scout Loop';
  }
}

async function updateAutonomyLevel(level) {
  try {
    await fetch(`${API_BASE}/settings/autonomy`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ autonomy_level: parseInt(level) })
    });
    await loadSettings();
  } catch (err) {
    console.error('Failed to update autonomy:', err);
  }
}

async function resolveApproval(approvalId, decision) {
  try {
    await fetch(`${API_BASE}/approvals/${approvalId}/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ decision })
    });
    await loadApprovals();
    await loadBriefing();
  } catch (err) {
    alert('Failed to resolve approval: ' + err.message);
  }
}

async function prepareApplication(jobId) {
  try {
    const res = await fetch(`${API_BASE}/applications/prepare?job_id=${jobId}`, { method: 'POST' });
    const packet = await res.json();
    alert(`Application packet ready for ${packet.company_name}!\nTailored PDF Resume: ${packet.resume_version}.pdf`);
    await loadPipeline();
    await loadBriefing();
  } catch (err) {
    alert('Failed to prepare application: ' + err.message);
  }
}

async function prepareInterview(jobId) {
  try {
    const res = await fetch(`${API_BASE}/interviews/dossier?job_id=${jobId}`, { method: 'POST' });
    const inv = await res.json();
    alert(`Interview dossier created for ${inv.company_name}!\nSTAR stories and domain questions prepared.`);
    await loadInterviews();
    await loadBriefing();
  } catch (err) {
    alert('Failed to prepare interview: ' + err.message);
  }
}

// Modal Handlers
async function openMatchInspector(jobId) {
  try {
    const res = await fetch(`${API_BASE}/jobs/${jobId}`);
    const data = await res.json();
    const job = data.job;
    const match = data.match_report;
    
    document.getElementById('modal-match-title').textContent = job.title;
    document.getElementById('modal-match-company').textContent = `${job.company_name} • ${job.location}`;
    
    const body = document.getElementById('modal-match-body');
    
    let matchHtml = '';
    if (match && match.match_areas) {
      matchHtml = match.match_areas.map(m => `
        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); border-left: 3px solid var(--accent-emerald); padding: 0.85rem; border-radius: 8px; margin-bottom: 0.75rem;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
            <span style="font-weight: 700; color: var(--text-primary); font-size: 0.9rem;">${m.requirement}</span>
            <span class="fit-badge fit-strong">${m.status}</span>
          </div>
          <div style="font-size: 0.84rem; color: var(--accent-gold); margin-bottom: 0.25rem;">Candidate Evidence: ${m.candidate_evidence}</div>
          <div style="font-size: 0.72rem; color: var(--text-muted);">Source Provenance: ${m.provenance}</div>
        </div>
      `).join('');
    }
    
    let gapsHtml = '';
    if (match && match.gaps && match.gaps.length > 0) {
      gapsHtml = match.gaps.map(g => `
        <div style="background: rgba(245,158,11,0.05); border: 1px solid rgba(245,158,11,0.2); border-left: 3px solid var(--accent-gold); padding: 0.85rem; border-radius: 8px; margin-bottom: 0.75rem;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
            <span style="font-weight: 700; color: var(--text-primary); font-size: 0.9rem;">${g.unmet_requirement}</span>
            <span class="fit-badge fit-mod">${g.status}</span>
          </div>
          <div style="font-size: 0.82rem; color: var(--text-secondary);">${g.recommendation}</div>
        </div>
      `).join('');
    }
    
    const contacts = data.contacts || [];
    let contactsHtml = '';
    if (contacts.length > 0) {
      contactsHtml = `
        <div style="margin-bottom: 1.25rem; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem;">
          <h4 style="font-size: 0.95rem; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.4rem;">
            <span>👥</span> Key Decision Makers for this Opportunity
          </h4>
          <div style="display: flex; flex-direction: column; gap: 0.6rem;">
            ${contacts.map(c => `
              <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 0.6rem 0.85rem; border-radius: 6px; gap: 0.5rem; flex-wrap: wrap;">
                <div>
                  <div style="font-weight: 700; color: var(--text-primary); font-size: 0.88rem;">${escapeHtml(c.full_name)}</div>
                  <div style="font-size: 0.76rem; color: var(--text-secondary);">${escapeHtml(c.job_title)}</div>
                  ${c.email ? `<div style="font-size: 0.74rem; color: var(--accent-gold); font-family: monospace; margin-top: 0.2rem;">📧 ${escapeHtml(c.email)}</div>` : ''}
                </div>
                <div style="display: flex; gap: 0.35rem; align-items: center;">
                  ${c.email ? `<button class="btn-secondary" style="padding: 0.25rem 0.55rem; font-size: 0.72rem;" onclick="copyToClipboard('${escapeHtml(c.email)}', this)">📋 Copy Email</button>` : ''}
                  ${c.email ? `<a href="mailto:${escapeHtml(c.email)}" class="btn-primary" style="padding: 0.25rem 0.55rem; font-size: 0.72rem; text-decoration: none;">✉️ Email</a>` : ''}
                  ${c.linkedin_url ? `<a href="${escapeHtml(c.linkedin_url)}" target="_blank" class="btn-primary" style="padding: 0.25rem 0.55rem; font-size: 0.72rem; text-decoration: none; background: rgba(10,102,194,0.3); border-color: #0A66C2;">LinkedIn ↗</a>` : ''}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }
    
    body.innerHTML = `
      ${contactsHtml}

      <div style="margin-bottom: 1.25rem;">
        <h4 style="font-size: 0.95rem; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.5rem;">Verified Match Evidence</h4>
        ${matchHtml || '<div style="color: var(--text-muted);">No match areas evaluated yet.</div>'}
      </div>
      
      ${gapsHtml ? `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 0.95rem; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.5rem;">Requirement Nuances & Gaps</h4>
          ${gapsHtml}
        </div>
      ` : ''}
      
      <div style="margin-top: 1.5rem; display: flex; gap: 0.6rem;">
        <button class="btn-primary" onclick="prepareApplication('${job.id}')">Prepare Application Packet</button>
        <button class="btn-secondary" onclick="closeModal('modal-match')">Close</button>
      </div>
    `;
    
    document.getElementById('modal-match').classList.add('active');
  } catch (err) {
    alert('Failed to inspect opportunity: ' + err.message);
  }
}

async function viewApplicationPacket(jobId) {
  try {
    const res = await fetch(`${API_BASE}/applications/${jobId}`);
    const app = await res.json();
    
    document.getElementById('modal-app-title').textContent = `Application Dossier — ${app.company_name}`;
    document.getElementById('modal-app-company').textContent = app.role_title;
    
    const body = document.getElementById('modal-app-body');
    body.innerHTML = `
      <div style="margin-bottom: 1.5rem;">
        <h4 style="font-size: 0.95rem; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.5rem;">Tailored Executive Cover Letter</h4>
        <div style="white-space: pre-wrap; font-size: 0.85rem; color: var(--text-secondary); background: rgba(0,0,0,0.3); padding: 1.25rem; border-radius: 8px; font-family: monospace; line-height: 1.6;">
${escapeHtml(app.cover_letter)}
        </div>
      </div>
      
      <div style="margin-top: 1.5rem; display: flex; gap: 0.6rem;">
        <button class="btn-secondary" onclick="closeModal('modal-app')">Close</button>
      </div>
    `;
    
    document.getElementById('modal-app').classList.add('active');
  } catch (err) {
    alert('Failed to view application: ' + err.message);
  }
}

async function openInterviewDossier(interviewId) {
  try {
    const res = await fetch(`${API_BASE}/interviews`);
    const list = await res.json();
    const inv = list.find(i => i.id === interviewId);
    if (!inv) return;
    
    document.getElementById('modal-interview-title').textContent = `Interview Dossier: ${inv.company_name}`;
    document.getElementById('modal-interview-company').textContent = inv.role_title;
    
    const prep = inv.prep_dossier || {};
    const body = document.getElementById('modal-interview-body');
    
    let starHtml = '';
    if (prep.star_stories) {
      starHtml = prep.star_stories.map(s => `
        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem;">
          <div style="font-weight: 700; color: var(--accent-gold); font-size: 0.95rem; margin-bottom: 0.35rem;">${s.title}</div>
          <div style="font-size: 0.83rem; color: var(--text-secondary); margin-bottom: 0.25rem;"><b>Situation:</b> ${s.situation}</div>
          <div style="font-size: 0.83rem; color: var(--text-secondary); margin-bottom: 0.25rem;"><b>Task:</b> ${s.task}</div>
          <div style="font-size: 0.83rem; color: var(--text-secondary); margin-bottom: 0.25rem;"><b>Action:</b> ${s.action}</div>
          <div style="font-size: 0.83rem; color: var(--accent-emerald); font-weight: 600;"><b>Result:</b> ${s.result}</div>
        </div>
      `).join('');
    }
    
    let qHtml = '';
    if (prep.technical_domain_questions) {
      qHtml = prep.technical_domain_questions.map(q => `
        <li style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 0.35rem;">${q}</li>
      `).join('');
    }
    
    body.innerHTML = `
      <div style="margin-bottom: 1.5rem;">
        <h4 style="font-size: 0.95rem; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.5rem;">STAR Career Stories Mapped to Verified Facts</h4>
        ${starHtml}
      </div>
      
      <div style="margin-bottom: 1.5rem;">
        <h4 style="font-size: 0.95rem; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 0.5rem;">Anticipated Domain Questions</h4>
        <ul style="padding-left: 1.25rem;">${qHtml}</ul>
      </div>
      
      <div style="margin-top: 1.5rem; display: flex; gap: 0.6rem;">
        <button class="btn-secondary" onclick="closeModal('modal-interview')">Close</button>
      </div>
    `;
    
    document.getElementById('modal-interview').classList.add('active');
  } catch (err) {
    alert('Failed to view interview: ' + err.message);
  }
}

function closeModal(modalId, evt) {
  if (evt && evt.target.classList.contains('modal-box')) return;
  document.getElementById(modalId).classList.remove('active');
}

function formatAgentName(name) {
  return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// 11. Live Integrations Management
async function loadIntegrationsStatus() {
  try {
    const res = await fetch(`${API_BASE}/integrations`);
    const data = await res.json();

    const gmailConnected = data.gmail && data.gmail.status === 'CONNECTED';
    const linkedinConnected = data.linkedin && data.linkedin.status === 'CONNECTED';

    const statusBadge = document.getElementById('badge-integrations-status');
    const gmailPill = document.getElementById('gmail-status-pill');
    const linkedinPill = document.getElementById('linkedin-status-pill');
    const liveDispatchPill = document.getElementById('live-dispatch-pill');

    if (gmailPill) {
      if (gmailConnected) {
        gmailPill.textContent = 'CONNECTED';
        gmailPill.style.background = 'rgba(16, 185, 129, 0.15)';
        gmailPill.style.color = 'var(--accent-emerald)';
      } else {
        gmailPill.textContent = 'DISCONNECTED';
        gmailPill.style.background = 'rgba(244, 63, 94, 0.15)';
        gmailPill.style.color = '#F43F5E';
      }
    }

    if (linkedinPill) {
      if (linkedinConnected) {
        linkedinPill.textContent = 'CONNECTED';
        linkedinPill.style.background = 'rgba(16, 185, 129, 0.15)';
        linkedinPill.style.color = 'var(--accent-emerald)';
      } else {
        linkedinPill.textContent = 'DISCONNECTED';
        linkedinPill.style.background = 'rgba(244, 63, 94, 0.15)';
        linkedinPill.style.color = '#F43F5E';
      }
    }

    if (statusBadge) {
      if (gmailConnected || linkedinConnected) {
        statusBadge.textContent = 'ONLINE';
        statusBadge.style.background = 'rgba(16, 185, 129, 0.2)';
        statusBadge.style.color = 'var(--accent-emerald)';
      } else {
        statusBadge.textContent = 'OFFLINE';
        statusBadge.style.background = 'rgba(244, 63, 94, 0.2)';
        statusBadge.style.color = '#F43F5E';
      }
    }

    if (liveDispatchPill) {
      if (gmailConnected || linkedinConnected) {
        liveDispatchPill.innerHTML = '🟢 Autonomous Live Dispatch Active';
        liveDispatchPill.style.background = 'rgba(16, 185, 129, 0.15)';
        liveDispatchPill.style.color = 'var(--accent-emerald)';
        liveDispatchPill.style.borderColor = 'rgba(16, 185, 129, 0.3)';
      } else {
        liveDispatchPill.innerHTML = '⚠️ Staging Mode (Connect Gmail / LinkedIn to Dispatch Live)';
        liveDispatchPill.style.background = 'rgba(244, 63, 94, 0.15)';
        liveDispatchPill.style.color = '#F43F5E';
        liveDispatchPill.style.borderColor = 'rgba(244, 63, 94, 0.3)';
      }
    }
  } catch (err) {
    console.error('Failed to load integrations status:', err);
  }
}

async function connectGmailAccount() {
  const email = document.getElementById('input-gmail-addr').value.trim();
  const pwd = document.getElementById('input-gmail-pwd').value.trim();

  if (!email || !pwd) {
    alert('Please enter your candidate email address and 16-character Google App Password.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/integrations/gmail`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, app_password: pwd, live_dispatch: true })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Connection failed');
    }

    alert('Success: ' + data.message);
    await loadIntegrationsStatus();
    await refreshTelemetry();
  } catch (err) {
    alert('Gmail Connection Error: ' + err.message);
  }
}

async function connectLinkedInAccount() {
  const url = document.getElementById('input-linkedin-url').value.trim();
  const cookie = document.getElementById('input-linkedin-cookie').value.trim();

  if (!url || !cookie) {
    alert('Please enter your LinkedIn profile URL and session cookie (li_at).');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/integrations/linkedin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile_url: url, session_cookie: cookie, live_dispatch: true })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Connection failed');
    }

    alert('Success: ' + data.message);
    await loadIntegrationsStatus();
    await refreshTelemetry();
  } catch (err) {
    alert('LinkedIn Connection Error: ' + err.message);
  }
}

async function syncLiveInbox() {
  try {
    const res = await fetch(`${API_BASE}/integrations/sync-inbox`, { method: 'POST' });
    const data = await res.json();
    if (data.status === 'DISCONNECTED') {
      alert(data.message);
    } else {
      alert(`Inbox sync complete! Processed ${data.emails_processed} new incoming messages.`);
      await refreshTelemetry();
    }
  } catch (err) {
    alert('Failed to sync inbox: ' + err.message);
  }
}

async function sendTestEmail() {
  const recipient = document.getElementById('input-test-recipient').value.trim();
  if (!recipient) {
    alert('Please enter a recipient email address to send a test transmission.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/integrations/test-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipient })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Failed to dispatch test email');
    }

    alert('Test Email Dispatched Successfully!\n' + data.detail);
  } catch (err) {
    alert('Test Email Error: ' + err.message);
  }
}
