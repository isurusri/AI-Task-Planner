"""Coordinator agent for orchestrating multi-agent workflows."""

from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime
import uuid

from .base_agent import BaseAgent
from models import Task, AgentType, TaskStatus, Project
from services.openai_service import OpenAIService


class CoordinatorAgent(BaseAgent):
    """Agent responsible for orchestrating multi-agent workflows and task coordination."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.COORDINATOR,
            name="Workflow Coordinator",
            description="Orchestrates multi-agent workflows, manages task dependencies, and coordinates execution"
        )
        self.openai_service = OpenAIService()
        self.agent_registry = {}
        self.workflow_state = {}
    
    def get_capabilities(self) -> List[str]:
        """Return coordinator agent capabilities."""
        return [
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
    
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a coordination task."""
        self.log_execution(f"Processing coordination task: {task.title}")
        
        # Determine the type of coordination task
        task_type = self._classify_coordination_task(task)
        
        if task_type == "workflow_orchestration":
            return await self._handle_workflow_orchestration(task, context)
        elif task_type == "task_coordination":
            return await self._handle_task_coordination(task, context)
        elif task_type == "dependency_management":
            return await self._handle_dependency_management(task, context)
        elif task_type == "progress_monitoring":
            return await self._handle_progress_monitoring(task, context)
        else:
            return await self._handle_general_coordination(task, context)
    
    def _classify_coordination_task(self, task: Task) -> str:
        """Classify the type of coordination task."""
        description_lower = task.description.lower()
        
        if any(keyword in description_lower for keyword in ["workflow", "orchestrate", "coordinate", "manage"]):
            return "workflow_orchestration"
        elif any(keyword in description_lower for keyword in ["task", "assign", "schedule", "distribute"]):
            return "task_coordination"
        elif any(keyword in description_lower for keyword in ["dependency", "depend", "order", "sequence"]):
            return "dependency_management"
        elif any(keyword in description_lower for keyword in ["monitor", "track", "progress", "status"]):
            return "progress_monitoring"
        else:
            return "general_coordination"
    
    async def _handle_workflow_orchestration(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow orchestration tasks."""
        orchestration_prompt = self._build_orchestration_prompt(task, context)
        
        try:
            response = await self.openai_service.generate_completion(
                prompt=orchestration_prompt,
                max_tokens=3000,
                temperature=0.2
            )
            
            workflow_plan = self._parse_workflow_plan(response)
            
            results = {
                "workflow_plan": workflow_plan,
                "execution_sequence": self._extract_execution_sequence(response),
                "agent_assignments": self._extract_agent_assignments(response),
                "dependency_graph": self._extract_dependency_graph(response),
                "timeline_estimation": self._extract_timeline_estimation(response),
                "risk_assessment": self._extract_risk_assessment(response),
                "optimization_suggestions": self._extract_optimization_suggestions(response)
            }
            
            self.log_execution(f"Created workflow orchestration plan for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error orchestrating workflow {task.id}: {str(e)}")
            return {
                "error": str(e),
                "workflow_plan": "Workflow orchestration failed"
            }
    
    async def _handle_task_coordination(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle task coordination tasks."""
        coordination_prompt = self._build_coordination_prompt(task, context)
        
        try:
            response = await self.openai_service.generate_completion(
                prompt=coordination_prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            results = {
                "coordination_strategy": self._extract_coordination_strategy(response),
                "task_assignments": self._extract_task_assignments(response),
                "communication_plan": self._extract_communication_plan(response),
                "synchronization_points": self._extract_synchronization_points(response),
                "conflict_resolution": self._extract_conflict_resolution(response),
                "quality_gates": self._extract_quality_gates(response)
            }
            
            self.log_execution(f"Coordinated tasks for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error coordinating tasks {task.id}: {str(e)}")
            return {
                "error": str(e),
                "coordination_strategy": "Task coordination failed"
            }
    
    async def _handle_dependency_management(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle dependency management tasks."""
        dependency_prompt = self._build_dependency_prompt(task, context)
        
        try:
            response = await self.openai_service.generate_completion(
                prompt=dependency_prompt,
                max_tokens=2000,
                temperature=0.1
            )
            
            results = {
                "dependency_analysis": self._extract_dependency_analysis(response),
                "critical_path": self._extract_critical_path(response),
                "dependency_resolution": self._extract_dependency_resolution(response),
                "bottleneck_identification": self._extract_bottleneck_identification(response),
                "optimization_opportunities": self._extract_optimization_opportunities(response)
            }
            
            self.log_execution(f"Managed dependencies for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error managing dependencies {task.id}: {str(e)}")
            return {
                "error": str(e),
                "dependency_analysis": "Dependency management failed"
            }
    
    async def _handle_progress_monitoring(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle progress monitoring tasks."""
        monitoring_prompt = self._build_monitoring_prompt(task, context)
        
        try:
            response = await self.openai_service.generate_completion(
                prompt=monitoring_prompt,
                max_tokens=2000,
                temperature=0.2
            )
            
            results = {
                "monitoring_metrics": self._extract_monitoring_metrics(response),
                "progress_dashboard": self._extract_progress_dashboard(response),
                "alert_conditions": self._extract_alert_conditions(response),
                "reporting_schedule": self._extract_reporting_schedule(response),
                "escalation_procedures": self._extract_escalation_procedures(response)
            }
            
            self.log_execution(f"Set up progress monitoring for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error monitoring progress {task.id}: {str(e)}")
            return {
                "error": str(e),
                "monitoring_metrics": "Progress monitoring failed"
            }
    
    async def _handle_general_coordination(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general coordination tasks."""
        general_prompt = self._build_general_coordination_prompt(task, context)
        
        try:
            response = await self.openai_service.generate_completion(
                prompt=general_prompt,
                max_tokens=1500,
                temperature=0.3
            )
            
            results = {
                "coordination_approach": response[:500] + "..." if len(response) > 500 else response,
                "key_considerations": self._extract_key_considerations(response),
                "coordination_notes": response
            }
            
            self.log_execution(f"Provided coordination approach for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error processing coordination task {task.id}: {str(e)}")
            return {
                "error": str(e),
                "coordination_approach": "Coordination failed"
            }
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the coordinator."""
        self.agent_registry[agent.type.value] = agent
        self.log_execution(f"Registered agent: {agent.type.value}")
    
    async def assign_task_to_agent(self, task: Task, agent_type: AgentType) -> bool:
        """Assign a task to a specific agent type."""
        if agent_type.value not in self.agent_registry:
            self.log_execution(f"Agent type {agent_type.value} not registered")
            return False
        
        agent = self.agent_registry[agent_type.value]
        success = await agent.assign_task(task)
        
        if success:
            self.log_execution(f"Assigned task {task.id} to {agent_type.value}")
        else:
            self.log_execution(f"Failed to assign task {task.id} to {agent_type.value}")
        
        return success
    
    async def execute_workflow(self, project: Project) -> Dict[str, Any]:
        """Execute a complete workflow for a project."""
        self.log_execution(f"Starting workflow execution for project {project.id}")
        
        execution_results = {
            "project_id": project.id,
            "start_time": datetime.now().isoformat(),
            "task_results": {},
            "workflow_status": "running",
            "completed_tasks": 0,
            "total_tasks": len(project.tasks),
            "errors": []
        }
        
        try:
            # Sort tasks by priority and dependencies
            sorted_tasks = self._sort_tasks_by_dependencies(project.tasks)
            
            # Execute tasks in order
            for task in sorted_tasks:
                if task.status == TaskStatus.COMPLETED:
                    continue
                
                # Find appropriate agent for task
                agent_type = await self._select_agent_for_task(task, project)
                
                if agent_type and agent_type.value in self.agent_registry:
                    agent = self.agent_registry[agent_type.value]
                    
                    # Process task
                    task_result = await agent.process_task(task, {"project_context": project.description})
                    execution_results["task_results"][task.id] = task_result
                    
                    # Mark task as completed
                    await agent.complete_task(task, task_result)
                    execution_results["completed_tasks"] += 1
                    
                    self.log_execution(f"Completed task {task.id} with {agent_type.value}")
                else:
                    error_msg = f"No suitable agent found for task {task.id}"
                    execution_results["errors"].append(error_msg)
                    self.log_execution(error_msg)
            
            execution_results["workflow_status"] = "completed"
            execution_results["end_time"] = datetime.now().isoformat()
            
        except Exception as e:
            execution_results["workflow_status"] = "failed"
            execution_results["errors"].append(str(e))
            self.log_execution(f"Workflow execution failed: {str(e)}")
        
        return execution_results
    
    def _sort_tasks_by_dependencies(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their dependencies to ensure proper execution order."""
        # Simple topological sort implementation
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
                # Circular dependency or missing dependency
                break
            
            # Sort ready tasks by priority (higher priority first)
            ready_tasks.sort(key=lambda t: t.priority, reverse=True)
            
            # Add the highest priority ready task
            task = ready_tasks[0]
            sorted_tasks.append(task)
            remaining_tasks.remove(task)
        
        return sorted_tasks
    
    async def _select_agent_for_task(self, task: Task, project: Project) -> Optional[AgentType]:
        """Select the most appropriate agent for a task."""
        # Use AI to suggest agent assignment
        try:
            available_agents = [agent.to_agent_model() for agent in self.agent_registry.values()]
            suggestion = await self.openai_service.suggest_agent_assignment(
                {
                    "title": task.title,
                    "description": task.description,
                    "category": task.metadata.get("category", "general")
                },
                available_agents
            )
            
            suggested_agent = suggestion.get("suggested_agent", "developer")
            
            # Map string to AgentType enum
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
            self.log_execution(f"Error selecting agent for task {task.id}: {str(e)}")
            return AgentType.DEVELOPER  # Default fallback
    
    def _build_orchestration_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a workflow orchestration prompt."""
        return f"""
You are a senior project manager and workflow orchestrator. Design a comprehensive workflow for:

TASK: {task.title}
DESCRIPTION: {task.description}

PROJECT_CONTEXT: {context.get('project_context', 'Not specified')}
AVAILABLE_AGENTS: {context.get('available_agents', 'Planner, Analyzer, Developer, Tester, Reviewer, Coordinator')}

Please design a workflow that includes:

1. WORKFLOW_STRUCTURE:
   - Task breakdown and sequencing
   - Agent assignments and responsibilities
   - Dependencies and critical path
   - Parallel execution opportunities

2. EXECUTION_PLAN:
   - Step-by-step execution sequence
   - Synchronization points
   - Quality gates and checkpoints
   - Risk mitigation strategies

3. COORDINATION_STRATEGY:
   - Communication protocols
   - Progress monitoring
   - Conflict resolution
   - Escalation procedures

4. OPTIMIZATION:
   - Resource allocation
   - Timeline optimization
   - Bottleneck identification
   - Performance improvements

Format your response as a structured workflow plan with clear phases and responsibilities.
"""
    
    def _build_coordination_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a task coordination prompt."""
        return f"""
You are a senior coordinator managing task distribution and execution. Coordinate:

TASK: {task.title}
DESCRIPTION: {task.description}

TASK_LIST: {context.get('task_list', 'Not specified')}
AGENT_CAPABILITIES: {context.get('agent_capabilities', 'Not specified')}

Please provide:

1. TASK_ASSIGNMENT_STRATEGY:
   - How to match tasks to agents
   - Load balancing considerations
   - Skill-based assignment

2. COORDINATION_MECHANISMS:
   - Communication protocols
   - Status reporting
   - Progress tracking

3. SYNCHRONIZATION:
   - Dependencies management
   - Handoff procedures
   - Quality gates

4. CONFLICT_RESOLUTION:
   - Resource conflicts
   - Priority conflicts
   - Escalation procedures

Focus on efficient task distribution and smooth execution flow.
"""
    
    def _build_dependency_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a dependency management prompt."""
        return f"""
You are a senior project manager analyzing task dependencies. Analyze:

TASK: {task.title}
DESCRIPTION: {task.description}

TASK_DEPENDENCIES: {context.get('dependencies', 'Not specified')}
PROJECT_TIMELINE: {context.get('timeline', 'Not specified')}

Please provide:

1. DEPENDENCY_ANALYSIS:
   - Critical path identification
   - Dependency types and strengths
   - Bottleneck analysis

2. RESOLUTION_STRATEGY:
   - Dependency optimization
   - Parallel execution opportunities
   - Risk mitigation

3. TIMELINE_IMPACT:
   - Schedule implications
   - Resource requirements
   - Contingency planning

Focus on identifying and resolving dependency conflicts.
"""
    
    def _build_monitoring_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a progress monitoring prompt."""
        return f"""
You are a senior project manager setting up progress monitoring. Design monitoring for:

TASK: {task.title}
DESCRIPTION: {task.description}

MONITORING_REQUIREMENTS: {context.get('monitoring_requirements', 'Not specified')}
PROJECT_METRICS: {context.get('metrics', 'Not specified')}

Please provide:

1. MONITORING_METRICS:
   - Key performance indicators
   - Progress tracking methods
   - Quality metrics

2. DASHBOARD_DESIGN:
   - Real-time status display
   - Progress visualization
   - Alert systems

3. REPORTING_SCHEDULE:
   - Regular reporting intervals
   - Stakeholder communication
   - Escalation procedures

Focus on actionable insights and early warning systems.
"""
    
    def _build_general_coordination_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a general coordination prompt."""
        return f"""
You are a senior coordinator providing general coordination guidance for:

TASK: {task.title}
DESCRIPTION: {task.description}

CONTEXT: {context.get('project_context', 'No additional context')}

Please provide:
1. Coordination approach
2. Key considerations
3. Best practices
4. Recommendations

Provide practical, actionable coordination guidance.
"""
    
    def _parse_workflow_plan(self, response: str) -> Dict[str, Any]:
        """Parse workflow plan from response."""
        return {
            "plan_summary": response[:500] + "..." if len(response) > 500 else response,
            "phases": self._extract_phases(response),
            "timeline": self._extract_timeline(response),
            "resources": self._extract_resources(response)
        }
    
    def _extract_execution_sequence(self, response: str) -> List[str]:
        """Extract execution sequence from response."""
        lines = response.split('\n')
        sequence = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['step', 'phase', 'stage', '1.', '2.', '3.']):
                sequence.append(line.strip())
        
        return sequence[:10]  # First 10 sequence steps
    
    def _extract_agent_assignments(self, response: str) -> Dict[str, str]:
        """Extract agent assignments from response."""
        assignments = {}
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['assign', 'agent', 'responsible']):
                # Try to extract task-agent mapping
                parts = line.split(':')
                if len(parts) == 2:
                    task = parts[0].strip()
                    agent = parts[1].strip()
                    assignments[task] = agent
        
        return assignments
    
    def _extract_dependency_graph(self, response: str) -> Dict[str, List[str]]:
        """Extract dependency graph from response."""
        dependencies = {}
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['depend', 'requires', 'after', 'before']):
                # Try to extract dependency relationships
                if '->' in line or 'depends on' in line.lower():
                    parts = line.split('->' if '->' in line else 'depends on')
                    if len(parts) == 2:
                        dependent = parts[0].strip()
                        dependency = parts[1].strip()
                        if dependent not in dependencies:
                            dependencies[dependent] = []
                        dependencies[dependent].append(dependency)
        
        return dependencies
    
    def _extract_timeline_estimation(self, response: str) -> str:
        """Extract timeline estimation from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['timeline', 'duration', 'schedule', 'estimate']):
                return line.strip()
        return "Timeline not estimated"
    
    def _extract_risk_assessment(self, response: str) -> List[str]:
        """Extract risk assessment from response."""
        lines = response.split('\n')
        risks = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['risk', 'threat', 'challenge', 'issue']):
                risks.append(line.strip())
        
        return risks[:5]  # First 5 risks
    
    def _extract_optimization_suggestions(self, response: str) -> List[str]:
        """Extract optimization suggestions from response."""
        lines = response.split('\n')
        suggestions = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['optimize', 'improve', 'enhance', 'efficient']):
                suggestions.append(line.strip())
        
        return suggestions[:5]  # First 5 suggestions
    
    def _extract_coordination_strategy(self, response: str) -> str:
        """Extract coordination strategy from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['strategy', 'approach', 'method']):
                return line.strip()
        return "Coordination strategy not specified"
    
    def _extract_task_assignments(self, response: str) -> Dict[str, str]:
        """Extract task assignments from response."""
        return self._extract_agent_assignments(response)
    
    def _extract_communication_plan(self, response: str) -> str:
        """Extract communication plan from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['communication', 'meeting', 'report']):
                return line.strip()
        return "Communication plan not specified"
    
    def _extract_synchronization_points(self, response: str) -> List[str]:
        """Extract synchronization points from response."""
        lines = response.split('\n')
        sync_points = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['sync', 'synchronize', 'checkpoint', 'gate']):
                sync_points.append(line.strip())
        
        return sync_points[:5]  # First 5 sync points
    
    def _extract_conflict_resolution(self, response: str) -> str:
        """Extract conflict resolution from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['conflict', 'resolve', 'escalate']):
                return line.strip()
        return "Conflict resolution not specified"
    
    def _extract_quality_gates(self, response: str) -> List[str]:
        """Extract quality gates from response."""
        lines = response.split('\n')
        gates = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['quality', 'gate', 'checkpoint', 'review']):
                gates.append(line.strip())
        
        return gates[:5]  # First 5 quality gates
    
    def _extract_dependency_analysis(self, response: str) -> str:
        """Extract dependency analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['dependency', 'analysis', 'critical path']):
                return line.strip()
        return "Dependency analysis not provided"
    
    def _extract_critical_path(self, response: str) -> List[str]:
        """Extract critical path from response."""
        lines = response.split('\n')
        critical_path = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['critical', 'path', 'bottleneck']):
                critical_path.append(line.strip())
        
        return critical_path[:5]  # First 5 critical path items
    
    def _extract_dependency_resolution(self, response: str) -> str:
        """Extract dependency resolution from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['resolve', 'solution', 'fix']):
                return line.strip()
        return "Dependency resolution not provided"
    
    def _extract_bottleneck_identification(self, response: str) -> List[str]:
        """Extract bottleneck identification from response."""
        lines = response.split('\n')
        bottlenecks = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['bottleneck', 'blocking', 'delay']):
                bottlenecks.append(line.strip())
        
        return bottlenecks[:5]  # First 5 bottlenecks
    
    def _extract_optimization_opportunities(self, response: str) -> List[str]:
        """Extract optimization opportunities from response."""
        lines = response.split('\n')
        opportunities = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['optimize', 'improve', 'opportunity']):
                opportunities.append(line.strip())
        
        return opportunities[:5]  # First 5 opportunities
    
    def _extract_monitoring_metrics(self, response: str) -> Dict[str, Any]:
        """Extract monitoring metrics from response."""
        metrics = {
            "progress_tracking": "Not specified",
            "quality_metrics": "Not specified",
            "performance_metrics": "Not specified"
        }
        
        lines = response.split('\n')
        for line in lines:
            if 'progress' in line.lower():
                metrics["progress_tracking"] = line.strip()
            elif 'quality' in line.lower():
                metrics["quality_metrics"] = line.strip()
            elif 'performance' in line.lower():
                metrics["performance_metrics"] = line.strip()
        
        return metrics
    
    def _extract_progress_dashboard(self, response: str) -> str:
        """Extract progress dashboard from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['dashboard', 'display', 'visualization']):
                return line.strip()
        return "Progress dashboard not specified"
    
    def _extract_alert_conditions(self, response: str) -> List[str]:
        """Extract alert conditions from response."""
        lines = response.split('\n')
        alerts = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['alert', 'warning', 'threshold']):
                alerts.append(line.strip())
        
        return alerts[:5]  # First 5 alert conditions
    
    def _extract_reporting_schedule(self, response: str) -> str:
        """Extract reporting schedule from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['schedule', 'report', 'frequency']):
                return line.strip()
        return "Reporting schedule not specified"
    
    def _extract_escalation_procedures(self, response: str) -> str:
        """Extract escalation procedures from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['escalate', 'escalation', 'procedure']):
                return line.strip()
        return "Escalation procedures not specified"
    
    def _extract_key_considerations(self, response: str) -> List[str]:
        """Extract key considerations from response."""
        lines = response.split('\n')
        considerations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['consider', 'important', 'key', 'note']):
                considerations.append(line.strip())
        
        return considerations[:5]  # First 5 considerations
    
    def _extract_phases(self, response: str) -> List[str]:
        """Extract phases from response."""
        lines = response.split('\n')
        phases = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['phase', 'stage', 'step']):
                phases.append(line.strip())
        
        return phases[:5]  # First 5 phases
    
    def _extract_timeline(self, response: str) -> str:
        """Extract timeline from response."""
        return self._extract_timeline_estimation(response)
    
    def _extract_resources(self, response: str) -> List[str]:
        """Extract resources from response."""
        lines = response.split('\n')
        resources = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['resource', 'agent', 'person', 'tool']):
                resources.append(line.strip())
        
        return resources[:5]  # First 5 resources

