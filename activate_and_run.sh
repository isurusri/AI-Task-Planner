#!/bin/bash

# AI Task Planner - Virtual Environment Setup and Run Script

echo "🚀 AI Task Planner - Virtual Environment Setup"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating .venv..."
    python -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if requirements are installed
echo "📦 Checking dependencies..."
pip list | grep -q "fastapi" || {
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
}

# Set up environment variables if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment variables..."
    cp env.example .env
    echo "📝 Please edit .env file to add your OpenAI API key or configure Ollama"
fi

# Run the application
echo "🎯 Starting AI Task Planner..."
echo "🌐 Web interface: http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop"
echo ""

python run.py
