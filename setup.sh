#!/bin/bash

echo "🚂 Railway Document Intelligence System - Development Setup"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed or not in PATH"
    echo "Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

echo "✅ Python and Node.js detected"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

echo ""
echo "✅ All dependencies installed successfully!"
echo ""
echo "🚀 To start the application:"
echo "   1. Backend:  python3 app.py"
echo "   2. Frontend: npm run dev"
echo ""
echo "📋 Don't forget to:"
echo "   1. Create a .env file with your GITHUB_TOKEN"
echo "   2. Install Tesseract OCR for text extraction"
echo ""
echo "🧪 To test the system: python3 test_system.py"
echo ""