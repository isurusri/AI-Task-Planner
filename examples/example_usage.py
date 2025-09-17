"""Example usage of the AI Task Planner API."""

import asyncio
import json
from typing import Dict, Any

from models import TaskDecompositionRequest, AgentExecutionRequest
from services import TaskDecompositionService, ExecutionSimulationService


async def example_task_decomposition():
    """Example of decomposing a feature request into tasks."""
    
    print("🚀 AI Task Planner - Example Usage")
    print("=" * 50)
    
    # Initialize services
    decomposition_service = TaskDecompositionService()
    simulation_service = ExecutionSimulationService()
    
    # Example 1: Simple feature request
    print("\n📝 Example 1: Simple Feature Request")
    print("-" * 40)
    
    simple_request = TaskDecompositionRequest(
        user_input="Create a user registration form with email validation and password strength checking",
        project_context="React web application",
        max_depth=2,
        include_estimates=True
    )
    
    try:
        result = await decomposition_service.decompose_task(simple_request)
        
        print(f"✅ Project created: {result.project.name}")
        print(f"📊 Total tasks: {len(result.project.tasks)}")
        print(f"📋 Execution steps: {len(result.execution_plan)}")
        print(f"📝 Summary: {result.decomposition_summary[:200]}...")
        
        # Display first few tasks
        print("\n🎯 Sample Tasks:")
        for i, task in enumerate(result.project.tasks[:3]):
            print(f"  {i+1}. {task.title}")
            print(f"     Priority: {task.priority}, Hours: {task.estimated_hours or 'N/A'}")
            print(f"     Description: {task.description[:100]}...")
            print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Example 2: Complex feature request
    print("\n📝 Example 2: Complex Feature Request")
    print("-" * 40)
    
    complex_request = TaskDecompositionRequest(
        user_input="""
        Build a comprehensive e-commerce platform with the following features:
        - User authentication and authorization with JWT tokens
        - Product catalog with search, filtering, and pagination
        - Shopping cart and checkout process
        - Payment integration with Stripe
        - Order management and tracking
        - Admin dashboard for inventory management
        - Email notifications for order updates
        - Mobile-responsive design
        """,
        project_context="Full-stack web application using React, Node.js, PostgreSQL, and Redis",
        max_depth=4,
        include_estimates=True
    )
    
    try:
        result = await decomposition_service.decompose_task(complex_request)
        
        print(f"✅ Project created: {result.project.name}")
        print(f"📊 Total tasks: {len(result.project.tasks)}")
        print(f"📋 Execution steps: {len(result.execution_plan)}")
        
        # Analyze task distribution by category
        categories = {}
        for task in result.project.tasks:
            category = task.metadata.get('category', 'general')
            categories[category] = categories.get(category, 0) + 1
        
        print(f"\n📈 Task Distribution by Category:")
        for category, count in categories.items():
            print(f"  {category}: {count} tasks")
        
        # Show execution plan
        print(f"\n🎯 Execution Plan (First 5 steps):")
        for i, step in enumerate(result.execution_plan[:5]):
            print(f"  {step['step']}. {step['task_title']}")
            print(f"     Agent: {step['suggested_agent']}, Hours: {step['estimated_hours']}")
            print(f"     Category: {step['category']}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Example 3: Execution simulation
    print("\n📝 Example 3: Execution Simulation")
    print("-" * 40)
    
    if 'result' in locals():
        simulation_request = AgentExecutionRequest(
            project_id=result.project.id,
            simulation_mode=True,
            max_concurrent_tasks=3
        )
        
        try:
            simulation_result = await simulation_service.simulate_execution(simulation_request)
            
            print(f"✅ Simulation completed")
            print(f"📊 Completion: {simulation_result.completion_percentage:.1f}%")
            print(f"⏱️  Remaining hours: {simulation_result.estimated_remaining_hours:.1f}")
            print(f"📝 Log entries: {len(simulation_result.execution_log)}")
            
            # Show final status
            final_status = simulation_result.final_status
            print(f"\n📈 Final Status:")
            print(f"  Total tasks: {final_status.get('total_tasks', 0)}")
            print(f"  Completed: {final_status.get('completed_tasks', 0)}")
            print(f"  Failed: {final_status.get('failed_tasks', 0)}")
            print(f"  Remaining: {final_status.get('remaining_tasks', 0)}")
            
        except Exception as e:
            print(f"❌ Simulation error: {str(e)}")


async def example_agent_capabilities():
    """Example demonstrating different agent capabilities."""
    
    print("\n🤖 Agent Capabilities Demo")
    print("=" * 50)
    
    from agents import (
        PlannerAgent, AnalyzerAgent, DeveloperAgent,
        TesterAgent, ReviewerAgent, CoordinatorAgent
    )
    
    # Create sample task
    from models import Task, TaskStatus
    sample_task = Task(
        id="sample-task-1",
        title="Implement user authentication",
        description="Create a secure user authentication system with JWT tokens and password hashing",
        status=TaskStatus.PENDING,
        priority=4,
        metadata={"category": "backend", "complexity": "medium"}
    )
    
    context = {
        "project_context": "E-commerce platform",
        "tech_stack": "Node.js, Express, MongoDB, JWT"
    }
    
    # Test each agent
    agents = {
        "Planner": PlannerAgent(),
        "Analyzer": AnalyzerAgent(),
        "Developer": DeveloperAgent(),
        "Tester": TesterAgent(),
        "Reviewer": ReviewerAgent(),
        "Coordinator": CoordinatorAgent()
    }
    
    for agent_name, agent in agents.items():
        print(f"\n🔧 {agent_name} Agent")
        print("-" * 30)
        print(f"Capabilities: {', '.join(agent.get_capabilities()[:3])}...")
        
        try:
            result = await agent.process_task(sample_task, context)
            print(f"✅ Processed successfully")
            print(f"📊 Result keys: {list(result.keys())}")
            
            # Show a sample result
            if 'summary' in result:
                print(f"📝 Summary: {result['summary'][:100]}...")
            elif 'analysis_summary' in result:
                print(f"📝 Analysis: {result['analysis_summary'][:100]}...")
            elif 'implementation_approach' in result:
                print(f"📝 Approach: {result['implementation_approach'][:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


async def example_custom_prompts():
    """Example of customizing prompts for specific use cases."""
    
    print("\n🎨 Custom Prompts Demo")
    print("=" * 50)
    
    from services.openai_service import OpenAIService
    
    openai_service = OpenAIService()
    
    # Example 1: Chain-of-thought reasoning
    print("\n🧠 Chain-of-Thought Reasoning")
    print("-" * 30)
    
    problem = "How should I structure a microservices architecture for a social media platform?"
    
    try:
        reasoning_result = await openai_service.generate_chain_of_thought(problem, {
            "context": "High-traffic application with 1M+ users",
            "requirements": "Scalability, maintainability, real-time features"
        })
        
        print(f"🤔 Reasoning: {reasoning_result['reasoning'][:200]}...")
        print(f"💡 Solution: {reasoning_result['solution'][:200]}...")
        print(f"🎯 Confidence: {reasoning_result['confidence']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Example 2: Task complexity analysis
    print("\n📊 Task Complexity Analysis")
    print("-" * 30)
    
    task_description = "Implement real-time chat functionality with WebSocket connections, message persistence, and online user status"
    
    try:
        complexity_result = await openai_service.analyze_task_complexity(task_description)
        
        print(f"📈 Complexity: {complexity_result['complexity_level']}")
        print(f"⏱️  Hours: {complexity_result['estimated_hours']['min']}-{complexity_result['estimated_hours']['max']}")
        print(f"🛠️  Skills: {', '.join(complexity_result['required_skills'])}")
        print(f"⚠️  Risks: {', '.join(complexity_result['risks'])}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_data_models():
    """Example of using the data models."""
    
    print("\n📋 Data Models Demo")
    print("=" * 50)
    
    from models import Task, Project, AgentType, TaskStatus
    from datetime import datetime
    
    # Create a sample project
    project = Project(
        id="demo-project-1",
        name="Demo E-commerce Platform",
        description="A comprehensive e-commerce solution with modern features"
    )
    
    # Create sample tasks
    tasks = [
        Task(
            id="task-1",
            title="Set up project structure",
            description="Initialize the project with proper folder structure and configuration files",
            status=TaskStatus.PENDING,
            priority=5,
            estimated_hours=2,
            metadata={"category": "setup", "complexity": "low"}
        ),
        Task(
            id="task-2",
            title="Implement user authentication",
            description="Create secure user authentication with JWT tokens",
            status=TaskStatus.PENDING,
            priority=4,
            estimated_hours=8,
            dependencies=["task-1"],
            metadata={"category": "backend", "complexity": "medium"}
        ),
        Task(
            id="task-3",
            title="Design product catalog UI",
            description="Create responsive product catalog interface with search and filtering",
            status=TaskStatus.PENDING,
            priority=3,
            estimated_hours=12,
            dependencies=["task-1"],
            metadata={"category": "frontend", "complexity": "high"}
        )
    ]
    
    project.tasks = tasks
    
    print(f"📁 Project: {project.name}")
    print(f"📊 Total tasks: {len(project.tasks)}")
    print(f"📅 Created: {project.created_at}")
    
    print(f"\n🎯 Tasks:")
    for task in project.tasks:
        print(f"  {task.title}")
        print(f"    Status: {task.status.value}")
        print(f"    Priority: {task.priority}")
        print(f"    Hours: {task.estimated_hours}")
        print(f"    Dependencies: {task.dependencies}")
        print(f"    Category: {task.metadata.get('category', 'N/A')}")
        print()


async def main():
    """Run all examples."""
    
    print("🎉 AI Task Planner - Complete Example Suite")
    print("=" * 60)
    
    # Run examples
    await example_task_decomposition()
    await example_agent_capabilities()
    await example_custom_prompts()
    example_data_models()
    
    print("\n✅ All examples completed!")
    print("\n💡 To run the web interface:")
    print("   python main.py")
    print("   Then open http://localhost:8000 in your browser")


if __name__ == "__main__":
    asyncio.run(main())

