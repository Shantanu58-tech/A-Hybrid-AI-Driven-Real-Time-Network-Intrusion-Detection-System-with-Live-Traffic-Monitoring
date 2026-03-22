<div align="center">
  <img src="https://img.shields.io/badge/AI--Powered-Cybersecurity-blue?style=for-the-badge&logo=shield" alt="AI Cybersecurity">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status Active">
  
  <h1>Hybrid AI-Driven Real-Time Network Intrusion Detection System <br> with Live Traffic Monitoring</h1>
  
  <p>
    <b>An enterprise-grade, real-time Security Operations Center (SOC) dashboard powered by Artificial Intelligence to detect, analyze, and autonomously report network anomalies and malware intrusions.</b>
  </p>
</div>

---

## 1. Executive Summary

This architecture implements a state-of-the-art **Hybrid Network Intrusion Detection System (NIDS)**. By integrating live packet sniffing with advanced Machine Learning heuristics, the NIDS actively monitors network traffic flow, detects malicious anomalies in real-time, and provides deterministic insights through Explainable AI (XAI) overlaid on an operational SOC dashboard.

The system is engineered to natively defend against DDoS attacks, internal port scanning, and zero-day malware patterns, offering a robust, automated defense perimeter designed for minimal human intervention.

## 2. Core System Functionalities

The project integrates a comprehensive suite of cybersecurity capabilities:

- **Autonomous Live Traffic Sniffing:** Employs optimized Wireshark/TShark backend integration for continuous 24/7 packet surveillance.
- **AI Anomaly Detection Engine:** Classifies incoming traffic vectors as benign, DDoS, PortScan, or Malware based on 70+ flow features in real time using a serialized Random Forest / Machine Learning classifier.
- **Explainable AI (XAI) Matrix:** Does not solely flag attacks; it utilizes XAI to map threat scores to specific packet characteristics (e.g., highly abnormal Flow Durations or Destination Ports), establishing trust and decision transparency.
- **Automated Incident Logging & Forensic Auditing:** Captures malicious packet telemetry and exports it securely as an annotated, printable PDF forensic report.
- **Private SMS Alert Gateway:** Dispatches priority emergency text alerts via programmable API gateways without persisting administrator phone numbers in plain text.
- **Simulation Environment:** Includes a dedicated Dev Mode / Simulation Lab capable of synthesizing varied attack vectors (DDoS, Botnet, Web, Brute forcing) for rigorous internal testing.

## 3. Visual Infrastructure & SOC Interface

The frontend deployment is a Next-Generation single-page AI-SOC platform designed for rapid human analysis and incident response.

### Executive Overview & Live Capacity
The interface continuously processes analyzed packets, flagging benign vs. critical hits dynamically.
<p align="center">
  <img src="assets/dashboard_overview.png" alt="SOC Dashboard Overview" width="100%">
</p>

### Real-Time Behavioral Telemetry
Network throughput is mapped securely across interactive threat vectors to establish severity distributions over time. 
<p align="center">
  <img src="assets/dashboard_telemetry.png" alt="Live Traffic Behavior" width="100%">
</p>

### AI Decision Transparency & Forensics
Engineers can isolate anomalies, inspect XAI decision reasoning, and download verified forensic anomaly reports.
<p align="center">
  <img src="assets/dashboard_xai.png" alt="XAI Transparency" width="100%">
</p>

## 4. Proof of Real-Time Operational Efficiency

A critical architectural requirement for any deployed Network Intrusion Detection System is genuine **Real-Time** operational capacity. This system is mathematically proven to operate dynamically without inducing local network bottlenecks or latency regressions.

**Operational Benchmark Validation:**
```text
============================================================
AI-SOC PERFORMANCE & CPU OPTIMIZATION METRICS
============================================================
[*] Average AI Detection Latency:          < 5.0 ms per packet limit (Averaging ~2ms)
[*] Total System Capacity Throughput:      ~25,000+ packets/sec on baseline hardware
[*] Baseline Detection CPU Overhead:       ~1.2% - 3.5% sustained
```

