
import pyshark
import threading
import time
import pandas as pd

# Configuration (Should ideally be in a config file)
# Configuration
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSHARK_PATH = os.path.join(BASE_DIR, "realtime", "Wireshark", "tshark.exe")
# Start with the interface from the old file, but we can also auto-detect or let user change it
INTERFACE = r"\Device\NPF_{9BEF1959-774D-46E5-AD3E-0B7676C9F481}" 

import asyncio

import psutil

class PacketCapture(threading.Thread):
    def __init__(self, callback, interface=INTERFACE, tshark_path=TSHARK_PATH):
        super().__init__()
        self.callback = callback
        self.interface = interface
        self.tshark_path = tshark_path
        self.running = False
        self.capture = None
        self.last_cpu_check = 0
        self.cpu_usage = 0

    def run(self):
        # Create a new event loop for this thread (Required by pyshark)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        self.running = True
        print(f"Starting Packet Capture on {self.interface}...")
        
        try:
            self.capture = pyshark.LiveCapture(
                interface=self.interface,
                tshark_path=self.tshark_path
            )
            
            for packet in self.capture.sniff_continuously():
                if not self.running:
                    break
                
                try:
                    self.process_packet(packet)
                except Exception as e:
                    print(f"Error processing packet: {e}")
                    
        except Exception as e:
            print(f"Capture Error: {e}")
        finally:
            print("Packet Capture Stopped.")

    def process_packet(self, packet):
        try:
            # 1. Self-Adaptive Resource Check (Novel Idea 2)
            # Check CPU every 2 seconds to avoid overhead of psutil calls
            if time.time() - self.last_cpu_check > 2:
                self.cpu_usage = psutil.cpu_percent()
                self.last_cpu_check = time.time()

            protocol = packet.highest_layer
            length = int(packet.length)
            
            # Extract basic info
            src_ip = packet.ip.src if hasattr(packet, 'ip') else "Unknown"
            dst_port = 0
            if hasattr(packet, "transport_layer"):
                dst_port = int(packet[packet.transport_layer].dstport)

            # 2. Latency-Aware Feature Switching
            # If CPU > 80%, we switch to 'Critical Mode' (Extract only top 6 features)
            is_critical_mode = self.cpu_usage > 80
            
            if is_critical_mode:
                # Optimized 'Fast-Path' Extraction
                features = {
                    " Destination Port": dst_port,
                    "Total Length of Fwd Packets": length,
                    " Fwd Packet Length Max": length,
                    " Fwd Packet Length Min": length,
                    " Fwd Packet Length Mean": length,
                    " Flow Duration": 1 # Minimal set
                }
                # Fill others with neutral default (0) to maintain model compatibility
                defaults = [" Total Fwd Packets", " Total Backward Packets", " Total Length of Bwd Packets", " Fwd Packet Length Std"]
                for d in defaults:
                    features[d] = 0
            else:
                # Standard Full-Featured Extraction
                features = {
                    " Destination Port": dst_port,
                    " Flow Duration": 1,
                    " Total Fwd Packets": 1,
                    " Total Backward Packets": 0,
                    "Total Length of Fwd Packets": length,
                    " Total Length of Bwd Packets": 0,
                    " Fwd Packet Length Max": length,
                    " Fwd Packet Length Min": length,
                    " Fwd Packet Length Mean": length,
                    " Fwd Packet Length Std": 0
                }

            packet_data = {
                "features": features,
                "protocol": protocol,
                "length": length,
                "src_ip": src_ip,
                "dst_port": dst_port,
                "cpu_load": self.cpu_usage, # Metadata for dashboard/hybrid logic
                "mode": "Critical" if is_critical_mode else "Full"
            }
            
            # Send to callback (which will be the detection logic in app.py)
            self.callback(packet_data)
            
        except AttributeError:
            pass # Some packets might not have IP layer etc.

    def stop(self):
        self.running = False
