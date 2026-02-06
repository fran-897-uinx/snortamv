# ==============================
# CONFIGURATION
# ==============================
$SNORT_PATH   = "C:\Snort\bin\snort.exe"
$CONF_FILE    = "C:\Snort\etc\snort.conf"
$RULE_PATH    = ".\rules\local.rules"
$LOG_DIR      = "C:\Snort\log"
$LOG_DOC      = "C:\Snort\log_doc\log_file.log"
$INTERFACE    = "4"
$DAYSofVALID  = 7

# ==============================
# USER INPUT
# ==============================

Write-Host "[0] What is your AIM please..." -ForegroundColor Blue
$AIM = Read-Host

# ==============================
# CHECK SNORT VERSION
# ==============================
Write-Host "[1] Checking Snort Version..." -ForegroundColor Green
if (!(Test-Path $SNORT_PATH)) {
    Write-Host "Snort not found! Check SNORT_PATH." -ForegroundColor Red
    exit 1
}
& $SNORT_PATH -V

# ==============================
# UPDATE RULES
# ==============================
Write-Host "[2] Updating custom rules..." -ForegroundColor Green



Write-Host "RULES UPDATED:" -ForegroundColor Yellow
Get-Content $RULE_PATH

# ==============================
# VIEW ADAPTERS
# ==============================
Write-Host "[2.2] Viewing Adapters..." -ForegroundColor Green
& $SNORT_PATH -W

# ==============================
# RUN SNORT
# ==============================
Write-Host "[3] Running Snort..." -ForegroundColor Green
& $SNORT_PATH -c $CONF_FILE -i $INTERFACE -A console -l $LOG_DIR

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error running Snort!" -ForegroundColor Red
    exit 1
}

# ==============================
# READ ALERT LOGS
# ==============================
Write-Host "[4] Reading alert logs..." -ForegroundColor Green
$ALERT_FILE = Join-Path $LOG_DIR "alert_fast"

if (Test-Path $ALERT_FILE) {
    Write-Host "--- Snort Alerts ---" -ForegroundColor Yellow
    Get-Content $ALERT_FILE
} else {
    Write-Host "No Alert logs found yet." -ForegroundColor Red
}

# ==============================
# WRITE AUDIT LOG
# ==============================
$logEntry = @"
-----------------------------------
Week:   $(Get-Date -Format dddd)
Month:  $(Get-Date -Format MMMM)
Time:   $(Get-Date -Format T)
Name:   $env:USERNAME
Date:   $(Get-Date)
Reason: $AIM
-----------------------------------
"@

Add-Content -Path $LOG_DOC -Value $logEntry
Write-Host "Logs UPDATED." -ForegroundColor Yellow

# ==============================
# DELETE OLD LOGS
# ==============================
Write-Host "[6] Deleting logs older than $DAYSofVALID days..." -ForegroundColor Green

Get-ChildItem $LOG_DIR -File |
Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$DAYSofVALID) } |
Remove-Item -Force

Write-Host "Old logs cleaned." -ForegroundColor Yellow
Write-Host "=== Snort completed ===" -ForegroundColor Green
