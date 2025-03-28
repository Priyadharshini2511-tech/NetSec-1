import requests
import subprocess
import os

# URL for downloading known VPN IPs (example)
VPN_IPS_URL = "https://example.com/vpn-ip-list.txt"  # Replace with an actual URL

class VPNBlocklistManager:
    """
    A class to manage a blocklist of VPN IPs.
    """

    def __init__(self, use_nftables=False):
        self.use_nftables = use_nftables
        self.blocked_ips = set()

    def fetch_vpn_ips(self):
        """
        Fetches the latest list of VPN IPs from a remote source.
        """
        try:
            print("[INFO] Fetching VPN IPs...")
            response = requests.get(VPN_IPS_URL)
            response.raise_for_status()
            ip_list = response.text.splitlines()
            print(f"[INFO] Fetched {len(ip_list)} VPN IPs.")
            return ip_list
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch VPN IPs: {e}")
            return []

    def block_ip(self, ip):
        """
        Blocks the given IP using iptables or nftables.
        """
        if ip in self.blocked_ips:
            print(f"[INFO] IP {ip} is already blocked.")
            return

        try:
            if self.use_nftables:
                subprocess.run(
                    ["nft", "add", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"],
                    check=True
                )
            else:
                subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            self.blocked_ips.add(ip)
            print(f"[INFO] Blocked IP: {ip}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to block IP {ip}: {e}")

    def update_blocklist(self):
        """
        Updates the blocklist with the latest VPN IPs.
        """
        vpn_ips = self.fetch_vpn_ips()
        for ip in vpn_ips:
            self.block_ip(ip)

    def list_blocked_ips(self):
        """
        Lists all blocked VPN IPs.
        """
        print("[INFO] Blocked VPN IPs:")
        for ip in self.blocked_ips:
            print(ip)

def main():
    """
    Main function to manage the VPN blocklist.
    """
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root. Please use sudo.")
        return

    manager = VPNBlocklistManager(use_nftables=False)  # Set to True for nftables

    print("[INFO] VPN Blocklist Manager initialized.")
    print("Available commands:")
    print("  1. Update Blocklist")
    print("  2. List Blocked IPs")
    print("  3. Exit")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                manager.update_blocklist()
            elif choice == 2:
                manager.list_blocked_ips()
            elif choice == 3:
                print("[INFO] Exiting VPN Blocklist Manager.")
                break
            else:
                print("[ERROR] Invalid choice. Please try again.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")


if __name__ == "__main__":
    main()