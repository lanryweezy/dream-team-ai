"""
Universal Tool Integration Framework
Connects to all YC tools, development tools, scheduling tools, and AI services
Provides unified API access and intelligent orchestration
"""

import json
import logging
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class ToolCategory(Enum):
    DEVELOPMENT = "development"
    PROJECT_MANAGEMENT = "project_management"
    COMMUNICATION = "communication"
    AI_SERVICES = "ai_services"
    MARKETING = "marketing"
    SALES = "sales"
    FINANCE = "finance"
    SCHEDULING = "scheduling"

class IntegrationStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

@dataclass
class ToolCredentials:
    """Secure credential storage for tool integrations"""
    tool_name: str
    credential_type: str
    credentials: Dict[str, str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ToolIntegration:
    """Tool integration configuration and status"""
    tool_name: str
    category: ToolCategory
    status: IntegrationStatus
    api_base_url: str
    supported_operations: List[str]
    rate_limits: Dict[str, int]

@dataclass
class ToolOperation:
    """Individual tool operation tracking"""
    operation_id: str
    tool_name: str
    operation_type: str
    parameters: Dict[str, Any]
    status: str
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class UniversalToolIntegration:
    """Universal Tool Integration Framework"""
    
    def __init__(self):
        self.integrations: Dict[str, ToolIntegration] = {}
        self.credentials: Dict[str, ToolCredentials] = {}
        self.operations: Dict[str, ToolOperation] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
        self._initialize_tool_configurations()
    
    def _initialize_tool_configurations(self):
        """Initialize configurations for all supported tools"""
        
        tools_config = {
            "github": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.github.com",
                "operations": ["get_repos", "create_repo", "get_issues", "create_issue"],
                "rate_limits": {"get_repos": 5000, "create_repo": 100}
            },
            "slack": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://slack.com/api",
                "operations": ["send_message", "get_channels"],
                "rate_limits": {"send_message": 1, "get_channels": 100}
            },
            "linear": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.linear.app/graphql",
                "operations": ["get_issues", "create_issue"],
                "rate_limits": {"get_issues": 1000, "create_issue": 200}
            },
            "openai": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.openai.com/v1",
                "operations": ["chat_completion", "embeddings"],
                "rate_limits": {"chat_completion": 3500, "embeddings": 3000}
            },
            "stripe": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://api.stripe.com/v1",
                "operations": ["create_payment", "get_customers"],
                "rate_limits": {"create_payment": 100, "get_customers": 100}
            }
        }
        
        for tool_name, config in tools_config.items():
            self.integrations[tool_name] = ToolIntegration(
                tool_name=tool_name,
                category=config["category"],
                status=IntegrationStatus.DISCONNECTED,
                api_base_url=config["api_base_url"],
                supported_operations=config["operations"],
                rate_limits=config["rate_limits"]
            )
    
    async def start(self):
        """Initialize the integration framework"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"User-Agent": "DreamMachine/1.0"}
        )
        logger.info("Universal Tool Integration Framework started")
    
    async def stop(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        logger.info("Universal Tool Integration Framework stopped")
    
    async def connect_tool(self, tool_name: str, credentials: Dict[str, str], 
                          credential_type: str = "api_key") -> bool:
        """Connect to a tool with credentials"""
        
        if tool_name not in self.integrations:
            logger.error(f"Tool '{tool_name}' not supported")
            return False
        
        try:
            self.credentials[tool_name] = ToolCredentials(
                tool_name=tool_name,
                credential_type=credential_type,
                credentials=credentials
            )
            
            test_result = await self._test_connection(tool_name)
            
            if test_result:
                self.integrations[tool_name].status = IntegrationStatus.CONNECTED
                logger.info(f"Successfully connected to {tool_name}")
                return True
            else:
                self.integrations[tool_name].status = IntegrationStatus.ERROR
                logger.error(f"Failed to connect to {tool_name}")
                return False
                
        except Exception as e:
            self.integrations[tool_name].status = IntegrationStatus.ERROR
            logger.error(f"Error connecting to {tool_name}: {e}")
            return False
    
    async def _test_connection(self, tool_name: str) -> bool:
        """Test connection to a tool"""
        
        if tool_name not in self.credentials:
            return False
        
        try:
            if tool_name == "github":
                return await self._test_github_connection()
            elif tool_name == "slack":
                return await self._test_slack_connection()
            elif tool_name == "openai":
                return await self._test_openai_connection()
            else:
                return await self._test_generic_connection(tool_name)
                
        except Exception as e:
            logger.error(f"Connection test failed for {tool_name}: {e}")
            return False
    
    async def _test_github_connection(self) -> bool:
        """Test GitHub API connection"""
        credentials = self.credentials["github"]
        headers = {
            "Authorization": f"token {credentials.credentials['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with self.session.get("https://api.github.com/user", headers=headers) as response:
            return response.status == 200
    
    async def _test_slack_connection(self) -> bool:
        """Test Slack API connection"""
        credentials = self.credentials["slack"]
        headers = {"Authorization": f"Bearer {credentials.credentials['token']}"}
        
        async with self.session.get("https://slack.com/api/auth.test", headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("ok", False)
            return False
    
    async def _test_openai_connection(self) -> bool:
        """Test OpenAI API connection"""
        credentials = self.credentials["openai"]
        headers = {"Authorization": f"Bearer {credentials.credentials['api_key']}"}
        
        async with self.session.get("https://api.openai.com/v1/models", headers=headers) as response:
            return response.status == 200
    
    async def _test_generic_connection(self, tool_name: str) -> bool:
        """Generic connection test"""
        integration = self.integrations[tool_name]
        
        try:
            async with self.session.get(integration.api_base_url) as response:
                return response.status in [200, 401]
        except:
            return False
    
    async def execute_operation(self, tool_name: str, operation: str, 
                               parameters: Dict[str, Any]) -> ToolOperation:
        """Execute an operation on a connected tool"""
        
        operation_id = f"op_{uuid.uuid4().hex[:8]}"
        
        tool_operation = ToolOperation(
            operation_id=operation_id,
            tool_name=tool_name,
            operation_type=operation,
            parameters=parameters,
            status="pending"
        )
        
        self.operations[operation_id] = tool_operation
        
        try:
            if tool_name not in self.integrations:
                raise ValueError(f"Tool '{tool_name}' not supported")
            
            integration = self.integrations[tool_name]
            if integration.status != IntegrationStatus.CONNECTED:
                raise ValueError(f"Tool '{tool_name}' not connected")
            
            result = await self._execute_tool_operation(tool_name, operation, parameters)
            
            tool_operation.status = "success"
            tool_operation.result = result
            
            return tool_operation
            
        except Exception as e:
            tool_operation.status = "failed"
            tool_operation.error_message = str(e)
            logger.error(f"Operation failed: {tool_name}.{operation} - {e}")
            return tool_operation
    
    async def _execute_tool_operation(self, tool_name: str, operation: str, 
                                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific tool operation"""
        
        if tool_name == "github":
            return await self._execute_github_operation(operation, parameters)
        elif tool_name == "slack":
            return await self._execute_slack_operation(operation, parameters)
        elif tool_name == "openai":
            return await self._execute_openai_operation(operation, parameters)
        else:
            return await self._execute_generic_operation(tool_name, operation, parameters)
    
    async def _execute_github_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GitHub API operations"""
        credentials = self.credentials["github"]
        headers = {
            "Authorization": f"token {credentials.credentials['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if operation == "get_repos":
            async with self.session.get("https://api.github.com/user/repos", 
                                       headers=headers, params=parameters) as response:
                return await response.json()
        elif operation == "create_repo":
            async with self.session.post("https://api.github.com/user/repos", 
                                        headers=headers, json=parameters) as response:
                return await response.json()
        else:
            raise ValueError(f"Unsupported GitHub operation: {operation}")
    
    async def _execute_slack_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Slack API operations"""
        credentials = self.credentials["slack"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Content-Type": "application/json"
        }
        
        if operation == "send_message":
            async with self.session.post("https://slack.com/api/chat.postMessage", 
                                        headers=headers, json=parameters) as response:
                return await response.json()
        else:
            raise ValueError(f"Unsupported Slack operation: {operation}")
    
    async def _execute_openai_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OpenAI API operations"""
        credentials = self.credentials["openai"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['api_key']}",
            "Content-Type": "application/json"
        }
        
        if operation == "chat_completion":
            async with self.session.post("https://api.openai.com/v1/chat/completions", 
                                        headers=headers, json=parameters) as response:
                return await response.json()
        else:
            raise ValueError(f"Unsupported OpenAI operation: {operation}")
    
    async def _execute_generic_operation(self, tool_name: str, operation: str, 
                                        parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic REST API operation"""
        integration = self.integrations[tool_name]
        
        async with self.session.get(integration.api_base_url, params=parameters) as response:
            return await response.json()
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        
        status_summary = {
            "total_integrations": len(self.integrations),
            "connected": 0,
            "disconnected": 0,
            "error": 0,
            "integrations": {}
        }
        
        for tool_name, integration in self.integrations.items():
            status = integration.status.value
            
            if status == "connected":
                status_summary["connected"] += 1
            elif status == "disconnected":
                status_summary["disconnected"] += 1
            elif status == "error":
                status_summary["error"] += 1
            
            status_summary["integrations"][tool_name] = {
                "status": status,
                "category": integration.category.value
            }
        
        return status_summary

# Global universal tool integration
universal_tools = UniversalToolIntegration()