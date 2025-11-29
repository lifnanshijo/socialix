# Setup script for Social Connect Backend
# Run this script to set up the virtual environment and install dependencies

Write-Host "Setting up Social Connect Backend..." -ForegroundColor Green

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To start the server, run: python app.py" -ForegroundColor Cyan
