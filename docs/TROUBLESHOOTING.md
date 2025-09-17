# Troubleshooting Guide

## Common Issues and Solutions

### 1. OpenAI API Issues

#### Problem: "OpenAI API error: Invalid API key"

**Symptoms:**
- Error message: "OpenAI API error: Invalid API key"
- 401 Unauthorized responses
- Task decomposition fails

**Solutions:**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Verify API key format
# Should start with 'sk-' and be 51 characters long
echo $OPENAI_API_KEY | wc -c

# Test API key with curl
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

**Prevention:**
- Always use environment variables for API keys
- Never commit API keys to version control
- Use `.env` files for local development
- Rotate API keys regularly

#### Problem: "OpenAI API error: Rate limit exceeded"

**Symptoms:**
- Error message: "Rate limit exceeded"
- 429 Too Many Requests responses
- Intermittent failures

**Solutions:**
```python
# Implement exponential backoff
import time
import random
from openai import RateLimitError

async def call_openai_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await openai_service.generate_completion(prompt)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                await asyncio.sleep(wait_time)
            else:
                raise
```

**Prevention:**
- Implement rate limiting in your application
- Use request queuing for high-volume scenarios
- Monitor API usage and costs
- Consider upgrading to higher rate limits

#### Problem: "OpenAI API error: Model not found"

**Symptoms:**
- Error message: "Model not found"
- 404 Not Found responses
- Specific model errors

**Solutions:**
```python
# Check available models
import openai

models = openai.Model.list()
available_models = [model.id for model in models.data]
print(f"Available models: {available_models}")

# Use a fallback model
def get_model_with_fallback():
    preferred_model = "gpt-4"
    fallback_model = "gpt-3.5-turbo"
    
    try:
        # Test if preferred model is available
        openai.Model.retrieve(preferred_model)
        return preferred_model
    except:
        return fallback_model
```

### 2. Application Startup Issues

#### Problem: "ModuleNotFoundError: No module named 'openai'"

**Symptoms:**
- Import errors on startup
- Missing dependency errors

**Solutions:**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check if virtual environment is activated
which python
# Should show path to venv/bin/python

# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Problem: "Port 8000 is already in use"

**Symptoms:**
- Error: "Address already in use"
- Application fails to start

**Solutions:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001

# Or configure in .env
echo "PORT=8001" >> .env
```

#### Problem: "Permission denied" errors

**Symptoms:**
- File permission errors
- Cannot write to directories

**Solutions:**
```bash
# Fix file permissions
chmod +x run.py
chmod -R 755 .

# Fix ownership (if needed)
sudo chown -R $USER:$USER .

# Create necessary directories
mkdir -p logs static templates
```

### 3. Task Decomposition Issues

#### Problem: "No suitable agent found for task"

**Symptoms:**
- Tasks remain unassigned
- Agent selection fails

**Solutions:**
```python
# Debug agent selection
async def debug_agent_selection(task, project):
    print(f"Task: {task.title}")
    print(f"Category: {task.metadata.get('category', 'unknown')}")
    
    # Check available agents
    for agent in project.agents:
        print(f"Agent {agent.type}: {agent.is_available}")
    
    # Manual agent assignment
    if task.metadata.get('category') == 'backend':
        return AgentType.DEVELOPER
    elif task.metadata.get('category') == 'frontend':
        return AgentType.DEVELOPER
    else:
        return AgentType.PLANNER
```

#### Problem: "Task decomposition returns empty results"

**Symptoms:**
- No subtasks created
- Empty decomposition response

**Solutions:**
```python
# Debug decomposition process
async def debug_decomposition(task, context):
    print(f"Original task: {task.description}")
    
    # Test with simpler prompt
    simple_prompt = f"Break down this task: {task.description}"
    
    try:
        response = await openai_service.generate_completion(
            prompt=simple_prompt,
            max_tokens=500,
            temperature=0.3
        )
        print(f"OpenAI response: {response}")
        
        # Parse response manually
        subtasks = parse_response_manually(response)
        return subtasks
        
    except Exception as e:
        print(f"Error: {e}")
        return []
```

#### Problem: "Invalid JSON response from OpenAI"

**Symptoms:**
- JSON parsing errors
- Malformed responses

**Solutions:**
```python
import json
import re

def safe_parse_json(response):
    """Safely parse JSON from OpenAI response."""
    try:
        # Try direct JSON parsing
        return json.loads(response)
    except json.JSONDecodeError:
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Return fallback structure
            return {
                "subtasks": [{
                    "title": "Parsed Task",
                    "description": response[:200],
                    "estimated_hours": 4,
                    "priority": 3
                }]
            }
```

### 4. Performance Issues

#### Problem: "Slow response times"

**Symptoms:**
- Long wait times for task decomposition
- Timeout errors

**Solutions:**
```python
# Implement timeout handling
import asyncio
from asyncio import TimeoutError

async def decompose_with_timeout(request, timeout=60):
    try:
        return await asyncio.wait_for(
            decomposition_service.decompose_task(request),
            timeout=timeout
        )
    except TimeoutError:
        return {
            "error": "Decomposition timeout",
            "suggestion": "Try with simpler input or lower max_depth"
        }

