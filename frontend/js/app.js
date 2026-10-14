/**
 * Vanganur Jagannath — Real Estate & Asset Management Executive Hub
 * Ultra-Simple, High-Performance Frontend Client
 */

const state = {
  candidate: null,
  jobs: [],
  contacts: [],
  email_settings: {},
  stats: {},
  currentTab: 'jobs',
  currentSector: 'ALL',
  searchQuery: '',
  selectedContactIds: new Set(),
  activeEmailContact: null
};

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
  loadCatalogData();
});

async function loadCatalogData() {
  try {
    const res = await fetch('/api/simple/catalog');
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    const data = await res.json();

    state.candidate = data.candidate;
    state.jobs = data.jobs || [];
    state.contacts = data.contacts || [];
    state.email_settings = data.email_settings || {};
    state.stats = data.stats || {};

    updateStatsDisplay();
    updateEmailStatusBadge();
    renderSectorCounts();
    renderFilteredViews();
  } catch (err) {
    console.error('Failed to load catalog data:', err);
    showToast('Failed to load catalog data. Is backend server running?', 'error');
  }
}

function updateStatsDisplay() {
  document.getElementById('kpi-jobs-count').innerText = state.jobs.length;
  document.getElementById('kpi-contacts-count').innerText = state.contacts.length;
  document.getElementById('kpi-emails-count').innerText = state.contacts.filter(c => c.email).length;
  
  const sentCount = state.contacts.filter(c => 
    c.outreach_status && (c.outreach_status.includes('SENT') || c.outreach_status.includes('LIVE'))
  ).length;
  
  document.getElementById('kpi-sent-count').innerText = sentCount;
  document.getElementById('badge-jobs-count').innerText = state.jobs.length;
  document.getElementById('badge-contacts-count').innerText = state.contacts.length;
  document.getElementById('count-all').innerText = state.jobs.length;

  if (sentCount > 0) {
    document.getElementById('kpi-sent-sub').innerText = `${sentCount} verified leaders contacted`;
  }
}

function updateEmailStatusBadge() {
  const isConnected = state.email_settings && state.email_settings.status === 'CONNECTED';
  const hasRealPw = state.email_settings && state.email_settings.has_real_password;
  const isSimulated = state.email_settings && state.email_settings.is_simulated;
  const badge = document.getElementById('email-status-badge');
  const text = document.getElementById('email-status-text');
  const dot = document.getElementById('status-dot');

  if (isConnected && hasRealPw && !isSimulated) {
    badge.className = 'email-status-pill connected';
    text.innerText = `Gmail Connected (${state.email_settings.account || 'v.jagannath3@gmail.com'})`;
    dot.style.background = '#10B981';
  } else if (isConnected && isSimulated) {
    badge.className = 'email-status-pill simulated';
    text.innerText = 'Email Dispatch: Sandbox Mode Active';
    dot.style.background = '#8B5CF6';
  } else {
    badge.className = 'email-status-pill disconnected';
    text.innerText = 'Connect Gmail for 1-Click Sending';
    dot.style.background = '#F59E0B';
  }
}

function renderSectorCounts() {
  // Count by sector
  const sectors = ['Investment Banking & PE', 'Prime Developers', 'Sovereign Wealth', 'Global Tech & Retail', 'Consultancies & Agencies'];
  sectors.forEach(sec => {
    const count = state.jobs.filter(j => j.sector === sec).length;
    const btn = document.querySelector(`.sector-pill[data-sector="${sec}"]`);
    if (btn) {
      btn.innerText = `${sec} (${count})`;
    }
  });
}

// Tab Switching
function switchSimpleTab(tabName) {
  state.currentTab = tabName;
  document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-view').forEach(v => {
    v.classList.remove('active');
    v.style.display = 'none';
  });

  if (tabName === 'jobs') {
    document.getElementById('tab-btn-jobs').classList.add('active');
    const view = document.getElementById('view-jobs');
    view.classList.add('active');
    view.style.display = 'block';
  } else if (tabName === 'contacts') {
    document.getElementById('tab-btn-contacts').classList.add('active');
    const view = document.getElementById('view-contacts');
    view.classList.add('active');
    view.style.display = 'block';
  } else if (tabName === 'dossier') {
    document.getElementById('tab-btn-dossier').classList.add('active');
    const view = document.getElementById('view-dossier');
    view.classList.add('active');
    view.style.display = 'block';
  }
}

// Search and Sector Filtering
function handleSearch(val) {
  state.searchQuery = val.trim().toLowerCase();
  const clearBtn = document.getElementById('btn-clear-search');
  if (state.searchQuery) {
    clearBtn.style.display = 'block';
  } else {
    clearBtn.style.display = 'none';
  }
  renderFilteredViews();
}

function clearSearch() {
  document.getElementById('catalog-search').value = '';
  handleSearch('');
}

function filterBySector(sector) {
  state.currentSector = sector;
  document.querySelectorAll('.sector-pill').forEach(b => b.classList.remove('active'));
  const activeBtn = document.querySelector(`.sector-pill[data-sector="${sector}"]`);
  if (activeBtn) activeBtn.classList.add('active');
  renderFilteredViews();
}

