# ==============================
# CONFIGURATION
# ==============================
$SNORT_PATH   = "C:\Snort\bin\snort.exe"
CONFFILE     = ".\modules\Snort_Config\windows\snort.conf"
$CONF_FILE    = "C:\Snort\etc\snort.conf"
$RULE_PATH    = ".\rules\generated"
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
Get-ChildItem $RULE_PATH -Filter "*.rules" | ForEach-Object { Write-Host $_.BaseName -ForegroundColor Cyan }

# ==============================
# VIEW ADAPTERS
# ==============================
Write-Host "[2.2] Viewing Adapters..." -ForegroundColor Green
& $SNORT_PATH -W


#=============================
# Edit snort.conf to include custom rules
#=============================
Copy-Item $CONFFILE "$CONF_FILE" -Force
$confContent = Get-Content "$CONF_FILE"
$customRules = Get-ChildItem $RULE_PATH -Filter "*.rules" | ForEach-Object { "include $($_.FullName)" }
$confContent += $customRules
Set-Content $CONF_FILE -Value $confContent
Write-Host "Custom rules included in snort.conf" -ForegroundColor Yellow

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
Copy-Item $LOG_DIR.(Get-Date)
Write-Host "File save for Rotation" -ForegroundColor Yellow

Get-ChildItem $LOG_DIR -File |
Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$DAYSofVALID) } |
Remove-Item -Force

Write-Host "Old logs cleaned. and Rotated" -ForegroundColor Yellow
Write-Host "=== Snort completed ===" -ForegroundColor Green
