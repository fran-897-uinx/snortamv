#!/usr/bin/env bash
set -euo pipefail

# >>> Configure these paths <<<
LOG_DIR="/mnt/c/Snort/log"                       # Snort log directory
SSLKEYLOGFILE="/mnt/c/Users/DELL/Downloads/ssl.log.txt"  # Path to your SSL key log
OUT_DIR="/tmp/snort_decrypt"                     # Temporary output directory
# <<< end config >>>

mkdir -p "$OUT_DIR"
COMBINED="$OUT_DIR/snort_combined.log"
HEXFILE="$OUT_DIR/snort_hex.txt"
PCAP="$OUT_DIR/snort_reconstruct.pcap"

echo
echo "========================================"
echo "   🔐 SNORT TRAFFIC DECRYPTION SCRIPT   "
echo "========================================"
echo
echo "[*] LOG_DIR: $LOG_DIR"
echo "[*] SSLKEYLOGFILE: $SSLKEYLOGFILE"
echo "[*] Output dir: $OUT_DIR"
echo
echo "Available log files:"
ls -lh "$LOG_DIR" | awk '{print $9}' | grep -E 'snort' || true
echo
read -rp "📂 Enter the filename you want to decrypt (from above): " filename
FILEPATH="$LOG_DIR/$filename"

if [ ! -f "$FILEPATH" ]; then
  echo "[!] File not found: $FILEPATH"
  exit 1
fi

echo
echo "[*] Checking file type..."
FILETYPE=$(file "$FILEPATH")
echo "[*] File type: $FILETYPE"
echo

# --- CASE 1: Binary log (already PCAP) ---
if echo "$FILETYPE" | grep -qi "pcap"; then
  echo "[*] Detected binary Snort log (.pcap format). Skipping hex extraction."
  PCAP="$FILEPATH"

# --- CASE 2: Text log (console dump) ---
else
  echo "[*] Detected text Snort log. Extracting hex bytes..."
  cat "$FILEPATH" > "$COMBINED"

  sed -nE 's/^[[:space:]]*[0-9A-Fa-f]{4}[[:space:]]+//p' "$COMBINED" \
    | sed -E 's/[[:space:]]{2,}.*$//' > "$HEXFILE"

  if [ ! -s "$HEXFILE" ]; then
    echo "[!] No hex bytes found in $COMBINED."
    echo "[!] This might be a binary log — or not a valid hex dump."
    exit 2
  fi

  echo "[*] Converting hex -> PCAP..."
  text2pcap -l 1 "$HEXFILE" "$PCAP"

  if [ ! -s "$PCAP" ]; then
    echo "[!] text2pcap failed to create pcap. Exiting."
    exit 3
  fi
fi

# --- Decryption step ---
echo
echo "[*] Decrypting traffic using SSL key log..."
if [ ! -f "$SSLKEYLOGFILE" ]; then
  echo "[!] SSL key log not found at $SSLKEYLOGFILE"
  echo "    You must provide the key log from your browser or client."
  exit 4
fi
echo clear
echo
echo ">>> Showing first 200 lines of decrypted packets:"
tshark -o tls.keylog_file:"$SSLKEYLOGFILE" -r "$PCAP" -V | head -n 200

echo
echo "========================================"
echo "✅ DONE — OUTPUT FILES:"
echo "  - PCAP: $PCAP"
echo "  - SSLKEYLOGFILE: $SSLKEYLOGFILE"
echo "  - TEMP DIR: $OUT_DIR"
echo "========================================"
echo
echo "👉 To open in Wireshark (GUI):"
echo "    wireshark \"$PCAP\" &"
echo "Then go to:"
echo "    Edit → Preferences → Protocols → TLS →"
echo "    (Pre)-Master-Secret log filename → select $SSLKEYLOGFILE"
echo
