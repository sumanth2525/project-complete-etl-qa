# Bank Statement ETL Application - PowerShell Startup Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Bank Statement ETL Application - Starting..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask" 2>&1 | Out-Null
    Write-Host "Dependencies OK" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Flask Server..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Application will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Start the Flask application
python app.py

Read-Host "Press Enter to exit"

