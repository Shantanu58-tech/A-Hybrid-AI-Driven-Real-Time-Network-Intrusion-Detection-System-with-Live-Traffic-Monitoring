import random
import time
from datetime import datetime
import csv
import os

LOG_FILE = "logs/attack_log.csv"

attack_types = [
    "DDoS",
    "PortScan",
    "Botnet",
    "Web Attack",
    "Brute Force",
    "Infiltration"
]

protocols = ["TCP", "UDP", "HTTP", "TLS"]

def generate_fake_attack():
    attack = random.choice(attack_types)
    protocol = random.choice(protocols)
    length = random.randint(200, 1500)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Time", "Attack Type", "Protocol", "Length"])
        writer.writerow([time_now, attack, protocol, length])

    print(f"🚨 Simulated Attack → {attack} | {protocol} | {length} bytes")

print("Starting Attack Simulation... (Press CTRL+C to stop)\n")

while True:
    generate_fake_attack()
    time.sleep(5)