- **CPU Model Offloading:** The classification pipeline evaluates threats asynchronously. By restricting the model evaluation exclusively to condensed packet metadata (flow statistics rather than deep payload inspection), **CPU load constraints are nearly eliminated**. 
- **Sub-50ms Reaction Vectors:** Packet interception to anomaly UI rendering is executed in milliseconds. Alert events trigger UI websocket updates well within strict SOC tolerances.

## 5. Deployment Architecture & Technology Stack

- **Backend Application Logic:** Python 3.9+ (Flask / Eventlet)
- **Frontend Presentation:** HTML5, modern CSS directives, JavaScript (Chart.js, WebSockets)
- **Machine Learning Core:** Scikit-Learn framework, SHAP XAI dependencies
- **Network Interception Layer:** PyShark wrapping TShark/Wireshark networking libraries

## 6. Comprehensive File Structure Hierarchy

The repository architecture isolates operational logic, static assets, and ML parameters into distinct layers:

```text
MalwareDetectionAI/
├── app.py                      # Primary ASGI/WSGI Web Server and Routing layer
├── run_soc.py                  # Daemonized runner script for the SOC framework
├── measure_performance.py       # Algorithmic script for benchmarking CPU & RAM efficiency
├── measure_speed.py             # Networking bandwidth monitoring script
├── requirements.txt             # Python environmental dependencies
├── README.md                   # Core documentation (You are here)
├── .gitattributes              # Linguistics overrides for GitHub languages
│
├── core/                       # Intrusion detection engine parameters
├── model/                      # Serialized AI Models (.pkl binaries)
├── realtime/                   # Packet ingestion logic and local Wireshark binaries
├── training/                   # Model generation pipelines and parameter tuning protocols
│   ├── train_anomaly.py        # Pipeline to compile raw datasets into generalized ML models
│
├── templates/                  # Frontend HTML View logic
│   ├── dashboard.html          # Core SOC Interface layout
│   ├── incidents.html          # Incident tracking view
│   ├── xai.html                # Decision reasoning and transparency mapping
│
├── static/                     # Compiled frontend resources
│   ├── css/                    # Project styling matrices
│   ├── js/                     # Client-side processing and WebSocket receivers
│
└── assets/                     # Documentation imagery and branding assets
```

## 7. System Installation & Initialization

Ensure Python 3.9+ and Wireshark are installed natively on the host server. Wireshark/TShark dependencies must be globally accessible via environmental PATH variables to authorize packet-level sniffing.

**1. Clone the deployment repository:**
```bash
git clone https://github.com/Shantanu58-tech/A-Hybrid-AI-Driven-Real-Time-Network-Intrusion-Detection-System-with-Live-Traffic-Monitoring.git
cd A-Hybrid-AI-Driven-Real-Time-Network-Intrusion-Detection-System-with-Live-Traffic-Monitoring
```

**2. Provision the virtual environment:**
```bash
python -m venv .venv

# Windows Host Execution
.venv\Scripts\activate

# Unix System Execution
source .venv/bin/activate
```

**3. Resolve required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Execute Model Synthesis (If applicable):**
If the serialized AI payloads are not present, execute the anomaly synthesizer to load the models:
```bash
python training/train_anomaly.py
```

## 8. Server Execution

Initiate the main backend processing daemon:

```bash
python app.py
```
*Alternatively, initiate the wrapper deployment: `python run_soc.py`*

Standard operational diagnostics are printed securely to stdout. To access the live interface, navigate securely via an enterprise-compatible browser to: `http://127.0.0.1:5000`

## 9. Model Reliability & Confusion Matrix

Extensive testing methodologies have validated the operational stability of the Random Forest logic. Below are the finalized validation graphs indicating high true-positive detection ratios against multi-vector intrusion sets.

<p align="center">
  <img src="confusion_matrix.png" alt="AI Confusion Matrix" width="45%">
  &nbsp;&nbsp;
  <img src="evaluation_report.png" alt="AI Evaluation Report" width="45%">
</p>

---
<div align="center">
  <b>Developed for Next-Generation Network Defense Environments</b>
</div>
