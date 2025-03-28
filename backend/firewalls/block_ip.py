# File: backend/firewalls/block_ip.py
     




import subprocess
import os

# List of malicious IPs (this can be replaced with a dynamic source)
malicious_ips = [
    "192.168.1.100",
    "203.0.113.50",
    "198.51.100.23"
]

def block_ip(ip):
    """
    Blocks the given IP using iptables.
    """
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"[INFO] Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to block IP {ip}: {e}")

def block_malicious_ips():
    """
    Loops through the list of malicious IPs and blocks each one.
    """
    print("[INFO] Starting to block malicious IPs...")
    for ip in malicious_ips:
        block_ip(ip)
    print("[INFO] Blocking process completed.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root. Please use sudo.")
    else:
        block_malicious_ips()
