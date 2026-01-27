#!/bin/bash

# CONFIGURATION
SNORT_PATH="C:\Snort\bin\snort.exe"
CONF_FILE="C:\Snort\etc\snort.conf"
RULE_PATH="C:\Snort\rules\local.rules"
LOG_DIR="C:\Snort\log"
LOG_DOC="C:\Snort\log_doc\log_file.log"
INTERFACE="4"
# EMAIL=""
DAYSofVALID="7"

# colors of output
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

 echo -e "${YELLOW} [0] what is your AIM please....:${RESET}"
read AIM

echo 
echo -e "${GREEN}[1] checking Snort Version...${RESET}"
"$SNORT_PATH" -V || { echo -e "${RED} Snort not found! check SNORT_PATH.${RESET}"; exit 1; }

# update / defining snort
echo -e "${GREEN}[2] Updating custom rules...${RESET}"

cat >"$RULE_PATH" << 'EOF'
alert icmp any any -> any any (msg:"ICMP ping Detected"; sid:1000001; rev:2;)

alert tcp any any -> any 80 (msg:"TCP trace Detected"; sid:1000002; rev:1;)

alert udp any any -> any 53 (msg:"UDP query Detected"; sid:1000003; rev:3;)
EOF

echo -e "${YELLOW}RULES UPDATED:${RESET}"

cat "$RULE_PATH"

# Viewing adapters 
echo -e "${GREEN}[2.2] Viewing Adapters...${RESET}"
"$SNORT_PATH" -W || { echo -e "${RED} Snort no adapter to view ! check SNORT_PATH.${RESET}"; exit 1; }


# runing snort with rule file
echo -e "${GREEN}[3] Running Snort...${RESET}"
"$SNORT_PATH" -c "$CONF_FILE" -i "$INTERFACE" -A console -l "$LOG_DIR"
if [ $? -ne 0 ]; then 
    echo -e "${RED}Error running Snort!${RESET}"
    exit 1
fi 


# displaying Logs 
echo -e "${GREEN}[4] Reading alert logs...${RESET}"
ALERT_FILE="$LOG_DIR/alert_fast"
if [ -f "$ALERT_FILE" ]; then 
    echo -e "${YELLOW}---Snort Alerts---${RESET}"
    cat "$ALERT_FILE"
else 
    echo -e "${RED}No Alert logs found yet.${RESET}"
fi 

# adding info of who loged
cat >>"$LOG_DOC" << EOF
-----------------------------------

Week:$(date +%A)
Month:$(date +%B)
Time:$(date +%r)
Name: $USERNAME                  
Date:$(date +%c)
Reason: $AIM
-----------------------------------
EOF
echo -e "${YELLOW}Logs UPDATED:${RESET}"


# Rotate old logs / delete logs 
echo -e "${GRREN}[6] Deleting old logs older than ${DAYSofVALID} days...${RESET}"
find "$LOG_DIR" -type f -mtime +$DAYSofVALID -delete 
echo -e "${YELLOW}Old logs Cleaned.${RESET}"

echo -e "${GREEN}=== snort completed ===${RESET}"

