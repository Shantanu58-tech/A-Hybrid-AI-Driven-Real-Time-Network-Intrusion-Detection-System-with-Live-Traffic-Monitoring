import pyshark

TSHARK_PATH = r"C:\Users\Shantanu\OneDrive\Desktop\Computer Networking\MalwareDetectionAI\realtime\Wireshark\tshark.exe"

print("Listing available capture interfaces...\n")

interfaces = pyshark.tshark.tshark.get_tshark_interfaces(tshark_path=TSHARK_PATH)

for i, iface in enumerate(interfaces):
    print(f"{i}: {iface}")
