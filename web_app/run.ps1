# PowerShell script to run the Financial Planner app with comprehensive error handling
Write-Host "🏦 Financial Planner AI - Stable Startup Script" -ForegroundColor Blue
Write-Host "=" * 60 -ForegroundColor Blue

# Function to check prerequisites
function Test-Prerequisites {
    Write-Host "🔧 Checking prerequisites..." -ForegroundColor Yellow
    
    # Check if we're in the right directory
    if (-not (Test-Path "app.py")) {
        Write-Host "❌ Error: app.py not found. Make sure you're in the web_app directory." -ForegroundColor Red
        return $false
    }
    
    # Check Python installation
    try {
        $pythonVersion = python --version 2>$null
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: Python not found. Please install Python 3.8+." -ForegroundColor Red
        return $false
    }
    
    # Check/create virtual environment
    if (-not (Test-Path "venv")) {
        Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
        try {
            python -m venv venv
            Write-Host "✓ Virtual environment created" -ForegroundColor Green
        } catch {
            Write-Host "❌ Error: Failed to create virtual environment" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ Virtual environment found" -ForegroundColor Green
    }
    
    return $true
}

# Function to setup environment
function Initialize-Environment {
    Write-Host "⚙️ Setting up environment..." -ForegroundColor Yellow
    
    # Activate virtual environment
    try {
        & .\venv\Scripts\Activate.ps1
        Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: Failed to activate virtual environment" -ForegroundColor Red
        return $false
    }
    
    # Check .env file
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Write-Host "📄 Creating .env from template..." -ForegroundColor Yellow
            Copy-Item ".env.example" ".env"
            Write-Host "⚠️  Please edit .env and add your OPENAI_API_KEY" -ForegroundColor Yellow
            Write-Host "   Then run this script again." -ForegroundColor Yellow
            Start-Process notepad ".env"
            return $false
        } else {
            Write-Host "⚠️  No .env file found. Please set OPENAI_API_KEY manually:" -ForegroundColor Yellow
            Write-Host '   $env:OPENAI_API_KEY="your-key-here"' -ForegroundColor Cyan
        }
    }
    
    # Check API key
    if (-not $env:OPENAI_API_KEY) {
        Write-Host "❌ OPENAI_API_KEY not set. Please set your API key first." -ForegroundColor Red
        return $false
    } else {
        Write-Host "✓ OpenAI API key configured" -ForegroundColor Green
    }
    
    return $true
}

# Function to install dependencies
function Install-Dependencies {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    
    try {
        # Upgrade pip first
        python -m pip install --upgrade pip --quiet
        
        # Install requirements
        python -m pip install -r requirements.txt --quiet
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error: Failed to install dependencies" -ForegroundColor Red
        Write-Host "   Try running: pip install -r requirements.txt" -ForegroundColor Yellow
        return $false
    }
}

# Function to test the application
function Test-Application {
    Write-Host "🧪 Testing application..." -ForegroundColor Yellow
    
    try {
        python -c "
import flask, langchain, openai, reportlab, docx, numpy
from app import app
print('✓ All imports successful')
" 2>$null
        Write-Host "✓ Application test passed" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error: Application test failed" -ForegroundColor Red
        return $false
    }
}

# Main execution
try {
    # Run all checks
    if (-not (Test-Prerequisites)) { exit 1 }
    if (-not (Initialize-Environment)) { exit 1 }
    if (-not (Install-Dependencies)) { exit 1 }
    if (-not (Test-Application)) { exit 1 }
    
    # Start the application
    Write-Host ""
    Write-Host "🚀 Starting Financial Planner AI..." -ForegroundColor Green
    Write-Host "🌐 Server will be available at: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "📖 Documentation: See docs/ folder" -ForegroundColor Cyan
    Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    
    # Use the stable startup script
    python start.py
    
} catch {
    Write-Host ""
    Write-Host "❌ Startup failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Ensure you have Python 3.8+ installed" -ForegroundColor White
    Write-Host "2. Set your OpenAI API key in .env file" -ForegroundColor White
    Write-Host "3. Run from the web_app directory" -ForegroundColor White
    Write-Host "4. Check error messages above" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
