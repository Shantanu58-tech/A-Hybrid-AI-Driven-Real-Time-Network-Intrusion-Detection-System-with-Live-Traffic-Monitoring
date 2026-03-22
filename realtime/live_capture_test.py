import pyshark

TSHARK_PATH = r"C:\Users\Shantanu\OneDrive\Desktop\Computer Networking\MalwareDetectionAI\realtime\Wireshark\tshark.exe"

INTERFACE = r"\Device\NPF_{9BEF1959-774D-46E5-AD3E-0B7676C9F481}"

print("Starting live packet capture on interface 0...")

capture = pyshark.LiveCapture(
    interface=INTERFACE,
    tshark_path=TSHARK_PATH
)

for packet in capture.sniff_continuously(packet_count=10):
    try:
        print("\nPacket captured:")
        print("Protocol:", packet.highest_layer)
        print("Length:", packet.length)
        print("Source:", packet.ip.src)
        print("Destination:", packet.ip.dst)
    except:
        pass
