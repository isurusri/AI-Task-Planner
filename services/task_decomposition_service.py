"""Service for decomposing user input into detailed subtasks."""

from typing import List, Dict, Any, Optional
import asyncio
import uuid
from datetime import datetime

from models import (
    Task, Project, AgentType, TaskStatus, 
    TaskDecompositionRequest, TaskDecompositionResponse
)
from services.openai_service import OpenAIService
from agents import PlannerAgent, AnalyzerAgent, DeveloperAgent, TesterAgent, ReviewerAgent, CoordinatorAgent


class TaskDecompositionService:
    """Service for decomposing user input into detailed, actionable tasks."""
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.planner_agent = PlannerAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.developer_agent = DeveloperAgent()
        self.tester_agent = TesterAgent()
        self.reviewer_agent = ReviewerAgent()
        self.coordinator_agent = CoordinatorAgent()
        
        # Register agents with coordinator
        self.coordinator_agent.register_agent(self.planner_agent)
        self.coordinator_agent.register_agent(self.analyzer_agent)
        self.coordinator_agent.register_agent(self.developer_agent)
        self.coordinator_agent.register_agent(self.tester_agent)
        self.coordinator_agent.register_agent(self.reviewer_agent)
    
    async def decompose_task(self, request: TaskDecompositionRequest) -> TaskDecompositionResponse:
        """Decompose a user input into detailed subtasks using multi-agent approach."""
        
        # Create initial project
        project_id = str(uuid.uuid4())
        project = Project(
            id=project_id,
            name=f"Project: {request.user_input[:50]}...",
            description=request.user_input
        )
        
        # Create root task
        root_task = Task(
            id=str(uuid.uuid4()),
            title="Main Feature Request",
            description=request.user_input,
            priority=5,
            status=TaskStatus.PENDING,
            metadata={
                "category": "planning",
                "decomposition_depth": 0,
                "project_context": request.project_context or ""
            }
        )
        
        project.tasks.append(root_task)
        
        # Initialize agents
        agents = [
            AgentType.PLANNER,
            AgentType.ANALYZER, 
            AgentType.DEVELOPER,
            AgentType.TESTER,
            AgentType.REVIEWER,
            AgentType.COORDINATOR
        ]
        
        # Create agent instances
        for agent_type in agents:
            agent = self._create_agent(agent_type)
            project.agents.append(agent)
        
        # Decompose using chain-of-thought approach
        decomposition_results = await self._perform_decomposition(
            root_task, 
            project, 
            request.max_depth,
            request.include_estimates
        )
        
        # Create execution plan
        execution_plan = await self._create_execution_plan(project)
        
        # Generate decomposition summary
        summary = await self._generate_decomposition_summary(project, decomposition_results)
        
        return TaskDecompositionResponse(
            project=project,
            decomposition_summary=summary,
            execution_plan=execution_plan
        )
    
    async def _perform_decomposition(
        self, 
        root_task: Task, 
        project: Project, 
        max_depth: int,
        include_estimates: bool
    ) -> Dict[str, Any]:
        """Perform multi-agent decomposition of the root task."""
        
        decomposition_results = {
            "total_tasks_created": 0,
            "decomposition_layers": [],
            "agent_contributions": {},
            "quality_metrics": {}
        }
        
        current_tasks = [root_task]
        current_depth = 0
        
        while current_depth < max_depth and current_tasks:
            next_layer_tasks = []
            layer_results = {
                "depth": current_depth,
                "tasks_processed": 0,
                "subtasks_created": 0,
                "agent_assignments": {}
            }
            
            for task in current_tasks:
                if task.status == TaskStatus.COMPLETED:
                    continue
                
                # Select appropriate agent for decomposition
                agent_type = await self._select_decomposition_agent(task, project)
                
                if agent_type:
                    # Process task with selected agent
                    task_result = await self._process_with_agent(task, agent_type, project)
                    
                    if task_result and "subtasks" in task_result:
                        # Create subtasks
                        subtasks = await self._create_subtasks(
                            task_result["subtasks"], 
                            task.id, 
                            current_depth + 1,
                            include_estimates
                        )
                        
                        # Add subtasks to project
                        project.tasks.extend(subtasks)
                        task.subtasks = [st.id for st in subtasks]
                        
                        next_layer_tasks.extend(subtasks)
                        layer_results["subtasks_created"] += len(subtasks)
                        layer_results["agent_assignments"][task.id] = agent_type.value
                        
                        # Mark parent task as completed
                        task.status = TaskStatus.COMPLETED
                        task.updated_at = datetime.now()
                    
                    layer_results["tasks_processed"] += 1
                    
                    # Track agent contributions
                    if agent_type.value not in decomposition_results["agent_contributions"]:
                        decomposition_results["agent_contributions"][agent_type.value] = 0
                    decomposition_results["agent_contributions"][agent_type.value] += 1
            
            decomposition_results["decomposition_layers"].append(layer_results)
            decomposition_results["total_tasks_created"] += layer_results["subtasks_created"]
            
            current_tasks = next_layer_tasks
            current_depth += 1
        
        # Calculate quality metrics
        decomposition_results["quality_metrics"] = await self._calculate_quality_metrics(project)
        
        return decomposition_results
    
    async def _select_decomposition_agent(self, task: Task, project: Project) -> Optional[AgentType]:
        """Select the most appropriate agent for task decomposition."""
        
        # Use AI to determine the best agent
        try:
            available_agents = [
                {
                    "type": agent.type.value,
                    "description": agent.description,
                    "capabilities": agent.capabilities,
                    "is_available": agent.is_available
                }
                for agent in project.agents
            ]
            suggestion = await self.openai_service.suggest_agent_assignment(
                {
                    "title": task.title,
                    "description": task.description,
                    "category": task.metadata.get("category", "general"),
                    "depth": task.metadata.get("decomposition_depth", 0)
                },
                available_agents
            )
            
            suggested_agent = suggestion.get("suggested_agent", "planner")
            
            # Map to AgentType enum
            agent_mapping = {
                "planner": AgentType.PLANNER,
                "analyzer": AgentType.ANALYZER,
                "developer": AgentType.DEVELOPER,
                "tester": AgentType.TESTER,
                "reviewer": AgentType.REVIEWER,
                "coordinator": AgentType.COORDINATOR
            }
            
            return agent_mapping.get(suggested_agent, AgentType.PLANNER)
            
        except Exception as e:
            print(f"Error selecting agent: {str(e)}")
            return AgentType.PLANNER  # Default fallback
    
    async def _process_with_agent(
        self, 
        task: Task, 
        agent_type: AgentType, 
        project: Project
    ) -> Optional[Dict[str, Any]]:
        """Process a task with a specific agent."""
        
        try:
            if agent_type == AgentType.PLANNER:
                return await self.planner_agent.process_task(task, {
                    "project_context": project.description,
                    "tech_stack": "Python, FastAPI, OpenAI"
                })
            elif agent_type == AgentType.ANALYZER:
                return await self.analyzer_agent.process_task(task, {
                    "project_context": project.description,
                    "tech_stack": "Python, FastAPI, OpenAI"
                })
            elif agent_type == AgentType.DEVELOPER:
                return await self.developer_agent.process_task(task, {
                    "project_context": project.description,
                    "tech_stack": "Python, FastAPI, OpenAI"
                })
            elif agent_type == AgentType.TESTER:
                return await self.tester_agent.process_task(task, {
                    "project_context": project.description,
                    "tech_stack": "Python, FastAPI, OpenAI"
                })
            elif agent_type == AgentType.REVIEWER:
                return await self.reviewer_agent.process_task(task, {
                    "project_context": project.description,
                    "tech_stack": "Python, FastAPI, OpenAI"
                })
            elif agent_type == AgentType.COORDINATOR:
                return await self.coordinator_agent.process_task(task, {
                    "project_context": project.description,
                    "tech_stack": "Python, FastAPI, OpenAI"
                })
            else:
                return None
                
        except Exception as e:
            print(f"Error processing task with {agent_type.value}: {str(e)}")
            return None
    
    async def _create_subtasks(
        self, 
        subtask_data: List[Dict[str, Any]], 
        parent_task_id: str,
        depth: int,
        include_estimates: bool
    ) -> List[Task]:
        """Create Task objects from subtask data."""
        
        subtasks = []
        
        for i, subtask_info in enumerate(subtask_data):
            # Generate unique ID if not provided
            task_id = subtask_info.get("id", str(uuid.uuid4()))
            
            # Create task
            task = Task(
                id=task_id,
                title=subtask_info.get("title", f"Subtask {i+1}"),
                description=subtask_info.get("description", ""),
                priority=subtask_info.get("priority", 3),
                status=TaskStatus.PENDING,
                parent_task=parent_task_id,
                dependencies=subtask_info.get("dependencies", []),
                metadata={
                    "category": subtask_info.get("category", "general"),
                    "decomposition_depth": depth,
                    "original_index": i
                }
            )
            
            # Add time estimates if requested
            if include_estimates and "estimated_hours" in subtask_info:
                task.estimated_hours = subtask_info["estimated_hours"]
            
            subtasks.append(task)
        
        return subtasks
    
    async def _create_execution_plan(self, project: Project) -> List[Dict[str, Any]]:
        """Create an execution plan for the project."""
        
        # Sort tasks by dependencies and priority
        sorted_tasks = self._sort_tasks_for_execution(project.tasks)
        
        execution_plan = []
        
        for i, task in enumerate(sorted_tasks):
            # Determine suggested agent for execution
            suggested_agent = await self._select_decomposition_agent(task, project)
            
            plan_entry = {
                "step": i + 1,
                "task_id": task.id,
                "task_title": task.title,
                "suggested_agent": suggested_agent.value if suggested_agent else "developer",
                "priority": task.priority,
                "estimated_hours": task.estimated_hours or 4,
                "dependencies": task.dependencies,
                "category": task.metadata.get("category", "general")
            }
            
            execution_plan.append(plan_entry)
        
        return execution_plan
    
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
    
    async def _generate_decomposition_summary(
        self, 
        project: Project, 
        decomposition_results: Dict[str, Any]
    ) -> str:
        """Generate a summary of the decomposition process."""
        
        summary_prompt = f"""
Summarize the task decomposition process for this project:

PROJECT: {project.name}
DESCRIPTION: {project.description}

DECOMPOSITION_RESULTS:
- Total tasks created: {decomposition_results['total_tasks_created']}
- Decomposition layers: {len(decomposition_results['decomposition_layers'])}
- Agent contributions: {decomposition_results['agent_contributions']}

TASKS_CREATED:
{chr(10).join([f"- {task.title} (Priority: {task.priority})" for task in project.tasks[:10]])}

Please provide a concise summary of:
1. What was decomposed
2. How many tasks were created
3. The decomposition approach used
4. Key insights and recommendations
"""
        
        try:
            summary = await self.openai_service.generate_completion(
                prompt=summary_prompt,
                max_tokens=500,
                temperature=0.3
            )
            return summary
        except Exception as e:
            return f"Decomposition completed with {decomposition_results['total_tasks_created']} tasks created across {len(decomposition_results['decomposition_layers'])} layers."
    
    async def _calculate_quality_metrics(self, project: Project) -> Dict[str, Any]:
        """Calculate quality metrics for the decomposition."""
        
        total_tasks = len(project.tasks)
        tasks_with_descriptions = len([t for t in project.tasks if t.description])
        tasks_with_estimates = len([t for t in project.tasks if t.estimated_hours])
        tasks_with_dependencies = len([t for t in project.tasks if t.dependencies])
        
        # Calculate average task size
        avg_estimated_hours = 0
        if tasks_with_estimates > 0:
            total_hours = sum(t.estimated_hours for t in project.tasks if t.estimated_hours)
            avg_estimated_hours = total_hours / tasks_with_estimates
        
        return {
            "total_tasks": total_tasks,
            "description_coverage": (tasks_with_descriptions / total_tasks * 100) if total_tasks > 0 else 0,
            "estimation_coverage": (tasks_with_estimates / total_tasks * 100) if total_tasks > 0 else 0,
            "dependency_coverage": (tasks_with_dependencies / total_tasks * 100) if total_tasks > 0 else 0,
            "average_task_size_hours": avg_estimated_hours,
            "complexity_distribution": self._calculate_complexity_distribution(project.tasks)
        }
    
    def _calculate_complexity_distribution(self, tasks: List[Task]) -> Dict[str, int]:
        """Calculate complexity distribution of tasks."""
        complexity_counts = {"low": 0, "medium": 0, "high": 0}
        
        for task in tasks:
            estimated_hours = task.estimated_hours or 4
            
            if estimated_hours <= 4:
                complexity_counts["low"] += 1
            elif estimated_hours <= 12:
                complexity_counts["medium"] += 1
            else:
                complexity_counts["high"] += 1
        
        return complexity_counts
    
    def _create_agent(self, agent_type: AgentType) -> Any:
        """Create an agent instance of the specified type."""
        if agent_type == AgentType.PLANNER:
            return self.planner_agent
        elif agent_type == AgentType.ANALYZER:
            return self.analyzer_agent
        elif agent_type == AgentType.DEVELOPER:
            return self.developer_agent
        elif agent_type == AgentType.TESTER:
            return self.tester_agent
        elif agent_type == AgentType.REVIEWER:
            return self.reviewer_agent
        elif agent_type == AgentType.COORDINATOR:
            return self.coordinator_agent
        else:
            return self.planner_agent
