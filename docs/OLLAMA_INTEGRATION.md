# Ollama Integration Guide

## Overview

The AI Task Planner now supports local LLM models through Ollama integration, allowing you to run the application with models like Llama2, CodeLlama, Mistral, and other locally-hosted models. This provides benefits like:

- **Privacy**: Your data stays on your local machine
- **Cost**: No API costs for LLM usage
- **Offline**: Works without internet connection
- **Customization**: Use specialized models for different tasks

## Prerequisites

### 1. Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai/download)

### 2. Install a Model

```bash
# Install Llama2 (recommended for general use)
ollama pull llama2:latest

# Install CodeLlama (better for code-related tasks)
ollama pull codellama:latest

# Install Mistral (alternative option)
ollama pull mistral:latest

# Install smaller models for faster responses
ollama pull llama2:7b
ollama pull codellama:7b
```

### 3. Start Ollama Service

```bash
# Start Ollama server (runs on port 11434 by default)
ollama serve
```

## Configuration

### Environment Variables

Update your `.env` file to use Ollama:

```env
# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2:latest
OLLAMA_BASE_URL=http://localhost:11434

# Optional: Keep OpenAI as fallback
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Other settings
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### Model Selection

Choose the best model for your use case:

| Model | Size | Best For | Speed | Quality |
|-------|------|----------|-------|---------|
| `llama2:7b` | 7B | General tasks, fast responses | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| `llama2:13b` | 13B | Balanced performance | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `llama2:70b` | 70B | Highest quality | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| `codellama:7b` | 7B | Code generation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `codellama:13b` | 13B | Complex code tasks | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `mistral:7b` | 7B | Fast, efficient | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Usage

### 1. Start the Application

```bash
# With Ollama configuration
LLM_PROVIDER=ollama OLLAMA_MODEL=llama2:latest python run.py

# Or update .env file and run normally
python run.py
```

### 2. Verify Integration

Check the web interface at `http://localhost:8000` - you should see "Powered by Ollama (llama2:latest)" in the header.

### 3. Test LLM Connection

```bash
# Test the LLM endpoint
curl -X POST http://localhost:8000/api/llm/test

# Get LLM provider info
curl http://localhost:8000/api/llm/info
```

## API Endpoints

### Get LLM Information
```http
GET /api/llm/info
```

Response:
```json
{
  "provider": "ollama",
  "model": "llama2:latest",
  "base_url": "http://localhost:11434",
  "status": "configured"
}
```

### Test LLM Connection
```http
POST /api/llm/test
```

Response:
```json
{
  "status": "success",
  "response": "LLM test successful",
  "provider": {
    "provider": "ollama",
    "model": "llama2:latest",
    "base_url": "http://localhost:11434",
    "status": "configured"
  }
}
```

## Performance Optimization

### 1. Model Selection

For different use cases:

**Fast Development:**
```env
OLLAMA_MODEL=llama2:7b
```

**High Quality:**
```env
OLLAMA_MODEL=llama2:13b
```

**Code-Focused:**
```env
OLLAMA_MODEL=codellama:13b
```

### 2. System Requirements

| Model Size | RAM Required | GPU Recommended |
|------------|--------------|-----------------|
| 7B | 8GB | 4GB VRAM |
| 13B | 16GB | 8GB VRAM |
| 70B | 64GB | 40GB VRAM |

### 3. Ollama Configuration

Create `~/.ollama/config.json` for custom settings:

```json
{
  "gpu_layers": 35,
  "num_ctx": 4096,
  "num_thread": 8
}
```

## Troubleshooting

### Common Issues

#### 1. Ollama Not Running
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama if not running
ollama serve
```

#### 2. Model Not Found
```bash
# List available models
ollama list

# Pull the model if missing
ollama pull llama2:latest
```

#### 3. Connection Refused
```bash
# Check if Ollama is listening on correct port
netstat -tulpn | grep 11434

# Test connection
curl http://localhost:11434/api/tags
```

#### 4. Out of Memory
- Use smaller models (7B instead of 13B/70B)
- Close other applications
- Increase swap space
- Use GPU acceleration if available

### Debug Mode

Enable debug logging:

```env
DEBUG=True
```

Check application logs for detailed error messages.

## Advanced Configuration

### 1. Custom Ollama Server

If running Ollama on a different machine:

```env
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

### 2. Model Parameters

Customize model behavior by modifying the Ollama service:

```python
# In services/llm_service.py
response = await self.client.chat(
    model=self.model,
    messages=messages,
    options={
        "num_predict": max_tokens or 2000,
        "temperature": temperature or 0.7,
        "top_p": 0.9,
        "repeat_penalty": 1.1,  # Reduce repetition
        "num_ctx": 4096,        # Context window
    }
)
```

### 3. Multiple Models

Switch between models dynamically:

```python
# Create different services for different tasks
planner_service = LLMServiceFactory.create_service(
    provider="ollama", 
    model="llama2:13b"
)

developer_service = LLMServiceFactory.create_service(
    provider="ollama", 
    model="codellama:13b"
)
```

## Comparison: OpenAI vs Ollama

| Feature | OpenAI | Ollama |
|---------|--------|--------|
| **Cost** | Pay per token | Free |
| **Privacy** | Data sent to OpenAI | Local only |
| **Internet** | Required | Not required |
| **Speed** | Fast | Depends on hardware |
| **Quality** | Excellent | Good to Excellent |
| **Customization** | Limited | Full control |
| **Setup** | API key only | Install Ollama + models |

## Best Practices

### 1. Model Selection
- Start with `llama2:7b` for testing
- Use `llama2:13b` for production
- Use `codellama:13b` for code-heavy tasks

### 2. Performance
- Use GPU acceleration when available
- Monitor memory usage
- Adjust context window based on needs

### 3. Quality
- Fine-tune temperature settings
- Use appropriate prompts for local models
- Consider model-specific prompt engineering

### 4. Fallback Strategy
```env
# Primary: Ollama
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2:latest

# Fallback: OpenAI (if Ollama fails)
OPENAI_API_KEY=your_key_here
```

## Example Usage

### 1. Basic Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Install model
ollama pull llama2:latest

# Start Ollama
ollama serve &

# Configure application
echo "LLM_PROVIDER=ollama" >> .env
echo "OLLAMA_MODEL=llama2:latest" >> .env

# Run application
python run.py
```

### 2. Test Integration
```bash
# Test LLM connection
curl -X POST http://localhost:8000/api/llm/test

# Decompose a task
curl -X POST "http://localhost:8000/api/decompose" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Build a REST API with authentication",
    "max_depth": 2
  }'
```

### 3. Monitor Performance
```bash
# Check Ollama status
ollama ps

# Monitor system resources
htop

# Check application logs
tail -f logs/app.log
```

## Support

For issues with Ollama integration:

1. Check Ollama documentation: [ollama.ai/docs](https://ollama.ai/docs)
2. Verify model installation: `ollama list`
3. Test Ollama directly: `ollama run llama2:latest`
4. Check application logs for detailed errors
5. Ensure sufficient system resources

The Ollama integration provides a powerful, privacy-focused alternative to cloud-based LLM services while maintaining the full functionality of the AI Task Planner.