function getFilteredData() {
  let filteredJobs = state.jobs;
  let filteredContacts = state.contacts;

  // Filter by sector
  if (state.currentSector !== 'ALL') {
    filteredJobs = filteredJobs.filter(j => j.sector === state.currentSector);
    filteredContacts = filteredContacts.filter(c => c.sector === state.currentSector);
  }

  // Filter by search query
  if (state.searchQuery) {
    const q = state.searchQuery;
    filteredJobs = filteredJobs.filter(j => {
      const matchJob = (j.title || '').toLowerCase().includes(q) ||
                       (j.company_name || '').toLowerCase().includes(q) ||
                       (j.location || '').toLowerCase().includes(q) ||
                       (j.description || '').toLowerCase().includes(q);
      const matchContact = (j.contacts || []).some(c => 
        (c.full_name || '').toLowerCase().includes(q) ||
        (c.job_title || '').toLowerCase().includes(q) ||
        (c.email || '').toLowerCase().includes(q)
      );
      return matchJob || matchContact;
    });

    filteredContacts = filteredContacts.filter(c => 
      (c.full_name || '').toLowerCase().includes(q) ||
      (c.job_title || '').toLowerCase().includes(q) ||
      (c.company_name || '').toLowerCase().includes(q) ||
      (c.email || '').toLowerCase().includes(q) ||
      (c.notes || '').toLowerCase().includes(q)
    );
  }

  return { filteredJobs, filteredContacts };
}

function renderFilteredViews() {
  const { filteredJobs, filteredContacts } = getFilteredData();
  renderJobs(filteredJobs);
  renderContacts(filteredContacts);
}

