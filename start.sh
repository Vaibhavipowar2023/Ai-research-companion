#!/bin/bash

# Quick Start Script for AI Research Companion
# This script helps you set up and run the project locally

echo "🔬 AI Research Companion - Quick Start"
echo "======================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Check if .env file exists
if [ ! -f .env.local ]; then
    echo ""
    echo "⚠️  No .env.local file found!"
    echo "Creating .env.local from template..."
    cp .env.example .env.local
    echo ""
    echo "📝 Please edit .env.local and add your OpenAI API key:"
    echo "   OPENAI_API_KEY=sk-your-key-here"
    echo ""
    read -p "Press enter after you've added your API key..."
fi

# Install Node.js dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Download NLTK data
echo ""
echo "📚 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True)"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting development server..."
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev
