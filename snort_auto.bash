#!/usr/bin/env bash
set -euo pipefail

# ==============================
# CONFIGURATION
# ==============================
SNORT_PATH="/usr/sbin/snort"
CONF_FILE="/etc/snort/snort.conf"
RULE_PATH="/etc/snort/rules/local.rules"
LOG_DIR="/var/log/snort"
LOG_DOC="/var/log/snort/log_doc/log_file.log"
INTERFACE="eth0"
DAYSofVALID="7"
# ==============================

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

# AIM
echo -e "${YELLOW}[0] What is your AIM please:${RESET}"
read -r AIM

echo
echo -e "${GREEN}[1] Checking Snort Version...${RESET}"
$SNORT_PATH -V || { echo -e "${RED}Snort not found!${RESET}"; exit 1; }

# Ensure directories
mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$LOG_DOC")"

# Update rules
echo -e "${GREEN}[2] Updating custom rules...${RESET}"
cat >"$RULE_PATH" <<EOF
alert icmp any any -> any any (msg:"ICMP ping Detected"; sid:1000001; rev:2;)
alert tcp any any -> any 80 (msg:"TCP trace Detected"; sid:1000002; rev:1;)
alert udp any any -> any 53 (msg:"UDP query Detected"; sid:1000003; rev:3;)
EOF

echo -e "${YELLOW}RULES UPDATED:${RESET}"
cat "$RULE_PATH"

# Validate config
echo -e "${GREEN}[2.1] Validating Snort config...${RESET}"
$SNORT_PATH -T -c "$CONF_FILE"

# Run Snort
echo -e "${GREEN}[3] Running Snort...${RESET}"
$SNORT_PATH -i "$INTERFACE" -c "$CONF_FILE" -A console -l "$LOG_DIR"

# Read alerts
ALERT_FILE="$LOG_DIR/alert_fast"
echo -e "${GREEN}[4] Reading alert logs...${RESET}"
if [ -f "$ALERT_FILE" ]; then
    cat "$ALERT_FILE"
else
    echo -e "${YELLOW}No alerts yet.${RESET}"
fi

# Log activity
cat >>"$LOG_DOC" <<EOF
-----------------------------------
Week: $(date +%A)
Month: $(date +%B)
Time: $(date +%r)
User: $(whoami)
Date: $(date +%c)
Reason: $AIM
-----------------------------------
EOF

echo -e "${YELLOW}Log documentation updated.${RESET}"

# Cleanup old logs
echo -e "${GREEN}[6] Deleting logs older than $DAYSofVALID days...${RESET}"
find "$LOG_DIR" -type f -mtime +"$DAYSofVALID" -delete
echo -e "${YELLOW}Old logs cleaned.${RESET}"

echo -e "${GREEN}=== SNORT COMPLETED SUCCESSFULLY ===${RESET}"
