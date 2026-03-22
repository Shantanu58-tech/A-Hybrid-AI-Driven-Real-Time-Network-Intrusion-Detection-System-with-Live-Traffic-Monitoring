import csv
from datetime import datetime
import os

LOG_FILE = "logs/attack_log.csv"

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

def log_attack(attack_type, protocol, length):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time", "Attack Type", "Protocol", "Packet Length"])

        writer.writerow([time, attack_type, protocol, length])

    print(f"📝 Attack Logged: {attack_type} | {protocol} | {length}")