// Render Jobs View
function renderJobs(jobs) {
  const container = document.getElementById('jobs-cards-container');
  const counter = document.getElementById('jobs-shown-counter');
  counter.innerText = `Showing ${jobs.length} opening${jobs.length === 1 ? '' : 's'}`;

  if (!jobs || jobs.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon">🔍</span>
        <h3>No matching openings found</h3>
        <p>Try clearing your search query or switching sectors.</p>
        <button class="btn-secondary" onclick="clearSearch(); filterBySector('ALL');">Reset Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = jobs.map(j => {
    const contactsHtml = (j.contacts && j.contacts.length > 0) ? `
      <div class="job-decision-makers">
        <div class="dm-header">
          <span class="dm-badge">Verified Decision-Maker${j.contacts.length > 1 ? 's' : ''}</span>
        </div>
        <div class="dm-list">
          ${j.contacts.map(c => `
            <div class="dm-item">
              <div class="dm-avatar">${getInitials(c.full_name)}</div>
              <div class="dm-info">
                <div class="dm-name-row">
                  <strong>${escapeHtml(c.full_name)}</strong>
                  <span class="dm-title">${escapeHtml(c.job_title)}</span>
                </div>
                <div class="dm-contact-links">
                  ${c.email ? `
                    <span class="verified-email-tag" onclick="copyText('${c.email}')" title="Click to copy email">
                      ✉️ ${escapeHtml(c.email)}
                    </span>
                  ` : ''}
                  ${c.linkedin_url ? `
                    <a href="${c.linkedin_url}" target="_blank" class="linkedin-link-tag" title="Open LinkedIn Profile">
                      🔗 LinkedIn Profile
                    </a>
                  ` : ''}
                  ${c.outreach_status && c.outreach_status.includes('SENT') ? `
                    <span class="status-tag sent">✓ Pitch Sent</span>
                  ` : ''}
                </div>
              </div>
              <div class="dm-actions">
                <button class="btn-action-primary" onclick="openEmailModalForContact('${c.id}')" title="Send personalized email pitch">
                  <span>✉️</span> Send Pitch
                </button>
                <button class="btn-action-secondary" onclick="quickGmailContact('${c.id}')" title="1-Click Open in Gmail (Web)" style="color:#ea4335; border-color:rgba(234, 67, 53, 0.35);">
                  <span>✉️</span> Gmail
                </button>
                <button class="btn-action-secondary" onclick="quickLinkedInContact('${c.id}')" title="Copy Tailored LinkedIn Pitch & Open Profile" style="color:#0a66c2; border-color:rgba(10, 102, 194, 0.35);">
                  <span>🔗</span> LinkedIn
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    ` : `
      <div class="job-decision-makers empty-dm">
        <span class="text-muted">Direct company mandate — submit via portal or executive search</span>
      </div>
    `;

    return `
      <div class="job-card">
        <div class="job-card-top">
          <div class="job-card-company-row">
            <span class="job-company-name">${escapeHtml(j.company_name)}</span>
            <span class="job-sector-tag">${escapeHtml(j.sector)}</span>
            <span class="job-match-badge">★ 100% Experience Fit</span>
          </div>
          <h3 class="job-card-title">${escapeHtml(j.title)}</h3>
          <div class="job-card-meta">
            <span>📍 ${escapeHtml(j.location || 'Dubai, UAE')}</span>
            <span>💼 ${escapeHtml(j.seniority || 'Senior Manager / Director')}</span>
          </div>
        </div>

        <div class="job-card-desc">
          ${escapeHtml(j.description)}
        </div>

        ${contactsHtml}

        <div class="job-card-footer">
          <div class="job-fit-reason">
            <span class="fit-check">✓</span> Aligns with Jagannath's 15+ yrs commercial leasing, AED 800M portfolio, and One Za'abeel track record.
          </div>
          <div class="job-card-links">
            ${j.source_url ? `
              <a href="${j.source_url}" target="_blank" class="btn-link-portal">
                <span>🌐</span> Careers Page
              </a>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Render Contacts Table View
function renderContacts(contacts) {
  const tbody = document.getElementById('contacts-table-body');
  
  if (!contacts || contacts.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center" style="padding: 3rem;">
          <div class="empty-state">
            <p>No decision-makers found matching your filter.</p>
          </div>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = contacts.map(c => {
    const isSelected = state.selectedContactIds.has(c.id);
    const hasEmail = Boolean(c.email);
    const hasLinkedIn = Boolean(c.linkedin_url);

    let statusBadge = '<span class="status-badge draft">Draft Ready</span>';
    if (c.outreach_status === 'SENT_LIVE_GMAIL') {
      statusBadge = '<span class="status-badge sent-live">✓ Sent via Gmail</span>';
    } else if (c.outreach_status === 'SENT_SIMULATED') {
      statusBadge = '<span class="status-badge sent-sim">✓ Simulated Sent</span>';
    } else if (c.outreach_status === 'SENT_MANUAL') {
      statusBadge = '<span class="status-badge sent-manual">✓ Sent via Mail App</span>';
    } else if (c.outreach_status === 'SENT') {
      statusBadge = '<span class="status-badge sent-live">✓ Sent</span>';
    }

    return `
      <tr class="${isSelected ? 'selected-row' : ''}">
        <td>
          <input type="checkbox" class="contact-checkbox" data-id="${c.id}" ${isSelected ? 'checked' : ''} onchange="toggleSelectContact('${c.id}', this.checked)">
        </td>
        <td>
          <div class="contact-name-cell">
            <div class="dm-avatar sm">${getInitials(c.full_name)}</div>
            <div>
              <div class="table-contact-name">${escapeHtml(c.full_name)}</div>
              <div class="table-contact-title">${escapeHtml(c.job_title)}</div>
            </div>
          </div>
        </td>
        <td>
          <div class="table-comp-name">${escapeHtml(c.company_name)}</div>
          <span class="sector-subtag">${escapeHtml(c.sector)}</span>
        </td>
        <td>
          ${hasEmail ? `
            <div class="table-email-cell">
              <span class="email-text" onclick="copyText('${c.email}')" title="Click to copy">${escapeHtml(c.email)}</span>
              <button class="btn-tiny" onclick="copyText('${c.email}')" title="Copy Email">📋</button>
            </div>
          ` : '<span class="text-muted">Corporate Portal</span>'}
        </td>
        <td>
          ${hasLinkedIn ? `
            <a href="${c.linkedin_url}" target="_blank" class="table-linkedin-link" title="Open LinkedIn Profile">
              <span>🔗</span> Profile
            </a>
          ` : '<span class="text-muted">—</span>'}
        </td>
        <td>
          ${statusBadge}
          ${c.outreach_sent_at ? `<div class="sent-time-label">${formatDate(c.outreach_sent_at)}</div>` : ''}
        </td>
        <td>
          <div class="table-actions-cell">
            <button class="btn-table-action" onclick="openEmailModalForContact('${c.id}')" title="Preview & Send Email">
              ✉️ Send
            </button>
            <button class="btn-table-action secondary" onclick="quickGmailContact('${c.id}')" title="1-Click Open in Gmail (Web)" style="color:#ea4335;">
              ✉️ Gmail
            </button>
            <button class="btn-table-action secondary" onclick="quickLinkedInContact('${c.id}')" title="Copy Tailored LinkedIn Pitch & Open Profile" style="color:#0a66c2;">
              🔗 In
            </button>
            <button class="btn-table-action secondary" onclick="copyPitchForContact('${c.id}')" title="Copy Tailored Email Pitch">
              📋 Email
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');

  updateBatchActionBar();
}

// Multi-select & Batch Actions
function toggleSelectContact(id, isChecked) {
  if (isChecked) {
    state.selectedContactIds.add(id);
  } else {
    state.selectedContactIds.delete(id);
  }
  updateBatchActionBar();
  // Highlight row
  const row = document.querySelector(`.contact-checkbox[data-id="${id}"]`)?.closest('tr');
  if (row) {
    if (isChecked) row.classList.add('selected-row');
    else row.classList.remove('selected-row');
  }
}

function toggleSelectAll(isChecked) {
  const { filteredContacts } = getFilteredData();
  filteredContacts.forEach(c => {
    if (isChecked) state.selectedContactIds.add(c.id);
    else state.selectedContactIds.delete(c.id);
  });
  renderContacts(filteredContacts);
}

function selectAllVisibleContacts() {
  const { filteredContacts } = getFilteredData();
  filteredContacts.forEach(c => state.selectedContactIds.add(c.id));
  renderContacts(filteredContacts);
  const cb = document.getElementById('select-all-checkbox');
  if (cb) cb.checked = true;
}

function deselectAll() {
  state.selectedContactIds.clear();
  const { filteredContacts } = getFilteredData();
  renderContacts(filteredContacts);
  const cb = document.getElementById('select-all-checkbox');
  if (cb) cb.checked = false;
}

function updateBatchActionBar() {
  const bar = document.getElementById('batch-action-bar');
  const counter = document.getElementById('selected-counter-text');
  const count = state.selectedContactIds.size;

  if (count > 0) {
    bar.style.display = 'flex';
    counter.innerText = `${count} contact${count === 1 ? '' : 's'} selected`;
  } else {
    bar.style.display = 'none';
  }
}

// Batch Send Selected
async function batchSendSelected() {
  const count = state.selectedContactIds.size;
  if (count === 0) {
    showToast('Please select at least one contact to batch send.', 'warning');
    return;
  }

  const confirmMsg = `Are you sure you want to dispatch tailored executive emails to ${count} decision-makers?`;
  if (!confirm(confirmMsg)) return;

  showToast(`Dispatching ${count} emails... Please wait.`, 'info');

  try {
    const res = await fetch('/api/simple/batch-send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contact_ids: Array.from(state.selectedContactIds) })
    });

    const data = await res.json();
    if (data.sent_count > 0) {
      showToast(`Successfully dispatched ${data.sent_count} email${data.sent_count === 1 ? '' : 's'}!`, 'success');
    } else {
      showToast(`Batch completed: ${data.sent_count} sent. Please check email setup or use 1-Click Mail App.`, 'warning');
    }

    deselectAll();
    loadCatalogData();
  } catch (err) {
    console.error('Batch send failed:', err);
    showToast('Batch send failed. Check network or server status.', 'error');
  }
}

// Single Email Modal Handling
function openEmailModalForContact(contactId) {
  const contact = state.contacts.find(c => c.id === contactId);
  if (!contact) {
    showToast('Contact not found.', 'error');
    return;
  }

  state.activeEmailContact = contact;

  document.getElementById('modal-email-title').innerText = `Send Tailored Outreach to ${contact.full_name}`;
  document.getElementById('modal-email-target').innerText = `${contact.job_title} • ${contact.company_name}`;

  // Populate Company Profile Intelligence Box
  const compProf = contact.company_profile;
  const intelBox = document.getElementById('modal-company-intel');
  if (compProf && intelBox) {
    document.getElementById('modal-company-focus-title').innerText = `${contact.company_name} • ${compProf.sector || 'Commercial Real Estate'}`;
    document.getElementById('modal-company-focus-desc').innerHTML = `
      <strong>Signature Assets &amp; Footprint:</strong> ${escapeHtml(compProf.signature_assets || 'Prime UAE Portfolio')}<br>
      <strong>Strategic Focus:</strong> ${escapeHtml(compProf.corporate_focus || 'Asset expansion & commercial leasing')}
    `;
    intelBox.style.display = 'block';
  } else if (intelBox) {
    intelBox.style.display = 'none';
  }

  // Auto-fill Recipient
  document.getElementById('modal-email-recipient').value = contact.email || 'corporate-recruiting@' + contact.company_name.toLowerCase().replace(/[^a-z0-9]/g, '') + '.com';

  // Auto-fill Company-Tailored Email Subject
  const defaultSubject = contact.outreach_subject || `V. Jagannath — Senior Asset Management & Leasing Leadership | ${contact.company_name} Alignment`;
  document.getElementById('modal-email-subject').value = defaultSubject;

  // Auto-fill Company-Tailored Email Body
  const defaultBody = contact.outreach_message_body || generateDefaultPitch(contact);
  document.getElementById('modal-email-body').value = defaultBody;

  // Auto-fill Company-Tailored LinkedIn URL & Note
  const linkedinUrlInput = document.getElementById('modal-linkedin-url');
  if (linkedinUrlInput) {
    linkedinUrlInput.value = contact.linkedin_url || `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(contact.full_name + ' ' + contact.company_name)}`;
  }
  const linkedinBodyInput = document.getElementById('modal-linkedin-body');
  if (linkedinBodyInput) {
    linkedinBodyInput.value = contact.outreach_linkedin_note || generateTailoredLinkedIn(contact);
  }

  // Show/Hide Quick App Password box depending on whether Gmail is live connected
  const hasRealPw = state.email_settings && state.email_settings.has_real_password;
  const pwBox = document.getElementById('modal-app-password-box');
  if (pwBox) {
    pwBox.style.display = hasRealPw ? 'none' : 'block';
  }

  // Reset tab to Email
  switchOutreachTab('email');

  document.getElementById('modal-send-alert').style.display = 'none';
  document.getElementById('email-modal').style.display = 'flex';
}

function switchOutreachTab(tab) {
  const emailSection = document.getElementById('composer-section-email');
  const linkedinSection = document.getElementById('composer-section-linkedin');
  const tabEmail = document.getElementById('tab-btn-email');
  const tabLinkedin = document.getElementById('tab-btn-linkedin');
  const footerEmailLeft = document.getElementById('modal-footer-email-left');
  const footerLinkedinLeft = document.getElementById('modal-footer-linkedin-left');
  const btnSend = document.getElementById('modal-btn-send');
  const btnOpenLinkedin = document.getElementById('modal-btn-open-linkedin');

  if (tab === 'linkedin') {
    if (emailSection) emailSection.style.display = 'none';
    if (linkedinSection) linkedinSection.style.display = 'block';
    if (footerEmailLeft) footerEmailLeft.style.display = 'none';
    if (footerLinkedinLeft) footerLinkedinLeft.style.display = 'flex';
    if (btnSend) btnSend.style.display = 'none';
    if (btnOpenLinkedin) btnOpenLinkedin.style.display = 'inline-flex';

    if (tabEmail) {
      tabEmail.style.background = 'transparent';
      tabEmail.style.borderColor = 'rgba(255, 255, 255, 0.15)';
      tabEmail.style.color = '#94a3b8';
      tabEmail.style.fontWeight = '500';
    }
    if (tabLinkedin) {
      tabLinkedin.style.background = 'rgba(10, 102, 194, 0.2)';
      tabLinkedin.style.borderColor = '#0a66c2';
      tabLinkedin.style.color = '#38bdf8';
      tabLinkedin.style.fontWeight = '600';
    }
  } else {
    if (emailSection) emailSection.style.display = 'block';
    if (linkedinSection) linkedinSection.style.display = 'none';
    if (footerEmailLeft) footerEmailLeft.style.display = 'flex';
    if (footerLinkedinLeft) footerLinkedinLeft.style.display = 'none';
    if (btnSend) btnSend.style.display = 'inline-flex';
    if (btnOpenLinkedin) btnOpenLinkedin.style.display = 'none';

    if (tabEmail) {
      tabEmail.style.background = 'rgba(56, 189, 248, 0.18)';
      tabEmail.style.borderColor = '#38bdf8';
      tabEmail.style.color = '#38bdf8';
      tabEmail.style.fontWeight = '600';
    }
    if (tabLinkedin) {
      tabLinkedin.style.background = 'transparent';
      tabLinkedin.style.borderColor = 'rgba(255, 255, 255, 0.15)';
      tabLinkedin.style.color = '#94a3b8';
      tabLinkedin.style.fontWeight = '500';
    }
  }
}

function copyLinkedInModalNote() {
  const note = document.getElementById('modal-linkedin-body').value.trim();
  copyText(note);
  showToast('Tailored LinkedIn note copied to clipboard!', 'success');
}

function openLinkedInDirect() {
  const url = document.getElementById('modal-linkedin-url').value.trim();
  if (url) window.open(url, '_blank');
}

function closeEmailModal() {
  document.getElementById('email-modal').style.display = 'none';
  state.activeEmailContact = null;
}

// Inline Quick Save Gmail App Password & Send
async function saveQuickPasswordAndSend(force = false) {
  const pwInput = document.getElementById('modal-quick-password');
  let password = pwInput.value.trim();
  const alertBox = document.getElementById('modal-send-alert');
  const saveBtn = document.getElementById('modal-quick-save-btn');

  if (!password) {
    showToast('Please paste your 16-character Google App Password.', 'warning');
    pwInput.focus();
    return;
  }

  // Clean password: strip spaces, dashes, quotes, and make lowercase
  password = password.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();

  saveBtn.disabled = true;
  saveBtn.innerText = force ? 'Saving...' : 'Verifying...';
  alertBox.style.display = 'block';
  alertBox.className = 'send-status-alert info';
  alertBox.innerHTML = '<span class="spinner"></span> Connecting to Google SMTP with your App Password...';

  try {
    const res = await fetch('/api/simple/save-email-settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'v.jagannath3@gmail.com',
        app_password: password,
        is_simulated: false,
        force_save: force
      })
    });

    const data = await res.json();
    if (data.success) {
      showToast('Gmail connected successfully!', 'success');
      if (state.email_settings) {
        state.email_settings.has_real_password = true;
        state.email_settings.status = 'CONNECTED';
        state.email_settings.is_simulated = false;
        updateEmailStatusBadge();
      }
      const pwBox = document.getElementById('modal-app-password-box');
      if (pwBox) pwBox.style.display = 'none';
      pwInput.value = '';
      
      // Immediately send the email for this contact
      await sendViaAutomatedSystem();
    } else {
      alertBox.className = 'send-status-alert error';
      alertBox.innerHTML = `
        <strong>Google Authentication Notice:</strong> ${escapeHtml(data.message)}<br>
        <div style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
          <button type="button" class="btn-primary" onclick="saveQuickPasswordAndSend(true)" style="font-size: 0.8rem; padding: 6px 14px; background: #ea580c; border-color: #ea580c;">
            ⚠️ Save Password &amp; Attempt Send Anyway
          </button>
          <a href="https://myaccount.google.com/apppasswords" target="_blank" style="font-size: 0.8rem; color: #38bdf8; text-decoration: underline;">
            Open Google App Passwords
          </a>
        </div>
      `;
      showToast('Authentication failed. Check App Password or click Save Anyway.', 'error');
    }
  } catch (err) {
    console.error('Failed to save password:', err);
    alertBox.className = 'send-status-alert error';
    alertBox.innerHTML = 'Network error connecting to backend service.';
  } finally {
    saveBtn.disabled = false;
    saveBtn.innerText = 'Save & Send Now';
  }
}

