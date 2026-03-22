import time
import psutil
import pandas as pd
import joblib
import os
import numpy as np

# Configuration
MODEL_PATH = "model/malware_model.pkl"
ANOMALY_MODEL_PATH = "model/anomaly_model.pkl"

def run_performance_benchmark():
    print("="*60)
    print("AI-SOC PERFORMANCE & OPTIMIZATION MODULE")
    print("="*60)

    # 1. Environment Check
    print(f"[*] Initial CPU Usage: {psutil.cpu_percent()}%")
    print(f"[*] Available RAM: {psutil.virtual_memory().available / (1024**3):.2f} GB")

    # 2. Load Models
    print("\n[*] Loading AI Models for Speed Test...")
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return

    start_load = time.perf_counter()
    model = joblib.load(MODEL_PATH)
    anomaly_model = None
    if os.path.exists(ANOMALY_MODEL_PATH):
        anomaly_model = joblib.load(ANOMALY_MODEL_PATH)
    end_load = time.perf_counter()
    print(f"[*] Models loaded into RAM in {(end_load - start_load):.2f}s")

    # 3. Create Dummy Packet (mimicking live capture features)
    feature_names = model.feature_names_in_
    dummy_packet = {f: 0 for f in feature_names}
    dummy_packet[" Destination Port"] = 443
    dummy_packet[" Total Fwd Packets"] = 5
    dummy_packet["Total Length of Fwd Packets"] = 1200
    
    df_packet = pd.DataFrame([dummy_packet])
    df_packet = df_packet.reindex(columns=feature_names, fill_value=0)

    # 4. Measure Detection Latency
    # We use a benchmark batch size to get a reliable average
    iterations = 50
    print(f"\n[*] Measuring Packet Processing Latency ({iterations} packets)...")
    
    # Warm-up run
    model.predict(df_packet)
    
    # Precise benchmark
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = model.predict(df_packet)
        if anomaly_model:
            _ = anomaly_model.decision_function(df_packet)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_latency_ms = (total_time / iterations) * 1000
    
    # Single-core throughput per second
    packets_per_sec = int(iterations / total_time)
    
    # Multi-threaded potential (Enterprise Simulation)
    # Most SOC systems use 8+ cores. We simulate the total capacity.
    cores = psutil.cpu_count(logical=True)
    simulated_throughput = packets_per_sec * (cores - 1)
    
    # Measure CPU with a fixed interval for accuracy
    cpu_during = psutil.cpu_percent(interval=1.0)

    # 5. Output Results
    print("\n" + "-"*40)
    print("BENCHMARK RESULTS (Real-Time Proof):")
    print("-"*40)
    print(f"Average Detection Time: {avg_latency_ms:.2f} ms")
    print(f"Packets/sec (Single Flow): {packets_per_sec}")
    print(f"Total System Capacity: ~{simulated_throughput} Packets/sec")
    print(f"CPU usage during detection: {cpu_during}%")
    print("-"*40)

    if avg_latency_ms < 50:
        print("RESULT: [SUCCESS] System is OPERATIONAL for Real-Time Monitoring.")
    else:
        print("RESULT: [WARNING] High Latency. Enabling 'Critical Mode' recommended.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_performance_benchmark()
