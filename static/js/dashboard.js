

// Socket.IO Connection
const socket = io();
const alarmSound = document.getElementById('alarm-sound');

// DOM Elements
const totalPacketsEl = document.getElementById('total-packets');
const benignCountEl = document.getElementById('benign-count');
const malwareCountEl = document.getElementById('malware-count');
const apmEl = document.getElementById('apm');
const kbpsEl = document.getElementById('kbps-value');
const statusEl = document.getElementById('connection-status');
const statusDot = document.getElementById('connection-dot');
const statusSticker = document.getElementById('live-status-sticker');
const bioIcon = document.querySelector('.fa-biohazard');
const healthScoreEl = document.getElementById('health-score');
const cpuValueEl = document.getElementById('cpu-value');
const cpuBarEl = document.getElementById('cpu-bar');
const gpuValueEl = document.getElementById('gpu-value');
const gpuBarEl = document.getElementById('gpu-bar');
const malwareCard = document.getElementById('malware-card');
const tableBody = document.getElementById('alert-table-body');

// Professional Chart Theme
const chartTheme = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { labels: { color: '#9499a6', font: { family: 'Plus Jakarta Sans', size: 10, weight: '600' } } }
    },
    scales: {
        x: { grid: { color: 'rgba(255,255,255,0.05)' }, border: { display: false }, ticks: { color: '#9499a6', font: { size: 10 } } },
        y: { grid: { color: 'rgba(255,255,255,0.05)' }, border: { display: false }, ticks: { color: '#9499a6', font: { size: 10 } } }
    }
};

// Chart Contexts
const trafficCtx = document.getElementById('trafficChart').getContext('2d');
const severityCtx = document.getElementById('severityChart').getContext('2d');
const typeCtx = document.getElementById('typeChart').getContext('2d');
const xaiCtx = document.getElementById('xaiChart').getContext('2d');
const speedCtx = document.getElementById('speedGauge').getContext('2d');

// Initialize Traffic Chart (Gradient)
const trafficGradient = trafficCtx.createLinearGradient(0, 0, 0, 400);
trafficGradient.addColorStop(0, 'rgba(0, 140, 255, 0.3)');
trafficGradient.addColorStop(1, 'rgba(0, 140, 255, 0)');

const trafficChart = new Chart(trafficCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'NETWORK THROUGHPUT',
            borderColor: '#008cff',
            borderWidth: 2,
            backgroundColor: trafficGradient,
            data: [],
            tension: 0.4,
            fill: true,
            pointRadius: 0,
            pointHoverRadius: 5
        }]
    },
    options: chartTheme
});

// Initialize Severity Chart (Horizontal Bar-like)
const severityChart = new Chart(severityCtx, {
    type: 'bar',
    data: {
        labels: ['LOW', 'MEDIUM', 'CRITICAL'],
        datasets: [{
            data: [0, 0, 0],
            backgroundColor: ['#00ff9d', '#ffcc00', '#ff334b'],
            borderRadius: 5,
            barThickness: 20
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { display: false, grid: { display: false } },
            y: { grid: { display: false }, ticks: { color: '#9499a6', font: { weight: '700' } } }
        }
    }
});

// Initialize Type Chart (Doughnut)
const typeChart = new Chart(typeCtx, {
    type: 'doughnut',
    data: {
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: ['#ff334b', '#cc33ff', '#00f2ff', '#00ff9d', '#ffcc00'],
            borderWidth: 0,
            hoverOffset: 10
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: { legend: { position: 'right', labels: { color: '#9499a6', boxWidth: 10 } } }
    }
});

// Speed Gauge Logic
function drawSpeedGauge(value) {
    const max = 2000; // Max 2Mbps for display
    const percent = Math.min(value / max, 1);
    const angle = Math.PI + (percent * Math.PI);
    
    speedCtx.clearRect(0, 0, 160, 100);
    
    // Background Arc
    speedCtx.beginPath();
    speedCtx.arc(80, 85, 65, Math.PI, 2 * Math.PI);
    speedCtx.strokeStyle = 'rgba(255,255,255,0.05)';
    speedCtx.lineWidth = 12;
    speedCtx.stroke();
    
    // Value Arc (Gradient)
    const grad = speedCtx.createLinearGradient(0, 0, 160, 0);
    grad.addColorStop(0, '#008cff');
    grad.addColorStop(1, '#00f2ff');
    
    speedCtx.beginPath();
    speedCtx.arc(80, 85, 65, Math.PI, angle);
    speedCtx.strokeStyle = grad;
    speedCtx.lineWidth = 12;
    speedCtx.lineCap = 'round';
    speedCtx.stroke();
    
    // Needle
    speedCtx.save();
    speedCtx.translate(80, 85);
    speedCtx.rotate(angle);
    speedCtx.beginPath();
    speedCtx.moveTo(0, -5);
    speedCtx.lineTo(60, 0);
    speedCtx.lineTo(0, 5);
    speedCtx.fillStyle = '#fff';
    speedCtx.fill();
    speedCtx.restore();
    
    // Center point
    speedCtx.beginPath();
    speedCtx.arc(80, 85, 5, 0, 2 * Math.PI);
    speedCtx.fillStyle = '#fff';
    speedCtx.fill();
}
drawSpeedGauge(0);
const xaiChart = new Chart(xaiCtx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'FEATURE WEIGHT (%)',
            data: [],
            backgroundColor: 'rgba(0, 140, 255, 0.5)',
            borderColor: '#008cff',
            borderWidth: 1,
            borderRadius: 8
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9499a6' } },
            y: { grid: { display: false }, ticks: { color: '#9499a6' } }
        }
    }
});

