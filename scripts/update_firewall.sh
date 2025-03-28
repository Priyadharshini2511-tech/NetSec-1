#!/bin/bash

# File: scripts/update_firewall.sh

# Purpose: Automates firewall rule updates.

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
  echo "[ERROR] This script must be run as root. Please use sudo."
  exit 1
fi

# Configuration
USE_NFTABLES=false # Set to true if using nftables
RULES_FILE="/etc/firewall/rules.conf" # Path to the rules configuration file
BACKUP_DIR="/var/backups/firewall"   # Directory to store backups

# Functions
backup_firewall_rules() {
  echo "[INFO] Backing up current firewall rules..."
  mkdir -p "$BACKUP_DIR"

  if $USE_NFTABLES; then
    nft list ruleset > "$BACKUP_DIR/nftables_rules_$(date +%F_%T).bak"
  else
    iptables-save > "$BACKUP_DIR/iptables_rules_$(date +%F_%T).bak"
  fi

  echo "[INFO] Backup completed."
}

apply_firewall_rules() {
  echo "[INFO] Applying firewall rules from $RULES_FILE..."

  if [[ ! -f $RULES_FILE ]]; then
    echo "[ERROR] Rules file not found: $RULES_FILE"
    exit 1
  fi

  if $USE_NFTABLES; then
    nft -f "$RULES_FILE"
  else
    iptables-restore < "$RULES_FILE"
  fi

  echo "[INFO] Firewall rules applied successfully."
}

list_firewall_rules() {
  echo "[INFO] Current firewall rules:"
  if $USE_NFTABLES; then
    nft list ruleset
  else
    iptables -L -v -n
  fi
}

flush_firewall_rules() {
  echo "[INFO] Flushing all firewall rules..."
  if $USE_NFTABLES; then
    nft flush ruleset
  else
    iptables -F
  fi
  echo "[INFO] All rules flushed."
}

# Main Script
echo "[INFO] Firewall Update Script Initialized."

# Parse options
while getopts "bafl" opt; do
  case $opt in
    b)
      backup_firewall_rules
      ;;
    a)
      apply_firewall_rules
      ;;
    f)
      flush_firewall_rules
      ;;
    l)
      list_firewall_rules
      ;;
    *)
      echo "[ERROR] Invalid option. Use -b (backup), -a (apply), -f (flush), or -l (list)."
      exit 1
      ;;
  esac
done

if [[ $OPTIND -eq 1 ]]; then
  echo "[INFO] Usage: $0 [-b] [-a] [-f] [-l]"
  echo "  -b : Backup current firewall rules"
  echo "  -a : Apply rules from $RULES_FILE"
  echo "  -f : Flush all firewall rules"
  echo "  -l : List current firewall rules"
fi

echo "[INFO] Script completed."