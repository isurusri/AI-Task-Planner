"""Analyzer agent for requirement analysis and technical assessment."""

from typing import List, Dict, Any
import asyncio
from datetime import datetime

from .base_agent import BaseAgent
from models import Task, AgentType, TaskStatus
from services.llm_factory_service import LLMFactoryService


class AnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing requirements and technical feasibility."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.ANALYZER,
            name="Technical Analyzer",
            description="Analyzes requirements, assesses technical feasibility, and identifies potential issues"
        )
        self.llm_service = LLMFactoryService()
    
    def get_capabilities(self) -> List[str]:
        """Return analyzer agent capabilities."""
        return [
            "requirement_analysis",
            "technical_feasibility_assessment",
            "risk_identification",
            "dependency_analysis",
            "performance_analysis",
            "security_assessment",
            "architecture_review"
        ]
    
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process an analysis task using detailed technical assessment."""
        self.log_execution(f"Processing analysis task: {task.title}")
        
        analysis_prompt = self._build_analysis_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=analysis_prompt,
                max_tokens=2000,
                temperature=0.2  # Lower temperature for more consistent analysis
            )
            
            # Parse the analysis response
            analysis_results = self._parse_analysis_response(response)
            
            results = {
                "analysis_summary": analysis_results.get("summary", ""),
                "technical_feasibility": analysis_results.get("feasibility", "unknown"),
                "identified_risks": analysis_results.get("risks", []),
                "recommendations": analysis_results.get("recommendations", []),
                "estimated_complexity": analysis_results.get("complexity", "medium"),
                "required_resources": analysis_results.get("resources", []),
                "dependencies": analysis_results.get("dependencies", []),
                "confidence_score": analysis_results.get("confidence", 0.5)
            }
            
            self.log_execution(f"Completed analysis for {task.title} with confidence {results['confidence_score']}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error analyzing task {task.id}: {str(e)}")
            return {
                "error": str(e),
                "analysis_summary": "Analysis failed",
                "technical_feasibility": "unknown",
                "confidence_score": 0.0
            }
    
    def _build_analysis_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a comprehensive analysis prompt."""
        return f"""
You are a senior technical analyst and software architect. Analyze the following task from multiple technical perspectives.

TASK: {task.title}
DESCRIPTION: {task.description}

CONTEXT: {context.get('project_context', 'No additional context')}
TECHNICAL_STACK: {context.get('tech_stack', 'Not specified')}

Please provide a comprehensive technical analysis covering:

1. REQUIREMENT ANALYSIS:
   - What are the explicit requirements?
   - What are the implicit requirements?
   - Are there any ambiguous or missing requirements?

2. TECHNICAL FEASIBILITY:
   - Is this technically achievable with current resources?
   - What are the technical challenges?
   - Are there any technology constraints?

3. RISK ASSESSMENT:
   - What are the technical risks?
   - What are the business risks?
   - What are the implementation risks?

4. DEPENDENCY ANALYSIS:
   - What external dependencies exist?
   - What internal dependencies are required?
   - What are the critical path dependencies?

5. RESOURCE REQUIREMENTS:
   - What skills are needed?
   - What tools or frameworks are required?
   - What infrastructure is needed?

6. PERFORMANCE CONSIDERATIONS:
   - What are the performance requirements?
   - What are the scalability considerations?
   - What are the optimization opportunities?

7. SECURITY IMPLICATIONS:
   - What security considerations apply?
   - What data protection requirements exist?
   - What access control needs are there?

Please format your response as JSON:
{{
    "summary": "Brief summary of the analysis",
    "feasibility": "high|medium|low",
    "risks": [
        {{"type": "technical|business|implementation", "description": "Risk description", "severity": "high|medium|low"}}
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ],
    "complexity": "low|medium|high",
    "resources": {{
        "skills": ["Skill 1", "Skill 2"],
        "tools": ["Tool 1", "Tool 2"],
        "infrastructure": ["Infrastructure 1"]
    }},
    "dependencies": [
        {{"type": "external|internal", "description": "Dependency description", "critical": true|false}}
    ],
    "confidence": 0.85
}}
"""
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse the analysis response from OpenAI."""
        import json
        
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, KeyError) as e:
            self.log_execution(f"Error parsing analysis response: {str(e)}")
        
        # Fallback parsing
        return {
            "summary": response[:300] + "..." if len(response) > 300 else response,
            "feasibility": "medium",
            "risks": [{"type": "technical", "description": "Analysis parsing failed", "severity": "medium"}],
            "recommendations": ["Review requirements carefully"],
            "complexity": "medium",
            "resources": {"skills": ["General Development"], "tools": [], "infrastructure": []},
            "dependencies": [],
            "confidence": 0.3
        }
    
    async def assess_technical_debt(self, codebase_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess technical debt in the codebase."""
        self.log_execution("Assessing technical debt")
        
        prompt = f"""
Analyze the following codebase for technical debt:

CODEBASE_CONTEXT: {codebase_context}

Identify:
1. Code quality issues
2. Performance bottlenecks
3. Security vulnerabilities
4. Maintainability concerns
5. Architecture problems

Provide recommendations for improvement.
"""
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.3
            )
            
            return {
                "technical_debt_assessment": response,
                "severity": "medium",  # Would be determined by analysis
                "recommendations": response.split('\n')[:5]  # First 5 lines as recommendations
            }
        except Exception as e:
            return {
                "technical_debt_assessment": f"Assessment failed: {str(e)}",
                "severity": "unknown",
                "recommendations": []
            }
    
    async def validate_architecture_decision(self, decision: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an architecture decision."""
        self.log_execution(f"Validating architecture decision: {decision}")
        
        prompt = f"""
Validate this architecture decision:

DECISION: {decision}
CONTEXT: {context}

Consider:
1. Technical soundness
2. Scalability implications
3. Maintainability
4. Performance impact
5. Security implications
6. Team capabilities

Provide validation score and recommendations.
"""
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.2
            )
            
            return {
                "validation_result": response,
                "is_valid": "valid" in response.lower(),
                "confidence": 0.7
            }
        except Exception as e:
            return {
                "validation_result": f"Validation failed: {str(e)}",
                "is_valid": False,
                "confidence": 0.0
            }

