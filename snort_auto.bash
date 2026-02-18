#!/usr/bin/env bash
set -euo pipefail

# ==============================
# CONFIGURATION
# ==============================
SNORT_PATH="/usr/sbin/snort"
RULE_PATH="./rules/local.rules"
LOG_DIR="/var/log/snortamv"
LOG_DOC="$LOG_DIR/log_file.log"
INTERFACE="eth0"
DAYS_OF_VALID=7

# ==============================
# COLORS
# ==============================
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

# ==============================
# ASK AIM
# ==============================
echo -e "${YELLOW}[0] What is your AIM please:${RESET}"
read -r AIM

# ==============================
# DETECT SNORT VERSION
# ==============================
if ! command -v "$SNORT_PATH" >/dev/null 2>&1; then
    echo -e "${RED}Snort not found at $SNORT_PATH!${RESET}"
    exit 1
fi

SNORT_VERSION=$($SNORT_PATH -V 2>/dev/null | head -n1)
if echo "$SNORT_VERSION" | grep -q "Snort++"; then
    SNORT_TYPE="snort3"
    SNORT_CONF="/etc/snort/snort.lua"
else
    SNORT_TYPE="snort2"
    SNORT_CONF="/etc/snort/snort.conf"
fi

# ==============================
# ENSURE CONFIG EXISTS
# ==============================
if [ ! -f "$SNORT_CONF" ]; then
    echo -e "${YELLOW}Snort config not found, generating default...${RESET}"
    sudo mkdir -p "$(dirname "$SNORT_CONF")"
    if [ "$SNORT_TYPE" == "snort3" ]; then
        sudo tee "$SNORT_CONF" > /dev/null <<EOF
-- Default snort.lua for SnortAMV
ips =
{
  rules = '$(realpath "$RULE_PATH")'
}
EOF
    else
        sudo tee "$SNORT_CONF" > /dev/null <<EOF
# Default snort.conf for SnortAMV
include $(realpath "$RULE_PATH")
EOF
    fi
    sudo chown root:root "$SNORT_CONF"
    echo -e "${GREEN}Default config created at $SNORT_CONF${RESET}"
fi

# ==============================
# ENSURE LOG DIR EXISTS
# ==============================
mkdir -p "$LOG_DIR"

# ==============================
# SHOW RULES
# ==============================
echo -e "${YELLOW}RULES UPDATED:${RESET}"
if [ -f "$RULE_PATH" ]; then
    cat "$RULE_PATH"
else
    echo -e "${RED}No rules found at $RULE_PATH${RESET}"
fi

# ==============================
# VALIDATE CONFIG
# ==============================
echo -e "${GREEN}[2.1] Validating Snort config...${RESET}"
if ! $SNORT_PATH -T -c "$SNORT_CONF"; then
    echo -e "${RED}Configuration test failed!${RESET}"
    exit 1
fi

# ==============================
# RUN SNORT
# ==============================
echo -e "${GREEN}[3] Running Snort...${RESET}"
$SNORT_PATH -i "$INTERFACE" -c "$SNORT_CONF" -A console -l "$LOG_DIR"

# ==============================
# READ ALERTS
# ==============================
ALERT_FILE="$LOG_DIR/alert_fast"
echo -e "${GREEN}[4] Reading alert logs...${RESET}"
if [ -f "$ALERT_FILE" ]; then
    cat "$ALERT_FILE"
else
    echo -e "${YELLOW}No alerts yet.${RESET}"
fi

# ==============================
# LOG ACTIVITY
# ==============================
echo >>"$LOG_DOC"
echo "-----------------------------------" >>"$LOG_DOC"
echo "Week: $(date +%A)" >>"$LOG_DOC"
echo "Month: $(date +%B)" >>"$LOG_DOC"
echo "Time: $(date +%r)" >>"$LOG_DOC"
echo "User: $(whoami)" >>"$LOG_DOC"
echo "Date: $(date +%c)" >>"$LOG_DOC"
echo "Reason: $AIM" >>"$LOG_DOC"
echo "-----------------------------------" >>"$LOG_DOC"
cat "$LOG_DOC"
echo -e "${YELLOW}Log documentation updated.${RESET}"

# ==============================
# CLEANUP OLD LOGS
# ==============================
echo -e "${GREEN}[6] Deleting logs older than $DAYS_OF_VALID days...${RESET}"
find "$LOG_DIR" -type f -mtime +"$DAYS_OF_VALID" -delete
echo -e "${YELLOW}Old logs cleaned.${RESET}"

echo -e "${GREEN}=== SNORT COMPLETED SUCCESSFULLY ===${RESET}"
