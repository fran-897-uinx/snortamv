$ErrorActionPreference = "Stop"

# ================= CONFIG =================
$LogDir = "C:\Snort\log"
$KeyLog = "$PSScriptRoot\lock\ssl.log.txt"
$OutDir = "$env:TEMP\snort_decrypt"
# =========================================

Write-Host "=== Snort TLS Decrypt (Windows) ==="

# ---- Dependency check ----
$tshark = Get-Command tshark -ErrorAction SilentlyContinue
$text2pcap = Get-Command text2pcap -ErrorAction SilentlyContinue

if (-not $tshark) {
    Write-Host "Missing required tool: tshark.exe" -ForegroundColor Red
    Write-Host "Install Wireshark from:"
    Write-Host "https://www.wireshark.org/download.html"
    exit 1
}

if (-not $text2pcap) {
    Write-Host "Missing required tool: text2pcap.exe" -ForegroundColor Red
    Write-Host "Install Wireshark with TShark support."
    Write-Host "Install Wireshark from:"
    Write-Host "https://www.wireshark.org/download.html"
    exit 1
}

# ---- Prepare output ----
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Pcap = Join-Path $OutDir "snort_reconstruct.pcap"

# ---- TLS key log ----
if (-not (Test-Path $KeyLog)) {
    Write-Host "TLS key log not found at $KeyLog" -ForegroundColor Red
    Write-Host "Set SSLKEYLOGFILE in your browser."
    exit 1
}

# ---- Select Snort log ----
Write-Host "`nAvailable Snort logs:`n"
Get-ChildItem $LogDir | Where-Object Name -like "snort*" | Format-Table Name

$File = Read-Host "Enter Snort log filename"
$FilePath = Join-Path $LogDir $File

if (-not (Test-Path $FilePath)) {
    Write-Host "Snort log not found: $FilePath" -ForegroundColor Red
    exit 1
}

# ---- Convert or use PCAP ----
Write-Host "`n[*] Processing log..."

& tshark -r $FilePath -c 1 2>$null
if ($LASTEXITCODE -eq 0) {
    $Pcap = $FilePath
    Write-Host "Detected PCAP format"
} else {
    Write-Host "Detected text log → converting to PCAP"
    & text2pcap -l 1 $FilePath $Pcap
}

# ---- Decrypt ----
Write-Host "`n>>> Showing first 200 decrypted packets"
& tshark -o tls.keylog_file="$KeyLog" -r $Pcap -V | Select-Object -First 200

Write-Host "`n========================================"
Write-Host "DONE"
Write-Host "PCAP : $Pcap"
Write-Host "KEYS : $KeyLog"
Write-Host "========================================"
