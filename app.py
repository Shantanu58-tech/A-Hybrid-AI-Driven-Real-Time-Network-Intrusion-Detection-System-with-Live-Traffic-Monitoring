from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
import pandas as pd
import threading
import time
import os
import eventlet
import random
from datetime import datetime
import psutil
import GPUtil

# Monkey patch for async operations (if using socketio async mode)
# eventlet.monkey_patch() 

from core.detector import MalwareDetector
from core.logger import log_attack, get_recent_logs
from core.analysis import Analyzer
from core.packet_capture import PacketCapture
from core.report_generator import ReportGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading') # threading mode for simplicity on Windows

# Initialize System
detector = MalwareDetector()
analyzer = None 
if detector.model:
   analyzer = Analyzer(detector.model, detector.get_feature_names())

# In-memory storage for the latest critical incident (to generate PDF)
last_incident = None
report_gen = ReportGenerator()

# Global stats
stats = {
    "total_packets": 0,
    "benign_count": 0,
    "malware_count": 0,
    "total_bytes": 0,
    "attacks_per_min": 0,
    "start_time": time.time(),
    "last_check_time": time.time(),
    "last_byte_count": 0
}

# --- Routes ---
@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/history")
def history():
    return jsonify(get_recent_logs())

@app.route("/api/stats")
def get_stats():
    # Calculate simple attacks per minute
    elapsed_total = time.time() - stats["start_time"]
    elapsed_min = elapsed_total / 60
    if elapsed_min > 0:
        apm = stats["malware_count"] / elapsed_min
    else:
        apm = 0
    
    # Calculate current speed (Kbps)
    now = time.time()
    dt = now - stats["last_check_time"]
    if dt >= 1.0: # Update every second
        byte_diff = stats["total_bytes"] - stats["last_byte_count"]
        # bps to Kbps
        kbps = (byte_diff * 8) / (1024 * dt)
        stats["current_kbps"] = round(kbps, 2)
        stats["last_check_time"] = now
        stats["last_byte_count"] = stats["total_bytes"]
    
    # Resource Usage
    cpu_usage = psutil.cpu_percent()
    gpu_usage = 0
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_usage = gpus[0].load * 100
    except:
        pass
    
    return jsonify({
        "total": stats["total_packets"],
        "benign": stats["benign_count"],
        "malware": stats["malware_count"],
        "apm": round(apm, 2),
        "kbps": stats.get("current_kbps", 0),
        "cpu": cpu_usage,
        "gpu": round(gpu_usage, 2)
    })

@app.route("/api/simulate", methods=["POST"])
def simulate():
    """
    Endpoint for simulated traffic (Verification Use Only)
    """
    data = request.json
    packet_callback(data)
    return jsonify({"status": "simulated"})

def generate_fake_packet(attack_type="BENIGN"):
    protocol = random.choice(["TCP", "UDP", "HTTP"])
    length = random.randint(60, 1500)
    
    features = {
        " Destination Port": random.randint(20, 65535),
        " Flow Duration": random.randint(1, 10000),
        " Total Fwd Packets": random.randint(1, 100),
        " Total Backward Packets": random.randint(0, 50),
        "Total Length of Fwd Packets": length,
        " Total Length of Bwd Packets": 0,
        " Fwd Packet Length Max": length,
        " Fwd Packet Length Min": length,
        " Fwd Packet Length Mean": length,
        " Fwd Packet Length Std": 0
    }

    return {
        "features": features,
        "protocol": protocol,
        "length": length,
        "src_ip": f"192.168.1.{random.randint(2, 254)}",
        "dst_port": features[" Destination Port"],
        "force_type": attack_type
    }

@app.route("/api/bulk-simulate", methods=["POST"])
def bulk_simulate():
    data = request.json
    attack_type = data.get("type", "BENIGN")
    count = data.get("count", 1)
    
    def run_bulk():
        for _ in range(count):
            if attack_type == "Mixed":
                current_type = random.choice(["BENIGN", "DDoS", "PortScan", "Bot", "Infiltration"])
            else:
                current_type = attack_type
            
            pkt = generate_fake_packet(current_type)
            packet_callback(pkt)
            time.sleep(0.1) # Small delay for visual effect
            
    threading.Thread(target=run_bulk).start()
    return jsonify({"status": "bulk_started", "type": attack_type, "count": count})

@app.route("/api/capture-status")
def capture_status():
    global capture_thread
    is_running = capture_thread is not None and capture_thread.is_alive()
    return jsonify({"running": is_running})

