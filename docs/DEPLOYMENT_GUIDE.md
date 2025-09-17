# Deployment Guide

## Overview

This guide covers deploying the AI Task Planner in various environments, from local development to production cloud deployments.

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git (for version control)
- Docker (optional, for containerized deployment)

## Local Development Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-task-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file
nano .env
```

Add your configuration:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 3. Run the Application

```bash
# Using the startup script
python run.py

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Verify Installation

```bash
# Check health endpoint
curl http://localhost:8000/api/health

# Test task decomposition
curl -X POST "http://localhost:8000/api/decompose" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Build a simple API", "max_depth": 2}'
```

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  ai-task-planner:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4
      - MAX_TOKENS=2000
      - TEMPERATURE=0.7
      - DEBUG=False
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - ai-task-planner
    restart: unless-stopped
```

### 3. Build and Run

```bash
# Build the image
docker build -t ai-task-planner .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f ai-task-planner
```

## Cloud Deployment

### AWS Deployment

#### 1. Using AWS App Runner

```yaml
# apprunner.yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Building the application"
      - pip install -r requirements.txt
run:
  runtime-version: 3.9.16
  command: uvicorn main:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
    env: PORT
  env:
    - name: OPENAI_API_KEY
      value: "your-api-key"
```

#### 2. Using AWS ECS with Fargate

```yaml
# task-definition.json
{
  "family": "ai-task-planner",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ai-task-planner",
      "image": "your-account.dkr.ecr.region.amazonaws.com/ai-task-planner:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-task-planner",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 3. Using AWS Lambda (Serverless)

```python
# lambda_handler.py
import json
from mangum import Mangum
from main import app

# Create ASGI adapter
handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

### Google Cloud Platform

#### 1. Using Cloud Run

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ai-task-planner', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/ai-task-planner']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'ai-task-planner',
      '--image', 'gcr.io/$PROJECT_ID/ai-task-planner',
      '--platform', 'managed',
      '--region', 'us-central1',
      '--allow-unauthenticated'
    ]
```

#### 2. Using App Engine

```yaml
# app.yaml
runtime: python39

env_variables:
  OPENAI_API_KEY: "your-api-key"
  OPENAI_MODEL: "gpt-4"
  MAX_TOKENS: "2000"
  TEMPERATURE: "0.7"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

handlers:
  - url: /.*
    script: auto
```

### Azure Deployment

#### 1. Using Azure Container Instances

```yaml
# azure-deploy.yaml
apiVersion: 2018-10-01
location: eastus
name: ai-task-planner
properties:
  containers:
  - name: ai-task-planner
    properties:
      image: your-registry.azurecr.io/ai-task-planner:latest
      resources:
        requests:
          cpu: 1
          memoryInGb: 2
      ports:
      - port: 8000
        protocol: TCP
      environmentVariables:
      - name: OPENAI_API_KEY
        value: "your-api-key"
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 8000
    dnsNameLabel: ai-task-planner
```

#### 2. Using Azure App Service

```json
{
  "name": "ai-task-planner",
  "type": "Microsoft.Web/sites",
  "apiVersion": "2021-02-01",
  "location": "East US",
  "properties": {
    "siteConfig": {
      "linuxFxVersion": "PYTHON|3.9",
      "appSettings": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-api-key"
        }
      ]
    }
  }
}
```

## Production Configuration

### 1. Environment Variables

```env
# Production environment
OPENAI_API_KEY=your_production_api_key
OPENAI_MODEL=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (if using persistent storage)
DATABASE_URL=postgresql://user:password@localhost:5432/ai_task_planner

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0

# Monitoring
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO
```

### 2. Nginx Configuration

```nginx
# nginx.conf
upstream ai_task_planner {
    server ai-task-planner:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location / {
        proxy_pass http://ai_task_planner;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 3. Monitoring and Logging

#### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-task-planner'
    static_configs:
      - targets: ['ai-task-planner:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

#### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "AI Task Planner Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

## Security Considerations

### 1. API Key Management

```python
# Use environment variables for sensitive data
import os
from cryptography.fernet import Fernet

def encrypt_api_key(api_key: str) -> str:
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_key.encode()).decode()
```

### 2. Input Validation

```python
from pydantic import BaseModel, validator
import re

class TaskDecompositionRequest(BaseModel):
    user_input: str
    project_context: Optional[str] = None
    max_depth: int = 3
    include_estimates: bool = True
    
    @validator('user_input')
    def validate_user_input(cls, v):
        if len(v) > 10000:
            raise ValueError('User input too long')
        if not re.match(r'^[a-zA-Z0-9\s\.,!?\-_()]+$', v):
            raise ValueError('Invalid characters in user input')
        return v
    
    @validator('max_depth')
    def validate_max_depth(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Max depth must be between 1 and 5')
        return v
```

### 3. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/decompose")
@limiter.limit("10/minute")
async def decompose_task(request: Request, task_request: TaskDecompositionRequest):
    # Implementation
    pass
```

## Performance Optimization

### 1. Caching

```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiry: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = redis_client.get(cache_key)
            
            if cached_result:
                return json.loads(cached_result)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiry, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(expiry=1800)  # 30 minutes
async def decompose_task(request: TaskDecompositionRequest):
    # Implementation
    pass
```

### 2. Database Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### 3. Async Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def process_tasks_async(tasks):
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(executor, process_task, task)
        for task in tasks
    ]
    return await asyncio.gather(*futures)
```

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   ```bash
   # Check API key
   echo $OPENAI_API_KEY
   
   # Test API connection
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

2. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats ai-task-planner
   
   # Increase memory limit
   docker run -m 2g ai-task-planner
   ```

3. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000
   
   # Use different port
   uvicorn main:app --port 8001
   ```

### Log Analysis

```bash
# View application logs
docker-compose logs -f ai-task-planner

# Filter error logs
docker-compose logs ai-task-planner | grep ERROR

# Monitor real-time logs
tail -f logs/app.log | grep -E "(ERROR|WARN)"
```

## Backup and Recovery

### 1. Database Backup

```bash
# PostgreSQL backup
pg_dump -h localhost -U username -d ai_task_planner > backup.sql

# Restore from backup
psql -h localhost -U username -d ai_task_planner < backup.sql
```

### 2. Configuration Backup

```bash
# Backup configuration
tar -czf config-backup.tar.gz .env nginx.conf docker-compose.yml

# Restore configuration
tar -xzf config-backup.tar.gz
```

## Scaling Considerations

### 1. Horizontal Scaling

```yaml
# docker-compose.yml with scaling
version: '3.8'
services:
  ai-task-planner:
    build: .
    deploy:
      replicas: 3
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    ports:
      - "8000-8002:8000"
```

### 2. Load Balancing

```nginx
upstream ai_task_planner {
    server ai-task-planner-1:8000;
    server ai-task-planner-2:8000;
    server ai-task-planner-3:8000;
}
```

### 3. Auto-scaling

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-task-planner-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-task-planner
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

