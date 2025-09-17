"""LLM factory service for dynamic LLM provider selection."""

from typing import Optional, Dict, Any
from config import settings
from .llm_service import LLMServiceFactory


class LLMFactoryService:
    """Service that creates LLM services based on configuration."""
    
    def __init__(self):
        self._service = None
        self._current_provider = None
    
    def get_service(self):
        """Get or create the appropriate LLM service."""
        current_provider = settings.llm_provider
        
        # Create new service if provider changed or service doesn't exist
        if self._service is None or self._current_provider != current_provider:
            if current_provider.lower() == "ollama":
                self._service = LLMServiceFactory.create_service(
                    provider="ollama",
                    model=settings.ollama_model,
                    base_url=settings.ollama_base_url
                )
            else:
                self._service = LLMServiceFactory.create_service(provider="openai")
            
            self._current_provider = current_provider
        
        return self._service
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_message: Optional[str] = None
    ) -> str:
        """Generate a completion using the configured LLM service."""
        service = self.get_service()
        return await service.generate_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            system_message=system_message
        )
    
    async def generate_chain_of_thought(
        self, 
        problem: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a chain-of-thought analysis."""
        service = self.get_service()
        return await service.generate_chain_of_thought(problem, context)
    
    async def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """Analyze task complexity."""
        service = self.get_service()
        return await service.analyze_task_complexity(task_description)
    
    async def suggest_agent_assignment(
        self, 
        task: Dict[str, Any], 
        available_agents: list
    ) -> Dict[str, Any]:
        """Suggest agent assignment."""
        service = self.get_service()
        return await service.suggest_agent_assignment(task, available_agents)
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current LLM provider."""
        provider = settings.llm_provider.lower()
        
        if provider == "ollama":
            return {
                "provider": "ollama",
                "model": settings.ollama_model,
                "base_url": settings.ollama_base_url,
                "status": "configured"
            }
        else:
            return {
                "provider": "openai",
                "model": settings.openai_model,
                "api_key_configured": bool(settings.openai_api_key),
                "status": "configured" if settings.openai_api_key else "missing_api_key"
            }
