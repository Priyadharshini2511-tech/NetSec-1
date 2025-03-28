import os
import subprocess
import time

class FirewallMonitor:
    """
    A class to monitor real-time changes in firewall rules.
    """

    def __init__(self, use_nftables=False, interval=5):
        """
        Initializes the monitor.
        Args:
            use_nftables: If True, monitors nftables rules; otherwise, monitors iptables.
            interval: Interval in seconds between checks.
        """
        self.use_nftables = use_nftables
        self.interval = interval
        self.previous_rules = ""

    def get_current_rules(self):
        """
        Retrieves the current firewall rules.
        Returns:
            A string containing the current rules.
        """
        try:
            if self.use_nftables:
                result = subprocess.run(
                    ["nft", "list", "ruleset"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                result = subprocess.run(
                    ["iptables", "-L", "-v", "-n"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to fetch firewall rules: {e.stderr}")
            return ""

    def monitor_changes(self):
        """
        Monitors the firewall for changes in rules.
        """
        print(f"[INFO] Monitoring firewall rules every {self.interval} seconds...")

        while True:
            try:
                current_rules = self.get_current_rules()
                if current_rules != self.previous_rules:
                    print("[INFO] Firewall rules have changed:")
                    print(current_rules)
                    self.previous_rules = current_rules
                time.sleep(self.interval)
            except KeyboardInterrupt:
                print("\n[INFO] Monitoring stopped by user.")
                break
            except Exception as e:
                print(f"[ERROR] An error occurred: {e}")
                break

def main():
    """
    Main function to start the FirewallMonitor.
    """
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root. Please use sudo.")
        return

    print("[INFO] Firewall Monitor initialized.")
    use_nftables = input("Use nftables? (yes/no): ").strip().lower() == "yes"
    interval = int(input("Enter monitoring interval (in seconds): "))

    monitor = FirewallMonitor(use_nftables=use_nftables, interval=interval)
    monitor.monitor_changes()

if __name__ == "__main__":
    main()