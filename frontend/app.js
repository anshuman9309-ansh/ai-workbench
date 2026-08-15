const API_BASE_URL = 'http://localhost:8000';

const taskSelect = document.getElementById('taskSelect');
const userInput = document.getElementById('userInput');
const runButton = document.getElementById('runButton');
const cancelButton = document.getElementById('cancelButton');
const historyList = document.getElementById('historyList');
const resultPreview = document.getElementById('resultPreview');
const statusPill = document.getElementById('statusPill');

const recentRuns = [];

function setStatus(message, isError = false) {
  statusPill.textContent = message;
  statusPill.style.borderColor = isError
    ? 'rgba(248, 113, 113, 0.5)'
    : 'rgba(124, 157, 255, 0.32)';
  statusPill.style.background = isError
    ? 'rgba(248, 113, 113, 0.08)'
    : 'rgba(124, 157, 255, 0.08)';
  statusPill.style.color = isError ? '#fecaca' : '#dfe7ff';
}

function getTaskLabel(taskValue) {
  const labels = {
    summarize: 'Summarize',
    rewrite: 'Rewrite',
    'key-points': 'Key Points',
    explain: 'Explain',
  };

  return labels[taskValue] || taskValue;
}

function renderHistory() {
  if (recentRuns.length === 0) {
    historyList.innerHTML = '<div class="empty-state">No tasks have been run yet.</div>';
    return;
  }

  historyList.innerHTML = recentRuns
    .map(
      (run) => `
        <article class="history-item">
          <div class="history-item-header">
            <h3>${run.taskType}</h3>
            <span class="token-badge">${run.tokens} tokens</span>
          </div>
          <div>
            <span class="meta-label">Original text</span>
            <blockquote>${escapeHtml(run.originalText)}</blockquote>
          </div>
          <div>
            <span class="meta-label">Response</span>
            <p>${escapeHtml(run.response)}</p>
          </div>
        </article>
      `,
    )
    .join('');
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function resetForm() {
  taskSelect.value = 'summarize';
  userInput.value = '';
  resultPreview.textContent = 'No task has been run yet.';
  setStatus('Ready');
}

async function runTask() {
  const taskValue = taskSelect.value;
  const text = userInput.value.trim();

  if (!text) {
    setStatus('Please enter some text first.', true);
    userInput.focus();
    return;
  }

  const endpoint = `${API_BASE_URL}/${taskValue}`;
  setStatus(`Running ${getTaskLabel(taskValue)}...`);
  runButton.disabled = true;
  cancelButton.disabled = true;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail?.[0]?.msg || payload.detail || 'The request failed.');
    }

    const result = {
      taskType: getTaskLabel(taskValue),
      originalText: text,
      response: payload.content || 'No content returned.',
      tokens: Number(payload.tokens || 0),
    };

    recentRuns.unshift(result);
    if (recentRuns.length > 10) {
      recentRuns.length = 10;
    }

    resultPreview.textContent = result.response;
    renderHistory();
    setStatus(`Completed: ${result.taskType}`);
  } catch (error) {
    resultPreview.textContent = `Error: ${error.message}`;
    setStatus('Task failed', true);
  } finally {
    runButton.disabled = false;
    cancelButton.disabled = false;
  }
}

runButton.addEventListener('click', runTask);
cancelButton.addEventListener('click', () => {
  resetForm();
  userInput.focus();
});

renderHistory();
resetForm();
