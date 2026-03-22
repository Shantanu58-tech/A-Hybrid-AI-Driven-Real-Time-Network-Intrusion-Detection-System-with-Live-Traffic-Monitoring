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

## 📊 Dashboard & System Evaluation

The dashboard incorporates dynamic metrics:
- **Ping/Latency & Speed** trackers.
- **Threat Matrices** classifying severity.
- **Incident Logs** with direct PDF report generation.

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
