# Android Game AI Bot - PowerShell Setup Script
# Usage: .\setup.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Android Game AI Bot - Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check Python
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Step 2: Create venv
Write-Host "`n[2/4] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Step 3: Activate venv
Write-Host "`n[3/4] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "`n[4/4] Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip setuptools wheel | Out-Null
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! ✅" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📚 Next steps:" -ForegroundColor Yellow
Write-Host "1. Read SETUP.md for detailed configuration"
Write-Host "2. Edit game_ai_bot/config.py:"
Write-Host "   - Set GRID_TOP_LEFT (measure from screenshot)"
Write-Host "   - Set GRID_CELL_SIZE"
Write-Host "   - Adjust COLOR_THRESHOLDS"
Write-Host "3. Enable USB Debugging on Android device"
Write-Host "4. Connect device via USB"
Write-Host "5. Run: python -m game_ai_bot.main`n"

Write-Host "🚀 Ready to develop! Good luck! 🎮`n" -ForegroundColor Green