# Optimize prompts
def create_optimized_prompt(task):
    return f"""
    Decompose this task into 3-5 specific subtasks:
    Task: {task.description}
    
    Format: JSON with title, description, hours, priority
    """
```

#### Problem: "High memory usage"

**Symptoms:**
- Application consumes too much memory
- Out of memory errors

**Solutions:**
```python
# Implement memory management
import gc
import psutil

def monitor_memory():
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")
    
    if memory_mb > 1000:  # 1GB threshold
        gc.collect()
        print("Garbage collection triggered")

# Limit task complexity
def limit_task_complexity(tasks, max_tasks=50):
    if len(tasks) > max_tasks:
        # Sort by priority and take top tasks
        return sorted(tasks, key=lambda t: t.priority, reverse=True)[:max_tasks]
    return tasks
```

### 5. Web Interface Issues

#### Problem: "Static files not loading"

**Symptoms:**
- CSS/JS not loading
- Broken styling

**Solutions:**
```bash
# Check static file directory
ls -la static/

# Create static directory if missing
mkdir -p static

# Check nginx configuration
nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### Problem: "CORS errors in browser"

**Symptoms:**
- CORS policy errors
- API calls blocked

**Solutions:**
```python
# Update CORS configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. Docker Issues

#### Problem: "Docker build fails"

**Symptoms:**
- Build errors
- Image creation fails

**Solutions:**
```bash
# Check Dockerfile syntax
docker build --no-cache -t ai-task-planner .

# Debug build process
docker build --progress=plain -t ai-task-planner .

# Check base image
docker run --rm python:3.9-slim python --version
```

#### Problem: "Container exits immediately"

**Symptoms:**
- Container starts and stops
- No logs available

**Solutions:**
```bash
# Run container interactively
docker run -it ai-task-planner /bin/bash

# Check container logs
docker logs <container_id>

# Run with environment variables
docker run -e OPENAI_API_KEY=your_key ai-task-planner
```

### 7. Database Issues

#### Problem: "Database connection failed"

**Symptoms:**
- Connection errors
- Database unavailable

**Solutions:**
```python
# Test database connection
import psycopg2

def test_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

# Implement connection retry
import time
from sqlalchemy.exc import OperationalError

def connect_with_retry(max_retries=5):
    for attempt in range(max_retries):
        try:
            return create_engine(DATABASE_URL)
        except OperationalError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

## Debugging Tools

### 1. Logging Configuration

```python
import logging
import sys

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Add request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    return response
```

### 2. Health Check Endpoint

```python
@app.get("/api/debug/health")
async def debug_health():
    """Comprehensive health check with detailed information."""
    
    health_status = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "services": {},
        "system": {}
    }
    
    # Check OpenAI API
    try:
        await openai_service.generate_completion("test", max_tokens=1)
        health_status["services"]["openai"] = "healthy"
    except Exception as e:
        health_status["services"]["openai"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check memory usage
    import psutil
    memory = psutil.virtual_memory()
    health_status["system"]["memory"] = {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent
    }
    
    # Check disk space
    disk = psutil.disk_usage('/')
    health_status["system"]["disk"] = {
        "total": disk.total,
        "free": disk.free,
        "percent": (disk.used / disk.total) * 100
    }
    
    return health_status
```

### 3. Performance Monitoring

```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
            
            # Alert if too slow
            if execution_time > 30:
                logger.warning(f"{func.__name__} took {execution_time:.3f}s (slow)")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {str(e)}")
            raise
    return wrapper

# Apply to critical functions
@monitor_performance
async def decompose_task(request: TaskDecompositionRequest):
    # Implementation
    pass
```

## Getting Help

### 1. Check Logs

```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f ai-task-planner

# System logs
journalctl -u ai-task-planner -f
```

### 2. Enable Debug Mode

```bash
# Set debug environment variable
export DEBUG=True

# Or in .env file
echo "DEBUG=True" >> .env
```

### 3. Test Individual Components

```python
# Test OpenAI connection
python -c "
import asyncio
from services.openai_service import OpenAIService

async def test():
    service = OpenAIService()
    result = await service.generate_completion('Hello, world!')
    print(result)

asyncio.run(test())
"

# Test agent processing
python -c "
import asyncio
from agents.planner_agent import PlannerAgent
from models import Task, TaskStatus

async def test():
    agent = PlannerAgent()
    task = Task(id='test', title='Test Task', description='Test description', status=TaskStatus.PENDING)
    result = await agent.process_task(task, {})
    print(result)

asyncio.run(test())
"
```

### 4. Community Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the comprehensive docs
- **Examples**: Review example usage patterns
- **Discord/Slack**: Join community discussions

### 5. Professional Support

For enterprise deployments or complex issues:
- **Consulting**: Professional implementation support
- **Training**: Team training and workshops
- **Custom Development**: Tailored solutions
- **24/7 Support**: Enterprise support contracts

