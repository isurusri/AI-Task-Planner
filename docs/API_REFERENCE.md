# API Reference

## Overview

The AI Task Planner provides a RESTful API for decomposing feature requests into detailed, actionable tasks using multi-agent AI workflows.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. In production, consider implementing API key authentication.

## Endpoints

### 1. Task Decomposition

Decompose a user input into detailed subtasks using multi-agent AI.

**Endpoint:** `POST /api/decompose`

**Request Body:**
```json
{
  "user_input": "string (required)",
  "project_context": "string (optional)",
  "max_depth": "integer (optional, default: 3, range: 1-5)",
  "include_estimates": "boolean (optional, default: true)"
}
```

**Response:**
```json
{
  "project": {
    "id": "string",
    "name": "string",
    "description": "string",
    "tasks": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "status": "pending|in_progress|completed|blocked|cancelled",
        "priority": "integer (1-5)",
        "estimated_hours": "number (optional)",
        "assigned_agent": "planner|analyzer|developer|tester|reviewer|coordinator",
        "dependencies": ["string"],
        "subtasks": ["string"],
        "parent_task": "string (optional)",
        "created_at": "datetime",
        "updated_at": "datetime",
        "metadata": {
          "category": "string",
          "decomposition_depth": "integer",
          "original_index": "integer"
        }
      }
    ],
    "agents": [
      {
        "id": "string",
        "type": "planner|analyzer|developer|tester|reviewer|coordinator",
        "name": "string",
        "description": "string",
        "capabilities": ["string"],
        "current_tasks": ["string"],
        "is_available": "boolean"
      }
    ],
    "created_at": "datetime",
    "updated_at": "datetime"
  },
  "decomposition_summary": "string",
  "execution_plan": [
    {
      "step": "integer",
      "task_id": "string",
      "task_title": "string",
      "suggested_agent": "string",
      "priority": "integer",
      "estimated_hours": "number",
      "dependencies": ["string"],
      "category": "string"
    }
  ]
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/decompose" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Build a user authentication system with JWT tokens and password reset",
    "project_context": "React and Node.js application",
    "max_depth": 3,
    "include_estimates": true
  }'
```

### 2. Execution Simulation

Simulate autonomous execution of tasks across multiple AI agents.

**Endpoint:** `POST /api/simulate`

**Request Body:**
```json
{
  "project_id": "string (required)",
  "simulation_mode": "boolean (optional, default: true)",
  "max_concurrent_tasks": "integer (optional, default: 3, range: 1-10)"
}
```

**Response:**
```json
{
  "execution_log": [
    {
      "timestamp": "datetime",
      "type": "state|task_start|task_progress|task_processing|task_completion|error",
      "message": "string",
      "task_id": "string (optional)",
      "task_title": "string (optional)",
      "agent_type": "string (optional)",
      "progress_percentage": "number (optional)",
      "processing_result": "string (optional)",
      "completion_time": "datetime (optional)"
    }
  ],
  "final_status": {
    "total_tasks": "integer",
    "completed_tasks": "integer",
    "failed_tasks": "integer",
    "remaining_tasks": "integer",
    "completion_rate": "number",
    "execution_duration": "timedelta",
    "agent_workloads": {
      "planner": "integer",
      "analyzer": "integer",
      "developer": "integer",
      "tester": "integer",
      "reviewer": "integer",
      "coordinator": "integer"
    },
    "success": "boolean"
  },
  "completion_percentage": "number",
  "estimated_remaining_hours": "number"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "123e4567-e89b-12d3-a456-426614174000",
    "simulation_mode": true,
    "max_concurrent_tasks": 3
  }'
```

### 3. Health Check

Check the health status of the API and services.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy|unhealthy",
  "services": {
    "task_decomposition": "boolean",
    "execution_simulation": "boolean"
  }
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/health"
```

### 4. Agent Information

Get information about available AI agents and their capabilities.

**Endpoint:** `GET /api/agents`

**Response:**
```json
{
  "agents": [
    {
      "type": "string",
      "name": "string",
      "description": "string",
      "capabilities": ["string"]
    }
  ]
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/agents"
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting based on your OpenAI API quota.

## Response Times

Typical response times:
- Task decomposition: 10-30 seconds (depending on complexity)
- Execution simulation: 5-15 seconds
- Health check: < 1 second
- Agent information: < 1 second

## Best Practices

1. **Input Validation**: Always validate user input before sending requests
2. **Error Handling**: Implement proper error handling for all API calls
3. **Caching**: Consider caching results for identical requests
4. **Monitoring**: Monitor API usage and OpenAI API costs
5. **Retry Logic**: Implement retry logic for transient failures

## SDK Examples

### Python
```python
import requests
import json

# Decompose a task
def decompose_task(user_input, project_context=None, max_depth=3):
    url = "http://localhost:8000/api/decompose"
    data = {
        "user_input": user_input,
        "project_context": project_context,
        "max_depth": max_depth,
        "include_estimates": True
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Simulate execution
def simulate_execution(project_id, max_concurrent_tasks=3):
    url = "http://localhost:8000/api/simulate"
    data = {
        "project_id": project_id,
        "simulation_mode": True,
        "max_concurrent_tasks": max_concurrent_tasks
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Example usage
result = decompose_task("Build a REST API with authentication")
project_id = result["project"]["id"]
simulation = simulate_execution(project_id)
```

### JavaScript
```javascript
// Decompose a task
async function decomposeTask(userInput, projectContext = null, maxDepth = 3) {
    const response = await fetch('http://localhost:8000/api/decompose', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_input: userInput,
            project_context: projectContext,
            max_depth: maxDepth,
            include_estimates: true
        })
    });
    
    return await response.json();
}

// Simulate execution
async function simulateExecution(projectId, maxConcurrentTasks = 3) {
    const response = await fetch('http://localhost:8000/api/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            project_id: projectId,
            simulation_mode: true,
            max_concurrent_tasks: maxConcurrentTasks
        })
    });
    
    return await response.json();
}

// Example usage
decomposeTask("Build a user dashboard with real-time updates")
    .then(result => {
        const projectId = result.project.id;
        return simulateExecution(projectId);
    })
    .then(simulation => {
        console.log('Simulation completed:', simulation);
    });
```

### cURL
```bash
# Decompose a task
curl -X POST "http://localhost:8000/api/decompose" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Create a real-time chat application",
    "project_context": "Web application using WebSocket",
    "max_depth": 3,
    "include_estimates": true
  }'

# Simulate execution
curl -X POST "http://localhost:8000/api/simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "your-project-id-here",
    "simulation_mode": true,
    "max_concurrent_tasks": 3
  }'
```

