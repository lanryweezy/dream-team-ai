"""
LLM Integration System for Dream Machine
Provides unified interface for multiple LLM providers
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
import os

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"
    MOCK = "mock"

class LLMRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class LLMMessage:
    role: LLMRole
    content: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class LLMResponse:
    content: str
    provider: LLMProvider
    model: str
    tokens_used: int
    cost_estimate: float
    response_time: float
    metadata: Dict[str, Any]

class LLMError(Exception):
    """Base exception for LLM-related errors"""
    pass

class LLMRateLimitError(LLMError):
    """Raised when rate limits are exceeded"""
    pass

class LLMQuotaExceededError(LLMError):
    """Raised when quota is exceeded"""
    pass

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.config = kwargs
        
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        **kwargs
    ) -> LLMResponse:
        """Generate response from LLM"""
        pass
        
    @abstractmethod
    async def generate_structured_response(
        self, 
        messages: List[LLMMessage], 
        schema: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured response matching schema"""
        pass

class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing"""
    
    def __init__(self, **kwargs):
        super().__init__("mock_key", "mock_model", **kwargs)
        
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        **kwargs
    ) -> LLMResponse:
        """Generate mock response"""
        await asyncio.sleep(0.1)  # Simulate API delay
        
        # Generate contextual mock response based on last message
        last_message = messages[-1].content.lower()
        
        if "blueprint" in last_message or "company" in last_message:
            content = """Based on your dream, I recommend creating a SaaS platform focused on productivity tools. 
            Key features should include task management, team collaboration, and analytics. 
            Target market: Small to medium businesses looking to improve efficiency."""
            
        elif "financial" in last_message or "budget" in last_message:
            content = """Current financial status looks healthy. Recommend allocating 40% to development, 
            30% to marketing, 20% to operations, and 10% to reserves. Monitor burn rate closely."""
            
        elif "marketing" in last_message:
            content = """Suggest focusing on content marketing and social media presence. 
            Target early adopters through tech communities and productivity forums. 
            Consider influencer partnerships in the business productivity space."""
            
        else:
            content = f"I understand you're asking about: {messages[-1].content[:100]}... Let me provide a thoughtful response based on the context."
            
        return LLMResponse(
            content=content,
            provider=LLMProvider.MOCK,
            model="mock_model",
            tokens_used=len(content.split()) * 2,  # Rough estimate
            cost_estimate=0.001,
            response_time=0.1,
            metadata={"mock": True, "timestamp": datetime.now(timezone.utc).isoformat()}
        )
        
    async def generate_structured_response(
        self, 
        messages: List[LLMMessage], 
        schema: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured mock response"""
        await asyncio.sleep(0.1)
        
        # Generate mock structured data based on schema
        if "company_blueprint" in str(schema).lower():
            return {
                "company_name": "DreamTech Solutions",
                "vision": "Revolutionize productivity through intelligent automation",
                "mission": "Empower businesses with cutting-edge productivity tools",
                "industry": "SaaS",
                "target_market": {
                    "primary": "Small to medium businesses",
                    "secondary": "Freelancers and consultants"
                },
                "business_model": "Subscription-based SaaS",
                "key_features": [
                    "Task management",
                    "Team collaboration",
                    "Analytics dashboard",
                    "API integrations"
                ],
                "competitive_advantages": [
                    "AI-powered insights",
                    "Seamless integrations",
                    "User-friendly interface"
                ]
            }
        elif "financial_analysis" in str(schema).lower():
            return {
                "total_budget": 100000,
                "allocations": {
                    "development": 40000,
                    "marketing": 30000,
                    "operations": 20000,
                    "reserves": 10000
                },
                "burn_rate": 8500,
                "runway_months": 12,
                "recommendations": [
                    "Focus on customer acquisition",
                    "Monitor development costs closely",
                    "Consider additional funding in 6 months"
                ]
            }
        else:
            return {"result": "Mock structured response", "schema_matched": True}

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = kwargs.get("base_url", "https://api.openai.com/v1")
        
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        **kwargs
    ) -> LLMResponse:
        """Generate response using OpenAI API"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # Convert messages to OpenAI format
            openai_messages = [
                {"role": msg.role.value, "content": msg.content}
                for msg in messages
            ]
            
            start_time = datetime.now()
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            return LLMResponse(
                content=response.choices[0].message.content,
                provider=LLMProvider.OPENAI,
                model=self.model,
                tokens_used=response.usage.total_tokens,
                cost_estimate=self._calculate_cost(response.usage.total_tokens),
                response_time=response_time,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMError(f"OpenAI API error: {e}")
            
    async def generate_structured_response(
        self, 
        messages: List[LLMMessage], 
        schema: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured response using OpenAI function calling"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # Add schema instruction to system message
            schema_instruction = f"Please respond with a JSON object that matches this schema: {json.dumps(schema, indent=2)}"
            
            # Modify messages to include schema instruction
            modified_messages = messages.copy()
            if modified_messages and modified_messages[0].role == LLMRole.SYSTEM:
                modified_messages[0].content += f"\n\n{schema_instruction}"
            else:
                modified_messages.insert(0, LLMMessage(
                    role=LLMRole.SYSTEM,
                    content=schema_instruction
                ))
            
            response = await self.generate_response(modified_messages, **kwargs)
            
            # Parse JSON response
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback: extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise LLMError("Could not parse structured response")
                    
        except Exception as e:
            logger.error(f"OpenAI structured response error: {e}")
            raise LLMError(f"OpenAI structured response error: {e}")
            
    def _calculate_cost(self, tokens: int) -> float:
        """Calculate estimated cost based on tokens"""
        # GPT-4 pricing (approximate)
        if "gpt-4" in self.model.lower():
            return tokens * 0.00003  # $0.03 per 1K tokens
        else:
            return tokens * 0.000002  # GPT-3.5 pricing

class LLMManager:
    """Central manager for LLM operations"""
    
    def __init__(self):
        self.providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self.default_provider = LLMProvider.MOCK
        self.cost_tracker = []
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }
        
    def register_provider(self, provider_type: LLMProvider, provider: BaseLLMProvider):
        """Register an LLM provider"""
        self.providers[provider_type] = provider
        logger.info(f"Registered LLM provider: {provider_type.value}")
        
    def set_default_provider(self, provider_type: LLMProvider):
        """Set default LLM provider"""
        if provider_type not in self.providers:
            raise ValueError(f"Provider {provider_type.value} not registered")
        self.default_provider = provider_type
        logger.info(f"Set default LLM provider: {provider_type.value}")
        
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate response using specified or default provider"""
        provider = provider or self.default_provider
        
        if provider not in self.providers:
            raise ValueError(f"Provider {provider.value} not registered")
            
        try:
            response = await self.providers[provider].generate_response(messages, **kwargs)
            
            # Track usage
            self._track_usage(response)
            
            return response
            
        except Exception as e:
            logger.error(f"LLM generation error with {provider.value}: {e}")
            raise
            
    async def generate_structured_response(
        self, 
        messages: List[LLMMessage], 
        schema: Dict[str, Any],
        provider: Optional[LLMProvider] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured response using specified or default provider"""
        provider = provider or self.default_provider
        
        if provider not in self.providers:
            raise ValueError(f"Provider {provider.value} not registered")
            
        try:
            response = await self.providers[provider].generate_structured_response(
                messages, schema, **kwargs
            )
            
            return response
            
        except Exception as e:
            logger.error(f"LLM structured generation error with {provider.value}: {e}")
            raise
            
    def _track_usage(self, response: LLMResponse):
        """Track LLM usage statistics"""
        self.usage_stats["total_requests"] += 1
        self.usage_stats["total_tokens"] += response.tokens_used
        self.usage_stats["total_cost"] += response.cost_estimate
        
        self.cost_tracker.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": response.provider.value,
            "model": response.model,
            "tokens": response.tokens_used,
            "cost": response.cost_estimate,
            "response_time": response.response_time
        })
        
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return self.usage_stats.copy()
        
    def get_cost_breakdown(self) -> List[Dict[str, Any]]:
        """Get detailed cost breakdown"""
        return self.cost_tracker.copy()

# Global LLM manager instance
llm_manager = LLMManager()

# Initialize with mock provider by default
llm_manager.register_provider(LLMProvider.MOCK, MockLLMProvider())

async def initialize_llm_providers():
    """Initialize LLM providers based on environment variables and available services"""
    
    # Try Ollama first (local)
    try:
        from .ollama_provider import ollama_manager, OllamaProvider
        
        if await ollama_manager.initialize():
            # Get the first available model
            provider = ollama_manager.get_provider()
            if provider:
                llm_manager.register_provider(LLMProvider.LOCAL, provider)
                llm_manager.set_default_provider(LLMProvider.LOCAL)
                logger.info(f"Ollama provider initialized with model: {provider.model}")
        else:
            logger.info("Ollama not available, trying other providers...")
            
    except Exception as e:
        logger.warning(f"Failed to initialize Ollama provider: {e}")
    
    # OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            provider = OpenAIProvider(
                api_key=openai_key,
                model=os.getenv("OPENAI_MODEL", "gpt-4")
            )
            llm_manager.register_provider(LLMProvider.OPENAI, provider)
            
            # Set as default if no local provider available
            if LLMProvider.LOCAL not in llm_manager.providers:
                llm_manager.set_default_provider(LLMProvider.OPENAI)
                
            logger.info("OpenAI provider initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI provider: {e}")
    
    # Add other providers here (Anthropic, Google, etc.)
    
    logger.info(f"LLM system initialized with {len(llm_manager.providers)} providers")
    logger.info(f"Default provider: {llm_manager.default_provider.value}")

# Convenience functions
async def ask_llm(
    prompt: str, 
    system_prompt: Optional[str] = None,
    provider: Optional[LLMProvider] = None,
    **kwargs
) -> str:
    """Simple function to ask LLM a question"""
    messages = []
    
    if system_prompt:
        messages.append(LLMMessage(role=LLMRole.SYSTEM, content=system_prompt))
        
    messages.append(LLMMessage(role=LLMRole.USER, content=prompt))
    
    response = await llm_manager.generate_response(messages, provider, **kwargs)
    return response.content

async def ask_llm_structured(
    prompt: str,
    schema: Dict[str, Any],
    system_prompt: Optional[str] = None,
    provider: Optional[LLMProvider] = None,
    **kwargs
) -> Dict[str, Any]:
    """Ask LLM for structured response"""
    messages = []
    
    if system_prompt:
        messages.append(LLMMessage(role=LLMRole.SYSTEM, content=system_prompt))
        
    messages.append(LLMMessage(role=LLMRole.USER, content=prompt))
    
    return await llm_manager.generate_structured_response(
        messages, schema, provider, **kwargs
    )