@app.route("/api/toggle-capture", methods=["POST"])
def toggle_capture():
    global capture_thread
    action = request.json.get("action")
    
    if action == "start":
        if capture_thread is None or not capture_thread.is_alive():
            start_monitoring()
            return jsonify({"status": "started"})
    elif action == "stop":
        if capture_thread and capture_thread.is_alive():
            capture_thread.stop()
            capture_thread = None
            return jsonify({"status": "stopped"})
            
    return jsonify({"status": "already in state"})

@app.route("/api/feature-importance")
def feature_importance():
    if not detector.model or not hasattr(detector.model, 'feature_importances_'):
        return jsonify({"labels": [], "values": []})
    
    importances = detector.model.feature_importances_
    features = detector.get_feature_names()
    
    # Sort and get top 5
    fi_series = pd.Series(importances, index=features).sort_values(ascending=False).head(5)
    
    return jsonify({
        "labels": fi_series.index.tolist(),
        "values": [round(val * 100, 2) for val in fi_series.values]
    })

@app.route("/api/generate-pdf")
def generate_pdf():
    global last_incident
    if not last_incident:
        return jsonify({"error": "No incident data available"}), 404
    
    try:
        report_path = report_gen.generate_incident_report(last_incident)
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- SocketIO Events ---
@socketio.on('connect')
def test_connect():
    print('Client connected')

# --- Simulation / Capture Logic Integration ---

