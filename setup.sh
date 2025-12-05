#!/bin/bash

echo "🚀 PolicySwarm - Auto Setup Script"
echo "=================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Install with: brew install ollama"
    echo "   Then run: ollama pull gemma3:12b"
fi

echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "virtualpyenv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv virtualpyenv
fi

# Activate and install dependencies
echo "Installing Python dependencies..."
source virtualpyenv/bin/activate
pip install --quiet -r requirements.txt

cd ..

echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Install npm dependencies
echo "Installing Node dependencies..."
npm install --silent

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Ensure Ollama is running: ollama serve"
echo "2. Start the application: ./start.sh"
echo "3. Open http://localhost:3001 in your browser"
echo ""
