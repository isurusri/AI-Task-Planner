#!/bin/bash

# AI Task Planner - Virtual Environment Activation Script

echo "🔧 Activating AI Task Planner virtual environment..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating .venv..."
    python -m venv .venv
    echo "📥 Installing dependencies..."
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Virtual environment created and dependencies installed"
else
    # Activate virtual environment
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

echo ""
echo "🎯 To run the AI Task Planner:"
echo "   python run.py"
echo ""
echo "🌐 Web interface: http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
echo "🛑 To deactivate: deactivate"