// Send via Automated System (Gmail SMTP / Background)
async function sendViaAutomatedSystem() {
  const contact = state.activeEmailContact;
  if (!contact) return;

  const recipient = document.getElementById('modal-email-recipient').value.trim();
  const subject = document.getElementById('modal-email-subject').value.trim();
  const body = document.getElementById('modal-email-body').value.trim();
  const alertBox = document.getElementById('modal-send-alert');
  const sendBtn = document.getElementById('modal-btn-send');

  if (!recipient || !subject || !body) {
    showToast('Please fill in recipient, subject, and body.', 'warning');
    return;
  }

  sendBtn.disabled = true;
  sendBtn.innerHTML = '<span class="spinner"></span> Sending via Gmail...';
  alertBox.style.display = 'none';

  try {
    const res = await fetch('/api/simple/send-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contact_id: contact.id,
        outreach_id: contact.outreach_id,
        recipient_email: recipient,
        subject: subject,
        message_body: body
      })
    });

    const data = await res.json();

    if (data.success) {
      alertBox.className = 'send-status-alert success';
      alertBox.innerHTML = `<strong>✓ Delivered:</strong> ${escapeHtml(data.message)}`;
      alertBox.style.display = 'block';
      showToast(`Email delivered to ${contact.full_name} via Gmail!`, 'success');

      setTimeout(() => {
        closeEmailModal();
        loadCatalogData();
      }, 1500);
    } else {
      // Need setup or authentication error
      alertBox.className = 'send-status-alert warning';
      const pwBox = document.getElementById('modal-app-password-box');
      if (pwBox) {
        pwBox.style.display = 'block';
        const pwInput = document.getElementById('modal-quick-password');
        if (pwInput) pwInput.focus();
      }

      const gmailDirectUrl = data.gmail_url || getGmailComposeUrl(recipient, subject, body);
      alertBox.innerHTML = `
        <strong>Notice:</strong> ${escapeHtml(data.message)}<br>
        <div style="margin-top: 8px;">
          <a href="${gmailDirectUrl}" target="_blank" class="btn-primary" style="display:inline-flex; padding: 6px 12px; font-size: 0.8rem; text-decoration: none; background:#ea4335; border-color:#ea4335;" onclick="markContactSent('${contact.id}')">
            ✉️ Or Open in Gmail Web Compose Tab
          </a>
        </div>
      `;
      alertBox.style.display = 'block';
      showToast('Enter your Google App Password to enable 1-click automated sending!', 'warning');
    }
  } catch (err) {
    console.error('Error sending email:', err);
    alertBox.className = 'send-status-alert error';
    alertBox.innerHTML = `<strong>Transmission Error:</strong> Failed to reach backend service.`;
    alertBox.style.display = 'block';
  } finally {
    sendBtn.disabled = false;
    sendBtn.innerHTML = '<span>🚀</span> Send Email via Gmail';
  }
}

