#!/usr/bin/env python3
"""
Test script for Ollama integration with AI Task Planner.

This script demonstrates how to use the AI Task Planner with local LLM models
through Ollama integration.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.llm_factory_service import LLMFactoryService
from config import settings


async def test_ollama_integration():
    """Test Ollama integration with various models."""
    
    print("🤖 AI Task Planner - Ollama Integration Test")
    print("=" * 50)
    
    # Test different LLM providers
    providers = [
        {"provider": "openai", "name": "OpenAI GPT-4"},
        {"provider": "ollama", "name": "Ollama Llama2", "model": "llama2:latest"},
        {"provider": "ollama", "name": "Ollama CodeLlama", "model": "codellama:latest"},
    ]
    
    for config in providers:
        print(f"\n🧪 Testing {config['name']}...")
        print("-" * 30)
        
        try:
            # Create service with specific configuration
            if config["provider"] == "ollama":
                service = LLMFactoryService()
                # Temporarily override settings for testing
                original_provider = settings.llm_provider
                original_model = settings.ollama_model
                settings.llm_provider = "ollama"
                settings.ollama_model = config.get("model", "llama2:latest")
            else:
                service = LLMFactoryService()
            
            # Test basic completion
            print("📝 Testing basic completion...")
            response = await service.generate_completion(
                prompt="What is the capital of France?",
                max_tokens=50,
                temperature=0.1
            )
            print(f"✅ Response: {response[:100]}...")
            
            # Test chain-of-thought reasoning
            print("🧠 Testing chain-of-thought reasoning...")
            cot_response = await service.generate_chain_of_thought(
                problem="How would you design a simple user authentication system?",
                context={"project_type": "web_application", "tech_stack": "Python/FastAPI"}
            )
            print(f"✅ Reasoning: {cot_response['reasoning'][:150]}...")
            print(f"✅ Solution: {cot_response['solution'][:150]}...")
            print(f"✅ Confidence: {cot_response['confidence']}")
            
            # Test task complexity analysis
            print("📊 Testing task complexity analysis...")
            complexity = await service.analyze_task_complexity(
                "Build a REST API with JWT authentication and rate limiting"
            )
            print(f"✅ Complexity: {complexity['complexity_level']}")
            print(f"✅ Estimated hours: {complexity['estimated_hours']}")
            print(f"✅ Required skills: {', '.join(complexity['required_skills'][:3])}")
            
            # Test agent assignment
            print("👥 Testing agent assignment...")
            agents = [
                {"type": "planner", "description": "Strategic planning and task decomposition"},
                {"type": "developer", "description": "Code implementation and technical tasks"},
                {"type": "tester", "description": "Quality assurance and testing"},
            ]
            
            assignment = await service.suggest_agent_assignment(
                task={
                    "title": "Implement user authentication",
                    "description": "Add JWT-based authentication to the API",
                    "category": "backend"
                },
                available_agents=agents
            )
            print(f"✅ Suggested agent: {assignment['suggested_agent']}")
            print(f"✅ Confidence: {assignment['confidence']}")
            
            # Get provider info
            info = service.get_provider_info()
            print(f"ℹ️  Provider info: {info}")
            
            print(f"✅ {config['name']} test completed successfully!")
            
        except Exception as e:
            print(f"❌ Error testing {config['name']}: {str(e)}")
            print("   This might be expected if Ollama is not running or model is not installed.")
        
        finally:
            # Restore original settings
            if config["provider"] == "ollama":
                settings.llm_provider = original_provider
                settings.ollama_model = original_model


async def test_ollama_models():
    """Test different Ollama models if available."""
    
    print("\n🔍 Testing Available Ollama Models")
    print("=" * 40)
    
    models_to_test = [
        "llama2:latest",
        "llama2:7b", 
        "codellama:latest",
        "codellama:7b",
        "mistral:latest"
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        try:
            # Temporarily set the model
            original_model = settings.ollama_model
            settings.llm_provider = "ollama"
            settings.ollama_model = model
            
            service = LLMFactoryService()
            
            # Simple test
            response = await service.generate_completion(
                prompt="Say 'Hello from Ollama!' and nothing else.",
                max_tokens=20,
                temperature=0.1
            )
            
            print(f"✅ {model}: {response.strip()}")
            
        except Exception as e:
            print(f"❌ {model}: Not available ({str(e)[:50]}...)")
        
        finally:
            settings.ollama_model = original_model


def print_setup_instructions():
    """Print setup instructions for Ollama."""
    
    print("\n📋 Ollama Setup Instructions")
    print("=" * 30)
    print("1. Install Ollama:")
    print("   curl -fsSL https://ollama.ai/install.sh | sh")
    print()
    print("2. Start Ollama service:")
    print("   ollama serve")
    print()
    print("3. Install models:")
    print("   ollama pull llama2:latest")
    print("   ollama pull codellama:latest")
    print("   ollama pull mistral:latest")
    print()
    print("4. Configure environment:")
    print("   echo 'LLM_PROVIDER=ollama' >> .env")
    print("   echo 'OLLAMA_MODEL=llama2:latest' >> .env")
    print()
    print("5. Run the application:")
    print("   python run.py")


async def main():
    """Main test function."""
    
    print("🚀 Starting Ollama Integration Tests...")
    print()
    
    # Check if Ollama is configured
    if settings.llm_provider == "ollama":
        print(f"✅ Ollama configured with model: {settings.ollama_model}")
    else:
        print(f"ℹ️  Current provider: {settings.llm_provider}")
        print("   To test Ollama, set LLM_PROVIDER=ollama in your .env file")
    
    print()
    
    # Run tests
    await test_ollama_integration()
    await test_ollama_models()
    
    print("\n" + "=" * 50)
    print("🎉 Ollama integration test completed!")
    print()
    print_setup_instructions()


if __name__ == "__main__":
    asyncio.run(main())
