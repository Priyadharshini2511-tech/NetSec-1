import subprocess
import os


class FirewallManager:
    """
    A class to manage iptables and nftables rules.
    """

    def __init__(self, use_nftables=False):
        self.use_nftables = use_nftables

    def add_rule(self, rule):
        """
        Adds a rule to the firewall.
        """
        if self.use_nftables:
            self._execute_command(["nft", "add", "rule", "inet", "filter", "input"] + rule.split())
        else:
            self._execute_command(["iptables"] + rule.split())

    def delete_rule(self, rule):
        """
        Deletes a rule from the firewall.
        """
        if self.use_nftables:
            self._execute_command(["nft", "delete", "rule", "inet", "filter", "input"] + rule.split())
        else:
            self._execute_command(["iptables", "-D"] + rule.split())

    def list_rules(self):
        """
        Lists all rules in the firewall.
        """
        if self.use_nftables:
            self._execute_command(["nft", "list", "ruleset"])
        else:
            self._execute_command(["iptables", "-L"])

    def flush_rules(self):
        """
        Flushes all rules from the firewall.
        """
        if self.use_nftables:
            self._execute_command(["nft", "flush", "ruleset"])
        else:
            self._execute_command(["iptables", "-F"])

    def _execute_command(self, command):
        """
        Executes a command and handles errors.
        """
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Command failed: {' '.join(command)}")
            print(e.stderr)


def main():
    """
    Main function to interact with the FirewallManager.
    """
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root. Please use sudo.")
        return

    manager = FirewallManager(use_nftables=False)  # Set to True for nftables

    print("[INFO] Firewall Manager initialized.")
    print("Available commands:")
    print("  1. Add Rule")
    print("  2. Delete Rule")
    print("  3. List Rules")
    print("  4. Flush Rules")
    print("  5. Exit")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                rule = input("Enter the rule to add (e.g., '-A INPUT -s 1.2.3.4 -j DROP'): ")
                manager.add_rule(rule)
            elif choice == 2:
                rule = input("Enter the rule to delete (e.g., '-A INPUT -s 1.2.3.4 -j DROP'): ")
                manager.delete_rule(rule)
            elif choice == 3:
                print("[INFO] Current Rules:")
                manager.list_rules()
            elif choice == 4:
                confirm = input("Are you sure you want to flush all rules? (yes/no): ")
                if confirm.lower() == "yes":
                    manager.flush_rules()
                    print("[INFO] All rules flushed.")
            elif choice == 5:
                print("[INFO] Exiting Firewall Manager.")
                break
            else:
                print("[ERROR] Invalid choice. Please try again.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")


if __name__ == "__main__":
    main()