// 1-Click Gmail Web Compose (Directly opens Gmail in browser under Jagannath's account)
function getGmailComposeUrl(recipient, subject, body) {
  return `https://mail.google.com/mail/?authuser=v.jagannath3@gmail.com&view=cm&fs=1&to=${encodeURIComponent(recipient || '')}&su=${encodeURIComponent(subject || '')}&body=${encodeURIComponent(body || '')}`;
}

function sendViaGmailWeb() {
  const contact = state.activeEmailContact;
  if (!contact) return;

  const recipient = document.getElementById('modal-email-recipient').value.trim();
  const subject = document.getElementById('modal-email-subject').value.trim();
  const body = document.getElementById('modal-email-body').value.trim();

  const gmailUrl = getGmailComposeUrl(recipient, subject, body);
  window.open(gmailUrl, '_blank');

  markContactSent(contact.id);
  showToast('Opened pre-filled draft in Gmail! Pitch marked as sent.', 'success');
  closeEmailModal();
}

function quickGmailContact(contactId) {
  const contact = state.contacts.find(c => c.id === contactId);
  if (!contact) return;

  const recipient = contact.email || '';
  const subject = contact.outreach_subject || `Senior Asset Manager & Commercial Strategy Profile — V. Jagannath`;
  const body = contact.outreach_message_body || generateDefaultPitch(contact);

  const gmailUrl = getGmailComposeUrl(recipient, subject, body);
  window.open(gmailUrl, '_blank');

  markContactSent(contact.id);
  showToast(`Opened Gmail compose draft to ${contact.full_name}!`, 'success');
}

