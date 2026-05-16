// Client Outreach App - Main JavaScript

const API_BASE = '/api';

// DOM Elements
const app = document.getElementById('app');
const toast = document.getElementById('toast');

// Initialize
async function init() {
    loadFollowUps();
    loadRecentActivity();
}

// Navigation
toggleMenu = () => {
    document.getElementById('nav-menu').classList.toggle('show');
};

// Modal Functions
function openAddClient() {
    document.getElementById('add-client-modal').classList.add('show');
    document.getElementById('nav-menu').classList.remove('show');
}

function closeModal() {
    document.getElementById('add-client-modal').classList.remove('show');
    document.getElementById('add-client-form').reset();
}

// Form Submission
async function submitClient(event) {
    event.preventDefault();
    const form = event.target;
    const data = Object.fromEntries(new FormData(form));
    
    // Convert empty strings to null
    Object.keys(data).forEach(key => {
        if (data[key] === '') data[key] = null;
    });
    
    try {
        const response = await fetch(`${API_BASE}/clients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast('Client added!', 'success');
            closeModal();
            loadFollowUps();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Failed to add client', 'error');
        }
    } catch (err) {
        showToast('Network error', 'error');
    }
}

// Load Follow-ups
async function loadFollowUps() {
    const container = document.getElementById('follow-ups-list');
    container.innerHTML = '<p class="loading">Loading...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/clients/need-contact/today`);
        const clients = await response.json();
        
        if (clients.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">✅</div>
                    <p>No follow-ups needed today!</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = clients.map(client => `
            <div class="client-card urgent" onclick="viewClient(${client.id})">
                <div class="client-header">
                    <div>
                        <div class="client-name">${client.name}</div>
                        <div class="client-company">${client.company || 'No company'}</div>
                    </div>
                </div>
                <div class="client-meta">
                    <span class="badge badge-tier-${client.tier.toLowerCase().replace(' ', '-')}">${client.tier}</span>
                    <span class="badge badge-status-${client.status}">${client.status}</span>
                    ${client.replacement_score ? `<span class="badge">Score: ${client.replacement_score}</span>` : ''}
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<p class="loading">Failed to load</p>';
    }
}

// Load Recent Activity (placeholder - would need actual endpoint)
async function loadRecentActivity() {
    const container = document.getElementById('recent-activity');
    container.innerHTML = `
        <div class="activity-item">
            <div class="activity-type">Email Sent</div>
            <div class="activity-desc">Welcome email to Emma Wilson</div>
            <div class="activity-time">Today, 10:00 AM</div>
        </div>
        <div class="activity-item">
            <div class="activity-type">Call</div>
            <div class="activity-desc">Discovery call with Sarah Chen</div>
            <div class="activity-time">Yesterday, 2:30 PM</div>
        </div>
        <div class="activity-item">
            <div class="activity-type">Demo Scheduled</div>
            <div class="activity-desc">Demo with Dave Kumar - May 19</div>
            <div class="activity-time">May 14, 4:00 PM</div>
        </div>
    `;
}

// View Client Detail
function viewClient(id) {
    window.location.href = `/clients/${id}`;
}

// View Follow-ups
function viewFollowUps() {
    window.location.href = '/clients?filter=follow-up';
}

// Schedule Email
function scheduleEmail() {
    window.location.href = '/scheduler';
}

// Process Queue
async function processQueue() {
    showToast('Processing email queue...', 'success');
    // This would trigger the email processor
}

// Toast Notifications
function showToast(message, type = '') {
    toast.textContent = message;
    toast.className = 'toast ' + type;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
