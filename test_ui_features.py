#!/usr/bin/env python3
"""
Test script to demonstrate the new UI features for model selection and API key management.
"""

import requests
import json
import time

def test_ui_features():
    """Test the new UI features for model selection and API key management."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing AI Task Planner UI Features")
    print("=" * 50)
    
    # Test 1: Get available models
    print("\n1. 📋 Getting available models...")
    try:
        response = requests.get(f"{base_url}/api/llm/models")
        models = response.json()
        
        print(f"   ✅ OpenAI models: {len(models['openai'])} available")
        for model in models['openai'][:2]:  # Show first 2
            print(f"      - {model['name']}: {model['description']}")
        
        print(f"   ✅ Ollama models: {len(models['ollama'])} available")
        for model in models['ollama'][:2]:  # Show first 2
            print(f"      - {model['name']}: {model['description']}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get current status
    print("\n2. 📊 Getting current LLM status...")
    try:
        response = requests.get(f"{base_url}/api/llm/info")
        info = response.json()
        
        print(f"   ✅ Current Provider: {info['provider']}")
        print(f"   ✅ Current Model: {info['model']}")
        print(f"   ✅ Status: {info['status']}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test API key validation
    print("\n3. 🔑 Testing API key validation...")
    try:
        # Test with invalid key
        response = requests.post(f"{base_url}/api/llm/validate-key", 
                               json={"api_key": "invalid_key"})
        result = response.json()
        
        if not result['valid']:
            print(f"   ✅ Invalid key correctly rejected: {result['error'][:50]}...")
        else:
            print(f"   ⚠️  Unexpected: invalid key was accepted")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Switch to different models
    print("\n4. 🔄 Testing model switching...")
    
    # Switch to OpenAI
    try:
        response = requests.post(f"{base_url}/api/llm/switch", 
                               json={
                                   "provider": "openai",
                                   "model": "gpt-3.5-turbo",
                                   "api_key": "demo_key"
                               })
        result = response.json()
        
        if result['status'] == 'success':
            print(f"   ✅ Switched to OpenAI: {result['message']}")
        else:
            print(f"   ❌ Failed to switch to OpenAI: {result['error']}")
            
    except Exception as e:
        print(f"   ❌ Error switching to OpenAI: {e}")
    
    # Switch back to Ollama
    try:
        response = requests.post(f"{base_url}/api/llm/switch", 
                               json={
                                   "provider": "ollama",
                                   "model": "llama2:latest"
                               })
        result = response.json()
        
        if result['status'] == 'success':
            print(f"   ✅ Switched to Ollama: {result['message']}")
        else:
            print(f"   ❌ Failed to switch to Ollama: {result['error']}")
            
    except Exception as e:
        print(f"   ❌ Error switching to Ollama: {e}")
    
    # Test 5: Test connection
    print("\n5. 🔌 Testing LLM connection...")
    try:
        response = requests.post(f"{base_url}/api/llm/test")
        result = response.json()
        
        if result['status'] == 'success':
            print(f"   ✅ Connection test successful!")
            print(f"   📝 Response: {result['response'][:100]}...")
        else:
            print(f"   ⚠️  Connection test failed: {result['error']}")
            
    except Exception as e:
        print(f"   ❌ Error testing connection: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 UI Features Test Complete!")
    print("\n📱 To test the UI:")
    print("   1. Open http://localhost:8000 in your browser")
    print("   2. Click the '⚙️ Model Settings' button in the header")
    print("   3. Try switching between OpenAI and Ollama providers")
    print("   4. Test API key validation for OpenAI")
    print("   5. Test different models and save settings")

if __name__ == "__main__":
    test_ui_features()
