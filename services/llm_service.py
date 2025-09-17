"""LLM service abstraction supporting both OpenAI and Ollama."""

import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import openai
from openai import AsyncOpenAI
import ollama
from config import settings


class BaseLLMService(ABC):
    """Base class for LLM services."""
    
    @abstractmethod
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_message: Optional[str] = None
    ) -> str:
        """Generate a completion using the LLM."""
        pass
    
    @abstractmethod
    async def generate_chain_of_thought(
        self, 
        problem: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a chain-of-thought analysis."""
        pass
    
    @abstractmethod
    async def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """Analyze task complexity."""
        pass
    
    @abstractmethod
    async def suggest_agent_assignment(
        self, 
        task: Dict[str, Any], 
        available_agents: list
    ) -> Dict[str, Any]:
        """Suggest agent assignment."""
        pass


class OpenAIService(BaseLLMService):
    """OpenAI LLM service implementation."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_message: Optional[str] = None
    ) -> str:
        """Generate a completion using OpenAI API."""
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_chain_of_thought(
        self, 
        problem: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a chain-of-thought analysis for a given problem."""
        system_message = """You are an expert problem solver. Use chain-of-thought reasoning to break down complex problems into logical steps. Always provide your reasoning process before giving the final answer."""
        
        context_str = ""
        if context:
            context_str = f"\n\nContext: {context}"
        
        prompt = f"""
Problem: {problem}{context_str}

Please solve this step by step:

1. First, understand the problem clearly
2. Identify the key components and requirements
3. Break down the solution into logical steps
4. Consider potential challenges and solutions
5. Provide a clear, actionable plan

Format your response as:
REASONING: [Your step-by-step reasoning process]
SOLUTION: [Your final solution or recommendation]
CONFIDENCE: [Your confidence level from 0.0 to 1.0]
"""
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3
        )
        
        return self._parse_chain_of_thought_response(response)
    
    async def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """Analyze the complexity of a task using AI."""
        prompt = f"""
Analyze the complexity of this software development task:

Task: {task_description}

Please provide:
1. Complexity level (Low/Medium/High)
2. Estimated hours (range)
3. Required skills
4. Potential risks
5. Dependencies

Format as JSON:
{{
    "complexity_level": "Medium",
    "estimated_hours": {{"min": 4, "max": 12}},
    "required_skills": ["Python", "FastAPI", "Database"],
    "risks": ["Risk 1", "Risk 2"],
    "dependencies": ["Dependency 1", "Dependency 2"]
}}
"""
        
        response = await self.generate_completion(
            prompt=prompt,
            temperature=0.2,
            max_tokens=500
        )
        
        return self._parse_json_response(response, {
            "complexity_level": "Medium",
            "estimated_hours": {"min": 4, "max": 12},
            "required_skills": ["General Development"],
            "risks": ["Unknown complexity"],
            "dependencies": []
        })
    
    async def suggest_agent_assignment(
        self, 
        task: Dict[str, Any], 
        available_agents: list
    ) -> Dict[str, Any]:
        """Suggest which agent should handle a task."""
        agent_descriptions = []
        for agent in available_agents:
            agent_descriptions.append(f"- {agent['type']}: {agent['description']}")
        
        prompt = f"""
Task: {task.get('title', 'Unknown')}
Description: {task.get('description', 'No description')}
Category: {task.get('category', 'general')}

Available agents:
{chr(10).join(agent_descriptions)}

Which agent type would be best suited for this task? Consider:
1. Task requirements
2. Agent capabilities
3. Current workload
4. Task complexity

Respond with just the agent type name.
"""
        
        response = await self.generate_completion(
            prompt=prompt,
            temperature=0.1,
            max_tokens=50
        )
        
        suggested_agent = response.strip().lower()
        
        agent_mapping = {
            'planner': 'planner',
            'analyzer': 'analyzer', 
            'developer': 'developer',
            'tester': 'tester',
            'reviewer': 'reviewer',
            'coordinator': 'coordinator'
        }
        
        for key, value in agent_mapping.items():
            if key in suggested_agent:
                return {"suggested_agent": value, "confidence": 0.8}
        
        return {"suggested_agent": "developer", "confidence": 0.5}
    
    def _parse_chain_of_thought_response(self, response: str) -> Dict[str, Any]:
        """Parse chain-of-thought response."""
        reasoning = ""
        solution = ""
        confidence = 0.5
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('REASONING:'):
                current_section = 'reasoning'
                reasoning = line.replace('REASONING:', '').strip()
            elif line.startswith('SOLUTION:'):
                current_section = 'solution'
                solution = line.replace('SOLUTION:', '').strip()
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence = float(line.replace('CONFIDENCE:', '').strip())
                except ValueError:
                    confidence = 0.5
            elif current_section and line:
                if current_section == 'reasoning':
                    reasoning += f"\n{line}"
                elif current_section == 'solution':
                    solution += f"\n{line}"
        
        return {
            "reasoning": reasoning,
            "solution": solution,
            "confidence": confidence,
            "raw_response": response
        }
    
    def _parse_json_response(self, response: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
        """Parse JSON response with fallback."""
        import json
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, KeyError):
            pass
        
        return fallback


class OllamaService(BaseLLMService):
    """Ollama LLM service implementation."""
    
    def __init__(self, model: str = "llama2:latest", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.client = ollama.AsyncClient(host=base_url)
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_message: Optional[str] = None
    ) -> str:
        """Generate a completion using Ollama."""
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "num_predict": max_tokens or 2000,
                    "temperature": temperature or 0.7,
                    "top_p": 0.9,
                }
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    async def generate_chain_of_thought(
        self, 
        problem: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a chain-of-thought analysis using Ollama."""
        system_message = """You are an expert problem solver. Use chain-of-thought reasoning to break down complex problems into logical steps. Always provide your reasoning process before giving the final answer."""
        
        context_str = ""
        if context:
            context_str = f"\n\nContext: {context}"
        
        prompt = f"""
Problem: {problem}{context_str}

Please solve this step by step:

1. First, understand the problem clearly
2. Identify the key components and requirements
3. Break down the solution into logical steps
4. Consider potential challenges and solutions
5. Provide a clear, actionable plan

Format your response as:
REASONING: [Your step-by-step reasoning process]
SOLUTION: [Your final solution or recommendation]
CONFIDENCE: [Your confidence level from 0.0 to 1.0]
"""
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3
        )
        
        return self._parse_chain_of_thought_response(response)
    
    async def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """Analyze task complexity using Ollama."""
        prompt = f"""
Analyze the complexity of this software development task:

Task: {task_description}

Please provide:
1. Complexity level (Low/Medium/High)
2. Estimated hours (range)
3. Required skills
4. Potential risks
5. Dependencies

Format as JSON:
{{
    "complexity_level": "Medium",
    "estimated_hours": {{"min": 4, "max": 12}},
    "required_skills": ["Python", "FastAPI", "Database"],
    "risks": ["Risk 1", "Risk 2"],
    "dependencies": ["Dependency 1", "Dependency 2"]
}}
"""
        
        response = await self.generate_completion(
            prompt=prompt,
            temperature=0.2,
            max_tokens=500
        )
        
        return self._parse_json_response(response, {
            "complexity_level": "Medium",
            "estimated_hours": {"min": 4, "max": 12},
            "required_skills": ["General Development"],
            "risks": ["Unknown complexity"],
            "dependencies": []
        })
    
    async def suggest_agent_assignment(
        self, 
        task: Dict[str, Any], 
        available_agents: list
    ) -> Dict[str, Any]:
        """Suggest agent assignment using Ollama."""
        agent_descriptions = []
        for agent in available_agents:
            agent_descriptions.append(f"- {agent['type']}: {agent['description']}")
        
        prompt = f"""
Task: {task.get('title', 'Unknown')}
Description: {task.get('description', 'No description')}
Category: {task.get('category', 'general')}

Available agents:
{chr(10).join(agent_descriptions)}

Which agent type would be best suited for this task? Consider:
1. Task requirements
2. Agent capabilities
3. Current workload
4. Task complexity

Respond with just the agent type name.
"""
        
        response = await self.generate_completion(
            prompt=prompt,
            temperature=0.1,
            max_tokens=50
        )
        
        suggested_agent = response.strip().lower()
        
        agent_mapping = {
            'planner': 'planner',
            'analyzer': 'analyzer', 
            'developer': 'developer',
            'tester': 'tester',
            'reviewer': 'reviewer',
            'coordinator': 'coordinator'
        }
        
        for key, value in agent_mapping.items():
            if key in suggested_agent:
                return {"suggested_agent": value, "confidence": 0.8}
        
        return {"suggested_agent": "developer", "confidence": 0.5}
    
    def _parse_chain_of_thought_response(self, response: str) -> Dict[str, Any]:
        """Parse chain-of-thought response."""
        reasoning = ""
        solution = ""
        confidence = 0.5
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('REASONING:'):
                current_section = 'reasoning'
                reasoning = line.replace('REASONING:', '').strip()
            elif line.startswith('SOLUTION:'):
                current_section = 'solution'
                solution = line.replace('SOLUTION:', '').strip()
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence = float(line.replace('CONFIDENCE:', '').strip())
                except ValueError:
                    confidence = 0.5
            elif current_section and line:
                if current_section == 'reasoning':
                    reasoning += f"\n{line}"
                elif current_section == 'solution':
                    solution += f"\n{line}"
        
        return {
            "reasoning": reasoning,
            "solution": solution,
            "confidence": confidence,
            "raw_response": response
        }
    
    def _parse_json_response(self, response: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
        """Parse JSON response with fallback."""
        import json
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, KeyError):
            pass
        
        return fallback


class LLMServiceFactory:
    """Factory for creating LLM services."""
    
    @staticmethod
    def create_service(provider: str = "openai", **kwargs) -> BaseLLMService:
        """Create an LLM service based on the provider."""
        if provider.lower() == "openai":
            return OpenAIService()
        elif provider.lower() == "ollama":
            model = kwargs.get('model', 'llama2:latest')
            base_url = kwargs.get('base_url', 'http://localhost:11434')
            return OllamaService(model=model, base_url=base_url)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


# Backward compatibility
OpenAIService = OpenAIService
