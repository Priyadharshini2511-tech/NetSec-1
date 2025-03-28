import os
import subprocess
from scapy.all import IP, TCP, send

class TCPResetManager:
    """
    A class to send TCP resets to terminate malicious connections.
    """

    def __init__(self):
        if os.geteuid() != 0:
            raise PermissionError("[ERROR] This script must be run as root. Please use sudo.")

    def send_tcp_reset(self, src_ip, src_port, dst_ip, dst_port, seq, ack):
        """
        Sends a TCP reset packet to terminate a connection.
        Args:
            src_ip: Source IP address of the malicious connection.
            src_port: Source port of the malicious connection.
            dst_ip: Destination IP address.
            dst_port: Destination port.
            seq: Sequence number for the TCP packet.
            ack: Acknowledgment number for the TCP packet.
        """
        try:
            # Build the TCP reset packet
            ip_layer = IP(src=src_ip, dst=dst_ip)
            tcp_layer = TCP(sport=src_port, dport=dst_port, flags="R", seq=seq, ack=ack)
            packet = ip_layer / tcp_layer

            # Send the packet
            send(packet, verbose=False)
            print(f"[INFO] Sent TCP reset from {src_ip}:{src_port} to {dst_ip}:{dst_port}")
        except Exception as e:
            print(f"[ERROR] Failed to send TCP reset: {e}")

def main():
    """
    Main function to manage TCP reset actions.
    """
    manager = TCPResetManager()

    print("[INFO] TCP Reset Manager initialized.")
    print("Available commands:")
    print("  1. Send TCP Reset")
    print("  2. Exit")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                src_ip = input("Enter source IP address: ")
                src_port = int(input("Enter source port: "))
                dst_ip = input("Enter destination IP address: ")
                dst_port = int(input("Enter destination port: "))
                seq = int(input("Enter TCP sequence number: "))
                ack = int(input("Enter TCP acknowledgment number: "))

                manager.send_tcp_reset(src_ip, src_port, dst_ip, dst_port, seq, ack)
            elif choice == 2:
                print("[INFO] Exiting TCP Reset Manager.")
                break
            else:
                print("[ERROR] Invalid choice. Please try again.")
        except ValueError:
            print("[ERROR] Please enter valid inputs.")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()