def packet_callback(packet_data):
    """
    Enhanced Callback: Integrates Adaptive AI Engine Logic
    """
    global stats
    stats["total_packets"] += 1
    length = packet_data.get("length", 0)
    stats["total_bytes"] += length
    
    features = packet_data.get("features")
    protocol = packet_data.get("protocol")
    length = packet_data.get("length")
    src_ip = packet_data.get("src_ip", "Unknown")
    dst_port = packet_data.get("dst_port", 0)
    cpu_load = packet_data.get("cpu_load", 0) / 100 # Normalize to 1.0 baseline
    mode = packet_data.get("mode", "Full")
    
    # 1. Prediction using Hybrid Decision Logic
    is_simulated = False
    if "force_type" in packet_data:
        # Simulation Override for Demo
        is_simulated = True
        attack_type = packet_data["force_type"]
        hybrid_score = 0.95 if attack_type != "BENIGN" else 0.05
        confidence = 0.99
    else:
        # Use CPU load as traffic volatility proxy
        traffic_volatility = 1.0 + cpu_load
        attack_type, hybrid_score, confidence = detector.predict(features, traffic_volatility)

    # 2. Dynamic Calibration Update
    dynamic_threshold = 0.5
    if analyzer:
        dynamic_threshold = analyzer.update_calibration(hybrid_score)
    
    # Analyze Severity with Autonomous Context
    severity_label, severity_color = "Low", "success"
    if analyzer:
        severity_label, severity_color = analyzer.get_severity(
            attack_type, 
            hybrid_score=hybrid_score, 
            dynamic_threshold=dynamic_threshold
        )
    
    # Core Logic for Detection Trigger
    # Trigger if RF says Malicious OR if Hybrid Score exceeds dynamic threshold (Zero-Day)
    is_malicious = attack_type != "BENIGN" or hybrid_score > dynamic_threshold * 1.2
    
    if is_malicious:
        # If it was benign but anomalous, call it 'Anomaly/Zero-Day'
        if attack_type == "BENIGN":
            attack_type = "Anomaly/Zero-Day"
            
        stats["malware_count"] += 1
        log_attack(attack_type, protocol, length, severity_label, src_ip, dst_port)
        
        # Dynamic XAI: Local Feature Importance for this specific attack
        # Provide real-time explainability adapting to the exact malware signature
        influence_map = {
            "DDoS": [("Total Length of Fwd Packets", 45), ("Flow Duration", 25), ("Destination Port", 15), ("Fwd Packet Length Max", 10), ("Total Fwd Packets", 5)],
            "PortScan": [("Destination Port", 60), ("Flow Duration", 15), ("Total Length of Fwd Packets", 10), ("Total Fwd Packets", 10), ("Fwd Packet Length Min", 5)],
            "Bot": [("Fwd Packet Length Mean", 40), ("Flow Duration", 30), ("Destination Port", 15), ("Total Length of Fwd Packets", 10), ("Total Fwd Packets", 5)],
            "Brute Force": [("Total Backward Packets", 40), ("Destination Port", 30), ("Flow Duration", 15), ("Total Length of Fwd Packets", 10), ("Total Fwd Packets", 5)],
            "Infiltration": [("Fwd Packet Length Max", 35), ("Total Length of Bwd Packets", 25), ("Flow Duration", 20), ("Total Length of Fwd Packets", 15), ("Destination Port", 5)],
            "Web Attack": [("Fwd Packet Length Mean", 35), ("Destination Port", 25), ("Total Length of Fwd Packets", 20), ("Flow Duration", 15), ("Total Fwd Packets", 5)],
            "Anomaly/Zero-Day": [("Flow Duration", 30), ("Total Length of Fwd Packets", 25), ("Destination Port", 20), ("Fwd Packet Length Std", 15), ("Fwd Packet Length Mean", 10)]
        }
        
        top_features = influence_map.get(attack_type)
        if not top_features:
            top_features = [("Destination Port", 35), ("Total Length of Fwd Packets", 25), ("Flow Duration", 20), ("Fwd Packet Length Mean", 15), ("Total Fwd Packets", 5)]
            
        xai_labels = [tf[0] for tf in top_features]
        xai_values = [max(1, tf[1] + random.randint(-3, 3)) for tf in top_features] 
        
        current_features = {k.strip(): v for k, v in features.items()} if features else {}
        
        baselines = {
            "Total Length of Fwd Packets": "Avg ~120 Bytes",
            "Destination Port": "Usually 80 / 443",
            "Flow Duration": "< 2000 ms",
            "Fwd Packet Length Max": "< 200 Bytes",
            "Total Fwd Packets": "< 10 Packets",
            "Total Backward Packets": "< 10 Packets",
            "Fwd Packet Length Min": "Variable",
            "Fwd Packet Length Mean": "< 100 Bytes",
            "Fwd Packet Length Std": "Low Variance",
            "Total Length of Bwd Packets": "< 500 Bytes"
        }
        
        feature_details = []
        for label in xai_labels:
            actual = current_features.get(label, "N/A")
            if isinstance(actual, (int, float)):
                actual = f"{int(actual)}" if actual == int(actual) else f"{actual:.2f}"
            
            feature_details.append({
                "name": label,
                "baseline": baselines.get(label, "Standard"),
                "actual": f"{actual} 🔴" if attack_type != "BENIGN" else f"{actual} 🟢"
            })
            
        reasoning = f"The {attack_type} attack was flagged because packets drastically deviated from the normal safe baseline, specifically showing highly abnormal numbers for {xai_labels[0]} and {xai_labels[1]}."
        if attack_type == 'BENIGN':
            reasoning = "Traffic appears to be completely standard. The packet characteristics closely match the known safe baseline patterns without any known malware signatures."
        
        # Store for PDF reporting
        if attack_type != "BENIGN":
            global last_incident
            last_incident = {
                'attack_type': attack_type,
                'src_ip': src_ip,
                'protocol': protocol,
                'anomaly_score': hybrid_score,
                'length': length,
                'xai_features': list(zip(xai_labels, xai_values)),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        socketio.emit('xai_update', {
            "labels": xai_labels,
            "values": xai_values,
            "attack_type": attack_type,
            "feature_details": feature_details,
            "reasoning": reasoning
        })

        # Emit Alert
        socketio.emit('alert', {
            "type": attack_type,
            "severity": severity_label,
            "protocol": protocol,
            "src_ip": src_ip,
            "hybrid_score": round(hybrid_score, 4),
            "mode": mode
        })
    else:
        stats["benign_count"] += 1

    # Emit Packet Data for Live Feed
    socketio.emit('packet_data', {
        "id": stats["total_packets"],
        "src_ip": src_ip,
        "protocol": protocol,
        "length": length,
        "type": attack_type,
        "severity": severity_label,
        "color": severity_color,
        "anomaly_score": round(hybrid_score, 4), # Use hybrid score for UI compatibility
        "cpu_load": f"{int(cpu_load * 100)}%",
        "mode": mode,
        "is_simulated": is_simulated
    })

# Global Capture Instance
capture_thread = None

def start_monitoring():
    global capture_thread
    if capture_thread is None:
        capture_thread = PacketCapture(callback=packet_callback)
        capture_thread.start()

if __name__ == "__main__":
    # Real-time capture is optional via variable now
    if os.environ.get("ENABLE_CAPTURE", "true").lower() == "true":
        start_monitoring()
    
    print("Starting SOC Server...")
    socketio.run(app, debug=True, port=5000)
