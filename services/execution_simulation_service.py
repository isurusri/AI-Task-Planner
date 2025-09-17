"""Service for simulating autonomous execution across agents."""

from typing import List, Dict, Any, Optional
import asyncio
import random
from datetime import datetime, timedelta

from models import (
    Project, Task, AgentType, TaskStatus,
    AgentExecutionRequest, AgentExecutionResponse
)
from services.llm_factory_service import LLMFactoryService
from agents import (
    PlannerAgent, AnalyzerAgent, DeveloperAgent, 
    TesterAgent, ReviewerAgent, CoordinatorAgent
)


class ExecutionSimulationService:
    """Service for simulating autonomous execution of tasks across multiple agents."""
    
    def __init__(self):
        self.llm_service = LLMFactoryService()
        self.agents = {
            AgentType.PLANNER: PlannerAgent(),
            AgentType.ANALYZER: AnalyzerAgent(),
            AgentType.DEVELOPER: DeveloperAgent(),
            AgentType.TESTER: TesterAgent(),
            AgentType.REVIEWER: ReviewerAgent(),
            AgentType.COORDINATOR: CoordinatorAgent()
        }
        
        # Register all agents with coordinator
        for agent in self.agents.values():
            self.agents[AgentType.COORDINATOR].register_agent(agent)
    
    async def simulate_execution(self, request: AgentExecutionRequest) -> AgentExecutionResponse:
        """Simulate autonomous execution of a project."""
        
        # Load project (in real implementation, this would come from database)
        project = await self._load_project(request.project_id)
        if not project:
            return AgentExecutionResponse(
                execution_log=[],
                final_status={"error": "Project not found"},
                completion_percentage=0.0,
                estimated_remaining_hours=0.0
            )
        
        # Initialize simulation state
        simulation_state = {
            "project_id": project.id,
            "start_time": datetime.now(),
            "current_time": datetime.now(),
            "completed_tasks": 0,
            "total_tasks": len(project.tasks),
            "execution_log": [],
            "agent_workloads": {agent_type.value: 0 for agent_type in AgentType},
            "task_queue": project.tasks.copy(),
            "running_tasks": [],
            "completed_tasks": [],
            "failed_tasks": []
        }
        
        # Sort tasks by dependencies and priority
        sorted_tasks = self._sort_tasks_for_execution(project.tasks)
        simulation_state["task_queue"] = sorted_tasks
        
        # Simulate execution
        if request.simulation_mode:
            execution_results = await self._simulate_autonomous_execution(
                simulation_state, 
                request.max_concurrent_tasks
            )
        else:
            execution_results = await self._execute_real_tasks(
                simulation_state,
                request.max_concurrent_tasks
            )
        
        # Calculate final metrics
        final_status = self._calculate_final_status(simulation_state, execution_results)
        completion_percentage = (simulation_state["completed_tasks"] / simulation_state["total_tasks"]) * 100
        estimated_remaining_hours = self._calculate_remaining_hours(simulation_state)
        
        return AgentExecutionResponse(
            execution_log=simulation_state["execution_log"],
            final_status=final_status,
            completion_percentage=completion_percentage,
            estimated_remaining_hours=estimated_remaining_hours
        )
    
    async def _simulate_autonomous_execution(
        self, 
        simulation_state: Dict[str, Any], 
        max_concurrent_tasks: int
    ) -> Dict[str, Any]:
        """Simulate autonomous execution with realistic timing and behavior."""
        
        execution_rounds = 0
        max_rounds = 50  # Prevent infinite loops
        
        while (simulation_state["task_queue"] or simulation_state["running_tasks"]) and execution_rounds < max_rounds:
            execution_rounds += 1
            
            # Log current state
            self._log_execution_state(simulation_state, f"Execution Round {execution_rounds}")
            
            # Process running tasks
            await self._process_running_tasks(simulation_state)
            
            # Start new tasks if capacity available
            await self._start_new_tasks(simulation_state, max_concurrent_tasks)
            
            # Advance simulation time
            simulation_state["current_time"] += timedelta(minutes=30)  # 30-minute increments
            
            # Add some randomness to make simulation more realistic
            await asyncio.sleep(0.1)  # Small delay for realism
        
        return {
            "execution_rounds": execution_rounds,
            "simulation_duration": simulation_state["current_time"] - simulation_state["start_time"],
            "success": execution_rounds < max_rounds
        }
    
    async def _process_running_tasks(self, simulation_state: Dict[str, Any]) -> None:
        """Process currently running tasks."""
        
        completed_tasks = []
        
        for task_info in simulation_state["running_tasks"]:
            task = task_info["task"]
            agent_type = task_info["agent_type"]
            start_time = task_info["start_time"]
            
            # Calculate if task should be completed based on estimated time
            estimated_duration = task.estimated_hours or 4
            elapsed_time = simulation_state["current_time"] - start_time
            required_duration = timedelta(hours=estimated_duration)
            
            if elapsed_time >= required_duration:
                # Task completed
                await self._complete_task_simulation(task, agent_type, simulation_state)
                completed_tasks.append(task_info)
                simulation_state["completed_tasks"] += 1
            else:
                # Task still running, add some progress
                progress = min(elapsed_time / required_duration, 1.0)
                self._log_task_progress(task, agent_type, progress, simulation_state)
        
        # Remove completed tasks from running list
        for task_info in completed_tasks:
            simulation_state["running_tasks"].remove(task_info)
    
    async def _start_new_tasks(
        self, 
        simulation_state: Dict[str, Any], 
        max_concurrent_tasks: int
    ) -> None:
        """Start new tasks if capacity is available."""
        
        available_slots = max_concurrent_tasks - len(simulation_state["running_tasks"])
        
        for _ in range(available_slots):
            if not simulation_state["task_queue"]:
                break
            
            # Find next available task
            next_task = self._find_next_available_task(simulation_state)
            if not next_task:
                break
            
            # Select agent for task
            agent_type = await self._select_agent_for_execution(next_task, simulation_state)
            if not agent_type:
                continue
            
            # Start task execution
            await self._start_task_execution(next_task, agent_type, simulation_state)
    
    def _find_next_available_task(self, simulation_state: Dict[str, Any]) -> Optional[Task]:
        """Find the next task that can be started (dependencies satisfied)."""
        
        for i, task in enumerate(simulation_state["task_queue"]):
            # Check if dependencies are satisfied
            if self._are_dependencies_satisfied(task, simulation_state):
                # Remove from queue and return
                return simulation_state["task_queue"].pop(i)
        
        return None
    
    def _are_dependencies_satisfied(self, task: Task, simulation_state: Dict[str, Any]) -> bool:
        """Check if all dependencies for a task are satisfied."""
        
        if not task.dependencies:
            return True
        
        completed_task_ids = [t.id for t in simulation_state["completed_tasks"]]
        return all(dep_id in completed_task_ids for dep_id in task.dependencies)
    
    async def _select_agent_for_execution(
        self, 
        task: Task, 
        simulation_state: Dict[str, Any]
    ) -> Optional[AgentType]:
        """Select the most appropriate agent for task execution."""
        
        # Use AI to suggest agent assignment
        try:
            available_agents = [
                {
                    "type": agent_type.value,
                    "description": agent.description,
                    "capabilities": agent.get_capabilities(),
                    "current_workload": simulation_state["agent_workloads"][agent_type.value]
                }
                for agent_type, agent in self.agents.items()
            ]
            
            suggestion = await self.llm_service.suggest_agent_assignment(
                {
                    "title": task.title,
                    "description": task.description,
                    "category": task.metadata.get("category", "general")
                },
                available_agents
            )
            
            suggested_agent = suggestion.get("suggested_agent", "developer")
            
            # Map to AgentType enum
            agent_mapping = {
                "planner": AgentType.PLANNER,
                "analyzer": AgentType.ANALYZER,
                "developer": AgentType.DEVELOPER,
                "tester": AgentType.TESTER,
                "reviewer": AgentType.REVIEWER,
                "coordinator": AgentType.COORDINATOR
            }
            
            return agent_mapping.get(suggested_agent, AgentType.DEVELOPER)
            
        except Exception as e:
            self._log_error(f"Error selecting agent: {str(e)}", simulation_state)
            return AgentType.DEVELOPER  # Default fallback
    
    async def _start_task_execution(
        self, 
        task: Task, 
        agent_type: AgentType, 
        simulation_state: Dict[str, Any]
    ) -> None:
        """Start execution of a task with the specified agent."""
        
        agent = self.agents[agent_type]
        
        # Assign task to agent
        success = await agent.assign_task(task)
        
        if success:
            # Add to running tasks
            task_info = {
                "task": task,
                "agent_type": agent_type,
                "start_time": simulation_state["current_time"],
                "agent_id": agent.id
            }
            simulation_state["running_tasks"].append(task_info)
            
            # Update agent workload
            simulation_state["agent_workloads"][agent_type.value] += 1
            
            # Log task start
            self._log_task_start(task, agent_type, simulation_state)
            
            # Simulate task processing
            await self._simulate_task_processing(task, agent_type, simulation_state)
        else:
            # Agent not available, put task back in queue
            simulation_state["task_queue"].insert(0, task)
            self._log_error(f"Agent {agent_type.value} not available for task {task.id}", simulation_state)
    
    async def _simulate_task_processing(
        self, 
        task: Task, 
        agent_type: AgentType, 
        simulation_state: Dict[str, Any]
    ) -> None:
        """Simulate the actual processing of a task by an agent."""
        
        try:
            # Create context for agent processing
            context = {
                "project_context": "Simulation context",
                "tech_stack": "Python, FastAPI, OpenAI",
                "simulation_mode": True
            }
            
            # Process task with agent
            agent = self.agents[agent_type]
            result = await agent.process_task(task, context)
            
            # Log processing result
            self._log_task_processing(task, agent_type, result, simulation_state)
            
        except Exception as e:
            self._log_error(f"Error processing task {task.id} with {agent_type.value}: {str(e)}", simulation_state)
    
    async def _complete_task_simulation(
        self, 
        task: Task, 
        agent_type: AgentType, 
        simulation_state: Dict[str, Any]
    ) -> None:
        """Complete a task simulation."""
        
        # Mark task as completed
        task.status = TaskStatus.COMPLETED
        task.updated_at = simulation_state["current_time"]
        
        # Add to completed tasks
        simulation_state["completed_tasks"].append(task)
        
        # Update agent workload
        simulation_state["agent_workloads"][agent_type.value] = max(0, simulation_state["agent_workloads"][agent_type.value] - 1)
        
        # Log completion
        self._log_task_completion(task, agent_type, simulation_state)
    
    async def _execute_real_tasks(
        self, 
        simulation_state: Dict[str, Any], 
        max_concurrent_tasks: int
    ) -> Dict[str, Any]:
        """Execute tasks in real mode (not simulation)."""
        
        # This would execute actual tasks with real agents
        # For now, we'll use the simulation but mark it as real execution
        return await self._simulate_autonomous_execution(simulation_state, max_concurrent_tasks)
    
    def _calculate_final_status(
        self, 
        simulation_state: Dict[str, Any], 
        execution_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate final status of the execution."""
        
        total_tasks = simulation_state["total_tasks"]
        completed_tasks = simulation_state["completed_tasks"]
        failed_tasks = len(simulation_state["failed_tasks"])
        remaining_tasks = total_tasks - completed_tasks - failed_tasks
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "remaining_tasks": remaining_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "execution_duration": simulation_state["current_time"] - simulation_state["start_time"],
            "agent_workloads": simulation_state["agent_workloads"],
            "success": execution_results.get("success", False)
        }
    
    def _calculate_remaining_hours(self, simulation_state: Dict[str, Any]) -> float:
        """Calculate estimated remaining work hours."""
        
        remaining_hours = 0.0
        
        # Hours for tasks in queue
        for task in simulation_state["task_queue"]:
            remaining_hours += task.estimated_hours or 4
        
        # Hours for running tasks (partial completion)
        for task_info in simulation_state["running_tasks"]:
            task = task_info["task"]
            estimated_hours = task.estimated_hours or 4
            elapsed_time = simulation_state["current_time"] - task_info["start_time"]
            remaining_time = max(0, estimated_hours - elapsed_time.total_seconds() / 3600)
            remaining_hours += remaining_time
        
        return remaining_hours
    
    def _sort_tasks_for_execution(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks for optimal execution order."""
        
        # Create a mapping of task IDs to tasks
        task_map = {task.id: task for task in tasks}
        
        # Topological sort considering dependencies
        sorted_tasks = []
        remaining_tasks = tasks.copy()
        
        while remaining_tasks:
            # Find tasks with no unresolved dependencies
            ready_tasks = []
            for task in remaining_tasks:
                if not task.dependencies or all(
                    dep_id in [t.id for t in sorted_tasks] for dep_id in task.dependencies
                ):
                    ready_tasks.append(task)
            
            if not ready_tasks:
                # Handle circular dependencies or missing dependencies
                # Add remaining tasks in priority order
                remaining_tasks.sort(key=lambda t: t.priority, reverse=True)
                sorted_tasks.extend(remaining_tasks)
                break
            
            # Sort ready tasks by priority (higher priority first)
            ready_tasks.sort(key=lambda t: t.priority, reverse=True)
            
            # Add the highest priority ready task
            task = ready_tasks[0]
            sorted_tasks.append(task)
            remaining_tasks.remove(task)
        
        return sorted_tasks
    
    async def _load_project(self, project_id: str) -> Optional[Project]:
        """Load a project by ID (placeholder implementation)."""
        
        # In a real implementation, this would load from a database
        # For now, return None as we don't have a project storage system
        return None
    
    def _log_execution_state(self, simulation_state: Dict[str, Any], message: str) -> None:
        """Log execution state."""
        
        log_entry = {
            "timestamp": simulation_state["current_time"].isoformat(),
            "type": "state",
            "message": message,
            "running_tasks": len(simulation_state["running_tasks"]),
            "queued_tasks": len(simulation_state["task_queue"]),
            "completed_tasks": simulation_state["completed_tasks"]
        }
        
        simulation_state["execution_log"].append(log_entry)
    
    def _log_task_start(self, task: Task, agent_type: AgentType, simulation_state: Dict[str, Any]) -> None:
        """Log task start."""
        
        log_entry = {
            "timestamp": simulation_state["current_time"].isoformat(),
            "type": "task_start",
            "task_id": task.id,
            "task_title": task.title,
            "agent_type": agent_type.value,
            "estimated_hours": task.estimated_hours or 4
        }
        
        simulation_state["execution_log"].append(log_entry)
    
    def _log_task_progress(
        self, 
        task: Task, 
        agent_type: AgentType, 
        progress: float, 
        simulation_state: Dict[str, Any]
    ) -> None:
        """Log task progress."""
        
        log_entry = {
            "timestamp": simulation_state["current_time"].isoformat(),
            "type": "task_progress",
            "task_id": task.id,
            "task_title": task.title,
            "agent_type": agent_type.value,
            "progress_percentage": progress * 100
        }
        
        simulation_state["execution_log"].append(log_entry)
    
    def _log_task_processing(
        self, 
        task: Task, 
        agent_type: AgentType, 
        result: Dict[str, Any], 
        simulation_state: Dict[str, Any]
    ) -> None:
        """Log task processing result."""
        
        log_entry = {
            "timestamp": simulation_state["current_time"].isoformat(),
            "type": "task_processing",
            "task_id": task.id,
            "task_title": task.title,
            "agent_type": agent_type.value,
            "processing_result": result.get("summary", "Processing completed")
        }
        
        simulation_state["execution_log"].append(log_entry)
    
    def _log_task_completion(
        self, 
        task: Task, 
        agent_type: AgentType, 
        simulation_state: Dict[str, Any]
    ) -> None:
        """Log task completion."""
        
        log_entry = {
            "timestamp": simulation_state["current_time"].isoformat(),
            "type": "task_completion",
            "task_id": task.id,
            "task_title": task.title,
            "agent_type": agent_type.value,
            "completion_time": simulation_state["current_time"].isoformat()
        }
        
        simulation_state["execution_log"].append(log_entry)
    
    def _log_error(self, message: str, simulation_state: Dict[str, Any]) -> None:
        """Log an error."""
        
        log_entry = {
            "timestamp": simulation_state["current_time"].isoformat(),
            "type": "error",
            "message": message
        }
        
        simulation_state["execution_log"].append(log_entry)

