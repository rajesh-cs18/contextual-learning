#!/bin/bash

# Theory2Practice AI Bridge - Quick Start Script
# This script sets up and runs the application

set -e

echo "🎓 Theory2Practice AI Bridge - Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  IMPORTANT: Configure your API key!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Get your Gemini API key from:"
    echo "   https://makersuite.google.com/app/apikey"
    echo ""
    echo "2. Edit the .env file and add your API key:"
    echo "   GEMINI_API_KEY=your_actual_key_here"
    echo ""
    read -p "Press Enter once you've added your API key to .env..."
else
    echo "✓ .env file found"
fi
echo ""

# Verify API key is set
if grep -q "your_gemini_api_key_here" .env; then
    echo "❌ ERROR: API key not configured in .env file"
    echo "Please edit .env and add your actual Gemini API key"
    exit 1
fi

echo "✓ API key configured"
echo ""

# Launch the app
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Launching Theory2Practice AI Bridge..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "The app will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
