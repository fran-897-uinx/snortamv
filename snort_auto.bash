#!/usr/bin/env bash
set -euo pipefail

# ==============================
# CONFIGURATION
# ==============================
SNORT_PATH="/usr/sbin/snort"
RULE_PATH="./rules/local.rules"
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

SNORT_VERSION=$($SNORT_PATH -V 2>/dev/null | head -n1)
if echo "$SNORT_VERSION" | grep -q "Snort++"; then
    SNORT_TYPE="snort3"
    SNORT_CONF="/etc/snort/snort.lua"
else
    SNORT_TYPE="snort2"
    SNORT_CONF="/etc/snort/snort.conf"
fi
echo
echo -e "${GREEN}[1] Checking Snort Version...${RESET}"
$SNORT_PATH -V || { echo -e "${RED}Snort not found!${RESET}"; exit 1; }

# Ensure directories
mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$LOG_DOC")"

echo -e "${YELLOW}RULES UPDATED:${RESET}"
cat "$RULE_PATH"
echo -e "${GREEN}[2.1] Validating Snort config...${RESET}"
$SNORT_PATH -T -c "$SNORT_CONF" || { echo -e "${RED}Configuration test failed!${RESET}"; exit 1; }

# Run Snort
echo -e "${GREEN}[3] Running Snort...${RESET}"
$SNORT_PATH -i "$INTERFACE" -c "$SNORT_CONF" -A console -l "$LOG_DIR"

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
