"""Tester agent for quality assurance and testing tasks."""

from typing import List, Dict, Any
import asyncio
from datetime import datetime

from .base_agent import BaseAgent
from models import Task, AgentType, TaskStatus
from services.llm_factory_service import LLMFactoryService


class TesterAgent(BaseAgent):
    """Agent responsible for testing, quality assurance, and validation."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.TESTER,
            name="Quality Tester",
            description="Creates test cases, performs quality assurance, and validates implementations"
        )
        self.llm_service = LLMFactoryService()
    
    def get_capabilities(self) -> List[str]:
        """Return tester agent capabilities."""
        return [
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
    
    async def process_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a testing task."""
        self.log_execution(f"Processing testing task: {task.title}")
        
        # Determine the type of testing task
        task_type = self._classify_testing_task(task)
        
        if task_type == "test_case_creation":
            return await self._handle_test_case_creation(task, context)
        elif task_type == "test_execution":
            return await self._handle_test_execution(task, context)
        elif task_type == "bug_investigation":
            return await self._handle_bug_investigation(task, context)
        elif task_type == "performance_testing":
            return await self._handle_performance_testing(task, context)
        else:
            return await self._handle_general_testing(task, context)
    
    def _classify_testing_task(self, task: Task) -> str:
        """Classify the type of testing task."""
        description_lower = task.description.lower()
        
        if any(keyword in description_lower for keyword in ["test case", "test plan", "create test", "write test"]):
            return "test_case_creation"
        elif any(keyword in description_lower for keyword in ["execute", "run test", "perform test", "test execution"]):
            return "test_execution"
        elif any(keyword in description_lower for keyword in ["bug", "investigate", "reproduce", "debug"]):
            return "bug_investigation"
        elif any(keyword in description_lower for keyword in ["performance", "load", "stress", "benchmark"]):
            return "performance_testing"
        else:
            return "general_testing"
    
    async def _handle_test_case_creation(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test case creation tasks."""
        test_prompt = self._build_test_case_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=test_prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            test_cases = self._extract_test_cases(response)
            
            results = {
                "test_cases": test_cases,
                "test_strategy": self._extract_test_strategy(response),
                "test_data": self._extract_test_data(response),
                "coverage_analysis": self._extract_coverage_analysis(response),
                "automation_notes": self._extract_automation_notes(response),
                "edge_cases": self._extract_edge_cases(response)
            }
            
            self.log_execution(f"Created {len(test_cases)} test cases for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error creating test cases for {task.id}: {str(e)}")
            return {
                "error": str(e),
                "test_cases": [],
                "test_strategy": "Test case creation failed"
            }
    
    async def _handle_test_execution(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test execution tasks."""
        execution_prompt = self._build_test_execution_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=execution_prompt,
                max_tokens=2000,
                temperature=0.1
            )
            
            results = {
                "execution_plan": self._extract_execution_plan(response),
                "test_results": self._extract_test_results(response),
                "failed_tests": self._extract_failed_tests(response),
                "performance_metrics": self._extract_performance_metrics(response),
                "recommendations": self._extract_recommendations(response)
            }
            
            self.log_execution(f"Executed tests for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error executing tests for {task.id}: {str(e)}")
            return {
                "error": str(e),
                "execution_plan": "Test execution failed"
            }
    
    async def _handle_bug_investigation(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle bug investigation tasks."""
        bug_prompt = self._build_bug_investigation_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=bug_prompt,
                max_tokens=2000,
                temperature=0.2
            )
            
            results = {
                "bug_analysis": self._extract_bug_analysis(response),
                "reproduction_steps": self._extract_reproduction_steps(response),
                "root_cause": self._extract_root_cause(response),
                "fix_suggestions": self._extract_fix_suggestions(response),
                "prevention_measures": self._extract_prevention_measures(response)
            }
            
            self.log_execution(f"Investigated bug for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error investigating bug {task.id}: {str(e)}")
            return {
                "error": str(e),
                "bug_analysis": "Bug investigation failed"
            }
    
    async def _handle_performance_testing(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle performance testing tasks."""
        perf_prompt = self._build_performance_testing_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=perf_prompt,
                max_tokens=2000,
                temperature=0.2
            )
            
            results = {
                "performance_plan": self._extract_performance_plan(response),
                "test_scenarios": self._extract_test_scenarios(response),
                "metrics_to_measure": self._extract_metrics(response),
                "tools_recommendations": self._extract_tools_recommendations(response),
                "optimization_suggestions": self._extract_optimization_suggestions(response)
            }
            
            self.log_execution(f"Created performance testing plan for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error creating performance tests for {task.id}: {str(e)}")
            return {
                "error": str(e),
                "performance_plan": "Performance testing failed"
            }
    
    async def _handle_general_testing(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general testing tasks."""
        general_prompt = self._build_general_testing_prompt(task, context)
        
        try:
            response = await self.llm_service.generate_completion(
                prompt=general_prompt,
                max_tokens=1500,
                temperature=0.3
            )
            
            results = {
                "testing_approach": response[:500] + "..." if len(response) > 500 else response,
                "quality_metrics": self._extract_quality_metrics(response),
                "testing_notes": response
            }
            
            self.log_execution(f"Provided testing approach for {task.title}")
            return results
            
        except Exception as e:
            self.log_execution(f"Error processing testing task {task.id}: {str(e)}")
            return {
                "error": str(e),
                "testing_approach": "Testing approach failed"
            }
    
    def _build_test_case_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a test case creation prompt."""
        return f"""
You are a senior QA engineer. Create comprehensive test cases for:

FEATURE: {task.title}
DESCRIPTION: {task.description}

TECHNICAL_CONTEXT: {context.get('tech_stack', 'Not specified')}
EXISTING_FUNCTIONALITY: {context.get('existing_functionality', 'Not specified')}

Please create:
1. Unit test cases
2. Integration test cases
3. End-to-end test cases
4. Edge case scenarios
5. Negative test cases
6. Performance test cases

For each test case, include:
- Test case ID
- Test description
- Preconditions
- Test steps
- Expected results
- Test data requirements
- Priority level

Format as structured test cases with clear organization.
"""
    
    def _build_test_execution_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a test execution prompt."""
        return f"""
You are a senior QA engineer. Plan and execute tests for:

TASK: {task.title}
DESCRIPTION: {task.description}

TEST_CONTEXT: {context.get('test_context', 'Not specified')}
TEST_ENVIRONMENT: {context.get('test_environment', 'Not specified')}

Please provide:
1. Test execution strategy
2. Test environment setup
3. Test data preparation
4. Execution sequence
5. Result validation criteria
6. Reporting format

Focus on thorough testing and clear result reporting.
"""
    
    def _build_bug_investigation_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a bug investigation prompt."""
        return f"""
You are a senior QA engineer. Investigate this bug:

BUG: {task.title}
DESCRIPTION: {task.description}

ERROR_CONTEXT: {context.get('error_context', 'Not specified')}
SYSTEM_STATE: {context.get('system_state', 'Not specified')}

Please provide:
1. Bug reproduction steps
2. Root cause analysis
3. Impact assessment
4. Fix recommendations
5. Prevention measures
6. Test cases to prevent regression

Focus on understanding the bug completely and preventing future occurrences.
"""
    
    def _build_performance_testing_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a performance testing prompt."""
        return f"""
You are a senior performance testing engineer. Create a performance testing plan for:

FEATURE: {task.title}
DESCRIPTION: {task.description}

PERFORMANCE_REQUIREMENTS: {context.get('performance_requirements', 'Not specified')}
TECHNICAL_STACK: {context.get('tech_stack', 'Not specified')}

Please provide:
1. Performance testing strategy
2. Load testing scenarios
3. Stress testing scenarios
4. Key performance indicators (KPIs)
5. Tools and frameworks to use
6. Test data requirements
7. Performance benchmarks
8. Optimization recommendations

Focus on realistic performance scenarios and measurable metrics.
"""
    
    def _build_general_testing_prompt(self, task: Task, context: Dict[str, Any]) -> str:
        """Build a general testing prompt."""
        return f"""
You are a senior QA engineer. Provide testing guidance for:

TASK: {task.title}
DESCRIPTION: {task.description}

CONTEXT: {context.get('project_context', 'No additional context')}

Please provide:
1. Testing approach
2. Quality assurance strategy
3. Key testing areas
4. Risk assessment
5. Testing recommendations

Provide practical, actionable testing guidance.
"""
    
    def _extract_test_cases(self, response: str) -> List[Dict[str, Any]]:
        """Extract test cases from response."""
        import re
        
        test_cases = []
        # Look for test case patterns
        test_patterns = [
            r'Test Case\s*(\d+)[:\-]\s*(.*?)(?=Test Case|\Z)',
            r'TC\d+[:\-]\s*(.*?)(?=TC\d+|\Z)',
            r'Test\s*(\d+)[:\-]\s*(.*?)(?=Test\s*\d+|\Z)'
        ]
        
        for pattern in test_patterns:
            matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    test_id, content = match
                    test_cases.append({
                        "id": f"TC{test_id}",
                        "content": content.strip(),
                        "type": "functional"
                    })
                else:
                    test_cases.append({
                        "id": f"TC{len(test_cases) + 1}",
                        "content": match.strip(),
                        "type": "functional"
                    })
        
        # If no structured test cases found, create from general content
        if not test_cases:
            lines = response.split('\n')
            current_test = ""
            for line in lines:
                if any(keyword in line.lower() for keyword in ['test', 'verify', 'check', 'validate']):
                    if current_test:
                        test_cases.append({
                            "id": f"TC{len(test_cases) + 1}",
                            "content": current_test.strip(),
                            "type": "functional"
                        })
                    current_test = line
                elif current_test and line.strip():
                    current_test += f"\n{line}"
            
            if current_test:
                test_cases.append({
                    "id": f"TC{len(test_cases) + 1}",
                    "content": current_test.strip(),
                    "type": "functional"
                })
        
        return test_cases[:10]  # Limit to first 10 test cases
    
    def _extract_test_strategy(self, response: str) -> str:
        """Extract test strategy from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['strategy', 'approach', 'methodology']):
                return line.strip()
        return "Test strategy not specified"
    
    def _extract_test_data(self, response: str) -> List[str]:
        """Extract test data requirements from response."""
        lines = response.split('\n')
        data_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['data', 'input', 'test data', 'sample']):
                data_lines.append(line.strip())
        
        return data_lines[:5]  # First 5 data-related lines
    
    def _extract_coverage_analysis(self, response: str) -> str:
        """Extract coverage analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['coverage', 'coverage analysis', 'test coverage']):
                return line.strip()
        return "Coverage analysis not provided"
    
    def _extract_automation_notes(self, response: str) -> str:
        """Extract automation notes from response."""
        lines = response.split('\n')
        automation_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['automation', 'automated', 'script', 'tool']):
                automation_lines.append(line.strip())
        
        return '\n'.join(automation_lines[:3])  # First 3 automation-related lines
    
    def _extract_edge_cases(self, response: str) -> List[str]:
        """Extract edge cases from response."""
        lines = response.split('\n')
        edge_cases = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['edge case', 'boundary', 'limit', 'extreme']):
                edge_cases.append(line.strip())
        
        return edge_cases[:5]  # First 5 edge cases
    
    def _extract_execution_plan(self, response: str) -> str:
        """Extract execution plan from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['execution', 'plan', 'sequence', 'order']):
                return line.strip()
        return "Execution plan not specified"
    
    def _extract_test_results(self, response: str) -> Dict[str, Any]:
        """Extract test results from response."""
        lines = response.split('\n')
        results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0
        }
        
        for line in lines:
            if 'passed' in line.lower():
                try:
                    results["passed"] = int(re.findall(r'\d+', line)[0])
                except:
                    pass
            elif 'failed' in line.lower():
                try:
                    results["failed"] = int(re.findall(r'\d+', line)[0])
                except:
                    pass
            elif 'skipped' in line.lower():
                try:
                    results["skipped"] = int(re.findall(r'\d+', line)[0])
                except:
                    pass
        
        results["total"] = results["passed"] + results["failed"] + results["skipped"]
        return results
    
    def _extract_failed_tests(self, response: str) -> List[str]:
        """Extract failed tests from response."""
        lines = response.split('\n')
        failed_tests = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['failed', 'error', 'failing', 'broken']):
                failed_tests.append(line.strip())
        
        return failed_tests[:5]  # First 5 failed tests
    
    def _extract_performance_metrics(self, response: str) -> Dict[str, Any]:
        """Extract performance metrics from response."""
        import re
        
        metrics = {}
        lines = response.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['response time', 'throughput', 'memory', 'cpu', 'latency']):
                # Extract numbers from the line
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    metric_name = line.split(':')[0].strip() if ':' in line else line.strip()
                    metrics[metric_name] = numbers[0]
        
        return metrics
    
    def _extract_recommendations(self, response: str) -> List[str]:
        """Extract recommendations from response."""
        lines = response.split('\n')
        recommendations = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'advise']):
                recommendations.append(line.strip())
        
        return recommendations[:5]  # First 5 recommendations
    
    def _extract_bug_analysis(self, response: str) -> str:
        """Extract bug analysis from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['analysis', 'investigation', 'root cause']):
                return line.strip()
        return "Bug analysis not provided"
    
    def _extract_reproduction_steps(self, response: str) -> List[str]:
        """Extract reproduction steps from response."""
        lines = response.split('\n')
        steps = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['step', 'reproduce', 'reproduction']):
                steps.append(line.strip())
        
        return steps[:10]  # First 10 reproduction steps
    
    def _extract_root_cause(self, response: str) -> str:
        """Extract root cause from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['root cause', 'cause', 'reason', 'why']):
                return line.strip()
        return "Root cause not identified"
    
    def _extract_fix_suggestions(self, response: str) -> List[str]:
        """Extract fix suggestions from response."""
        lines = response.split('\n')
        suggestions = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['fix', 'solution', 'suggest', 'recommend']):
                suggestions.append(line.strip())
        
        return suggestions[:5]  # First 5 fix suggestions
    
    def _extract_prevention_measures(self, response: str) -> List[str]:
        """Extract prevention measures from response."""
        lines = response.split('\n')
        measures = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['prevent', 'avoid', 'mitigate', 'protection']):
                measures.append(line.strip())
        
        return measures[:5]  # First 5 prevention measures
    
    def _extract_performance_plan(self, response: str) -> str:
        """Extract performance plan from response."""
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['plan', 'strategy', 'approach']):
                return line.strip()
        return "Performance plan not specified"
    
    def _extract_test_scenarios(self, response: str) -> List[str]:
        """Extract test scenarios from response."""
        lines = response.split('\n')
        scenarios = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['scenario', 'test case', 'load test', 'stress test']):
                scenarios.append(line.strip())
        
        return scenarios[:5]  # First 5 test scenarios
    
    def _extract_metrics(self, response: str) -> List[str]:
        """Extract metrics from response."""
        lines = response.split('\n')
        metrics = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['metric', 'kpi', 'measure', 'indicator']):
                metrics.append(line.strip())
        
        return metrics[:5]  # First 5 metrics
    
    def _extract_tools_recommendations(self, response: str) -> List[str]:
        """Extract tools recommendations from response."""
        lines = response.split('\n')
        tools = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['tool', 'framework', 'library', 'software']):
                tools.append(line.strip())
        
        return tools[:5]  # First 5 tool recommendations
    
    def _extract_optimization_suggestions(self, response: str) -> List[str]:
        """Extract optimization suggestions from response."""
        lines = response.split('\n')
        suggestions = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['optimize', 'improve', 'enhance', 'tune']):
                suggestions.append(line.strip())
        
        return suggestions[:5]  # First 5 optimization suggestions
    
    def _extract_quality_metrics(self, response: str) -> Dict[str, Any]:
        """Extract quality metrics from response."""
        metrics = {
            "test_coverage": "Not specified",
            "defect_density": "Not specified",
            "test_effectiveness": "Not specified"
        }
        
        lines = response.split('\n')
        for line in lines:
            if 'coverage' in line.lower():
                metrics["test_coverage"] = line.strip()
            elif 'defect' in line.lower():
                metrics["defect_density"] = line.strip()
            elif 'effectiveness' in line.lower():
                metrics["test_effectiveness"] = line.strip()
        
        return metrics

