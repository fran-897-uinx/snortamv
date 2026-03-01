#!/usr/bin/env bash
set -euo pipefail

# ==============================
# CONFIGURATION
# ==============================
SNORT_PATH="/usr/sbin/snort"
RULE_PATH="./rules/generated"
LOG_DIR="/var/log/snortamv"
LOG_DOC="$LOG_DIR/log_file.log"
SNORTCONF="./modules/Snort_Config/linux/snort.conf"
SNORTLUA="./modules/Snort_Config/linux/snort.lua"
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
        sudo cp "$SNORTLUA" "$SNORT_CONF"
    else
         sudo cp "$SNORTCONF" "$SNORT_CONF"
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
if [ -d "$RULE_PATH" ]; then
    cat "$RULE_PATH/snort.rules"
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
# VALIDATE RULES   
# ==============================
echo -e "${GREEN}[2.1] Validating Snort rules...${RESET}"
if ! $SNORT_PATH -T -c "$SNORT_CONF" -R "$RULE_PATH"; then
    echo -e "${RED}Configuration test failed!${RESET}"
    exit 1
fi

# ==============================
# View Adapters
# ==============================
echo -e "${GREEN}[1.1] Available network interfaces:${RESET}"
ip link show type ether
$SNORT_PATH --daq-dir /usr/lib/snort/ -W

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
find "$LOG_DIR" -type f -mtime +"$DAYS_OF_VALID" -exec cp $LOG_DIR $LOG_DIR.((date +%Y%m%d%H%M%S))
find "$LOG_DIR" -type f -mtime +"$DAYS_OF_VALID" -delete
echo -e "${YELLOW}Old logs cleaned.${RESET}"

echo -e "${GREEN}=== SNORT COMPLETED SUCCESSFULLY ===${RESET}"
