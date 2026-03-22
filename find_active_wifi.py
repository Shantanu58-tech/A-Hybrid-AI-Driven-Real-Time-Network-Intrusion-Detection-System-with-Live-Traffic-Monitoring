import pyshark
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TSHARK_PATH = os.path.join(BASE_DIR, "realtime", "Wireshark", "tshark.exe")

def get_active_interface():
    print(f"Checking for active traffic on interfaces...")
    try:
        interfaces = pyshark.tshark.tshark.get_tshark_interfaces(tshark_path=TSHARK_PATH)
        for iface in interfaces:
            # Skip loopback and generic ones for speed
            if "Loopback" in iface or "Adapter" not in iface and "Wi-Fi" not in iface:
                pass 
            
            print(f"Testing {iface} for 3 seconds...")
            capture = pyshark.LiveCapture(interface=iface, tshark_path=TSHARK_PATH)
            try:
                capture.sniff(timeout=3)
                if len(capture) > 0:
                    print(f"✅ FOUND ACTIVE TRAFFIC ON: {iface}")
                    return iface
            except:
                continue
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    iface = get_active_interface()
    if iface:
        print(f"\nCOPY THIS ID: {iface}")
    else:
        print("\nNo active traffic found. Are you connected to the internet?")
