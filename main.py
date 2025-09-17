"""Main FastAPI application for the AI Task Planner."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any

from models import (
    TaskDecompositionRequest, TaskDecompositionResponse,
    AgentExecutionRequest, AgentExecutionResponse,
    Project
)
from services import TaskDecompositionService, ExecutionSimulationService
from services.llm_factory_service import LLMFactoryService
from config import settings


# Global services
task_decomposition_service = None
execution_simulation_service = None
llm_factory_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global task_decomposition_service, execution_simulation_service, llm_factory_service
    
    # Initialize services
    task_decomposition_service = TaskDecompositionService()
    execution_simulation_service = ExecutionSimulationService()
    llm_factory_service = LLMFactoryService()
    
    print("AI Task Planner services initialized")
    
    yield
    
    # Cleanup
    print("AI Task Planner services shutdown")


# Create FastAPI app
app = FastAPI(
    title="AI Task Planner",
    description="Multi-agent planning tool for decomposing feature requests into detailed subtasks",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page."""
    return templates.TemplateResponse("index.html", {"request": {}})


@app.post("/api/decompose", response_model=TaskDecompositionResponse)
async def decompose_task(request: TaskDecompositionRequest):
    """Decompose a user input into detailed subtasks."""
    try:
        if not task_decomposition_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await task_decomposition_service.decompose_task(request)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decomposition failed: {str(e)}")


@app.post("/api/simulate", response_model=AgentExecutionResponse)
async def simulate_execution(request: AgentExecutionRequest):
    """Simulate autonomous execution of tasks across agents."""
    try:
        if not execution_simulation_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = await execution_simulation_service.simulate_execution(request)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "task_decomposition": task_decomposition_service is not None,
            "execution_simulation": execution_simulation_service is not None
        }
    }


@app.get("/api/llm/info")
async def get_llm_info():
    """Get information about the current LLM provider."""
    if not llm_factory_service:
        raise HTTPException(status_code=500, detail="LLM service not initialized")
    
    return llm_factory_service.get_provider_info()


@app.post("/api/llm/test")
async def test_llm():
    """Test the current LLM provider."""
    if not llm_factory_service:
        raise HTTPException(status_code=500, detail="LLM service not initialized")
    
    try:
        response = await llm_factory_service.generate_completion(
            prompt="Hello! Please respond with 'LLM test successful' to confirm the connection is working.",
            max_tokens=50,
            temperature=0.1
        )
        
        return {
            "status": "success",
            "response": response,
            "provider": llm_factory_service.get_provider_info()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "provider": llm_factory_service.get_provider_info()
        }


@app.post("/api/llm/switch")
async def switch_llm_provider(request: dict):
    """Switch LLM provider and model."""
    global llm_factory_service
    
    if not llm_factory_service:
        raise HTTPException(status_code=500, detail="LLM service not initialized")
    
    try:
        provider = request.get("provider", "openai")
        model = request.get("model", "")
        api_key = request.get("api_key", "")
        
        # Update settings
        if provider == "openai":
            settings.llm_provider = "openai"
            settings.openai_model = model or "gpt-4"
            if api_key:
                settings.openai_api_key = api_key
        else:
            settings.llm_provider = "ollama"
            settings.ollama_model = model or "llama2:latest"
        
        # Reinitialize the LLM service
        llm_factory_service = LLMFactoryService()
        
        return {
            "status": "success",
            "message": f"Switched to {provider} with model {model}",
            "provider": llm_factory_service.get_provider_info()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@app.get("/api/llm/models")
async def get_available_models():
    """Get available models for each provider."""
    return {
        "openai": [
            {"id": "gpt-4", "name": "GPT-4", "description": "Most capable model"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "Faster GPT-4"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient"},
            {"id": "gpt-3.5-turbo-16k", "name": "GPT-3.5 Turbo 16K", "description": "Extended context"}
        ],
        "ollama": [
            {"id": "llama2:latest", "name": "Llama2", "description": "Meta's Llama2 model"},
            {"id": "codellama:latest", "name": "CodeLlama", "description": "Code-specialized Llama"},
            {"id": "mistral:latest", "name": "Mistral", "description": "Efficient open-source model"},
            {"id": "llama2:7b", "name": "Llama2 7B", "description": "Smaller Llama2 model"},
            {"id": "llama2:13b", "name": "Llama2 13B", "description": "Larger Llama2 model"}
        ]
    }


@app.post("/api/llm/validate-key")
async def validate_api_key(request: dict):
    """Validate OpenAI API key."""
    api_key = request.get("api_key", "")
    if not api_key:
        return {"valid": False, "error": "API key is required"}
    
    try:
        # Test the API key with a simple request
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=api_key)
        
        # Make a simple test request
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        
        return {
            "valid": True,
            "message": "API key is valid"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


@app.get("/api/agents")
async def get_agents():
    """Get information about available agents."""
    return {
        "agents": [
            {
                "type": "planner",
                "name": "Strategic Planner",
                "description": "Decomposes high-level requirements into detailed, actionable tasks",
                "capabilities": [
                    "task_decomposition",
                    "requirement_analysis",
                    "work_breakdown_structure",
                    "dependency_mapping",
                    "priority_assignment",
                    "resource_estimation"
                ]
            },
            {
                "type": "analyzer",
                "name": "Technical Analyzer",
                "description": "Analyzes requirements, assesses technical feasibility, and identifies potential issues",
                "capabilities": [
                    "requirement_analysis",
                    "technical_feasibility_assessment",
                    "risk_identification",
                    "dependency_analysis",
                    "performance_analysis",
                    "security_assessment",
                    "architecture_review"
                ]
            },
            {
                "type": "developer",
                "name": "Code Developer",
                "description": "Implements features, writes code, and handles technical implementation tasks",
                "capabilities": [
                    "code_implementation",
                    "feature_development",
                    "bug_fixing",
                    "code_review",
                    "refactoring",
                    "api_development",
                    "database_design",
                    "frontend_development",
                    "backend_development",
                    "testing_implementation"
                ]
            },
            {
                "type": "tester",
                "name": "Quality Tester",
                "description": "Creates test cases, performs quality assurance, and validates implementations",
                "capabilities": [
                    "test_case_creation",
                    "unit_testing",
                    "integration_testing",
                    "end_to_end_testing",
                    "performance_testing",
                    "security_testing",
                    "bug_reproduction",
                    "test_automation",
                    "quality_assurance",
                    "validation_testing"
                ]
            },
            {
                "type": "reviewer",
                "name": "Code Reviewer",
                "description": "Reviews code, assesses quality, and provides feedback for improvements",
                "capabilities": [
                    "code_review",
                    "quality_assessment",
                    "security_review",
                    "performance_review",
                    "architecture_review",
                    "documentation_review",
                    "best_practices_validation",
                    "compliance_checking",
                    "technical_debt_assessment",
                    "mentoring_feedback"
                ]
            },
            {
                "type": "coordinator",
                "name": "Workflow Coordinator",
                "description": "Orchestrates multi-agent workflows, manages task dependencies, and coordinates execution",
                "capabilities": [
                    "workflow_orchestration",
                    "task_coordination",
                    "dependency_management",
                    "resource_allocation",
                    "progress_monitoring",
                    "conflict_resolution",
                    "workflow_optimization",
                    "agent_scheduling",
                    "execution_planning",
                    "quality_control"
                ]
            }
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

