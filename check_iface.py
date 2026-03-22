import pyshark
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TSHARK_PATH = os.path.join(BASE_DIR, "realtime", "Wireshark", "tshark.exe")

print(f"Using TShark at: {TSHARK_PATH}")
print("Fetching interfaces, please wait...")

try:
    interfaces = pyshark.tshark.tshark.get_tshark_interfaces(tshark_path=TSHARK_PATH)
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")
except Exception as e:
    print(f"Error: {e}")
