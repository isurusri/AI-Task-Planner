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
from config import settings


# Global services
task_decomposition_service = None
execution_simulation_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global task_decomposition_service, execution_simulation_service
    
    # Initialize services
    task_decomposition_service = TaskDecompositionService()
    execution_simulation_service = ExecutionSimulationService()
    
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

