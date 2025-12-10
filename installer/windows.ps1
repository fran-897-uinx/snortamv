Write-Host "🔍 Detecting Windows environment..." -ForegroundColor Cyan

# Allow script execution
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force


# ============================================================
# Function: Install If Missing
# ============================================================

function Install-IfMissing($command, $wingetId) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {

        if (Get-Command "winget" -ErrorAction SilentlyContinue) {
            Write-Host "📦 Installing $command..." -ForegroundColor Yellow
            winget install -e --id $wingetId --silent
        }
        else {
            Write-Host "❌ winget not available. Install $command manually." -ForegroundColor Red
            exit 1
        }

    } else {
        Write-Host "✔ $command already installed." -ForegroundColor Green
    }
}


# ============================================================
# Install Required Dependencies
# ============================================================

Install-IfMissing "python" "Python.Python.3"
Install-IfMissing "git" "Git.Git"


# ============================================================
# Install SnortAMV CLI
# ============================================================

Write-Host "⬇ Downloading SnortAMV..." -ForegroundColor Yellow

$installPath = "$env:USERPROFILE\.snortamv"
New-Item -ItemType Directory -Force -Path $installPath | Out-Null

# Download CLI (replace with your real URL)
Invoke-WebRequest `
    -Uri "https://your-domain.com/snortamv.py" `
    -OutFile "$installPath\snortamv.py"

# Set executable permission
attrib +x "$installPath\snortamv.py"


# ============================================================
# Add to PATH
# ============================================================

$envPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($envPath -notlike "*$installPath*") {
    Write-Host "🔧 Adding SnortAMV to PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("Path", "$envPath;$installPath", "User")
} else {
    Write-Host "✔ PATH already configured." -ForegroundColor Green
}


Write-Host "🎉 SnortAMV installed successfully!" -ForegroundColor Green


# ============================================================
# Verify Installation
# ============================================================

Write-Host "🔎 Verifying installation..." -ForegroundColor Cyan

$checkCmd = "python `"$installPath\snortamv.py`" --version"

try {
    Invoke-Expression $checkCmd
}
catch {
    Write-Host "⚠ Unable to run snortamv.py automatically. Try opening a new terminal." -ForegroundColor Yellow
}
