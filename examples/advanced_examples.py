"""Advanced examples demonstrating the AI Task Planner capabilities."""

import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

from models import TaskDecompositionRequest, AgentExecutionRequest
from services import TaskDecompositionService, ExecutionSimulationService
from agents import (
    PlannerAgent, AnalyzerAgent, DeveloperAgent,
    TesterAgent, ReviewerAgent, CoordinatorAgent
)


class AdvancedTaskPlannerDemo:
    """Advanced demonstration of AI Task Planner capabilities."""
    
    def __init__(self):
        self.decomposition_service = TaskDecompositionService()
        self.simulation_service = ExecutionSimulationService()
        self.agents = {
            "planner": PlannerAgent(),
            "analyzer": AnalyzerAgent(),
            "developer": DeveloperAgent(),
            "tester": TesterAgent(),
            "reviewer": ReviewerAgent(),
            "coordinator": CoordinatorAgent()
        }
    
    async def demonstrate_complex_project_decomposition(self):
        """Demonstrate decomposition of a complex, multi-faceted project."""
        
        print("🏗️  Complex Project Decomposition Demo")
        print("=" * 60)
        
        complex_request = TaskDecompositionRequest(
            user_input="""
            Build a comprehensive microservices-based e-commerce platform with the following features:
            
            CORE FEATURES:
            - Multi-tenant architecture supporting multiple stores
            - Advanced user authentication with OAuth2, JWT, and MFA
            - Comprehensive product catalog with AI-powered search and recommendations
            - Sophisticated shopping cart with real-time inventory management
            - Multi-payment gateway integration (Stripe, PayPal, Apple Pay)
            - Advanced order management with real-time tracking
            - Comprehensive admin dashboard with analytics
            - Mobile-responsive PWA with offline capabilities
            
            TECHNICAL REQUIREMENTS:
            - Microservices architecture with API Gateway
            - Event-driven architecture with message queues
            - Real-time notifications using WebSockets
            - Advanced caching with Redis
            - Database per service with eventual consistency
            - Container orchestration with Kubernetes
            - CI/CD pipeline with automated testing
            - Comprehensive monitoring and logging
            - Security-first approach with OWASP compliance
            
            INTEGRATIONS:
            - Third-party payment processors
            - Shipping and logistics APIs
            - Email and SMS notification services
            - Analytics and tracking services
            - Inventory management systems
            - Customer support tools
            """,
            project_context="""
            Enterprise-grade e-commerce platform for a large retail company.
            Expected to handle 100,000+ concurrent users and 1M+ products.
            Must be scalable, maintainable, and secure.
            Team size: 15-20 developers with various specializations.
            Timeline: 6-8 months for MVP, 12 months for full feature set.
            """,
            max_depth=5,
            include_estimates=True
        )
        
        try:
            print("🔄 Decomposing complex project...")
            result = await self.decomposition_service.decompose_task(complex_request)
            
            print(f"✅ Project: {result.project.name}")
            print(f"📊 Total tasks: {len(result.project.tasks)}")
            print(f"📋 Execution steps: {len(result.execution_plan)}")
            
            # Analyze task distribution
            self._analyze_task_distribution(result.project.tasks)
            
            # Show execution timeline
            self._show_execution_timeline(result.execution_plan)
            
            # Demonstrate agent collaboration
            await self._demonstrate_agent_collaboration(result.project)
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def _analyze_task_distribution(self, tasks: List[Any]):
        """Analyze and display task distribution metrics."""
        
        print(f"\n📈 Task Distribution Analysis")
        print("-" * 40)
        
        # Category distribution
        categories = {}
        priorities = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        complexity_levels = {"low": 0, "medium": 0, "high": 0}
        total_hours = 0
        
        for task in tasks:
            # Category analysis
            category = task.metadata.get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
            
            # Priority analysis
            priorities[task.priority] += 1
            
            # Complexity analysis
            estimated_hours = task.estimated_hours or 4
            total_hours += estimated_hours
            
            if estimated_hours <= 4:
                complexity_levels["low"] += 1
            elif estimated_hours <= 12:
                complexity_levels["medium"] += 1
            else:
                complexity_levels["high"] += 1
        
        # Display category distribution
        print("📂 By Category:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(tasks)) * 100
            print(f"  {category:15} {count:3d} tasks ({percentage:5.1f}%)")
        
        # Display priority distribution
        print(f"\n🎯 By Priority:")
        for priority in [5, 4, 3, 2, 1]:
            count = priorities[priority]
            percentage = (count / len(tasks)) * 100
            print(f"  Priority {priority}: {count:3d} tasks ({percentage:5.1f}%)")
        
        # Display complexity distribution
        print(f"\n⚡ By Complexity:")
        for complexity, count in complexity_levels.items():
            percentage = (count / len(tasks)) * 100
            print(f"  {complexity:6}: {count:3d} tasks ({percentage:5.1f}%)")
        
        # Display time estimates
        print(f"\n⏱️  Time Estimates:")
        print(f"  Total estimated hours: {total_hours:,.0f}")
        print(f"  Average task size: {total_hours / len(tasks):.1f} hours")
        print(f"  Estimated project duration: {total_hours / (8 * 5 * 4):.1f} months (8h/day, 5 days/week, 4 weeks/month)")
    
    def _show_execution_timeline(self, execution_plan: List[Dict[str, Any]]):
        """Show execution timeline with dependencies."""
        
        print(f"\n📅 Execution Timeline")
        print("-" * 40)
        
        # Group by suggested agent
        agent_tasks = {}
        for step in execution_plan:
            agent = step['suggested_agent']
            if agent not in agent_tasks:
                agent_tasks[agent] = []
            agent_tasks[agent].append(step)
        
        # Display timeline by agent
        for agent, tasks in agent_tasks.items():
            total_hours = sum(task['estimated_hours'] for task in tasks)
            print(f"\n🤖 {agent.title()} Agent:")
            print(f"   Tasks: {len(tasks)}, Total hours: {total_hours}")
            
            # Show first few tasks
            for task in tasks[:3]:
                print(f"   • {task['task_title'][:50]}... ({task['estimated_hours']}h)")
            if len(tasks) > 3:
                print(f"   ... and {len(tasks) - 3} more tasks")
    
    async def _demonstrate_agent_collaboration(self, project: Any):
        """Demonstrate how different agents collaborate on tasks."""
        
        print(f"\n🤝 Agent Collaboration Demo")
        print("-" * 40)
        
        # Select a complex task for demonstration
        complex_tasks = [task for task in project.tasks if task.estimated_hours and task.estimated_hours > 8]
        if not complex_tasks:
            complex_tasks = project.tasks[:3]
        
        for task in complex_tasks[:2]:  # Demonstrate with first 2 complex tasks
            print(f"\n📋 Task: {task.title}")
            print(f"   Description: {task.description[:100]}...")
            print(f"   Estimated hours: {task.estimated_hours}")
            
            # Show how different agents would approach this task
            context = {
                "project_context": project.description,
                "tech_stack": "Microservices, Node.js, React, PostgreSQL, Redis"
            }
            
            for agent_name, agent in self.agents.items():
                try:
                    print(f"\n   🔧 {agent_name.title()} Agent approach:")
                    result = await agent.process_task(task, context)
                    
                    # Extract key insights from each agent
                    if agent_name == "planner":
                        subtasks = result.get('subtasks', [])
                        print(f"      → Would create {len(subtasks)} subtasks")
                    elif agent_name == "analyzer":
                        feasibility = result.get('technical_feasibility', 'unknown')
                        risks = result.get('identified_risks', [])
                        print(f"      → Feasibility: {feasibility}, Risks: {len(risks)}")
                    elif agent_name == "developer":
                        approach = result.get('implementation_approach', 'No approach specified')
                        print(f"      → Approach: {approach[:60]}...")
                    elif agent_name == "tester":
                        test_cases = result.get('test_cases', [])
                        print(f"      → Would create {len(test_cases)} test cases")
                    elif agent_name == "reviewer":
                        quality_score = result.get('code_quality_score', 0)
                        print(f"      → Quality score: {quality_score}/10")
                    elif agent_name == "coordinator":
                        strategy = result.get('coordination_strategy', 'No strategy')
                        print(f"      → Strategy: {strategy[:60]}...")
                
                except Exception as e:
                    print(f"      → Error: {str(e)}")
    
    async def demonstrate_chain_of_thought_reasoning(self):
        """Demonstrate chain-of-thought reasoning capabilities."""
        
        print(f"\n🧠 Chain-of-Thought Reasoning Demo")
        print("=" * 60)
        
        from services.openai_service import OpenAIService
        openai_service = OpenAIService()
        
        # Example 1: Complex architectural decision
        print("\n🏗️  Architectural Decision Making")
        print("-" * 40)
        
        architectural_problem = """
        We need to design a real-time chat system that can handle 100,000 concurrent users.
        The system should support:
        - Real-time messaging with < 100ms latency
        - Message persistence and history
        - Online/offline status
        - File sharing and media messages
        - Group chats and channels
        - Message search and filtering
        - Mobile and web clients
        
        Constraints:
        - Must be scalable to 1M+ users
        - Budget is limited
        - Team has experience with Node.js and React
        - Must be deployed on AWS
        """
        
        try:
            reasoning_result = await openai_service.generate_chain_of_thought(
                architectural_problem,
                {
                    "context": "High-scale real-time application",
                    "requirements": "Low latency, high availability, cost-effective"
                }
            )
            
            print("🤔 Reasoning Process:")
            print(reasoning_result['reasoning'][:500] + "...")
            print(f"\n💡 Solution:")
            print(reasoning_result['solution'][:500] + "...")
            print(f"\n🎯 Confidence: {reasoning_result['confidence']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Example 2: Technical trade-off analysis
        print(f"\n⚖️  Technical Trade-off Analysis")
        print("-" * 40)
        
        tradeoff_problem = """
        We need to choose between two approaches for our user authentication system:
        
        Option A: JWT-based stateless authentication
        - Pros: Scalable, no server-side session storage, works well with microservices
        - Cons: Hard to revoke tokens, larger token size, security concerns with token storage
        
        Option B: Session-based stateful authentication
        - Pros: Easy to revoke sessions, smaller payload, more secure token storage
        - Cons: Requires server-side storage, harder to scale, not ideal for microservices
        
        Our context:
        - Microservices architecture
        - Need to scale to millions of users
        - Security is critical
        - Team is familiar with both approaches
        """
        
        try:
            tradeoff_result = await openai_service.generate_chain_of_thought(
                tradeoff_problem,
                {
                    "context": "Microservices authentication decision",
                    "requirements": "Security, scalability, maintainability"
                }
            )
            
            print("🤔 Trade-off Analysis:")
            print(tradeoff_result['reasoning'][:500] + "...")
            print(f"\n💡 Recommendation:")
            print(tradeoff_result['solution'][:500] + "...")
            print(f"\n🎯 Confidence: {tradeoff_result['confidence']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    async def demonstrate_quality_metrics(self):
        """Demonstrate quality metrics and assessment capabilities."""
        
        print(f"\n📊 Quality Metrics Demo")
        print("=" * 60)
        
        # Create a sample project for quality analysis
        sample_request = TaskDecompositionRequest(
            user_input="Build a REST API for a blog system with authentication, CRUD operations, and file uploads",
            project_context="Node.js and Express.js application",
            max_depth=3,
            include_estimates=True
        )
        
        try:
            result = await self.decomposition_service.decompose_task(sample_request)
            
            print(f"📈 Project Quality Metrics")
            print("-" * 40)
            
            # Calculate quality metrics
            total_tasks = len(result.project.tasks)
            tasks_with_descriptions = len([t for t in result.project.tasks if t.description])
            tasks_with_estimates = len([t for t in result.project.tasks if t.estimated_hours])
            tasks_with_dependencies = len([t for t in result.project.tasks if t.dependencies])
            
            print(f"Total tasks: {total_tasks}")
            print(f"Description coverage: {(tasks_with_descriptions / total_tasks * 100):.1f}%")
            print(f"Estimation coverage: {(tasks_with_estimates / total_tasks * 100):.1f}%")
            print(f"Dependency coverage: {(tasks_with_dependencies / total_tasks * 100):.1f}%")
            
            # Analyze task quality
            print(f"\n🎯 Task Quality Analysis")
            print("-" * 40)
            
            quality_scores = []
            for task in result.project.tasks:
                score = 0
                
                # Description quality
                if task.description and len(task.description) > 50:
                    score += 2
                elif task.description:
                    score += 1
                
                # Estimation quality
                if task.estimated_hours and 1 <= task.estimated_hours <= 40:
                    score += 2
                elif task.estimated_hours:
                    score += 1
                
                # Priority quality
                if 1 <= task.priority <= 5:
                    score += 1
                
                # Dependency quality
                if task.dependencies:
                    score += 1
                
                quality_scores.append(score)
            
            avg_quality = sum(quality_scores) / len(quality_scores)
            print(f"Average task quality score: {avg_quality:.2f}/6")
            print(f"High quality tasks (>4): {len([s for s in quality_scores if s > 4])}")
            print(f"Medium quality tasks (2-4): {len([s for s in quality_scores if 2 <= s <= 4])}")
            print(f"Low quality tasks (<2): {len([s for s in quality_scores if s < 2])}")
            
            # Show improvement recommendations
            print(f"\n💡 Improvement Recommendations")
            print("-" * 40)
            
            if tasks_with_descriptions / total_tasks < 0.8:
                print("• Add more detailed descriptions to tasks")
            
            if tasks_with_estimates / total_tasks < 0.7:
                print("• Provide time estimates for more tasks")
            
            if tasks_with_dependencies / total_tasks < 0.5:
                print("• Define more task dependencies")
            
            if avg_quality < 4:
                print("• Improve overall task quality and detail")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    async def demonstrate_execution_simulation(self, project: Any):
        """Demonstrate execution simulation with detailed analysis."""
        
        print(f"\n🎮 Execution Simulation Demo")
        print("=" * 60)
        
        if not project:
            print("❌ No project available for simulation")
            return
        
        # Run simulation
        simulation_request = AgentExecutionRequest(
            project_id=project.id,
            simulation_mode=True,
            max_concurrent_tasks=3
        )
        
        try:
            print("🔄 Running execution simulation...")
            simulation_result = await self.simulation_service.simulate_execution(simulation_request)
            
            print(f"✅ Simulation completed!")
            print(f"📊 Completion: {simulation_result.completion_percentage:.1f}%")
            print(f"⏱️  Remaining hours: {simulation_result.estimated_remaining_hours:.1f}")
            
            # Analyze execution log
            print(f"\n📝 Execution Analysis")
            print("-" * 40)
            
            log_entries = simulation_result.execution_log
            task_starts = len([log for log in log_entries if log['type'] == 'task_start'])
            task_completions = len([log for log in log_entries if log['type'] == 'task_completion'])
            errors = len([log for log in log_entries if log['type'] == 'error'])
            
            print(f"Task starts: {task_starts}")
            print(f"Task completions: {task_completions}")
            print(f"Errors: {errors}")
            print(f"Success rate: {(task_completions / max(task_starts, 1)) * 100:.1f}%")
            
            # Show agent workload distribution
            final_status = simulation_result.final_status
            agent_workloads = final_status.get('agent_workloads', {})
            
            print(f"\n🤖 Agent Workload Distribution")
            print("-" * 40)
            for agent, workload in agent_workloads.items():
                print(f"{agent.title():15}: {workload} tasks")
            
            # Show recent execution events
            print(f"\n📋 Recent Execution Events")
            print("-" * 40)
            recent_events = log_entries[-10:]  # Last 10 events
            for event in recent_events:
                timestamp = event['timestamp'][:19]  # Remove microseconds
                event_type = event['type']
                message = event.get('message', event.get('task_title', 'No message'))
                print(f"{timestamp} [{event_type:12}] {message}")
            
        except Exception as e:
            print(f"❌ Simulation error: {str(e)}")
    
    async def run_complete_demo(self):
        """Run the complete advanced demonstration."""
        
        print("🎉 AI Task Planner - Advanced Demonstration")
        print("=" * 80)
        print("This demo showcases advanced capabilities including:")
        print("• Complex project decomposition")
        print("• Multi-agent collaboration")
        print("• Chain-of-thought reasoning")
        print("• Quality metrics and analysis")
        print("• Execution simulation")
        print("=" * 80)
        
        # Step 1: Complex project decomposition
        project = await self.demonstrate_complex_project_decomposition()
        
        # Step 2: Chain-of-thought reasoning
        await self.demonstrate_chain_of_thought_reasoning()
        
        # Step 3: Quality metrics
        await self.demonstrate_quality_metrics()
        
        # Step 4: Execution simulation
        if project:
            await self.demonstrate_execution_simulation(project)
        
        print(f"\n✅ Advanced demonstration completed!")
        print(f"💡 To run the web interface: python main.py")
        print(f"📚 For more examples: python examples/example_usage.py")


async def main():
    """Run the advanced demonstration."""
    
    demo = AdvancedTaskPlannerDemo()
    await demo.run_complete_demo()


if __name__ == "__main__":
    asyncio.run(main())