// Fallback aliases ensuring no mailto triggers
function sendViaMailto() {
  sendViaGmailWeb();
}

function quickMailtoContact(contactId) {
  quickGmailContact(contactId);
}

async function markContactSent(contactId) {
  try {
    await fetch('/api/simple/mark-sent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contact_id: contactId })
    });
    loadCatalogData();
  } catch (err) {
    console.error('Failed to mark sent:', err);
  }
}

// Copy Pitch & Open LinkedIn
function openLinkedInAndCopy() {
  const contact = state.activeEmailContact;
  const linkedinInput = document.getElementById('modal-linkedin-body');
  const note = (linkedinInput && linkedinInput.value.trim()) || (contact && contact.outreach_linkedin_note) || (contact && generateTailoredLinkedIn(contact));
  copyText(note);

  const url = (contact && contact.linkedin_url) || (document.getElementById('modal-linkedin-url') && document.getElementById('modal-linkedin-url').value.trim());
  if (url) {
    window.open(url, '_blank');
    showToast('Company-tailored LinkedIn note copied! Opening LinkedIn profile...', 'success');
  } else {
    showToast('Company-tailored LinkedIn note copied to clipboard!', 'success');
  }
}

function quickLinkedInContact(contactId) {
  const contact = state.contacts.find(c => c.id === contactId);
  if (!contact) return;

  const note = contact.outreach_linkedin_note || generateTailoredLinkedIn(contact);
  copyText(note);

  if (contact.linkedin_url) {
    window.open(contact.linkedin_url, '_blank');
    showToast(`Tailored LinkedIn note for ${contact.company_name} copied! Opening ${contact.full_name}'s profile...`, 'success');
  } else {
    showToast(`Tailored LinkedIn note for ${contact.company_name} copied to clipboard!`, 'success');
  }
}

function copyPitchForContact(contactId) {
  const contact = state.contacts.find(c => c.id === contactId);
  if (!contact) return;
  const body = contact.outreach_message_body || generateDefaultPitch(contact);
  copyText(body);
  showToast(`Company-tailored email pitch for ${contact.company_name} copied!`, 'success');
}

