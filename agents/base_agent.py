"""Base agent class for the AI Task Planner."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import asyncio
import uuid
from datetime import datetime

from models import Task, Agent, AgentType, TaskStatus


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, agent_type: AgentType, name: str, description: str):
        self.id = str(uuid.uuid4())
        self.type = agent_type
        self.name = name
        self.description = description
        self.capabilities = []
        self.current_tasks = []
        self.is_available = True
        self.execution_log = []
    
    @abstractmethod
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single task and return results."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        pass
    
    async def assign_task(self, task: Task) -> bool:
        """Assign a task to this agent."""
        if not self.is_available or len(self.current_tasks) >= self.get_max_concurrent_tasks():
            return False
        
        self.current_tasks.append(task.id)
        task.assigned_agent = self.type
        task.status = TaskStatus.IN_PROGRESS
        task.updated_at = datetime.now()
        
        self.log_execution(f"Assigned task {task.id}: {task.title}")
        return True
    
    async def complete_task(self, task: Task, results: Dict[str, Any]) -> None:
        """Mark a task as completed and log results."""
        if task.id in self.current_tasks:
            self.current_tasks.remove(task.id)
        
        task.status = TaskStatus.COMPLETED
        task.updated_at = datetime.now()
        task.metadata.update(results)
        
        self.log_execution(f"Completed task {task.id}: {task.title}")
        self.log_execution(f"Results: {results}")
    
    def get_max_concurrent_tasks(self) -> int:
        """Get maximum number of concurrent tasks this agent can handle."""
        return 3  # Default value, can be overridden
    
    def log_execution(self, message: str) -> None:
        """Log an execution message with timestamp."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.id,
            "agent_type": self.type.value,
            "message": message
        }
        self.execution_log.append(log_entry)
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get the agent's execution log."""
        return self.execution_log.copy()
    
    def set_availability(self, available: bool) -> None:
        """Set agent availability."""
        self.is_available = available
        self.log_execution(f"Availability set to: {available}")
    
    def to_agent_model(self) -> Agent:
        """Convert to Agent model."""
        return Agent(
            id=self.id,
            type=self.type,
            name=self.name,
            description=self.description,
            capabilities=self.get_capabilities(),
            current_tasks=self.current_tasks.copy(),
            is_available=self.is_available
        )