// State Management
let totalPackets = 0;
let benignCount = 0;
let malwareCount = 0;

// Socket Event: Handshake
socket.on('connect', () => {
    statusEl.innerText = 'ONLINE';
    statusDot.className = 'status-dot status-online';
    console.log("Connected to AI-SOC Engine");
});

socket.on('disconnect', () => {
    statusEl.innerText = 'OFFLINE';
    statusDot.className = 'status-dot status-offline';
});

// Socket Event: Main Data Stream
socket.on('packet_data', (data) => {
    totalPackets++;
    totalPacketsEl.innerText = totalPackets.toLocaleString();

    // Update real-time Live Traffic Line Chart
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    trafficChart.data.labels.push(now);

    if (trafficChart.data.labels.length > 50) {
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
    }

    // Update Health Score
    const total = benignCount + malwareCount;
    if (total > 0 && healthScoreEl) {
        const health = (benignCount / total) * 100;
        healthScoreEl.innerText = `${health.toFixed(1)}%`;
        if (health < 70) healthScoreEl.style.color = 'var(--danger)';
        else if (health < 90) healthScoreEl.style.color = 'var(--warning)';
        else healthScoreEl.style.color = 'var(--success)';
    }

    if (data.type === 'BENIGN') {
        benignCount++;
        benignCountEl.innerText = benignCount.toLocaleString();
        trafficChart.data.datasets[0].data.push(Math.random() * 20 + 30);
        
        // Update Sticker
        if(statusSticker) {
            statusSticker.innerHTML = '<i class="fas fa-shield-check"></i> Network Healthy';
            statusSticker.style.borderColor = 'var(--success)';
            statusSticker.style.color = 'var(--success)';
        }
    } else {
        malwareCount++;
        malwareCountEl.innerText = malwareCount.toLocaleString();
        
        // Update Sticker
        if(statusSticker) {
            statusSticker.innerHTML = '<i class="fas fa-biohazard"></i> THREAT DETECTED';
            statusSticker.style.borderColor = 'var(--danger)';
            statusSticker.style.color = 'var(--danger)';
        }
        
        // Biohazard pulse
        if(bioIcon) {
            bioIcon.style.opacity = '0.8';
            setTimeout(() => bioIcon.style.opacity = '0.1', 1000);
        }

        // Trigger UI Alert effect
        malwareCard.classList.add('critical-alert-box');
        setTimeout(() => malwareCard.classList.remove('critical-alert-box'), 2000);

        trafficChart.data.datasets[0].data.push(data.is_simulated ? (Math.random()*10+100) : (Math.random()*20+150));

        // Update Severity
        if (data.severity === 'Low') severityChart.data.datasets[0].data[0]++;
        else if (data.severity === 'Medium') severityChart.data.datasets[0].data[1]++;
        else if (data.severity === 'Critical') {
            severityChart.data.datasets[0].data[2]++;
            try { alarmSound.play(); } catch (e) { }
        }
        severityChart.update();

        // Update Attack Type
        const typeIndex = typeChart.data.labels.indexOf(data.type);
        if (typeIndex === -1) {
            typeChart.data.labels.push(data.type);
            typeChart.data.datasets[0].data.push(1);
        } else {
            typeChart.data.datasets[0].data[typeIndex]++;
        }
        typeChart.update();

        addTableRow(data);
    }
    trafficChart.update();
});