function generateTailoredLinkedIn(contact) {
  const firstName = (contact.full_name || 'Leader').split(' ')[0];
  const comp = contact.company_name || 'your company';
  return `Hi ${firstName}, I follow ${comp}'s strategic real estate developments across Dubai and the GCC with great admiration.

With 15+ years directing UAE real estate asset management (AED 800M portfolio, 2,500+ leases, and leasing lead on One Za'abeel under Ithra Dubai / ICD), I specialize in commercial leasing governance, high-value tenant acquisition, and asset yield optimization.

I would welcome connecting to explore synergies with ${comp}'s commercial milestones in Dubai.

Best regards,
V. Jagannath (+971 50 5099065)`;
}

function generateDefaultPitch(contact) {
  const firstName = (contact.full_name || 'Leader').split(' ')[0];
  const comp = contact.company_name || 'your organization';
  return `Dear ${firstName},

I hope this message finds you well.

I am writing to introduce my candidacy for senior real estate asset management and commercial leasing leadership opportunities within ${comp}.

Over the past 15+ years in the UAE, I have managed commercial and mixed-use portfolios exceeding AED 800M in asset value and successfully negotiated over 2,500 retail, commercial, and mixed-use lease agreements. Most recently, I led leasing and asset strategies across prime developments including One Za'abeel and the Deira Enrichment Project under Ithra Dubai LLC (Investment Corporation of Dubai).

Given ${comp}'s premier position and regional footprint, I would welcome the opportunity to connect and explore how my leasing governance, asset enhancement, and tenant relationship track record can support your strategic growth.

My executive ATS resume and full dossier are available for review. I would be pleased to schedule a brief introductory conversation at your convenience.

Best regards,

Vanganur Jagannath
Senior Manager – Real Estate Asset Management & Commercial Leasing
Dubai, United Arab Emirates
Phone: +971 50 5099065
Email: v.jagannath3@gmail.com
LinkedIn: https://www.linkedin.com/in/v-jagannath-re`;
}

// Settings Modal Handling
function openSettingsModal() {
  document.getElementById('settings-email').value = (state.email_settings && state.email_settings.account) || 'v.jagannath3@gmail.com';
  document.getElementById('settings-simulate').checked = Boolean(state.email_settings && state.email_settings.is_simulated);
  document.getElementById('settings-password').value = '';
  document.getElementById('settings-alert').style.display = 'none';
  document.getElementById('settings-modal').style.display = 'flex';
}

function closeSettingsModal() {
  document.getElementById('settings-modal').style.display = 'none';
}

async function saveEmailSettings(force = false) {
  const email = document.getElementById('settings-email').value.trim();
  let password = document.getElementById('settings-password').value.trim();
  const isSimulated = document.getElementById('settings-simulate').checked;
  const alertBox = document.getElementById('settings-alert');

  if (!email) {
    showToast('Please enter an email address.', 'warning');
    return;
  }

  // Clean password
  password = password.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();

  alertBox.style.display = 'block';
  alertBox.className = 'send-status-alert info';
  alertBox.innerHTML = '<span class="spinner"></span> ' + (force ? 'Saving App Password...' : 'Connecting to Google SMTP with your credentials...');

  try {
    const res = await fetch('/api/simple/save-email-settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email,
        app_password: password,
        is_simulated: isSimulated,
        force_save: force
      })
    });

    const data = await res.json();

    if (data.success) {
      alertBox.className = 'send-status-alert success';
      alertBox.innerHTML = `<strong>✓ Connected:</strong> ${escapeHtml(data.message)}`;
      showToast('Email settings updated successfully!', 'success');
      setTimeout(() => {
        closeSettingsModal();
        loadCatalogData();
      }, 1200);
    } else {
      alertBox.className = 'send-status-alert error';
      alertBox.innerHTML = `
        <strong>Authentication Notice:</strong> ${escapeHtml(data.message)}<br>
        <div style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
          <button type="button" class="btn-primary" onclick="saveEmailSettings(true)" style="font-size: 0.8rem; padding: 6px 14px; background: #ea580c; border-color: #ea580c;">
            ⚠️ Save Password Anyway
          </button>
          <a href="https://myaccount.google.com/apppasswords" target="_blank" style="font-size: 0.8rem; color: #38bdf8; text-decoration: underline;">
            Generate New App Password
          </a>
        </div>
      `;
    }
  } catch (err) {
    console.error('Settings save failed:', err);
    alertBox.className = 'send-status-alert error';
    alertBox.innerHTML = 'Failed to connect to backend server.';
  }
}

// Quick Test Email Modal
function openTestEmailModal() {
  document.getElementById('test-email-alert').style.display = 'none';
  document.getElementById('test-email-modal').style.display = 'flex';
}

function closeTestEmailModal() {
  document.getElementById('test-email-modal').style.display = 'none';
}

function openTestInGmailWeb() {
  const recipient = (document.getElementById('test-email-recipient') && document.getElementById('test-email-recipient').value.trim()) || 'v.jagannath3@gmail.com';
  const subject = 'AI7 Career Agent Test Dispatch — V. Jagannath Profile';
  const body = 'This is a test pitch email sent on behalf of Vanganur Jagannath (Real Estate Asset & Operations Executive, AED 800M+ Portfolio).';
  const url = getGmailComposeUrl(recipient, subject, body);
  window.open(url, '_blank');
}

