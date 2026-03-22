
// SOC Core JS - Handles shared logic across modules
const socket = io();

// Shared State
let socStats = {
    total: 0,
    benign: 0,
    malware: 0,
    apm: 0
};

// UI Elements (Shared)
const statusDot = document.getElementById('connection-status-dot');
const statusText = document.getElementById('connection-status-text');

// Socket Events
socket.on('connect', () => {
    if (statusDot) statusDot.className = 'fas fa-circle text-success';
    if (statusText) statusText.innerText = 'System Online';
    console.log("SOC Core: Connected to Backend");
});

socket.on('disconnect', () => {
    if (statusDot) statusDot.className = 'fas fa-circle text-danger';
    if (statusText) statusText.innerText = 'System Offline';
});

// Update global stats periodically
function refreshStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            socStats = data;
            updateGlobalUI(data);
        })
        .catch(e => console.error("Stats refresh failed", e));
}

function updateGlobalUI(data) {
    // Modules will override this if they need specific global updates
}

setInterval(refreshStats, 3000);

// Utility: Format numbers
function formatNum(n) {
    return n.toLocaleString();
}

// Utility: Create chart config snippet
function getChartTheme() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: '#888888', font: { family: 'Inter' } }
            }
        },
        scales: {
            x: { grid: { color: '#222222' }, ticks: { color: '#888888' } },
            y: { grid: { color: '#222222' }, ticks: { color: '#888888' } }
        }
    };
}

// Global alert handler
socket.on('alert', (data) => {
    // Show a small notification or toast if on any page
    showNotification(data.type, data.severity);
});

function showNotification(type, severity) {
    // Simple notification implementation
    const container = document.getElementById('notification-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `soc-toast ${severity.toLowerCase()}`;
    toast.innerHTML = `
        <div class="toast-icon"><i class="fas fa-shield-virus"></i></div>
        <div class="toast-content">
            <div class="toast-title">${type} Detected</div>
            <div class="toast-msg">Severity: ${severity}</div>
        </div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 5000);
}
