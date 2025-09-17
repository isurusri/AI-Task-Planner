"""Reviewer agent for code review and quality assessment."""

from typing import List, Dict, Any
import asyncio
from datetime import datetime

from .base_agent import BaseAgent
from models import Task, AgentType, TaskStatus
from services.llm_factory_service import LLMFactoryService


class ReviewerAgent(BaseAgent):
    """Agent responsible for code review, quality assessment, and validation."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.REVIEWER,
            name="Code Reviewer",
            description="Reviews code, assesses quality, and provides feedback for improvements"
        )
        self.llm_service = LLMFactoryService()
    
    def get_capabilities(self) -> List[str]:
        """Return reviewer agent capabilities."""
        return [
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
    
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a review task."""
        self.log_execution(f"Processing review task: {task.title}")
        
        # Determine the type of review task
        task_type = self._classify_review_task(task)
        
        if task_type == "code_review":
            return await self._handle_code_review(task, context)
        elif task_type == "quality_assessment":
            return await self._handle_quality_assessment(task, context)
        elif task_type == "security_review":
            return await self._handle_security_review(task, context)
        elif task_type == "architecture_review":
            return await self._handle_architecture_review(task, context)
        else:
            return await self._handle_general_review(task, context)
    
    def _classify_review_task(self, task: Task) -> str:
        """Classify the type of review task."""
        description_lower = task.description.lower()
        
        if any(keyword in description_lower for keyword in ["code review", "review code", "code quality"]):
            return "code_review"
        elif any(keyword in description_lower for keyword in ["quality", "assessment", "evaluate"]):
            return "quality_assessment"
        elif any(keyword in description_lower for keyword in ["security", "vulnerability", "secure"]):
            return "security_review"
        elif any(keyword in description_lower for keyword in ["architecture", "design", "structure"]):
            return "architecture_review"
        else:
            return "general_review"
    
    async def _handle_code_review(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle code review tasks."""
        review_prompt = self._build_code_review_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=review_prompt,
                max_tokens=3000,
                temperature=0.1  # Low temperature for consistent reviews
            )
            
            review_results = self._parse_code_review_response(response)
            
            results = {
                "review_summary": review_results.get("summary", ""),
                "code_quality_score": review_results.get("quality_score", 0),
                "issues_found": review_results.get("issues", []),
                "suggestions": review_results.get("suggestions", []),
                "security_concerns": review_results.get("security_concerns", []),
                "performance_issues": review_results.get("performance_issues", []),
                "best_practices_violations": review_results.get("best_practices", []),
                "overall_assessment": review_results.get("assessment", ""),
                "approval_status": review_results.get("approval", "needs_work")
            }
            
            self.log_execution(f"Completed code review for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error reviewing code {task.id}: {str(e)}")
            return {
                "error": str(e),
                "review_summary": "Code review failed",
                "code_quality_score": 0
            }
    
    async def _handle_quality_assessment(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle quality assessment tasks."""
        quality_prompt = self._build_quality_assessment_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=quality_prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            results = {
                "quality_metrics": self._extract_quality_metrics(response),
                "maintainability_score": self._extract_maintainability_score(response),
                "readability_score": self._extract_readability_score(response),
                "testability_score": self._extract_testability_score(response),
                "performance_score": self._extract_performance_score(response),
                "improvement_recommendations": self._extract_improvement_recommendations(response),
                "technical_debt_assessment": self._extract_technical_debt(response)
            }
            
            self.log_execution(f"Completed quality assessment for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error assessing quality {task.id}: {str(e)}")
            return {
                "error": str(e),
                "quality_metrics": {},
                "maintainability_score": 0
            }
    
    async def _handle_security_review(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle security review tasks."""
        security_prompt = self._build_security_review_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=security_prompt,
                max_tokens=2000,
                temperature=0.1
            )
            
            results = {
                "security_vulnerabilities": self._extract_security_vulnerabilities(response),
                "security_score": self._extract_security_score(response),
                "owasp_issues": self._extract_owasp_issues(response),
                "authentication_issues": self._extract_authentication_issues(response),
                "authorization_issues": self._extract_authorization_issues(response),
                "data_protection_issues": self._extract_data_protection_issues(response),
                "security_recommendations": self._extract_security_recommendations(response)
            }
            
            self.log_execution(f"Completed security review for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error reviewing security {task.id}: {str(e)}")
            return {
                "error": str(e),
                "security_vulnerabilities": [],
                "security_score": 0
            }
    
    async def _handle_architecture_review(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle architecture review tasks."""
        arch_prompt = self._build_architecture_review_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=arch_prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            results = {
                "architecture_assessment": self._extract_architecture_assessment(response),
                "scalability_analysis": self._extract_scalability_analysis(response),
                "maintainability_analysis": self._extract_maintainability_analysis(response),
                "design_patterns_usage": self._extract_design_patterns(response),
                "coupling_analysis": self._extract_coupling_analysis(response),
                "cohesion_analysis": self._extract_cohesion_analysis(response),
                "architecture_recommendations": self._extract_architecture_recommendations(response)
            }
            
            self.log_execution(f"Completed architecture review for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error reviewing architecture {task.id}: {str(e)}")
            return {
                "error": str(e),
                "architecture_assessment": "Architecture review failed"
            }
    
    async def _handle_general_review(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general review tasks."""
        general_prompt = self._build_general_review_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=general_prompt,
                max_tokens=1500,
                temperature=0.3
            )
            
            results = {
                "review_feedback": response[:500] + "..." if len(response) > 500 else response,
                "strengths": self._extract_strengths(response),
                "weaknesses": self._extract_weaknesses(response),
                "overall_rating": self._extract_overall_rating(response)
            }
            
            self.log_execution(f"Completed general review for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error processing review {task.id}: {str(e)}")
            return {
                "error": str(e),
                "review_feedback": "Review failed"
            }
    
    def _build_code_review_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a code review prompt."""
        return f"""
You are a senior software engineer conducting a thorough code review. Review the following code:

TASK: {task.title}
DESCRIPTION: {task.description}

CODE_TO_REVIEW: {context.get('code', 'No code provided')}
TECHNICAL_CONTEXT: {context.get('tech_stack', 'Not specified')}
REVIEW_CRITERIA: {context.get('review_criteria', 'Standard code review criteria')}

Please provide a comprehensive review covering:

1. CODE QUALITY:
   - Readability and clarity
   - Code organization and structure
   - Naming conventions
   - Comments and documentation

2. FUNCTIONALITY:
   - Correctness of logic
   - Edge case handling
   - Error handling
   - Input validation

3. PERFORMANCE:
   - Algorithm efficiency
   - Memory usage
   - Potential bottlenecks
   - Optimization opportunities

4. SECURITY:
   - Security vulnerabilities
   - Input sanitization
   - Authentication/authorization
   - Data protection

5. MAINTAINABILITY:
   - Code reusability
   - Testability
   - Coupling and cohesion
   - Technical debt

6. BEST PRACTICES:
   - Design patterns usage
   - SOLID principles
   - Framework conventions
   - Industry standards

Format your response as JSON:
{{
    "summary": "Overall review summary",
    "quality_score": 8.5,
    "issues": [
        {{"type": "bug|performance|security|style", "severity": "high|medium|low", "description": "Issue description", "line": 42, "suggestion": "Fix suggestion"}}
    ],
    "suggestions": [
        "Improvement suggestion 1",
        "Improvement suggestion 2"
    ],
    "security_concerns": ["Security issue 1", "Security issue 2"],
    "performance_issues": ["Performance issue 1", "Performance issue 2"],
    "best_practices": ["Best practice violation 1", "Best practice violation 2"],
    "assessment": "Detailed assessment",
    "approval": "approved|needs_work|rejected"
}}
"""
    
    def _build_quality_assessment_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a quality assessment prompt."""
        return f"""
You are a senior software quality engineer. Assess the quality of:

TASK: {task.title}
DESCRIPTION: {task.description}

CODE_CONTEXT: {context.get('code', 'No code provided')}
QUALITY_STANDARDS: {context.get('quality_standards', 'Industry best practices')}

Please assess quality across these dimensions:

1. MAINTAINABILITY (0-10):
   - Code organization
   - Documentation quality
   - Modularity
   - Complexity

2. READABILITY (0-10):
   - Code clarity
   - Naming conventions
   - Comments quality
   - Structure

3. TESTABILITY (0-10):
   - Unit test coverage
   - Test design
   - Mocking capabilities
   - Test isolation

4. PERFORMANCE (0-10):
   - Algorithm efficiency
   - Memory usage
   - Response time
   - Scalability

5. RELIABILITY (0-10):
   - Error handling
   - Edge case coverage
   - Defect rate
   - Stability

Provide scores and detailed analysis for each dimension.
"""
    
    def _build_security_review_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a security review prompt."""
        return f"""
You are a senior security engineer. Conduct a security review of:

TASK: {task.title}
DESCRIPTION: {task.description}

CODE_CONTEXT: {context.get('code', 'No code provided')}
SECURITY_CONTEXT: {context.get('security_context', 'General web application')}

Review for these security aspects:

1. OWASP TOP 10 VULNERABILITIES:
   - Injection attacks
   - Broken authentication
   - Sensitive data exposure
   - XML external entities
   - Broken access control
   - Security misconfiguration
   - Cross-site scripting
   - Insecure deserialization
   - Known vulnerabilities
   - Insufficient logging

2. AUTHENTICATION & AUTHORIZATION:
   - User authentication
   - Session management
   - Access control
   - Privilege escalation

3. DATA PROTECTION:
   - Data encryption
   - Data validation
   - Data sanitization
   - PII handling

4. INFRASTRUCTURE SECURITY:
   - HTTPS usage
   - Security headers
   - Error handling
   - Logging

Provide detailed security assessment and recommendations.
"""
    
    def _build_architecture_review_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build an architecture review prompt."""
        return f"""
You are a senior software architect. Review the architecture of:

TASK: {task.title}
DESCRIPTION: {task.description}

ARCHITECTURE_CONTEXT: {context.get('architecture', 'Not specified')}
TECHNICAL_STACK: {context.get('tech_stack', 'Not specified')}

Assess the architecture across these dimensions:

1. SCALABILITY:
   - Horizontal scaling capability
   - Performance under load
   - Resource utilization
   - Bottleneck identification

2. MAINTAINABILITY:
   - Code organization
   - Module separation
   - Dependency management
   - Change impact

3. RELIABILITY:
   - Fault tolerance
   - Error handling
   - Recovery mechanisms
   - Monitoring

4. SECURITY:
   - Security architecture
   - Data protection
   - Access control
   - Threat modeling

5. DESIGN PATTERNS:
   - Appropriate pattern usage
   - SOLID principles
   - DRY principle
   - Separation of concerns

Provide architectural assessment and improvement recommendations.
"""
    
    def _build_general_review_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a general review prompt."""
        return f"""
You are a senior software engineer. Provide a general review of:

TASK: {task.title}
DESCRIPTION: {task.description}

CONTEXT: {context.get('project_context', 'No additional context')}

Please provide:
1. Overall assessment
2. Key strengths
3. Areas for improvement
4. Recommendations
5. Overall rating (1-10)

Focus on practical, actionable feedback.
"""
    
    def _parse_code_review_response(self, response: str) -> Dict[str, Any]:
        """Parse code review response from OpenAI."""
        import json
        
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, KeyError) as e:
            self.log_execution(f"Error parsing code review response: {str(e)}")
        
        # Fallback parsing
        return {
            "summary": response[:300] + "..." if len(response) > 300 else response,
            "quality_score": 5.0,
            "issues": [{"type": "general", "severity": "medium", "description": "Review parsing failed", "suggestion": "Manual review needed"}],
            "suggestions": ["Review the code manually"],
            "security_concerns": [],
            "performance_issues": [],
            "best_practices": [],
            "assessment": "Review parsing failed",
            "approval": "needs_work"
        }
    
    def _extract_quality_metrics(self, response: str) -> Dict[str, Any]:
        """Extract quality metrics from response."""
        metrics = {
            "maintainability": 0,
            "readability": 0,
            "testability": 0,
            "performance": 0,
            "reliability": 0
        }
        
        lines = response.split('\n')
        for line in lines:
            for metric in metrics.keys():
                if metric in line.lower():
                    # Extract number from line
                    import re
                    numbers = re.findall(r'\d+\.?\d*', line)
                    if numbers:
                        metrics[metric] = float(numbers[0])
        
        return metrics
    
    def _extract_maintainability_score(self, response: str) -> float:
        """Extract maintainability score from response."""
        return self._extract_quality_metrics(response).get("maintainability", 0)
    
    def _extract_readability_score(self, response: str) -> float:
        """Extract readability score from response."""
        return self._extract_quality_metrics(response).get("readability", 0)
    
    def _extract_testability_score(self, response: str) -> float:
        """Extract testability score from response."""
        return self._extract_quality_metrics(response).get("testability", 0)
    
    def _extract_performance_score(self, response: str) -> float:
        """Extract performance score from response."""
        return self._extract_quality_metrics(response).get("performance", 0)
    
    def _extract_improvement_recommendations(self, response: str) -> List[str]:
        """Extract improvement recommendations from response."""
        lines = response.split('\n')
        recommendations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'improve', 'enhance']):
                recommendations.append(line.strip())
        
        return recommendations[:5]  # First 5 recommendations
    
    def _extract_technical_debt(self, response: str) -> str:
        """Extract technical debt assessment from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['technical debt', 'debt', 'refactor']):
                return line.strip()
        return "Technical debt assessment not provided"
    
    def _extract_security_vulnerabilities(self, response: str) -> List[str]:
        """Extract security vulnerabilities from response."""
        lines = response.split('\n')
        vulnerabilities = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['vulnerability', 'security', 'exploit', 'attack']):
                vulnerabilities.append(line.strip())
        
        return vulnerabilities[:5]  # First 5 vulnerabilities
    
    def _extract_security_score(self, response: str) -> float:
        """Extract security score from response."""
        lines = response.split('\n')
        for line in lines:
            if 'security' in line.lower() and any(char.isdigit() for char in line):
                import re
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    return float(numbers[0])
        return 5.0  # Default score
    
    def _extract_owasp_issues(self, response: str) -> List[str]:
        """Extract OWASP issues from response."""
        lines = response.split('\n')
        owasp_issues = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['owasp', 'injection', 'xss', 'csrf', 'authentication']):
                owasp_issues.append(line.strip())
        
        return owasp_issues[:5]  # First 5 OWASP issues
    
    def _extract_authentication_issues(self, response: str) -> List[str]:
        """Extract authentication issues from response."""
        lines = response.split('\n')
        auth_issues = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['authentication', 'login', 'password', 'session']):
                auth_issues.append(line.strip())
        
        return auth_issues[:3]  # First 3 authentication issues
    
    def _extract_authorization_issues(self, response: str) -> List[str]:
        """Extract authorization issues from response."""
        lines = response.split('\n')
        authz_issues = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['authorization', 'permission', 'access', 'role']):
                authz_issues.append(line.strip())
        
        return authz_issues[:3]  # First 3 authorization issues
    
    def _extract_data_protection_issues(self, response: str) -> List[str]:
        """Extract data protection issues from response."""
        lines = response.split('\n')
        data_issues = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['data protection', 'encryption', 'pii', 'privacy']):
                data_issues.append(line.strip())
        
        return data_issues[:3]  # First 3 data protection issues
    
    def _extract_security_recommendations(self, response: str) -> List[str]:
        """Extract security recommendations from response."""
        lines = response.split('\n')
        recommendations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'fix', 'secure']):
                recommendations.append(line.strip())
        
        return recommendations[:5]  # First 5 security recommendations
    
    def _extract_architecture_assessment(self, response: str) -> str:
        """Extract architecture assessment from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['architecture', 'assessment', 'evaluation']):
                return line.strip()
        return "Architecture assessment not provided"
    
    def _extract_scalability_analysis(self, response: str) -> str:
        """Extract scalability analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['scalability', 'scale', 'performance']):
                return line.strip()
        return "Scalability analysis not provided"
    
    def _extract_maintainability_analysis(self, response: str) -> str:
        """Extract maintainability analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['maintainability', 'maintain', 'maintenance']):
                return line.strip()
        return "Maintainability analysis not provided"
    
    def _extract_design_patterns(self, response: str) -> List[str]:
        """Extract design patterns from response."""
        lines = response.split('\n')
        patterns = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['pattern', 'singleton', 'factory', 'observer', 'mvc']):
                patterns.append(line.strip())
        
        return patterns[:5]  # First 5 design patterns
    
    def _extract_coupling_analysis(self, response: str) -> str:
        """Extract coupling analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['coupling', 'couple', 'dependency']):
                return line.strip()
        return "Coupling analysis not provided"
    
    def _extract_cohesion_analysis(self, response: str) -> str:
        """Extract cohesion analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['cohesion', 'cohesive', 'coherence']):
                return line.strip()
        return "Cohesion analysis not provided"
    
    def _extract_architecture_recommendations(self, response: str) -> List[str]:
        """Extract architecture recommendations from response."""
        lines = response.split('\n')
        recommendations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'improve', 'refactor']):
                recommendations.append(line.strip())
        
        return recommendations[:5]  # First 5 architecture recommendations
    
    def _extract_strengths(self, response: str) -> List[str]:
        """Extract strengths from response."""
        lines = response.split('\n')
        strengths = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['strength', 'good', 'excellent', 'well', 'strong']):
                strengths.append(line.strip())
        
        return strengths[:3]  # First 3 strengths
    
    def _extract_weaknesses(self, response: str) -> List[str]:
        """Extract weaknesses from response."""
        lines = response.split('\n')
        weaknesses = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['weakness', 'weak', 'poor', 'bad', 'issue', 'problem']):
                weaknesses.append(line.strip())
        
        return weaknesses[:3]  # First 3 weaknesses
    
    def _extract_overall_rating(self, response: str) -> float:
        """Extract overall rating from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['rating', 'score', 'grade']) and any(char.isdigit() for char in line):
                import re
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    return float(numbers[0])
        return 5.0  # Default rating

