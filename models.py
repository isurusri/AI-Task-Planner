"""Data models for the AI Task Planner."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from enum import Enum
from datetime import datetime


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class AgentType(str, Enum):
    """Agent type enumeration."""
    PLANNER = "planner"
    ANALYZER = "analyzer"
    DEVELOPER = "developer"
    TESTER = "tester"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"


class Task(BaseModel):
    """Individual task model."""
    id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")
    priority: int = Field(default=1, ge=1, le=5, description="Task priority (1-5)")
    estimated_hours: Optional[float] = Field(None, description="Estimated hours to complete")
    assigned_agent: Optional[AgentType] = Field(None, description="Assigned agent type")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    subtasks: List[str] = Field(default_factory=list, description="Child task IDs")
    parent_task: Optional[str] = Field(None, description="Parent task ID")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional task metadata")


class Agent(BaseModel):
    """Agent model."""
    id: str = Field(..., description="Unique agent identifier")
    type: AgentType = Field(..., description="Agent type")
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    current_tasks: List[str] = Field(default_factory=list, description="Currently assigned task IDs")
    is_available: bool = Field(default=True, description="Agent availability status")


class Project(BaseModel):
    """Project model containing tasks and agents."""
    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    tasks: List[Task] = Field(default_factory=list, description="Project tasks")
    agents: List[Agent] = Field(default_factory=list, description="Available agents")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TaskDecompositionRequest(BaseModel):
    """Request model for task decomposition."""
    user_input: str = Field(..., description="User's feature request or task description")
    project_context: Optional[str] = Field(None, description="Additional project context")
    max_depth: int = Field(default=3, ge=1, le=5, description="Maximum decomposition depth")
    include_estimates: bool = Field(default=True, description="Include time estimates")


class TaskDecompositionResponse(BaseModel):
    """Response model for task decomposition."""
    project: Project = Field(..., description="Generated project with decomposed tasks")
    decomposition_summary: str = Field(..., description="Summary of decomposition process")
    execution_plan: List[Dict[str, Any]] = Field(..., description="Suggested execution order")


class AgentExecutionRequest(BaseModel):
    """Request model for agent execution simulation."""
    project_id: str = Field(..., description="Project ID to execute")
    simulation_mode: bool = Field(default=True, description="Whether to simulate or actually execute")
    max_concurrent_tasks: int = Field(default=3, ge=1, le=10, description="Maximum concurrent tasks")


class AgentExecutionResponse(BaseModel):
    """Response model for agent execution simulation."""
    execution_log: List[Dict[str, Any]] = Field(..., description="Execution log entries")
    final_status: Dict[str, Any] = Field(..., description="Final project status")
    completion_percentage: float = Field(..., description="Overall completion percentage")
    estimated_remaining_hours: float = Field(..., description="Estimated remaining work hours")