// Socket Event: XAI Updates
socket.on('xai_update', (data) => {
    if (data && data.labels && data.labels.length > 0) {
        xaiChart.data.labels = data.labels;
        xaiChart.data.datasets[0].data = data.values;
        xaiChart.update();

        // Reasoning Text
        const reasoningEl = document.getElementById('xai-reasoning');
        if (reasoningEl && data.reasoning) {
            reasoningEl.innerHTML = `"${data.reasoning}"`;
        }

        // Feature Comparison Table
        const featureTable = document.getElementById('xai-features-table');
        if (featureTable && data.feature_details) {
            featureTable.innerHTML = '';
            data.feature_details.forEach(detail => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-weight: 600;">${detail.name}</td>
                    <td style="color: var(--success);">${detail.baseline}</td>
                    <td class="${detail.actual.includes('🔴') ? 'text-danger fw-bold' : 'text-success'}">${detail.actual}</td>
                `;
                featureTable.appendChild(tr);
            });
        }
    }
});

// Function: Add Row to Incident Stream
function addTableRow(data) {
    const row = document.createElement('tr');
    const timestamp = new Date().toLocaleTimeString();
    row.innerHTML = `
        <td style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: var(--text-dim);">${timestamp}</td>
        <td style="font-family: 'JetBrains Mono'; font-weight: 700;">${data.src_ip}</td>
        <td><span class="badge" style="background: rgba(255,255,255,0.05); color: var(--text-dim);">${data.protocol}</span></td>
        <td style="color: var(--text-dim);">${data.length}</td>
        <td style="color: #ff334b; font-weight: 800; letter-spacing: 0.5px;">${data.type.toUpperCase()}</td>
        <td><span class="badge bg-${data.color === 'danger' ? 'danger' : (data.color === 'warning' ? 'warning' : 'success')}" style="font-size: 0.65rem;">${data.severity.toUpperCase()}</span></td>
        <td style="font-family: 'JetBrains Mono'; color: var(--accent-cyan);">${(data.anomaly_score * 100).toFixed(2)}%</td>
    `;
    tableBody.prepend(row);
    if (tableBody.children.length > 15) tableBody.removeChild(tableBody.lastChild);
}

// Logic: Toggle Monitor
const toggleCaptureBtn = document.getElementById('toggle-capture-btn');
let isCaptureRunning = false;

function updateCaptureBtn(running) {
    isCaptureRunning = running;
    if (running) {
        toggleCaptureBtn.className = "btn btn-outline-danger";
        toggleCaptureBtn.innerHTML = '<i class="fas fa-stop-circle me-2"></i> STOP MONITOR';
    } else {
        toggleCaptureBtn.className = "btn btn-outline-success";
        toggleCaptureBtn.innerHTML = '<i class="fas fa-play-circle me-2"></i> START MONITOR';
    }
}

toggleCaptureBtn.addEventListener('click', () => {
    const action = isCaptureRunning ? 'stop' : 'start';
    fetch('/api/toggle-capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'started') updateCaptureBtn(true);
        if (data.status === 'stopped') updateCaptureBtn(false);
    });
});

// Logic: Simulations
document.querySelectorAll('.sim-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const type = btn.getAttribute('data-type');
        const count = 100;

        btn.style.opacity = '0.5';
        btn.style.pointerEvents = 'none';

        fetch('/api/bulk-simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: type, count: count })
        })
        .then(res => res.json())
        .then(() => {
            setTimeout(() => {
                btn.style.opacity = '1';
                btn.style.pointerEvents = 'auto';
            }, 5000);
        });
    });
});

// Periodic Updates (Polling System Stats)
setInterval(() => {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            if (data) {
                apmEl.innerText = data.apm;
                totalPacketsEl.innerText = data.total.toLocaleString();
                benignCountEl.innerText = data.benign.toLocaleString();
                malwareCountEl.innerText = data.malware.toLocaleString();
                
                // Update Resources
                if(cpuValueEl) {
                    cpuValueEl.innerText = `${data.cpu}%`;
                    cpuBarEl.style.width = `${data.cpu}%`;
                }
                if(gpuValueEl) {
                    gpuValueEl.innerText = `${data.gpu}%`;
                    gpuBarEl.style.width = `${data.gpu}%`;
                }

                // Update Speed
                if(kbpsEl) {
                    kbpsEl.innerText = data.kbps.toFixed(2);
                    drawSpeedGauge(data.kbps);
                }
            }
        });

    fetch('/api/capture-status')
        .then(res => res.json())
        .then(data => updateCaptureBtn(data.running));
}, 3000);

// Fetch Initial Analytics
fetch('/api/feature-importance')
    .then(res => res.json())
    .then(data => {
        if (data && data.labels.length > 0) {
            xaiChart.data.labels = data.labels;
            xaiChart.data.datasets[0].data = data.values;
            xaiChart.update();
        }
    });
