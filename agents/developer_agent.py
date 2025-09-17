"""Developer agent for implementation tasks."""

from typing import List, Dict, Any
import asyncio
from datetime import datetime

from .base_agent import BaseAgent
from models import Task, AgentType, TaskStatus
from services.llm_factory_service import LLMFactoryService


class DeveloperAgent(BaseAgent):
    """Agent responsible for implementing features and writing code."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.DEVELOPER,
            name="Code Developer",
            description="Implements features, writes code, and handles technical implementation tasks"
        )
        self.llm_service = LLMFactoryService()
    
    def get_capabilities(self) -> List[str]:
        """Return developer agent capabilities."""
        return [
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
    
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a development task."""
        self.log_execution(f"Processing development task: {task.title}")
        
        # Determine the type of development task
        task_type = self._classify_task_type(task)
        
        if task_type == "code_implementation":
            return await self._handle_code_implementation(task, context)
        elif task_type == "feature_development":
            return await self._handle_feature_development(task, context)
        elif task_type == "bug_fixing":
            return await self._handle_bug_fixing(task, context)
        elif task_type == "refactoring":
            return await self._handle_refactoring(task, context)
        else:
            return await self._handle_general_development(task, context)
    
    def _classify_task_type(self, task: Task) -> str:
        """Classify the type of development task."""
        description_lower = task.description.lower()
        
        if any(keyword in description_lower for keyword in ["implement", "write", "create", "build", "develop"]):
            return "code_implementation"
        elif any(keyword in description_lower for keyword in ["feature", "functionality", "capability"]):
            return "feature_development"
        elif any(keyword in description_lower for keyword in ["fix", "bug", "error", "issue", "problem"]):
            return "bug_fixing"
        elif any(keyword in description_lower for keyword in ["refactor", "improve", "optimize", "clean"]):
            return "refactoring"
        else:
            return "general_development"
    
    async def _handle_code_implementation(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle code implementation tasks."""
        implementation_prompt = self._build_implementation_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=implementation_prompt,
                max_tokens=3000,
                temperature=0.1  # Very low temperature for code generation
            )
            
            # Extract code from response
            code_blocks = self._extract_code_blocks(response)
            
            results = {
                "implementation_approach": self._extract_approach(response),
                "code_blocks": code_blocks,
                "dependencies": self._extract_dependencies(response),
                "testing_notes": self._extract_testing_notes(response),
                "documentation": self._extract_documentation(response),
                "complexity_assessment": self._assess_implementation_complexity(response)
            }
            
            self.log_execution(f"Generated {len(code_blocks)} code blocks for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error implementing task {task.id}: {str(e)}")
            return {
                "error": str(e),
                "implementation_approach": "Implementation failed",
                "code_blocks": [],
                "complexity_assessment": "unknown"
            }
    
    async def _handle_feature_development(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle feature development tasks."""
        feature_prompt = self._build_feature_development_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=feature_prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            results = {
                "feature_architecture": self._extract_architecture(response),
                "implementation_plan": self._extract_implementation_plan(response),
                "api_design": self._extract_api_design(response),
                "database_changes": self._extract_database_changes(response),
                "frontend_components": self._extract_frontend_components(response),
                "testing_strategy": self._extract_testing_strategy(response)
            }
            
            self.log_execution(f"Designed feature architecture for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error developing feature {task.id}: {str(e)}")
            return {
                "error": str(e),
                "feature_architecture": "Feature development failed"
            }
    
    async def _handle_bug_fixing(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle bug fixing tasks."""
        bug_prompt = self._build_bug_fixing_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=bug_prompt,
                max_tokens=2000,
                temperature=0.1
            )
            
            results = {
                "root_cause_analysis": self._extract_root_cause(response),
                "fix_approach": self._extract_fix_approach(response),
                "code_changes": self._extract_code_blocks(response),
                "testing_verification": self._extract_testing_verification(response),
                "prevention_measures": self._extract_prevention_measures(response)
            }
            
            self.log_execution(f"Analyzed and provided fix for bug in {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error fixing bug {task.id}: {str(e)}")
            return {
                "error": str(e),
                "root_cause_analysis": "Bug analysis failed"
            }
    
    async def _handle_refactoring(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle refactoring tasks."""
        refactor_prompt = self._build_refactoring_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=refactor_prompt,
                max_tokens=2000,
                temperature=0.2
            )
            
            results = {
                "refactoring_strategy": self._extract_refactoring_strategy(response),
                "code_improvements": self._extract_code_blocks(response),
                "performance_improvements": self._extract_performance_improvements(response),
                "maintainability_improvements": self._extract_maintainability_improvements(response),
                "migration_plan": self._extract_migration_plan(response)
            }
            
            self.log_execution(f"Provided refactoring strategy for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error refactoring {task.id}: {str(e)}")
            return {
                "error": str(e),
                "refactoring_strategy": "Refactoring failed"
            }
    
    async def _handle_general_development(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general development tasks."""
        general_prompt = self._build_general_development_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=general_prompt,
                max_tokens=2000,
                temperature=0.3
            )
            
            results = {
                "development_approach": response[:500] + "..." if len(response) > 500 else response,
                "implementation_notes": response,
                "next_steps": self._extract_next_steps(response)
            }
            
            self.log_execution(f"Provided development approach for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error processing general task {task.id}: {str(e)}")
            return {
                "error": str(e),
                "development_approach": "Development approach failed"
            }
    
    def _build_implementation_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a code implementation prompt."""
        return f"""
You are a senior software developer. Implement the following task:

TASK: {task.title}
DESCRIPTION: {task.description}

TECHNICAL_CONTEXT: {context.get('tech_stack', 'Python, FastAPI')}
EXISTING_CODE: {context.get('existing_code', 'No existing code provided')}

Please provide:
1. Clean, production-ready code
2. Proper error handling
3. Documentation and comments
4. Unit tests
5. Dependencies and requirements

Format your response with clear code blocks and explanations.
"""
    
    def _build_feature_development_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a feature development prompt."""
        return f"""
You are a senior software architect. Design and implement this feature:

FEATURE: {task.title}
DESCRIPTION: {task.description}

ARCHITECTURE_CONTEXT: {context.get('architecture', 'Not specified')}
TECHNICAL_STACK: {context.get('tech_stack', 'Python, FastAPI, React')}

Please provide:
1. Feature architecture design
2. API design and endpoints
3. Database schema changes
4. Frontend component structure
5. Implementation plan
6. Testing strategy

Focus on scalability, maintainability, and user experience.
"""
    
    def _build_bug_fixing_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a bug fixing prompt."""
        return f"""
You are a senior software engineer. Fix this bug:

BUG: {task.title}
DESCRIPTION: {task.description}

ERROR_CONTEXT: {context.get('error_context', 'No error context provided')}
CODE_CONTEXT: {context.get('code_context', 'No code context provided')}

Please provide:
1. Root cause analysis
2. Step-by-step fix approach
3. Corrected code
4. Testing verification steps
5. Prevention measures

Focus on understanding the root cause and providing a robust solution.
"""
    
    def _build_refactoring_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a refactoring prompt."""
        return f"""
You are a senior software engineer. Refactor this code:

REFACTORING_TASK: {task.title}
DESCRIPTION: {task.description}

CURRENT_CODE: {context.get('current_code', 'No code provided')}
REFACTORING_GOALS: {context.get('goals', 'Improve code quality and maintainability')}

Please provide:
1. Refactoring strategy
2. Improved code structure
3. Performance optimizations
4. Maintainability improvements
5. Migration plan

Focus on code quality, performance, and maintainability.
"""
    
    def _build_general_development_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a general development prompt."""
        return f"""
You are a senior software developer. Handle this development task:

TASK: {task.title}
DESCRIPTION: {task.description}

CONTEXT: {context.get('project_context', 'No additional context')}

Please provide:
1. Development approach
2. Implementation strategy
3. Key considerations
4. Next steps
5. Potential challenges

Provide practical, actionable guidance.
"""
    
    def _extract_code_blocks(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from the response."""
        import re
        
        code_blocks = []
        # Look for code blocks marked with ``` or indented code
        patterns = [
            r'```(\w+)?\n(.*?)\n```',
            r'```\n(.*?)\n```'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    language, code = match
                    code_blocks.append({
                        "language": language or "text",
                        "code": code.strip()
                    })
                else:
                    code_blocks.append({
                        "language": "text",
                        "code": match.strip()
                    })
        
        return code_blocks
    
    def _extract_approach(self, response: str) -> str:
        """Extract implementation approach from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['approach', 'strategy', 'method']):
                return line.strip()
        return "Implementation approach not specified"
    
    def _extract_dependencies(self, response: str) -> List[str]:
        """Extract dependencies from response."""
        import re
        
        dependencies = []
        # Look for dependency patterns
        patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)',
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'pip install\s+(\w+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            dependencies.extend(matches)
        
        return list(set(dependencies))
    
    def _extract_testing_notes(self, response: str) -> str:
        """Extract testing notes from response."""
        lines = response.split('\n')
        testing_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['test', 'testing', 'verify', 'validation']):
                testing_lines.append(line.strip())
        
        return '\n'.join(testing_lines[:5])  # First 5 testing-related lines
    
    def _extract_documentation(self, response: str) -> str:
        """Extract documentation from response."""
        lines = response.split('\n')
        doc_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['documentation', 'comment', 'docstring', 'readme']):
                doc_lines.append(line.strip())
        
        return '\n'.join(doc_lines[:3])  # First 3 documentation-related lines
    
    def _assess_implementation_complexity(self, response: str) -> str:
        """Assess implementation complexity based on response."""
        word_count = len(response.split())
        code_blocks = len(self._extract_code_blocks(response))
        
        if word_count > 1000 and code_blocks > 3:
            return "high"
        elif word_count > 500 and code_blocks > 1:
            return "medium"
        else:
            return "low"
    
    def _extract_architecture(self, response: str) -> str:
        """Extract architecture information from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['architecture', 'design', 'structure']):
                return line.strip()
        return "Architecture not specified"
    
    def _extract_implementation_plan(self, response: str) -> List[str]:
        """Extract implementation plan steps."""
        lines = response.split('\n')
        plan_steps = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['step', 'phase', 'stage', '1.', '2.', '3.']):
                plan_steps.append(line.strip())
        
        return plan_steps[:10]  # First 10 plan steps
    
    def _extract_api_design(self, response: str) -> str:
        """Extract API design from response."""
        lines = response.split('\n')
        api_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['api', 'endpoint', 'route', 'http']):
                api_lines.append(line.strip())
        
        return '\n'.join(api_lines[:5])  # First 5 API-related lines
    
    def _extract_database_changes(self, response: str) -> str:
        """Extract database changes from response."""
        lines = response.split('\n')
        db_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['database', 'table', 'schema', 'migration', 'sql']):
                db_lines.append(line.strip())
        
        return '\n'.join(db_lines[:5])  # First 5 database-related lines
    
    def _extract_frontend_components(self, response: str) -> List[str]:
        """Extract frontend components from response."""
        lines = response.split('\n')
        components = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['component', 'ui', 'frontend', 'react', 'vue', 'angular']):
                components.append(line.strip())
        
        return components[:5]  # First 5 frontend-related lines
    
    def _extract_testing_strategy(self, response: str) -> str:
        """Extract testing strategy from response."""
        lines = response.split('\n')
        testing_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['test', 'testing', 'qa', 'quality']):
                testing_lines.append(line.strip())
        
        return '\n'.join(testing_lines[:5])  # First 5 testing-related lines
    
    def _extract_root_cause(self, response: str) -> str:
        """Extract root cause analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['root cause', 'cause', 'reason', 'why']):
                return line.strip()
        return "Root cause not identified"
    
    def _extract_fix_approach(self, response: str) -> str:
        """Extract fix approach from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['fix', 'solution', 'approach', 'method']):
                return line.strip()
        return "Fix approach not specified"
    
    def _extract_testing_verification(self, response: str) -> str:
        """Extract testing verification from response."""
        lines = response.split('\n')
        testing_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['verify', 'test', 'check', 'validate']):
                testing_lines.append(line.strip())
        
        return '\n'.join(testing_lines[:3])  # First 3 verification lines
    
    def _extract_prevention_measures(self, response: str) -> List[str]:
        """Extract prevention measures from response."""
        lines = response.split('\n')
        prevention_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['prevent', 'avoid', 'mitigate', 'protection']):
                prevention_lines.append(line.strip())
        
        return prevention_lines[:5]  # First 5 prevention measures
    
    def _extract_refactoring_strategy(self, response: str) -> str:
        """Extract refactoring strategy from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['strategy', 'approach', 'plan', 'method']):
                return line.strip()
        return "Refactoring strategy not specified"
    
    def _extract_performance_improvements(self, response: str) -> List[str]:
        """Extract performance improvements from response."""
        lines = response.split('\n')
        perf_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['performance', 'speed', 'optimize', 'efficient']):
                perf_lines.append(line.strip())
        
        return perf_lines[:5]  # First 5 performance-related lines
    
    def _extract_maintainability_improvements(self, response: str) -> List[str]:
        """Extract maintainability improvements from response."""
        lines = response.split('\n')
        maint_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['maintain', 'readable', 'clean', 'structure']):
                maint_lines.append(line.strip())
        
        return maint_lines[:5]  # First 5 maintainability-related lines
    
    def _extract_migration_plan(self, response: str) -> str:
        """Extract migration plan from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['migration', 'migrate', 'transition', 'upgrade']):
                return line.strip()
        return "Migration plan not specified"
    
    def _extract_next_steps(self, response: str) -> List[str]:
        """Extract next steps from response."""
        lines = response.split('\n')
        steps = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['next', 'step', 'then', 'after', 'follow']):
                steps.append(line.strip())
        
        return steps[:5]  # First 5 next steps