async function runQuickTestSend(force = false) {
  const senderInput = document.getElementById('test-email-sender');
  const senderEmail = (senderInput && senderInput.value.trim()) ? senderInput.value.trim() : 'v.jagannath3@gmail.com';
  const recipient = document.getElementById('test-email-recipient').value.trim();
  const pwInput = document.getElementById('test-email-password');
  let password = pwInput ? pwInput.value.trim() : '';
  const alertBox = document.getElementById('test-email-alert');
  const btn = document.getElementById('btn-run-test-send');

  if (!recipient) {
    showToast('Please enter a recipient email.', 'warning');
    return;
  }

  // If a password was entered in the test box, save it first
  if (password) {
    password = password.replace(/[\s\-\'"]/g, '').toLowerCase();
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Connecting &amp; Saving Password...';
    alertBox.style.display = 'block';
    alertBox.className = 'send-status-alert info';
    alertBox.innerHTML = `<span class="spinner"></span> Authenticating ${escapeHtml(senderEmail)} with Google SMTP...`;

    try {
      const saveRes = await fetch('/api/simple/save-email-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: senderEmail,
          app_password: password,
          is_simulated: false,
          force_save: force
        })
      });
      const saveData = await saveRes.json();
      if (!saveData.success && !force) {
        alertBox.className = 'send-status-alert error';
        alertBox.innerHTML = `
          <strong>Authentication Notice:</strong> ${escapeHtml(saveData.message)}<br>
          <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
            <button type="button" class="btn-primary" onclick="runQuickTestSend(true)" style="font-size: 0.8rem; padding: 6px 12px; background: #ea580c; border-color: #ea580c;">
              ⚠️ Save Password &amp; Attempt Send Anyway
            </button>
            <a href="https://myaccount.google.com/apppasswords" target="_blank" style="font-size: 0.8rem; color: #38bdf8; text-decoration: underline;">
              Open Google App Passwords
            </a>
          </div>
        `;
        btn.disabled = false;
        btn.innerHTML = '<span>🚀</span> Dispatch Test Email';
        return;
      }
      if (state.email_settings) {
        state.email_settings.has_real_password = true;
        state.email_settings.status = 'CONNECTED';
        updateEmailStatusBadge();
      }
    } catch (err) {
      console.error('Password save error in test:', err);
    }
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Dispatching to Google SMTP...';
  alertBox.style.display = 'block';
  alertBox.className = 'send-status-alert info';
  alertBox.innerHTML = '<span class="spinner"></span> Dispatching test email via Gmail SMTP...';

  try {
    const res = await fetch('/api/integrations/test-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recipient: recipient,
        subject: 'AI7 Career Agent Test Dispatch — V. Jagannath Profile',
        body: 'This is a live test transmission from AI7 Career Agent demonstrating automated outbound capability for Vanganur Jagannath.'
      })
    });

    const data = await res.json();

    if (res.ok) {
      alertBox.className = 'send-status-alert success';
      alertBox.innerHTML = `<strong>✓ Success:</strong> Test email delivered directly to ${escapeHtml(recipient)} via Gmail SMTP!`;
      showToast('Test email delivered!', 'success');
      setTimeout(() => closeTestEmailModal(), 1800);
    } else {
      alertBox.className = 'send-status-alert warning';
      const detailMsg = data.detail || 'Failed to dispatch test email.';
      alertBox.innerHTML = `
        <strong>Delivery Notice:</strong> ${escapeHtml(detailMsg)}<br>
        <div style="margin-top: 8px; font-size: 0.82rem; color: #94a3b8;">
          Ensure you are using a 16-character Google App Password from <a href="https://myaccount.google.com/apppasswords" target="_blank" style="color: #38bdf8; text-decoration: underline;">myaccount.google.com/apppasswords</a> with 2-Step Verification ON.
        </div>
      `;
    }
  } catch (err) {
    console.error('Test send error:', err);
    alertBox.className = 'send-status-alert error';
    alertBox.innerHTML = 'Transmission failed. Ensure backend server is reachable.';
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🚀</span> Dispatch Test Email';
  }
}

// Executive Dossier Copy
function copyExecutiveSummary() {
  const bio = `VANGANUR JAGANNATH — EXECUTIVE PROFILE
Role: Senior Asset Manager • Commercial Leasing Director • Portfolio Development Lead
Location: Dubai, United Arab Emirates
Contact: +971 50 5099065 | v.jagannath3@gmail.com | https://www.linkedin.com/in/v-jagannath-re

SUMMARY:
Results-driven UAE Real Estate Leader with 15+ years of strategic commercial asset management, mixed-use development, and retail leasing expertise. Overseen portfolios exceeding AED 800M in asset value, negotiated 2,500+ commercial and retail leases, and spearheaded landmark leasing programs across ICD One Za'abeel and the Deira Enrichment Project under Ithra Dubai LLC. Deep mastery of UAE Civil Transactions Law, Dubai RERA regulations, Ejari governance, and institutional tenant structuring.`;

  copyText(bio);
  showToast('Executive bio copied to clipboard!', 'success');
}

// Helpers
function copyText(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied to clipboard!', 'info');
  }).catch(err => {
    console.error('Clipboard copy error:', err);
  });
}

function copyInputText(inputId) {
  const input = document.getElementById(inputId);
  if (input) {
    copyText(input.value);
  }
}

function getInitials(name) {
  if (!name) return 'DM';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch (e) {
    return dateStr;
  }
}

function handleModalOverlayClick(e, modalId) {
  if (e.target.id === modalId) {
    document.getElementById(modalId).style.display = 'none';
  }
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✓' : type === 'warning' ? '⚠️' : type === 'error' ? '✕' : 'ℹ️'}</span>
    <div>${escapeHtml(message)}</div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Global Keyboard Shortcuts (Escape closes modals)
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeEmailModal();
    closeSettingsModal();
    closeTestEmailModal();
  }
});
