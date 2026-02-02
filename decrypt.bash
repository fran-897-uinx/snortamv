#!/usr/bin/env bash
set -euo pipefail

# ==============================
# Resolve paths
# ==============================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_DIR="$SCRIPT_DIR/lock"
SSLKEYLOGFILE="$LOCK_DIR/ssl.log.txt"

LOG_DIR="/var/log/snort"
OUT_DIR="/tmp/snort_decrypt"

COMBINED="$OUT_DIR/snort_combined.log"
HEXFILE="$OUT_DIR/snort_hex.txt"
PCAP="$OUT_DIR/snort_reconstruct.pcap"

# ==============================
# Prepare directories & files
# ==============================
mkdir -p "$LOCK_DIR" "$OUT_DIR"

if [ ! -f "$SSLKEYLOGFILE" ]; then
  touch "$SSLKEYLOGFILE"
  chmod 600 "$SSLKEYLOGFILE"
fi

# ==============================
# Banner & instructions
# ==============================
echo
echo "========================================"
echo "   🔐 SNORT TLS DECRYPTION TOOL"
echo "========================================"
echo
echo "[*] TLS key log file:"
echo "    $SSLKEYLOGFILE"
echo
echo "👉 IMPORTANT:"
echo "   Run this BEFORE opening your browser:"
echo "   export SSLKEYLOGFILE=\"$SSLKEYLOGFILE\""
echo

# ---- Dependency check ----
if ! command -v tshark >/dev/null 2>&1; then
  echo "[!] tshark not found"
  echo "Install Wireshark:"
  echo "  sudo apt install wireshark"
  exit 1
fi

# ==============================
# Check TLS key presence
# ==============================
if [ ! -s "$SSLKEYLOGFILE" ]; then
  echo "⚠ TLS key log is currently empty."
  echo "  Open your browser AFTER exporting SSLKEYLOGFILE"
  echo "  Visit HTTPS websites, then press ENTER."
  read -r
fi

if [ ! -s "$SSLKEYLOGFILE" ]; then
  echo "[!] Still no TLS keys detected."
  echo "    Cannot decrypt TLS traffic yet."
  exit 1
fi

echo "[✓] TLS keys detected."

# ==============================
# Select Snort log
# ==============================
echo
echo "Available Snort log files:"
ls -lh "$LOG_DIR" | awk '{print $9}' | grep -E 'snort' || true
echo
read -rp "📂 Enter Snort log filename: eg. snort.log.192729972 " filename
FILEPATH="$LOG_DIR/$filename"

if [ ! -f "$FILEPATH" ]; then
  echo "[!] File not found: $FILEPATH"
  exit 1
fi

# ==============================
# Detect file type
# ==============================
FILETYPE=$(file "$FILEPATH")
echo "[*] File type: $FILETYPE"

if echo "$FILETYPE" | grep -qi "pcap"; then
  PCAP="$FILEPATH"
else
  echo "[*] Converting text log → PCAP"
  cat "$FILEPATH" > "$COMBINED"

  sed -nE 's/^[[:space:]]*[0-9A-Fa-f]{4}[[:space:]]+//p' "$COMBINED" \
    | sed -E 's/[[:space:]]{2,}.*$//' > "$HEXFILE"

  text2pcap -l 1 "$HEXFILE" "$PCAP"
fi

# ==============================
# Decrypt
# ==============================
echo
echo ">>> Showing first 200 decrypted packets"
tshark -o tls.keylog_file:"$SSLKEYLOGFILE" -r "$PCAP" -V | head -n 200

echo
echo "========================================"
echo "✅ DONE"
echo " PCAP : $PCAP"
echo " KEYS : $SSLKEYLOGFILE"
echo "========================================"
