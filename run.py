#!/usr/bin/env python3
"""Simple startup script for the AI Task Planner."""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Main entry point for the application."""
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("📝 Please create a .env file with your OpenAI API key:")
        print("   cp env.example .env")
        print("   # Then edit .env and add your OPENAI_API_KEY")
        print()
        
        # Check if OPENAI_API_KEY is set in environment
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ OPENAI_API_KEY not found in environment variables")
            print("🔑 Please set your OpenAI API key:")
            print("   export OPENAI_API_KEY=your_api_key_here")
            print("   # or create a .env file")
            sys.exit(1)
    
    # Check if required directories exist
    required_dirs = ["templates", "static"]
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            print(f"📁 Creating {dir_name} directory...")
            Path(dir_name).mkdir(exist_ok=True)
    
    # Start the application
    print("🚀 Starting AI Task Planner...")
    print("🌐 Web interface will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 AI Task Planner stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

