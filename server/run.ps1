# Run script for Social Connect Backend
# This script activates the virtual environment and starts the Flask server

Write-Host "Starting Social Connect Backend..." -ForegroundColor Green

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Yellow
} else {
    Write-Host "Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit
}

# Start Flask server
Write-Host "Starting Flask server on http://localhost:5000..." -ForegroundColor Cyan
python app.py
