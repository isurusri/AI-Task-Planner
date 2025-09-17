@echo off
REM AI Task Planner - Virtual Environment Setup and Run Script for Windows

echo 🚀 AI Task Planner - Virtual Environment Setup
echo ==============================================

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Virtual environment not found. Creating .venv...
    python -m venv .venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if requirements are installed
echo 📦 Checking dependencies...
pip list | findstr "fastapi" >nul || (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Set up environment variables if .env doesn't exist
if not exist ".env" (
    echo ⚙️  Setting up environment variables...
    copy env.example .env
    echo 📝 Please edit .env file to add your OpenAI API key or configure Ollama
)

REM Run the application
echo 🎯 Starting AI Task Planner...
echo 🌐 Web interface: http://localhost:8000
echo 📚 API docs: http://localhost:8000/docs
echo 🛑 Press Ctrl+C to stop
echo.

python run.py
