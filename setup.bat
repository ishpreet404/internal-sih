@echo off
echo 🚂 Railway Document Intelligence System - Development Setup
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python and Node.js detected

REM Install Python dependencies
echo.
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

REM Install Node.js dependencies
echo.
echo 📦 Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully!
echo.
echo 🚀 To start the application:
echo    1. Backend:  python app.py
echo    2. Frontend: npm run dev
echo.
echo 📋 Don't forget to:
echo    1. Create a .env file with your GITHUB_TOKEN
echo    2. Install Tesseract OCR for text extraction
echo.
echo 🧪 To test the system: python test_system.py
echo.
pause