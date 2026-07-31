let entries = [];
let currentFilter = 'all';

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  return res.json();
}

async function loadEntries() {
  const data = await fetchJSON('/api/entries');
  entries = data.entries || [];
  renderStats();
  renderEntries();
}

function renderStats() {
  const stats = { total: entries.length, auto_accepted: 0, flag_yellow: 0, flag_red: 0, rejected: 0 };
  entries.forEach(e => {
    const v = e._vote || 'flag_red';
    if (v in stats) stats[v]++;
  });
  document.getElementById('statsBar').textContent =
    `${stats.total} entries | ${stats.auto_accepted} accepted | ${stats.flag_yellow} to review | ${stats.flag_red} low conf | ${stats.rejected} rejected`;
}

function renderEntries() {
  const list = document.getElementById('entryList');
  let filtered = entries;
  if (currentFilter !== 'all') {
    filtered = filtered.filter(e => (e._vote || 'flag_red') === currentFilter);
  }
  if (filtered.length === 0) {
    list.innerHTML = '<div class="empty-state">No entries match this filter.</div>';
    return;
  }
  list.innerHTML = filtered.map((e, i) => {
    const vote = e._vote || 'flag_red';
    const concept = e.concept || 'Unknown';
    const def = (e.definition || '').substring(0, 120);
    const conf = (e.confidence || 0).toFixed(2);
    const source = e.source_file || '';
    return `<div class="entry-card vote-${vote}" onclick="openDetail(${i})" data-index="${i}">
      <div class="entry-header">
        <span class="entry-concept">${concept}</span>
        <span class="entry-confidence">${conf}</span>
      </div>
      <div class="entry-source">${source}</div>
      <div class="entry-preview">${def}${def.length >= 120 ? '...' : ''}</div>
      <div class="entry-tags">
        ${vote === 'auto_accepted' ? '<span class="tag">auto-accepted</span>' : ''}
        ${vote === 'flag_yellow' ? '<span class="tag" style="background:#fef3c7;color:#92400e;">needs review</span>' : ''}
        ${vote === 'flag_red' ? '<span class="tag" style="background:#fee2e2;color:#991b1b;">low confidence</span>' : ''}
        ${e.strategy ? `<span class="tag source">${e.strategy}</span>` : ''}
      </div>
    </div>`;
  }).join('');
}

function openDetail(index) {
  const e = entries[index];
  const modal = document.getElementById('modal');
  const body = document.getElementById('modalBody');
  const sv = e.sv || {};
  body.innerHTML = `
    <div class="detail-section">
      <div class="detail-label">Concept</div>
      <div class="detail-value"><input id="edit-concept" value="${esc(e.concept)}"></div>
    </div>
    <div class="detail-section">
      <div class="detail-label">Definition</div>
      <div class="detail-value"><textarea id="edit-definition">${esc(e.definition)}</textarea></div>
    </div>
    <div class="detail-section">
      <div class="detail-label">Real-World Scenario</div>
      <div class="detail-value"><textarea id="edit-scenario">${esc(e.real_world_scenario)}</textarea></div>
    </div>
    <div class="detail-section">
      <div class="detail-label">Case Study Cloze</div>
      <div class="detail-value"><textarea id="edit-cloze">${esc(e.case_study_cloze)}</textarea></div>
    </div>
    <div class="detail-section sv-section">
      <div class="detail-label">Swedish — Concept</div>
      <div class="detail-value"><input id="edit-sv-concept" value="${esc(sv.concept || '')}"></div>
    </div>
    <div class="detail-section sv-section">
      <div class="detail-label">Swedish — Definition</div>
      <div class="detail-value"><textarea id="edit-sv-definition">${esc(sv.definition || '')}</textarea></div>
    </div>
    <div class="detail-section sv-section">
      <div class="detail-label">Swedish — Scenario</div>
      <div class="detail-value"><textarea id="edit-sv-scenario">${esc(sv.real_world_scenario || '')}</textarea></div>
    </div>
    <div class="detail-section sv-section">
      <div class="detail-label">Swedish — Cloze</div>
      <div class="detail-value"><textarea id="edit-sv-cloze">${esc(sv.case_study_cloze || '')}</textarea></div>
    </div>
    <div class="detail-section">
      <div class="detail-label">Metadata</div>
      <div class="detail-value" style="font-size:12px;color:#888;">
        Confidence: ${(e.confidence || 0).toFixed(3)} | 
        Strategy: ${e.strategy || 'N/A'} | 
        Page: ${e.page_ref || 'N/A'} | 
        Source: ${e.source_file || 'N/A'}
      </div>
    </div>
    <div class="detail-actions">
      <button class="btn btn-save" onclick="saveEntry(${index})">Save</button>
      <button class="btn btn-approve" onclick="approveEntry(${index})">Approve</button>
      <button class="btn btn-reject" onclick="rejectEntry(${index})">Reject</button>
      <button class="btn btn-cancel" onclick="closeModal()">Close</button>
    </div>`;
  modal.style.display = 'block';
}

function esc(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

async function saveEntry(index) {
  const e = entries[index];
  const data = {
    _id: e._id || e.concept,
    concept: document.getElementById('edit-concept').value,
    definition: document.getElementById('edit-definition').value,
    real_world_scenario: document.getElementById('edit-scenario').value,
    case_study_cloze: document.getElementById('edit-cloze').value,
    sv: {
      concept: document.getElementById('edit-sv-concept').value,
      definition: document.getElementById('edit-sv-definition').value,
      real_world_scenario: document.getElementById('edit-sv-scenario').value,
      case_study_cloze: document.getElementById('edit-sv-cloze').value,
    },
  };
  const result = await fetchJSON('/api/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (result.success) {
    Object.assign(e, data);
    renderEntries();
    renderStats();
    closeModal();
  }
}

async function approveEntry(index) {
  const e = entries[index];
  const result = await fetchJSON('/api/approve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ _id: e._id || e.concept }),
  });
  if (result.success) {
    e._vote = 'auto_accepted';
    renderEntries();
    renderStats();
    closeModal();
  }
}

async function rejectEntry(index) {
  const e = entries[index];
  const result = await fetchJSON('/api/reject', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ _id: e._id || e.concept }),
  });
  if (result.success) {
    e._vote = 'rejected';
    renderEntries();
    renderStats();
    closeModal();
  }
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn[data-filter]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderEntries();
  });
});

document.getElementById('exportBtn').addEventListener('click', async () => {
  const result = await fetchJSON('/api/export-approved', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({}),
  });
  if (result.success) {
    alert(`Exported ${result.count} approved entries to:\n${result.path}`);
  }
});

document.getElementById('closeBtn').addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
  if (e.target === document.getElementById('modal')) closeModal();
});

loadEntries();
