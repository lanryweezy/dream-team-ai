"""
Ollama Local LLM Provider for Dream Machine
Provides integration with local Ollama models
"""

import asyncio
import json
import logging
import aiohttp
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from .llm_integration import BaseLLMProvider, LLMMessage, LLMResponse, LLMProvider, LLMError

logger = logging.getLogger(__name__)

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2", **kwargs):
        super().__init__("local", model, **kwargs)
        self.base_url = base_url.rstrip('/')
        self.timeout = kwargs.get("timeout", 120)  # 2 minutes default
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
        
    async def close(self):
        """Close HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()
            
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        **kwargs
    ) -> LLMResponse:
        """Generate response using Ollama API"""
        try:
            session = await self._get_session()
            
            # Convert messages to Ollama format
            prompt = self._messages_to_prompt(messages)
            
            # Prepare request data
            request_data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "top_p": kwargs.get("top_p", 0.9),
                    "top_k": kwargs.get("top_k", 40),
                    "num_predict": kwargs.get("max_tokens", 2000),
                }
            }
            
            start_time = datetime.now()
            
            # Make request to Ollama
            async with session.post(
                f"{self.base_url}/api/generate",
                json=request_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    raise LLMError(f"Ollama API error {response.status}: {error_text}")
                
                result = await response.json()
                
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Extract response content
            content = result.get("response", "")
            
            # Estimate tokens (rough approximation)
            tokens_used = len(content.split()) + len(prompt.split())
            
            return LLMResponse(
                content=content,
                provider=LLMProvider.LOCAL,
                model=self.model,
                tokens_used=tokens_used,
                cost_estimate=0.0,  # Local models are free
                response_time=response_time,
                metadata={
                    "ollama_model": self.model,
                    "total_duration": result.get("total_duration", 0),
                    "load_duration": result.get("load_duration", 0),
                    "prompt_eval_count": result.get("prompt_eval_count", 0),
                    "eval_count": result.get("eval_count", 0),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
        except aiohttp.ClientError as e:
            logger.error(f"Ollama connection error: {e}")
            raise LLMError(f"Failed to connect to Ollama: {e}")
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise LLMError(f"Ollama API error: {e}")
            
    async def generate_structured_response(
        self, 
        messages: List[LLMMessage], 
        schema: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured response using Ollama"""
        try:
            # Add schema instruction to the prompt
            schema_instruction = f"""
Please respond with a valid JSON object that matches this exact schema:
{json.dumps(schema, indent=2)}

Important: 
- Return ONLY the JSON object, no additional text
- Ensure all required fields are included
- Use appropriate data types as specified in the schema
"""
            
            # Modify messages to include schema instruction
            modified_messages = messages.copy()
            if modified_messages and modified_messages[0].role.value == "system":
                modified_messages[0].content += f"\n\n{schema_instruction}"
            else:
                from .llm_integration import LLMRole
                modified_messages.insert(0, LLMMessage(
                    role=LLMRole.SYSTEM,
                    content=schema_instruction
                ))
            
            response = await self.generate_response(modified_messages, **kwargs)
            
            # Parse JSON response
            content = response.content.strip()
            
            # Try to extract JSON from response
            try:
                # First, try to parse the entire response as JSON
                return json.loads(content)
            except json.JSONDecodeError:
                # If that fails, try to find JSON within the response
                import re
                
                # Look for JSON object patterns
                json_patterns = [
                    r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested objects
                    r'\{.*?\}',  # Basic object pattern
                ]
                
                for pattern in json_patterns:
                    matches = re.findall(pattern, content, re.DOTALL)
                    for match in matches:
                        try:
                            parsed = json.loads(match)
                            if isinstance(parsed, dict):
                                return parsed
                        except json.JSONDecodeError:
                            continue
                
                # If no valid JSON found, create a fallback response
                logger.warning(f"Could not parse JSON from Ollama response: {content[:200]}...")
                return {
                    "error": "Could not parse structured response",
                    "raw_response": content,
                    "schema_requested": schema
                }
                
        except Exception as e:
            logger.error(f"Ollama structured response error: {e}")
            raise LLMError(f"Ollama structured response error: {e}")
            
    def _messages_to_prompt(self, messages: List[LLMMessage]) -> str:
        """Convert messages to a single prompt for Ollama"""
        prompt_parts = []
        
        for message in messages:
            role = message.role.value
            content = message.content
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
                
        # Add final prompt for assistant response
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
        
    async def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            session = await self._get_session()
            
            async with session.get(f"{self.base_url}/api/tags") as response:
                if response.status != 200:
                    raise LLMError(f"Failed to list models: {response.status}")
                    
                result = await response.json()
                models = [model["name"] for model in result.get("models", [])]
                return models
                
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []
            
    async def pull_model(self, model_name: str) -> bool:
        """Pull/download a model in Ollama"""
        try:
            session = await self._get_session()
            
            request_data = {"name": model_name}
            
            async with session.post(
                f"{self.base_url}/api/pull",
                json=request_data
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Failed to pull model {model_name}: {error_text}")
                    return False
                    
                # Stream the pull progress
                async for line in response.content:
                    if line:
                        try:
                            progress = json.loads(line.decode())
                            if "status" in progress:
                                logger.info(f"Pull progress: {progress['status']}")
                        except json.JSONDecodeError:
                            pass
                            
                logger.info(f"Successfully pulled model: {model_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
            
    async def health_check(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            session = await self._get_session()
            
            async with session.get(f"{self.base_url}/api/tags") as response:
                return response.status == 200
                
        except Exception as e:
            logger.debug(f"Ollama health check failed: {e}")
            return False

class OllamaManager:
    """Manager for Ollama operations"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.providers: Dict[str, OllamaProvider] = {}
        
    async def initialize(self) -> bool:
        """Initialize Ollama connection and check available models"""
        try:
            # Create a temporary provider to check connection
            temp_provider = OllamaProvider(base_url=self.base_url)
            
            # Check if Ollama is running
            if not await temp_provider.health_check():
                logger.warning("Ollama is not running or not accessible")
                await temp_provider.close()
                return False
                
            # Get available models
            models = await temp_provider.list_models()
            logger.info(f"Available Ollama models: {models}")
            
            # Create providers for available models
            for model in models:
                self.providers[model] = OllamaProvider(
                    base_url=self.base_url,
                    model=model
                )
                
            await temp_provider.close()
            
            if not models:
                logger.warning("No Ollama models found. Consider pulling a model first.")
                # Try to pull a default model
                default_model = "llama2"
                logger.info(f"Attempting to pull default model: {default_model}")
                temp_provider = OllamaProvider(base_url=self.base_url)
                success = await temp_provider.pull_model(default_model)
                if success:
                    self.providers[default_model] = OllamaProvider(
                        base_url=self.base_url,
                        model=default_model
                    )
                await temp_provider.close()
                    
            return len(self.providers) > 0
            
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
            return False
            
    def get_provider(self, model: str = None) -> Optional[OllamaProvider]:
        """Get Ollama provider for specific model"""
        if model and model in self.providers:
            return self.providers[model]
        elif self.providers:
            # Return first available provider
            return next(iter(self.providers.values()))
        return None
        
    async def close_all(self):
        """Close all provider sessions"""
        for provider in self.providers.values():
            await provider.close()

# Global Ollama manager
ollama_manager = OllamaManager()