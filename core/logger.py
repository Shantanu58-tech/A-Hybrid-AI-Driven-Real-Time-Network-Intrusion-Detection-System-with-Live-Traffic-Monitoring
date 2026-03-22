
import csv
import os
from datetime import datetime

LOG_FILE = "logs/attack_log.csv"
os.makedirs("logs", exist_ok=True)

def log_attack(attack_type, protocol, length, severity, src_ip, dst_port):
    """
    Logs an attack to the CSV file.
    """
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(LOG_FILE)

    try:
        with open(LOG_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["Time", "Attack Type", "Severity", "Protocol", "Packet Length", "Source IP", "Destination Port"])
            
            writer.writerow([time_str, attack_type, severity, protocol, length, src_ip, dst_port])
            
    except Exception as e:
        print(f"Error logging attack: {e}")

def get_recent_logs(limit=50):
    """
    Returns the most recent log entries.
    """
    if not os.path.exists(LOG_FILE):
        return []
    
    try:
        with open(LOG_FILE, "r") as file:
            reader = list(csv.DictReader(file))
            return reader[-limit:][::-1] # Last 'limit' rows, reversed (newest first)
    except Exception:
        return []
