#!/usr/bin/env pwsh
# Financial Planner Web Application - Startup Script for PowerShell

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Financial Planner Web Application - Startup" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from template..."
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[INFO] .env created. Please edit it and add your OPENAI_API_KEY" -ForegroundColor Green
        Write-Host "[INFO] Opening .env file..." -ForegroundColor Green
        notepad.exe ".env"
        Write-Host "[INFO] After adding your API key, run this script again." -ForegroundColor Green
        Read-Host "Press Enter to exit"
        exit 1
    }
    else {
        Write-Host "[ERROR] .env.example not found!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Install/upgrade pip tooling first for compatibility
Write-Host "[INFO] Upgrading pip, setuptools, and wheel..." -ForegroundColor Green
python -m pip install --upgrade pip setuptools wheel --quiet

# Install project dependencies
Write-Host "[INFO] Installing dependencies..." -ForegroundColor Green
python -m pip install -r requirements.txt --quiet

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Starting Financial Planner Web Application" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening http://localhost:5000 in your browser..." -ForegroundColor Green
Write-Host ""

# Run the Flask app
python app.py
