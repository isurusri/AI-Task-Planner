"""Planner agent for high-level task decomposition and planning."""

from typing import List, Dict, Any
import asyncio
from datetime import datetime

from .base_agent import BaseAgent
from models import Task, AgentType, TaskStatus
from services.openai_service import OpenAIService


class PlannerAgent(BaseAgent):
    """Agent responsible for high-level planning and task decomposition."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.PLANNER,
            name="Strategic Planner",
            description="Decomposes high-level requirements into detailed, actionable tasks"
        )
        self.openai_service = OpenAIService()
    
    def get_capabilities(self) -> List[str]:
        """Return planner agent capabilities."""
        return [
            "task_decomposition",
            "requirement_analysis", 
            "work_breakdown_structure",
            "dependency_mapping",
            "priority_assignment",
            "resource_estimation"
        ]
    
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a planning task using chain-of-thought prompting."""
        self.log_execution(f"Processing planning task: {task.title}")
        
        # Use chain-of-thought prompting for task decomposition
        decomposition_prompt = self._build_decomposition_prompt(task, context)
        
        try:
            response = await self.openai_service.generate_completion(
                prompt=decomposition_prompt,
                max_tokens=1500,
                temperature=0.3  # Lower temperature for more consistent planning
            )
            
            # Parse the response to extract subtasks
            subtasks = self._parse_decomposition_response(response, task.id)
            
            results = {
                "subtasks_created": len(subtasks),
                "decomposition_details": response,
                "subtasks": subtasks,
                "planning_confidence": self._calculate_planning_confidence(response),
                "estimated_complexity": self._assess_complexity(task.description)
            }
            
            self.log_execution(f"Created {len(subtasks)} subtasks for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error processing task {task.id}: {str(e)}")
            return {
                "error": str(e),
                "subtasks_created": 0,
                "planning_confidence": 0.0
            }
    
    def _build_decomposition_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a chain-of-thought prompt for task decomposition."""
        return f"""
You are a senior software architect and project planner. Your task is to decompose the following requirement into detailed, actionable subtasks using chain-of-thought reasoning.

REQUIREMENT: {task.description}

CONTEXT: {context.get('project_context', 'No additional context provided')}

Please follow this chain-of-thought process:

1. ANALYSIS: First, analyze the requirement to understand:
   - What is the core functionality being requested?
   - What are the implicit requirements not explicitly stated?
   - What technical domains are involved?
   - What are the potential challenges or risks?

2. DECOMPOSITION: Break down the requirement into logical components:
   - What are the main functional areas?
   - What are the supporting infrastructure needs?
   - What are the integration points?
   - What are the testing requirements?

3. TASK CREATION: For each component, create specific, actionable tasks:
   - Each task should be clear and measurable
   - Include estimated hours (1-40 hours per task)
   - Assign priority levels (1-5, where 5 is highest)
   - Identify dependencies between tasks

4. VALIDATION: Review the decomposition for:
   - Completeness (all aspects covered)
   - Clarity (tasks are unambiguous)
   - Feasibility (tasks are achievable)
   - Dependencies (logical task ordering)

Please provide your response in the following JSON format:
{{
    "analysis": "Your analysis of the requirement",
    "decomposition_strategy": "Your approach to breaking down the work",
    "subtasks": [
        {{
            "title": "Task title",
            "description": "Detailed task description",
            "estimated_hours": 8,
            "priority": 3,
            "dependencies": ["task_id_1", "task_id_2"],
            "category": "frontend|backend|database|testing|deployment|documentation"
        }}
    ],
    "risks": ["Identified risk 1", "Identified risk 2"],
    "assumptions": ["Assumption 1", "Assumption 2"]
}}
"""
    
    def _parse_decomposition_response(self, response: str, parent_task_id: str) -> List[Dict[str, Any]]:
        """Parse the OpenAI response to extract subtask information."""
        import json
        import uuid
        
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                subtasks = []
                for i, subtask_data in enumerate(data.get('subtasks', [])):
                    subtask = {
                        "id": str(uuid.uuid4()),
                        "title": subtask_data.get('title', f'Subtask {i+1}'),
                        "description": subtask_data.get('description', ''),
                        "estimated_hours": subtask_data.get('estimated_hours', 4),
                        "priority": subtask_data.get('priority', 3),
                        "dependencies": subtask_data.get('dependencies', []),
                        "category": subtask_data.get('category', 'general'),
                        "parent_task": parent_task_id,
                        "status": TaskStatus.PENDING.value
                    }
                    subtasks.append(subtask)
                
                return subtasks
            else:
                # Fallback: create a simple subtask if JSON parsing fails
                return [{
                    "id": str(uuid.uuid4()),
                    "title": "Decomposed Task",
                    "description": response[:200] + "..." if len(response) > 200 else response,
                    "estimated_hours": 8,
                    "priority": 3,
                    "dependencies": [],
                    "category": "general",
                    "parent_task": parent_task_id,
                    "status": TaskStatus.PENDING.value
                }]
                
        except (json.JSONDecodeError, KeyError) as e:
            self.log_execution(f"Error parsing decomposition response: {str(e)}")
            # Return a fallback subtask
            return [{
                "id": str(uuid.uuid4()),
                "title": "Decomposed Task",
                "description": response[:200] + "..." if len(response) > 200 else response,
                "estimated_hours": 8,
                "priority": 3,
                "dependencies": [],
                "category": "general",
                "parent_task": parent_task_id,
                "status": TaskStatus.PENDING.value
            }]
    
    def _calculate_planning_confidence(self, response: str) -> float:
        """Calculate confidence score based on response quality."""
        # Simple heuristic: longer, more detailed responses get higher confidence
        word_count = len(response.split())
        
        if word_count > 500:
            return 0.9
        elif word_count > 300:
            return 0.7
        elif word_count > 150:
            return 0.5
        else:
            return 0.3
    
    def _assess_complexity(self, description: str) -> str:
        """Assess task complexity based on description."""
        complexity_indicators = {
            "high": ["integration", "architecture", "scalability", "performance", "security", "distributed"],
            "medium": ["api", "database", "ui", "authentication", "validation"],
            "low": ["simple", "basic", "static", "display", "show"]
        }
        
        description_lower = description.lower()
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                return complexity
        
        return "medium"  # Default complexity

