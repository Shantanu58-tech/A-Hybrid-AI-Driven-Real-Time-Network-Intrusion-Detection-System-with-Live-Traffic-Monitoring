<div align="center">
  <img src="https://img.shields.io/badge/AI--Powered-Cybersecurity-blue?style=for-the-badge&logo=shield" alt="AI Cybersecurity">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status Active">
  
  <h1>A Hybrid AI-Driven Real-Time Network Intrusion Detection System <br> with Live Traffic Monitoring 🛡️</h1>
  
  <p>
    <b>An enterprise-grade, real-time Security Operations Center (SOC) dashboard powered by Artificial Intelligence to detect, analyze, and report network anomalies and malware intrusions instantly.</b>
  </p>
</div>

---

## 🚀 Overview

This project implements a state-of-the-art **Hybrid Network Intrusion Detection System (NIDS)**. By combining live packet sniffing with advanced Machine Learning models, the system actively monitors network traffic, detects malicious anomalies in real-time, and provides deep insights through Explainable AI (XAI) and a visually stunning SOC dashboard.

Whether it's defending against DDoS attacks, port scanning, or zero-day malware patterns, this system offers a robust, automated defense layer with minimal human intervention.

## ✨ Key Features

- 🧠 **AI-Powered Detection Engine:** Uses machine learning models trained on vast networking datasets to classify traffic as benign or malicious with high accuracy.
- 🚦 **Real-Time Traffic Monitoring:** Integrates with Wireshark/TShark to capture and analyze live packets as they flow through the optimal network interface.
- 📊 **Next-Gen SOC Dashboard:** A beautifully designed, single-page application featuring:
  - Live network speed gauges.
  - Interactive attack timeline charts.
  - Security health score and dynamic status badges.
  - Beautiful UI elements (glassmorphism, radar effects, and micro-animations).
- 🔍 **Explainable AI (XAI):** Doesn't just flag an attack—it tells you *why*. XAI visually breaks down which network features contributed most to the anomaly score.
- 📄 **Automated PDF Incident Reporting:** Generates comprehensive, exportable PDF reports containing:
  - Attack timelines.
  - Feature contribution charts.
  - Countermeasure recommendations.
- 📱 **Instant SMS Alerts:** Privacy-focused, automated SMS alerting for high-severity incidents.

## 🏗️ Architecture & Technology Stack

- **Backend:** Python (Flask Engine)
- **Frontend:** HTML5, CSS3, JavaScript (Chart.js, modern dynamic animations)
- **Machine Learning:** Scikit-Learn / Custom Anomaly Training Pipeline
- **Networking:** TShark/Wireshark backend packet interception

## ⚙️ Installation & Setup

> [!IMPORTANT]
> Ensure you have Python 3.9+ and Wireshark installed on your system. Wireshark/TShark must be globally accessible in your PATH for live packet capture to function properly.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shantanu58-tech/A-Hybrid-AI-Driven-Real-Time-Network-Intrusion-Detection-System-with-Live-Traffic-Monitoring.git
   cd A-Hybrid-AI-Driven-Real-Time-Network-Intrusion-Detection-System-with-Live-Traffic-Monitoring
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the Models:**
   *Run the anomaly training script to generate the ML models if they aren't pre-loaded.*
   ```bash
   python train_anomaly.py
   ```

## 🚀 Running the System

Start the main SOC dashboard server:

```bash
python app.py
```
*(Or invoke via the dedicated runner: `python run_soc.py`)*

Navigate to `http://127.0.0.1:5000` (or the port specified in terminal) in your preferred modern web browser to view the SOC dashboard.

## 核心 System Functionalities

This project integrates a versatile suite of cybersecurity functions:
1. **Live Network Traffic Sniffing:** Employs Wireshark/TShark integration for 24/7 autonomous surveillance.
2. **AI Anomaly Detection:** Classifies traffic as benign, DDoS, PortScan, or Malware based on 70+ flow features in real time.
3. **Automated Incident Logging & PDF Generation:** Captures malicious packet telemetry and exports it securely as an annotated PDF report.
4. **Explainable AI (XAI) Matrix:** Maps threat scores to specific packet characteristics (e.g., flow duration, forward packet length).
5. **Private SMS Alert System:** Dispatch priority emergency texts via programmable gateways without logging the phone number in plaintext.

## ⚡ Proof of Real-Time Efficiency (Performance Metrics)

A core requirement for any operational Network Intrusion Detection System is **Real-Time capabilities**. This system is proven to operate dynamically without inducing network bottlenecks.

Based on operational benchmark tests: 
```text
============================================================
AI-SOC PERFORMANCE & OPTIMIZATION MODULE
============================================================
[*] Average Packet AI Detection Latency:   < 5.0 ms per packet (Often ~2ms)
[*] Total System Capacity Throughput:      ~25,000+ packets/sec
[*] Baseline Detection CPU Overhead:       ~1.2% - 3.5%
```
- **CPU Offloading:** The Random Forest and Machine Learning models predict classifications asynchronously. Because the model operates on condensed packet features (extracted metadata) rather than deep packet payloads, the **CPU usage remains exceptionally low**. 
- **Sub-50ms Reaction:** The average latency from packet interception to anomaly flagged is virtually instantaneous, allowing the dashboard to light up with red-alert warning pulses well within a reasonable SOC threshold.

## 📊 Dashboard & System Evaluation

The NIDS features a Next-Gen single-page AI-SOC Dashboard with:
- **Ping/Latency & Real-Time Network Speed Gauge** trackers dynamically reflecting active usage.
- **Threat Matrices** classifying severity and visualizing attack timelines.

*(For developers viewing the NIDS running locally or hosted online, the Dashboard is available dynamically at `localhost:5000` presenting live visual Radar animations and XAI feature plots!)*

<p align="center">
  <img src="confusion_matrix.png" alt="AI Confusion Matrix" width="45%">
  &nbsp;&nbsp;
  <img src="evaluation_report.png" alt="AI Evaluation Report" width="45%">
</p>
<p align="center">
    <em>Actual evaluation matrices from our ML Anomaly Detection model exhibiting classification accuracy.</em>
</p>

## 🧑‍💻 File Structure Snapshot

- `/templates/` - Contains the HTML files for Dashboard, XAI maps, and Incident logs. 
- `/static/` - Custom JS logic, dynamic CSS styling, and dashboard assets.
- `/training/` - Scripts dedicated to processing datasets and training the intrusion models.
- `app.py` - Core web application server and API router.
- `measure_speed.py` / `measure_performance.py` - Background metric calculation routines.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page and submit pull requests to help evolve this AI NIDS further.

---
<div align="center">
  <b>Built with passion by Shantanu & Team for Next-Gen Network Defense</b>
</div>
