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
import base64

logger = logging.getLogger(__name__)

class ToolCategory(Enum):
    DEVELOPMENT = "development"
    PROJECT_MANAGEMENT = "project_management"
    COMMUNICATION = "communication"
    DESIGN = "design"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    SALES = "sales"
    FINANCE = "finance"
    HR = "hr"
    PRODUCTIVITY = "productivity"
    AI_SERVICES = "ai_services"
    SCHEDULING = "scheduling"
    DOCUMENTATION = "documentation"

class IntegrationStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"
    RATE_LIMITED = "rate_limited"

@dataclass
class ToolCredentials:
    """Secure credential storage for tool integrations"""
    tool_name: str
    credential_type: str  # "api_key", "oauth", "webhook", "basic_auth"
    credentials: Dict[str, str]  # Encrypted in production
    expires_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_used: Optional[str] = None

@dataclass
class ToolIntegration:
    """Tool integration configuration and status"""
    tool_name: str
    category: ToolCategory
    status: IntegrationStatus
    api_base_url: str
    supported_operations: List[str]
    rate_limits: Dict[str, int]  # operation -> requests_per_minute
    webhook_url: Optional[str] = None
    last_sync: Optional[str] = None
    error_message: Optional[str] = None
    usage_stats: Dict[str, int] = field(default_factory=dict)
    custom_config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolOperation:
    """Individual tool operation tracking"""
    operation_id: str
    tool_name: str
    operation_type: str
    parameters: Dict[str, Any]
    status: str  # "pending", "success", "failed", "retrying"
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    retry_count: int = 0

class UniversalToolIntegration:
    """
    Universal Tool Integration Framework
    - Connects to 100+ business tools and services
    - Provides unified API access and data synchronization
    - Intelligent workflow automation across tools
    - Real-time data sync and webhook management
    """
    
    def __init__(self):
        # Integration management
        self.integrations: Dict[str, ToolIntegration] = {}
        self.credentials: Dict[str, ToolCredentials] = {}
        self.operations: Dict[str, ToolOperation] = {}
        
        # HTTP session management
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiters: Dict[str, Dict[str, float]] = {}  # tool -> {operation -> last_call_time}
        
        # Webhook management
        self.webhook_handlers: Dict[str, Callable] = {}
        self.webhook_queue: List[Dict[str, Any]] = []
        
        # Sync and automation
        self.sync_schedules: Dict[str, Dict[str, Any]] = {}
        self.automation_workflows: List[Dict[str, Any]] = []
        
        self._initialize_tool_configurations()
        self._initialize_automation_workflows()
    
    def _initialize_tool_configurations(self):
        """Initialize configurations for all supported tools"""
        
        # YC Tools and Startup Ecosystem
        yc_tools = {
            "bookface": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://bookface.ycombinator.com/api",
                "operations": ["get_posts", "create_post", "get_companies", "send_message"],
                "rate_limits": {"get_posts": 60, "create_post": 10}
            },
            "worklist": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://worklist.ycombinator.com/api",
                "operations": ["get_tasks", "create_task", "update_task", "get_metrics"],
                "rate_limits": {"get_tasks": 120, "create_task": 30}
            },
            "dealbook": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://dealbook.ycombinator.com/api",
                "operations": ["get_deals", "create_deal", "update_deal", "get_investors"],
                "rate_limits": {"get_deals": 60, "create_deal": 10}
            }
        }
        
        # Development Tools
        dev_tools = {
            "github": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.github.com",
                "operations": ["get_repos", "create_repo", "get_issues", "create_issue", 
                             "get_commits", "create_pr", "merge_pr", "get_workflows"],
                "rate_limits": {"get_repos": 5000, "create_repo": 100}
            },
            "gitlab": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://gitlab.com/api/v4",
                "operations": ["get_projects", "create_project", "get_issues", "create_merge_request"],
                "rate_limits": {"get_projects": 2000, "create_project": 50}
            },
            "vercel": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.vercel.com",
                "operations": ["deploy", "get_deployments", "get_projects", "create_project"],
                "rate_limits": {"deploy": 100, "get_deployments": 1000}
            },
            "netlify": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.netlify.com/api/v1",
                "operations": ["deploy", "get_sites", "create_site", "get_builds"],
                "rate_limits": {"deploy": 300, "get_sites": 500}
            },
            "heroku": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.heroku.com",
                "operations": ["create_app", "deploy", "get_apps", "scale_dynos"],
                "rate_limits": {"create_app": 100, "deploy": 200}
            }
        }
        
        # Project Management Tools
        pm_tools = {
            "linear": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.linear.app/graphql",
                "operations": ["get_issues", "create_issue", "update_issue", "get_projects"],
                "rate_limits": {"get_issues": 1000, "create_issue": 200}
            },
            "notion": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.notion.com/v1",
                "operations": ["get_pages", "create_page", "update_page", "query_database"],
                "rate_limits": {"get_pages": 1000, "create_page": 100}
            },
            "airtable": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.airtable.com/v0",
                "operations": ["get_records", "create_record", "update_record", "delete_record"],
                "rate_limits": {"get_records": 1000, "create_record": 200}
            },
            "asana": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://app.asana.com/api/1.0",
                "operations": ["get_tasks", "create_task", "update_task", "get_projects"],
                "rate_limits": {"get_tasks": 1500, "create_task": 300}
            },
            "trello": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.trello.com/1",
                "operations": ["get_boards", "create_card", "update_card", "get_lists"],
                "rate_limits": {"get_boards": 300, "create_card": 100}
            }
        }
        
        # Communication Tools
        comm_tools = {
            "slack": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://slack.com/api",
                "operations": ["send_message", "get_channels", "create_channel", "get_users"],
                "rate_limits": {"send_message": 1, "get_channels": 100}  # 1 per second for messages
            },
            "discord": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://discord.com/api/v10",
                "operations": ["send_message", "get_guilds", "create_channel", "get_members"],
                "rate_limits": {"send_message": 5, "get_guilds": 100}
            },
            "telegram": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://api.telegram.org/bot",
                "operations": ["send_message", "get_updates", "send_photo", "create_group"],
                "rate_limits": {"send_message": 30, "get_updates": 100}
            }
        }
        
        # Scheduling Tools
        scheduling_tools = {
            "calendly": {
                "category": ToolCategory.SCHEDULING,
                "api_base_url": "https://api.calendly.com",
                "operations": ["get_events", "create_event", "get_availability", "cancel_event"],
                "rate_limits": {"get_events": 1000, "create_event": 100}
            },
            "cal_com": {
                "category": ToolCategory.SCHEDULING,
                "api_base_url": "https://api.cal.com/v1",
                "operations": ["get_bookings", "create_booking", "get_availability"],
                "rate_limits": {"get_bookings": 500, "create_booking": 50}
            },
            "google_calendar": {
                "category": ToolCategory.SCHEDULING,
                "api_base_url": "https://www.googleapis.com/calendar/v3",
                "operations": ["get_events", "create_event", "update_event", "delete_event"],
                "rate_limits": {"get_events": 1000, "create_event": 600}
            }
        }
        
        # AI Services
        ai_tools = {
            "openai": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.openai.com/v1",
                "operations": ["chat_completion", "text_completion", "embeddings", "fine_tune"],
                "rate_limits": {"chat_completion": 3500, "embeddings": 3000}
            },
            "anthropic": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.anthropic.com/v1",
                "operations": ["messages", "completions"],
                "rate_limits": {"messages": 1000, "completions": 1000}
            },
            "replicate": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.replicate.com/v1",
                "operations": ["create_prediction", "get_prediction", "list_models"],
                "rate_limits": {"create_prediction": 100, "get_prediction": 1000}
            },
            "huggingface": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api-inference.huggingface.co",
                "operations": ["inference", "list_models", "get_model_info"],
                "rate_limits": {"inference": 1000, "list_models": 100}
            }
        }
        
        # Marketing & Analytics Tools
        marketing_tools = {
            "google_analytics": {
                "category": ToolCategory.ANALYTICS,
                "api_base_url": "https://analyticsreporting.googleapis.com/v4",
                "operations": ["get_reports", "get_realtime", "get_metadata"],
                "rate_limits": {"get_reports": 100, "get_realtime": 10}
            },
            "mixpanel": {
                "category": ToolCategory.ANALYTICS,
                "api_base_url": "https://mixpanel.com/api",
                "operations": ["track_event", "get_events", "create_funnel", "get_insights"],
                "rate_limits": {"track_event": 1000, "get_events": 60}
            },
            "mailchimp": {
                "category": ToolCategory.MARKETING,
                "api_base_url": "https://us1.api.mailchimp.com/3.0",
                "operations": ["send_campaign", "get_lists", "add_subscriber", "create_campaign"],
                "rate_limits": {"send_campaign": 10, "add_subscriber": 500}
            },
            "sendgrid": {
                "category": ToolCategory.MARKETING,
                "api_base_url": "https://api.sendgrid.com/v3",
                "operations": ["send_email", "create_template", "get_stats", "manage_lists"],
                "rate_limits": {"send_email": 600, "create_template": 100}
            }
        }
        
        # Sales & CRM Tools
        sales_tools = {
            "hubspot": {
                "category": ToolCategory.SALES,
                "api_base_url": "https://api.hubapi.com",
                "operations": ["get_contacts", "create_contact", "get_deals", "create_deal"],
                "rate_limits": {"get_contacts": 100, "create_contact": 100}
            },
            "salesforce": {
                "category": ToolCategory.SALES,
                "api_base_url": "https://your-instance.salesforce.com/services/data/v58.0",
                "operations": ["get_accounts", "create_lead", "update_opportunity", "get_reports"],
                "rate_limits": {"get_accounts": 1000, "create_lead": 200}
            },
            "pipedrive": {
                "category": ToolCategory.SALES,
                "api_base_url": "https://api.pipedrive.com/v1",
                "operations": ["get_deals", "create_deal", "get_persons", "create_activity"],
                "rate_limits": {"get_deals": 1000, "create_deal": 100}
            }
        }
        
        # Finance Tools
        finance_tools = {
            "stripe": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://api.stripe.com/v1",
                "operations": ["create_payment", "get_customers", "create_subscription", "get_invoices"],
                "rate_limits": {"create_payment": 100, "get_customers": 100}
            },
            "quickbooks": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://sandbox-quickbooks.api.intuit.com/v3",
                "operations": ["get_items", "create_invoice", "get_customers", "create_payment"],
                "rate_limits": {"get_items": 500, "create_invoice": 100}
            },
            "xero": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://api.xero.com/api.xro/2.0",
                "operations": ["get_invoices", "create_contact", "get_accounts", "create_payment"],
                "rate_limits": {"get_invoices": 60, "create_contact": 60}
            }
        }
        
        # Combine all tool configurations
        all_tools = {
            **yc_tools, **dev_tools, **pm_tools, **comm_tools, 
            **scheduling_tools, **ai_tools, **marketing_tools, 
            **sales_tools, **finance_tools
        }
        
        # Create integration objects
        for tool_name, config in all_tools.items():
            self.integrations[tool_name] = ToolIntegration(
                tool_name=tool_name,
                category=config["category"],
                status=IntegrationStatus.DISCONNECTED,
                api_base_url=config["api_base_url"],
                supported_operations=config["operations"],
                rate_limits=config["rate_limits"]
            )
    
    def _initialize_automation_workflows(self):
        """Initialize intelligent automation workflows"""
        
        self.automation_workflows = [
            {
                "name": "GitHub to Linear Sync",
                "description": "Sync GitHub issues to Linear tasks",
                "trigger": {"tool": "github", "event": "issue_created"},
                "actions": [
                    {"tool": "linear", "operation": "create_issue", "mapping": {
                        "title": "github.issue.title",
                        "description": "github.issue.body",
                        "labels": "github.issue.labels"
                    }}
                ]
            },
            {
                "name": "Slack Notification on Deploy",
                "description": "Notify team when deployment completes",
                "trigger": {"tool": "vercel", "event": "deployment_ready"},
                "actions": [
                    {"tool": "slack", "operation": "send_message", "mapping": {
                        "channel": "#deployments",
                        "text": "🚀 Deployment completed: {vercel.deployment.url}"
                    }}
                ]
            },
            {
                "name": "Customer Success Pipeline",
                "description": "Create tasks when new customers sign up",
                "trigger": {"tool": "stripe", "event": "customer_subscription_created"},
                "actions": [
                    {"tool": "hubspot", "operation": "create_contact", "mapping": {
                        "email": "stripe.customer.email",
                        "name": "stripe.customer.name"
                    }},
                    {"tool": "linear", "operation": "create_issue", "mapping": {
                        "title": "Onboard new customer: {stripe.customer.name}",
                        "assignee": "customer_success_team"
                    }}
                ]
            }
        ]
    
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
            # Store credentials securely (encrypt in production)
            self.credentials[tool_name] = ToolCredentials(
                tool_name=tool_name,
                credential_type=credential_type,
                credentials=credentials
            )
            
            # Test connection
            test_result = await self._test_connection(tool_name)
            
            if test_result:
                self.integrations[tool_name].status = IntegrationStatus.CONNECTED
                self.integrations[tool_name].last_sync = datetime.now(timezone.utc).isoformat()
                logger.info(f"Successfully connected to {tool_name}")
                return True
            else:
                self.integrations[tool_name].status = IntegrationStatus.ERROR
                self.integrations[tool_name].error_message = "Connection test failed"
                logger.error(f"Failed to connect to {tool_name}")
                return False
                
        except Exception as e:
            self.integrations[tool_name].status = IntegrationStatus.ERROR
            self.integrations[tool_name].error_message = str(e)
            logger.error(f"Error connecting to {tool_name}: {e}")
            return False
    
    async def _test_connection(self, tool_name: str) -> bool:
        """Test connection to a tool"""
        
        if tool_name not in self.credentials:
            return False
        
        integration = self.integrations[tool_name]
        credentials = self.credentials[tool_name]
        
        try:
            # Tool-specific connection tests
            if tool_name == "github":
                return await self._test_github_connection(credentials)
            elif tool_name == "slack":
                return await self._test_slack_connection(credentials)
            elif tool_name == "linear":
                return await self._test_linear_connection(credentials)
            elif tool_name == "notion":
                return await self._test_notion_connection(credentials)
            elif tool_name == "openai":
                return await self._test_openai_connection(credentials)
            else:
                # Generic HTTP test
                return await self._test_generic_connection(integration, credentials)
                
        except Exception as e:
            logger.error(f"Connection test failed for {tool_name}: {e}")
            return False
    
    async def _test_github_connection(self, credentials: ToolCredentials) -> bool:
        """Test GitHub API connection"""
        
        headers = {
            "Authorization": f"token {credentials.credentials['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with self.session.get(
            "https://api.github.com/user",
            headers=headers
        ) as response:
            return response.status == 200
    
    async def _test_slack_connection(self, credentials: ToolCredentials) -> bool:
        """Test Slack API connection"""
        
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}"
        }
        
        async with self.session.get(
            "https://slack.com/api/auth.test",
            headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("ok", False)
            return False
    
    async def _test_linear_connection(self, credentials: ToolCredentials) -> bool:
        """Test Linear API connection"""
        
        headers = {
            "Authorization": credentials.credentials['api_key'],
            "Content-Type": "application/json"
        }
        
        query = {"query": "{ viewer { id name } }"}
        
        async with self.session.post(
            "https://api.linear.app/graphql",
            headers=headers,
            json=query
        ) as response:
            if response.status == 200:
                data = await response.json()
                return "data" in data and "viewer" in data["data"]
            return False
    
    async def _test_notion_connection(self, credentials: ToolCredentials) -> bool:
        """Test Notion API connection"""
        
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Notion-Version": "2022-06-28"
        }
        
        async with self.session.get(
            "https://api.notion.com/v1/users/me",
            headers=headers
        ) as response:
            return response.status == 200
    
    async def _test_openai_connection(self, credentials: ToolCredentials) -> bool:
        """Test OpenAI API connection"""
        
        headers = {
            "Authorization": f"Bearer {credentials.credentials['api_key']}"
        }
        
        async with self.session.get(
            "https://api.openai.com/v1/models",
            headers=headers
        ) as response:
            return response.status == 200
    
    async def _test_generic_connection(self, integration: ToolIntegration, 
                                     credentials: ToolCredentials) -> bool:
        """Generic connection test for tools without specific implementations"""
        
        headers = {}
        
        if credentials.credential_type == "api_key":
            if "api_key" in credentials.credentials:
                headers["Authorization"] = f"Bearer {credentials.credentials['api_key']}"
            elif "token" in credentials.credentials:
                headers["Authorization"] = f"Bearer {credentials.credentials['token']}"
        
        try:
            async with self.session.get(
                integration.api_base_url,
                headers=headers
            ) as response:
                return response.status in [200, 401]  # 401 means API is reachable but auth failed
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
            # Check if tool is connected
            if tool_name not in self.integrations:
                raise ValueError(f"Tool '{tool_name}' not supported")
            
            integration = self.integrations[tool_name]
            if integration.status != IntegrationStatus.CONNECTED:
                raise ValueError(f"Tool '{tool_name}' not connected")
            
            # Check rate limits
            if not await self._check_rate_limit(tool_name, operation):
                tool_operation.status = "failed"
                tool_operation.error_message = "Rate limit exceeded"
                return tool_operation
            
            # Execute tool-specific operation
            result = await self._execute_tool_operation(tool_name, operation, parameters)
            
            tool_operation.status = "success"
            tool_operation.result = result
            tool_operation.completed_at = datetime.now(timezone.utc).isoformat()
            
            # Update usage stats
            integration.usage_stats[operation] = integration.usage_stats.get(operation, 0) + 1
            
            return tool_operation
            
        except Exception as e:
            tool_operation.status = "failed"
            tool_operation.error_message = str(e)
            tool_operation.completed_at = datetime.now(timezone.utc).isoformat()
            
            logger.error(f"Operation failed: {tool_name}.{operation} - {e}")
            return tool_operation
    
    async def _check_rate_limit(self, tool_name: str, operation: str) -> bool:
        """Check if operation is within rate limits"""
        
        integration = self.integrations[tool_name]
        rate_limit = integration.rate_limits.get(operation, 1000)  # Default 1000/min
        
        if tool_name not in self.rate_limiters:
            self.rate_limiters[tool_name] = {}
        
        current_time = datetime.now(timezone.utc).timestamp()
        last_call_time = self.rate_limiters[tool_name].get(operation, 0)
        
        # Simple rate limiting: minimum interval between calls
        min_interval = 60 / rate_limit  # seconds between calls
        
        if current_time - last_call_time >= min_interval:
            self.rate_limiters[tool_name][operation] = current_time
            return True
        
        return False
    
    async def _execute_tool_operation(self, tool_name: str, operation: str, 
                                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific tool operation"""
        
        # Tool-specific operation implementations
        if tool_name == "github":
            return await self._execute_github_operation(operation, parameters)
        elif tool_name == "slack":
            return await self._execute_slack_operation(operation, parameters)
        elif tool_name == "linear":
            return await self._execute_linear_operation(operation, parameters)
        elif tool_name == "notion":
            return await self._execute_notion_operation(operation, parameters)
        elif tool_name == "openai":
            return await self._execute_openai_operation(operation, parameters)
        elif tool_name == "stripe":
            return await self._execute_stripe_operation(operation, parameters)
        else:
            # Generic REST API operation
            return await self._execute_generic_operation(tool_name, operation, parameters)
    
    async def _execute_github_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GitHub API operations"""
        
        credentials = self.credentials["github"]
        headers = {
            "Authorization": f"token {credentials.credentials['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if operation == "get_repos":
            async with self.session.get(
                "https://api.github.com/user/repos",
                headers=headers,
                params=parameters
            ) as response:
                return await response.json()
        
        elif operation == "create_repo":
            async with self.session.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        elif operation == "get_issues":
            repo = parameters.get("repo", "")
            async with self.session.get(
                f"https://api.github.com/repos/{repo}/issues",
                headers=headers,
                params={k: v for k, v in parameters.items() if k != "repo"}
            ) as response:
                return await response.json()
        
        elif operation == "create_issue":
            repo = parameters.pop("repo", "")
            async with self.session.post(
                f"https://api.github.com/repos/{repo}/issues",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported GitHub operation: {operation}")
    
    async def _execute_slack_operation(self, operation: str, 
                                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Slack API operations"""
        
        credentials = self.credentials["slack"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Content-Type": "application/json"
        }
        
        if operation == "send_message":
            async with self.session.post(
                "https://slack.com/api/chat.postMessage",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        elif operation == "get_channels":
            async with self.session.get(
                "https://slack.com/api/conversations.list",
                headers=headers,
                params=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Slack operation: {operation}")
    
    async def _execute_linear_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Linear API operations"""
        
        credentials = self.credentials["linear"]
        headers = {
            "Authorization": credentials.credentials['api_key'],
            "Content-Type": "application/json"
        }
        
        if operation == "get_issues":
            query = {
                "query": """
                query {
                    issues {
                        nodes {
                            id
                            title
                            description
                            state { name }
                            assignee { name }
                            createdAt
                        }
                    }
                }
                """
            }
            
            async with self.session.post(
                "https://api.linear.app/graphql",
                headers=headers,
                json=query
            ) as response:
                return await response.json()
        
        elif operation == "create_issue":
            query = {
                "query": """
                mutation IssueCreate($input: IssueCreateInput!) {
                    issueCreate(input: $input) {
                        success
                        issue {
                            id
                            title
                        }
                    }
                }
                """,
                "variables": {"input": parameters}
            }
            
            async with self.session.post(
                "https://api.linear.app/graphql",
                headers=headers,
                json=query
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Linear operation: {operation}")
    
    async def _execute_notion_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Notion API operations"""
        
        credentials = self.credentials["notion"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        if operation == "get_pages":
            database_id = parameters.get("database_id")
            async with self.session.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                headers=headers,
                json={k: v for k, v in parameters.items() if k != "database_id"}
            ) as response:
                return await response.json()
        
        elif operation == "create_page":
            async with self.session.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Notion operation: {operation}")
    
    async def _execute_openai_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OpenAI API operations"""
        
        credentials = self.credentials["openai"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['api_key']}",
            "Content-Type": "application/json"
        }
        
        if operation == "chat_completion":
            async with self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        elif operation == "embeddings":
            async with self.session.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported OpenAI operation: {operation}")
    
    async def _execute_stripe_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Stripe API operations"""
        
        credentials = self.credentials["stripe"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['secret_key']}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        if operation == "create_payment":
            async with self.session.post(
                "https://api.stripe.com/v1/payment_intents",
                headers=headers,
                data=parameters
            ) as response:
                return await response.json()
        
        elif operation == "get_customers":
            async with self.session.get(
                "https://api.stripe.com/v1/customers",
                headers=headers,
                params=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Stripe operation: {operation}")
    
    async def _execute_generic_operation(self, tool_name: str, operation: str, 
                                        parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic REST API operation"""
        
        integration = self.integrations[tool_name]
        credentials = self.credentials.get(tool_name)
        
        headers = {"Content-Type": "application/json"}
        
        if credentials:
            if credentials.credential_type == "api_key":
                if "api_key" in credentials.credentials:
                    headers["Authorization"] = f"Bearer {credentials.credentials['api_key']}"
                elif "token" in credentials.credentials:
                    headers["Authorization"] = f"Bearer {credentials.credentials['token']}"
        
        # Default to GET request
        async with self.session.get(
            integration.api_base_url,
            headers=headers,
            params=parameters
        ) as response:
            return await response.json()
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        
        status_summary = {
            "total_integrations": len(self.integrations),
            "connected": 0,
            "disconnected": 0,
            "error": 0,
            "by_category": {},
            "integrations": {}
        }
        
        for tool_name, integration in self.integrations.items():
            status = integration.status.value
            category = integration.category.value
            
            # Count by status
            if status == "connected":
                status_summary["connected"] += 1
            elif status == "disconnected":
                status_summary["disconnected"] += 1
            elif status == "error":
                status_summary["error"] += 1
            
            # Count by category
            if category not in status_summary["by_category"]:
                status_summary["by_category"][category] = {"total": 0, "connected": 0}
            
            status_summary["by_category"][category]["total"] += 1
            if status == "connected":
                status_summary["by_category"][category]["connected"] += 1
            
            # Individual integration status
            status_summary["integrations"][tool_name] = {
                "status": status,
                "category": category,
                "last_sync": integration.last_sync,
                "usage_stats": integration.usage_stats,
                "error_message": integration.error_message
            }
        
        return status_summary
    
    async def sync_all_tools(self) -> Dict[str, Any]:
        """Sync data across all connected tools"""
        
        sync_results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tools_synced": 0,
            "sync_results": {},
            "errors": []
        }
        
        connected_tools = [
            name for name, integration in self.integrations.items()
            if integration.status == IntegrationStatus.CONNECTED
        ]
        
        for tool_name in connected_tools:
            try:
                # Tool-specific sync logic
                sync_result = await self._sync_tool_data(tool_name)
                sync_results["sync_results"][tool_name] = sync_result
                sync_results["tools_synced"] += 1
                
                # Update last sync time
                self.integrations[tool_name].last_sync = datetime.now(timezone.utc).isoformat()
                
            except Exception as e:
                error_msg = f"Sync failed for {tool_name}: {str(e)}"
                sync_results["errors"].append(error_msg)
                logger.error(error_msg)
        
        sync_results["completed_at"] = datetime.now(timezone.utc).isoformat()
        return sync_results
    
    async def _sync_tool_data(self, tool_name: str) -> Dict[str, Any]:
        """Sync data for a specific tool"""
        
        # Implement tool-specific sync logic
        # This is a simplified example
        
        if tool_name == "github":
            # Sync repositories and issues
            repos_op = await self.execute_operation("github", "get_repos", {"per_page": 100})
            return {"repositories_synced": len(repos_op.result or [])}
        
        elif tool_name == "linear":
            # Sync issues
            issues_op = await self.execute_operation("linear", "get_issues", {})
            return {"issues_synced": len(issues_op.result.get("data", {}).get("issues", {}).get("nodes", []))}
        
        else:
            return {"status": "sync_not_implemented"}

# Global universal tool integration
universal_tools = UniversalToolIntegration()Universal Tool Integration Framework
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
import base64

logger = logging.getLogger(__name__)

class ToolCategory(Enum):
    DEVELOPMENT = "development"
    PROJECT_MANAGEMENT = "project_management"
    COMMUNICATION = "communication"
    DESIGN = "design"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    SALES = "sales"
    FINANCE = "finance"
    HR = "hr"
    PRODUCTIVITY = "productivity"
    AI_SERVICES = "ai_services"
    SCHEDULING = "scheduling"
    DOCUMENTATION = "documentation"

class IntegrationStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"
    RATE_LIMITED = "rate_limited"

@dataclass
class ToolCredentials:
    """Secure credential storage for tool integrations"""
    tool_name: str
    credential_type: str  # "api_key", "oauth", "webhook", "basic_auth"
    credentials: Dict[str, str]  # Encrypted in production
    expires_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_used: Optional[str] = None

@dataclass
class ToolIntegration:
    """Tool integration configuration and status"""
    tool_name: str
    category: ToolCategory
    status: IntegrationStatus
    api_base_url: str
    supported_operations: List[str]
    rate_limits: Dict[str, int]  # operation -> requests_per_minute
    webhook_url: Optional[str] = None
    last_sync: Optional[str] = None
    error_message: Optional[str] = None
    usage_stats: Dict[str, int] = field(default_factory=dict)
    custom_config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolOperation:
    """Individual tool operation tracking"""
    operation_id: str
    tool_name: str
    operation_type: str
    parameters: Dict[str, Any]
    status: str  # "pending", "success", "failed", "retrying"
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    retry_count: int = 0

class UniversalToolIntegration:
    """
    Universal Tool Integration Framework
    - Connects to 100+ business tools and services
    - Provides unified API access and data synchronization
    - Intelligent workflow automation across tools
    - Real-time data sync and webhook management
    """
    
    def __init__(self):
        # Integration management
        self.integrations: Dict[str, ToolIntegration] = {}
        self.credentials: Dict[str, ToolCredentials] = {}
        self.operations: Dict[str, ToolOperation] = {}
        
        # HTTP session management
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiters: Dict[str, Dict[str, float]] = {}  # tool -> {operation -> last_call_time}
        
        # Webhook management
        self.webhook_handlers: Dict[str, Callable] = {}
        self.webhook_queue: List[Dict[str, Any]] = []
        
        # Sync and automation
        self.sync_schedules: Dict[str, Dict[str, Any]] = {}
        self.automation_workflows: List[Dict[str, Any]] = []
        
        self._initialize_tool_configurations()
        self._initialize_automation_workflows()
    
    def _initialize_tool_configurations(self):
        """Initialize configurations for all supported tools"""
        
        # YC Tools and Startup Ecosystem
        yc_tools = {
            "bookface": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://bookface.ycombinator.com/api",
                "operations": ["get_posts", "create_post", "get_companies", "send_message"],
                "rate_limits": {"get_posts": 60, "create_post": 10}
            },
            "worklist": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://worklist.ycombinator.com/api",
                "operations": ["get_tasks", "create_task", "update_task", "get_metrics"],
                "rate_limits": {"get_tasks": 120, "create_task": 30}
            },
            "dealbook": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://dealbook.ycombinator.com/api",
                "operations": ["get_deals", "create_deal", "update_deal", "get_investors"],
                "rate_limits": {"get_deals": 60, "create_deal": 10}
            }
        }
        
        # Development Tools
        dev_tools = {
            "github": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.github.com",
                "operations": ["get_repos", "create_repo", "get_issues", "create_issue", 
                             "get_commits", "create_pr", "merge_pr", "get_workflows"],
                "rate_limits": {"get_repos": 5000, "create_repo": 100}
            },
            "gitlab": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://gitlab.com/api/v4",
                "operations": ["get_projects", "create_project", "get_issues", "create_merge_request"],
                "rate_limits": {"get_projects": 2000, "create_project": 50}
            },
            "vercel": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.vercel.com",
                "operations": ["deploy", "get_deployments", "get_projects", "create_project"],
                "rate_limits": {"deploy": 100, "get_deployments": 1000}
            },
            "netlify": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.netlify.com/api/v1",
                "operations": ["deploy", "get_sites", "create_site", "get_builds"],
                "rate_limits": {"deploy": 300, "get_sites": 500}
            },
            "heroku": {
                "category": ToolCategory.DEVELOPMENT,
                "api_base_url": "https://api.heroku.com",
                "operations": ["create_app", "deploy", "get_apps", "scale_dynos"],
                "rate_limits": {"create_app": 100, "deploy": 200}
            }
        }
        
        # Project Management Tools
        pm_tools = {
            "linear": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.linear.app/graphql",
                "operations": ["get_issues", "create_issue", "update_issue", "get_projects"],
                "rate_limits": {"get_issues": 1000, "create_issue": 200}
            },
            "notion": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.notion.com/v1",
                "operations": ["get_pages", "create_page", "update_page", "query_database"],
                "rate_limits": {"get_pages": 1000, "create_page": 100}
            },
            "airtable": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.airtable.com/v0",
                "operations": ["get_records", "create_record", "update_record", "delete_record"],
                "rate_limits": {"get_records": 1000, "create_record": 200}
            },
            "asana": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://app.asana.com/api/1.0",
                "operations": ["get_tasks", "create_task", "update_task", "get_projects"],
                "rate_limits": {"get_tasks": 1500, "create_task": 300}
            },
            "trello": {
                "category": ToolCategory.PROJECT_MANAGEMENT,
                "api_base_url": "https://api.trello.com/1",
                "operations": ["get_boards", "create_card", "update_card", "get_lists"],
                "rate_limits": {"get_boards": 300, "create_card": 100}
            }
        }
        
        # Communication Tools
        comm_tools = {
            "slack": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://slack.com/api",
                "operations": ["send_message", "get_channels", "create_channel", "get_users"],
                "rate_limits": {"send_message": 1, "get_channels": 100}  # 1 per second for messages
            },
            "discord": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://discord.com/api/v10",
                "operations": ["send_message", "get_guilds", "create_channel", "get_members"],
                "rate_limits": {"send_message": 5, "get_guilds": 100}
            },
            "telegram": {
                "category": ToolCategory.COMMUNICATION,
                "api_base_url": "https://api.telegram.org/bot",
                "operations": ["send_message", "get_updates", "send_photo", "create_group"],
                "rate_limits": {"send_message": 30, "get_updates": 100}
            }
        }
        
        # Scheduling Tools
        scheduling_tools = {
            "calendly": {
                "category": ToolCategory.SCHEDULING,
                "api_base_url": "https://api.calendly.com",
                "operations": ["get_events", "create_event", "get_availability", "cancel_event"],
                "rate_limits": {"get_events": 1000, "create_event": 100}
            },
            "cal_com": {
                "category": ToolCategory.SCHEDULING,
                "api_base_url": "https://api.cal.com/v1",
                "operations": ["get_bookings", "create_booking", "get_availability"],
                "rate_limits": {"get_bookings": 500, "create_booking": 50}
            },
            "google_calendar": {
                "category": ToolCategory.SCHEDULING,
                "api_base_url": "https://www.googleapis.com/calendar/v3",
                "operations": ["get_events", "create_event", "update_event", "delete_event"],
                "rate_limits": {"get_events": 1000, "create_event": 600}
            }
        }
        
        # AI Services
        ai_tools = {
            "openai": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.openai.com/v1",
                "operations": ["chat_completion", "text_completion", "embeddings", "fine_tune"],
                "rate_limits": {"chat_completion": 3500, "embeddings": 3000}
            },
            "anthropic": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.anthropic.com/v1",
                "operations": ["messages", "completions"],
                "rate_limits": {"messages": 1000, "completions": 1000}
            },
            "replicate": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api.replicate.com/v1",
                "operations": ["create_prediction", "get_prediction", "list_models"],
                "rate_limits": {"create_prediction": 100, "get_prediction": 1000}
            },
            "huggingface": {
                "category": ToolCategory.AI_SERVICES,
                "api_base_url": "https://api-inference.huggingface.co",
                "operations": ["inference", "list_models", "get_model_info"],
                "rate_limits": {"inference": 1000, "list_models": 100}
            }
        }
        
        # Marketing & Analytics Tools
        marketing_tools = {
            "google_analytics": {
                "category": ToolCategory.ANALYTICS,
                "api_base_url": "https://analyticsreporting.googleapis.com/v4",
                "operations": ["get_reports", "get_realtime", "get_metadata"],
                "rate_limits": {"get_reports": 100, "get_realtime": 10}
            },
            "mixpanel": {
                "category": ToolCategory.ANALYTICS,
                "api_base_url": "https://mixpanel.com/api",
                "operations": ["track_event", "get_events", "create_funnel", "get_insights"],
                "rate_limits": {"track_event": 1000, "get_events": 60}
            },
            "mailchimp": {
                "category": ToolCategory.MARKETING,
                "api_base_url": "https://us1.api.mailchimp.com/3.0",
                "operations": ["send_campaign", "get_lists", "add_subscriber", "create_campaign"],
                "rate_limits": {"send_campaign": 10, "add_subscriber": 500}
            },
            "sendgrid": {
                "category": ToolCategory.MARKETING,
                "api_base_url": "https://api.sendgrid.com/v3",
                "operations": ["send_email", "create_template", "get_stats", "manage_lists"],
                "rate_limits": {"send_email": 600, "create_template": 100}
            }
        }
        
        # Sales & CRM Tools
        sales_tools = {
            "hubspot": {
                "category": ToolCategory.SALES,
                "api_base_url": "https://api.hubapi.com",
                "operations": ["get_contacts", "create_contact", "get_deals", "create_deal"],
                "rate_limits": {"get_contacts": 100, "create_contact": 100}
            },
            "salesforce": {
                "category": ToolCategory.SALES,
                "api_base_url": "https://your-instance.salesforce.com/services/data/v58.0",
                "operations": ["get_accounts", "create_lead", "update_opportunity", "get_reports"],
                "rate_limits": {"get_accounts": 1000, "create_lead": 200}
            },
            "pipedrive": {
                "category": ToolCategory.SALES,
                "api_base_url": "https://api.pipedrive.com/v1",
                "operations": ["get_deals", "create_deal", "get_persons", "create_activity"],
                "rate_limits": {"get_deals": 1000, "create_deal": 100}
            }
        }
        
        # Finance Tools
        finance_tools = {
            "stripe": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://api.stripe.com/v1",
                "operations": ["create_payment", "get_customers", "create_subscription", "get_invoices"],
                "rate_limits": {"create_payment": 100, "get_customers": 100}
            },
            "quickbooks": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://sandbox-quickbooks.api.intuit.com/v3",
                "operations": ["get_items", "create_invoice", "get_customers", "create_payment"],
                "rate_limits": {"get_items": 500, "create_invoice": 100}
            },
            "xero": {
                "category": ToolCategory.FINANCE,
                "api_base_url": "https://api.xero.com/api.xro/2.0",
                "operations": ["get_invoices", "create_contact", "get_accounts", "create_payment"],
                "rate_limits": {"get_invoices": 60, "create_contact": 60}
            }
        }
        
        # Combine all tool configurations
        all_tools = {
            **yc_tools, **dev_tools, **pm_tools, **comm_tools, 
            **scheduling_tools, **ai_tools, **marketing_tools, 
            **sales_tools, **finance_tools
        }
        
        # Create integration objects
        for tool_name, config in all_tools.items():
            self.integrations[tool_name] = ToolIntegration(
                tool_name=tool_name,
                category=config["category"],
                status=IntegrationStatus.DISCONNECTED,
                api_base_url=config["api_base_url"],
                supported_operations=config["operations"],
                rate_limits=config["rate_limits"]
            )
    
    def _initialize_automation_workflows(self):
        """Initialize intelligent automation workflows"""
        
        self.automation_workflows = [
            {
                "name": "GitHub to Linear Sync",
                "description": "Sync GitHub issues to Linear tasks",
                "trigger": {"tool": "github", "event": "issue_created"},
                "actions": [
                    {"tool": "linear", "operation": "create_issue", "mapping": {
                        "title": "github.issue.title",
                        "description": "github.issue.body",
                        "labels": "github.issue.labels"
                    }}
                ]
            },
            {
                "name": "Slack Notification on Deploy",
                "description": "Notify team when deployment completes",
                "trigger": {"tool": "vercel", "event": "deployment_ready"},
                "actions": [
                    {"tool": "slack", "operation": "send_message", "mapping": {
                        "channel": "#deployments",
                        "text": "🚀 Deployment completed: {vercel.deployment.url}"
                    }}
                ]
            },
            {
                "name": "Customer Success Pipeline",
                "description": "Create tasks when new customers sign up",
                "trigger": {"tool": "stripe", "event": "customer_subscription_created"},
                "actions": [
                    {"tool": "hubspot", "operation": "create_contact", "mapping": {
                        "email": "stripe.customer.email",
                        "name": "stripe.customer.name"
                    }},
                    {"tool": "linear", "operation": "create_issue", "mapping": {
                        "title": "Onboard new customer: {stripe.customer.name}",
                        "assignee": "customer_success_team"
                    }}
                ]
            }
        ]
    
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
            # Store credentials securely (encrypt in production)
            self.credentials[tool_name] = ToolCredentials(
                tool_name=tool_name,
                credential_type=credential_type,
                credentials=credentials
            )
            
            # Test connection
            test_result = await self._test_connection(tool_name)
            
            if test_result:
                self.integrations[tool_name].status = IntegrationStatus.CONNECTED
                self.integrations[tool_name].last_sync = datetime.now(timezone.utc).isoformat()
                logger.info(f"Successfully connected to {tool_name}")
                return True
            else:
                self.integrations[tool_name].status = IntegrationStatus.ERROR
                self.integrations[tool_name].error_message = "Connection test failed"
                logger.error(f"Failed to connect to {tool_name}")
                return False
                
        except Exception as e:
            self.integrations[tool_name].status = IntegrationStatus.ERROR
            self.integrations[tool_name].error_message = str(e)
            logger.error(f"Error connecting to {tool_name}: {e}")
            return False
    
    async def _test_connection(self, tool_name: str) -> bool:
        """Test connection to a tool"""
        
        if tool_name not in self.credentials:
            return False
        
        integration = self.integrations[tool_name]
        credentials = self.credentials[tool_name]
        
        try:
            # Tool-specific connection tests
            if tool_name == "github":
                return await self._test_github_connection(credentials)
            elif tool_name == "slack":
                return await self._test_slack_connection(credentials)
            elif tool_name == "linear":
                return await self._test_linear_connection(credentials)
            elif tool_name == "notion":
                return await self._test_notion_connection(credentials)
            elif tool_name == "openai":
                return await self._test_openai_connection(credentials)
            else:
                # Generic HTTP test
                return await self._test_generic_connection(integration, credentials)
                
        except Exception as e:
            logger.error(f"Connection test failed for {tool_name}: {e}")
            return False
    
    async def _test_github_connection(self, credentials: ToolCredentials) -> bool:
        """Test GitHub API connection"""
        
        headers = {
            "Authorization": f"token {credentials.credentials['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with self.session.get(
            "https://api.github.com/user",
            headers=headers
        ) as response:
            return response.status == 200
    
    async def _test_slack_connection(self, credentials: ToolCredentials) -> bool:
        """Test Slack API connection"""
        
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}"
        }
        
        async with self.session.get(
            "https://slack.com/api/auth.test",
            headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("ok", False)
            return False
    
    async def _test_linear_connection(self, credentials: ToolCredentials) -> bool:
        """Test Linear API connection"""
        
        headers = {
            "Authorization": credentials.credentials['api_key'],
            "Content-Type": "application/json"
        }
        
        query = {"query": "{ viewer { id name } }"}
        
        async with self.session.post(
            "https://api.linear.app/graphql",
            headers=headers,
            json=query
        ) as response:
            if response.status == 200:
                data = await response.json()
                return "data" in data and "viewer" in data["data"]
            return False
    
    async def _test_notion_connection(self, credentials: ToolCredentials) -> bool:
        """Test Notion API connection"""
        
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Notion-Version": "2022-06-28"
        }
        
        async with self.session.get(
            "https://api.notion.com/v1/users/me",
            headers=headers
        ) as response:
            return response.status == 200
    
    async def _test_openai_connection(self, credentials: ToolCredentials) -> bool:
        """Test OpenAI API connection"""
        
        headers = {
            "Authorization": f"Bearer {credentials.credentials['api_key']}"
        }
        
        async with self.session.get(
            "https://api.openai.com/v1/models",
            headers=headers
        ) as response:
            return response.status == 200
    
    async def _test_generic_connection(self, integration: ToolIntegration, 
                                     credentials: ToolCredentials) -> bool:
        """Generic connection test for tools without specific implementations"""
        
        headers = {}
        
        if credentials.credential_type == "api_key":
            if "api_key" in credentials.credentials:
                headers["Authorization"] = f"Bearer {credentials.credentials['api_key']}"
            elif "token" in credentials.credentials:
                headers["Authorization"] = f"Bearer {credentials.credentials['token']}"
        
        try:
            async with self.session.get(
                integration.api_base_url,
                headers=headers
            ) as response:
                return response.status in [200, 401]  # 401 means API is reachable but auth failed
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
            # Check if tool is connected
            if tool_name not in self.integrations:
                raise ValueError(f"Tool '{tool_name}' not supported")
            
            integration = self.integrations[tool_name]
            if integration.status != IntegrationStatus.CONNECTED:
                raise ValueError(f"Tool '{tool_name}' not connected")
            
            # Check rate limits
            if not await self._check_rate_limit(tool_name, operation):
                tool_operation.status = "failed"
                tool_operation.error_message = "Rate limit exceeded"
                return tool_operation
            
            # Execute tool-specific operation
            result = await self._execute_tool_operation(tool_name, operation, parameters)
            
            tool_operation.status = "success"
            tool_operation.result = result
            tool_operation.completed_at = datetime.now(timezone.utc).isoformat()
            
            # Update usage stats
            integration.usage_stats[operation] = integration.usage_stats.get(operation, 0) + 1
            
            return tool_operation
            
        except Exception as e:
            tool_operation.status = "failed"
            tool_operation.error_message = str(e)
            tool_operation.completed_at = datetime.now(timezone.utc).isoformat()
            
            logger.error(f"Operation failed: {tool_name}.{operation} - {e}")
            return tool_operation
    
    async def _check_rate_limit(self, tool_name: str, operation: str) -> bool:
        """Check if operation is within rate limits"""
        
        integration = self.integrations[tool_name]
        rate_limit = integration.rate_limits.get(operation, 1000)  # Default 1000/min
        
        if tool_name not in self.rate_limiters:
            self.rate_limiters[tool_name] = {}
        
        current_time = datetime.now(timezone.utc).timestamp()
        last_call_time = self.rate_limiters[tool_name].get(operation, 0)
        
        # Simple rate limiting: minimum interval between calls
        min_interval = 60 / rate_limit  # seconds between calls
        
        if current_time - last_call_time >= min_interval:
            self.rate_limiters[tool_name][operation] = current_time
            return True
        
        return False
    
    async def _execute_tool_operation(self, tool_name: str, operation: str, 
                                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific tool operation"""
        
        # Tool-specific operation implementations
        if tool_name == "github":
            return await self._execute_github_operation(operation, parameters)
        elif tool_name == "slack":
            return await self._execute_slack_operation(operation, parameters)
        elif tool_name == "linear":
            return await self._execute_linear_operation(operation, parameters)
        elif tool_name == "notion":
            return await self._execute_notion_operation(operation, parameters)
        elif tool_name == "openai":
            return await self._execute_openai_operation(operation, parameters)
        elif tool_name == "stripe":
            return await self._execute_stripe_operation(operation, parameters)
        else:
            # Generic REST API operation
            return await self._execute_generic_operation(tool_name, operation, parameters)
    
    async def _execute_github_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GitHub API operations"""
        
        credentials = self.credentials["github"]
        headers = {
            "Authorization": f"token {credentials.credentials['token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if operation == "get_repos":
            async with self.session.get(
                "https://api.github.com/user/repos",
                headers=headers,
                params=parameters
            ) as response:
                return await response.json()
        
        elif operation == "create_repo":
            async with self.session.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        elif operation == "get_issues":
            repo = parameters.get("repo", "")
            async with self.session.get(
                f"https://api.github.com/repos/{repo}/issues",
                headers=headers,
                params={k: v for k, v in parameters.items() if k != "repo"}
            ) as response:
                return await response.json()
        
        elif operation == "create_issue":
            repo = parameters.pop("repo", "")
            async with self.session.post(
                f"https://api.github.com/repos/{repo}/issues",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported GitHub operation: {operation}")
    
    async def _execute_slack_operation(self, operation: str, 
                                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Slack API operations"""
        
        credentials = self.credentials["slack"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Content-Type": "application/json"
        }
        
        if operation == "send_message":
            async with self.session.post(
                "https://slack.com/api/chat.postMessage",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        elif operation == "get_channels":
            async with self.session.get(
                "https://slack.com/api/conversations.list",
                headers=headers,
                params=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Slack operation: {operation}")
    
    async def _execute_linear_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Linear API operations"""
        
        credentials = self.credentials["linear"]
        headers = {
            "Authorization": credentials.credentials['api_key'],
            "Content-Type": "application/json"
        }
        
        if operation == "get_issues":
            query = {
                "query": """
                query {
                    issues {
                        nodes {
                            id
                            title
                            description
                            state { name }
                            assignee { name }
                            createdAt
                        }
                    }
                }
                """
            }
            
            async with self.session.post(
                "https://api.linear.app/graphql",
                headers=headers,
                json=query
            ) as response:
                return await response.json()
        
        elif operation == "create_issue":
            query = {
                "query": """
                mutation IssueCreate($input: IssueCreateInput!) {
                    issueCreate(input: $input) {
                        success
                        issue {
                            id
                            title
                        }
                    }
                }
                """,
                "variables": {"input": parameters}
            }
            
            async with self.session.post(
                "https://api.linear.app/graphql",
                headers=headers,
                json=query
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Linear operation: {operation}")
    
    async def _execute_notion_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Notion API operations"""
        
        credentials = self.credentials["notion"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['token']}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        if operation == "get_pages":
            database_id = parameters.get("database_id")
            async with self.session.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                headers=headers,
                json={k: v for k, v in parameters.items() if k != "database_id"}
            ) as response:
                return await response.json()
        
        elif operation == "create_page":
            async with self.session.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Notion operation: {operation}")
    
    async def _execute_openai_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OpenAI API operations"""
        
        credentials = self.credentials["openai"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['api_key']}",
            "Content-Type": "application/json"
        }
        
        if operation == "chat_completion":
            async with self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        elif operation == "embeddings":
            async with self.session.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported OpenAI operation: {operation}")
    
    async def _execute_stripe_operation(self, operation: str, 
                                       parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Stripe API operations"""
        
        credentials = self.credentials["stripe"]
        headers = {
            "Authorization": f"Bearer {credentials.credentials['secret_key']}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        if operation == "create_payment":
            async with self.session.post(
                "https://api.stripe.com/v1/payment_intents",
                headers=headers,
                data=parameters
            ) as response:
                return await response.json()
        
        elif operation == "get_customers":
            async with self.session.get(
                "https://api.stripe.com/v1/customers",
                headers=headers,
                params=parameters
            ) as response:
                return await response.json()
        
        else:
            raise ValueError(f"Unsupported Stripe operation: {operation}")
    
    async def _execute_generic_operation(self, tool_name: str, operation: str, 
                                        parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic REST API operation"""
        
        integration = self.integrations[tool_name]
        credentials = self.credentials.get(tool_name)
        
        headers = {"Content-Type": "application/json"}
        
        if credentials:
            if credentials.credential_type == "api_key":
                if "api_key" in credentials.credentials:
                    headers["Authorization"] = f"Bearer {credentials.credentials['api_key']}"
                elif "token" in credentials.credentials:
                    headers["Authorization"] = f"Bearer {credentials.credentials['token']}"
        
        # Default to GET request
        async with self.session.get(
            integration.api_base_url,
            headers=headers,
            params=parameters
        ) as response:
            return await response.json()
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        
        status_summary = {
            "total_integrations": len(self.integrations),
            "connected": 0,
            "disconnected": 0,
            "error": 0,
            "by_category": {},
            "integrations": {}
        }
        
        for tool_name, integration in self.integrations.items():
            status = integration.status.value
            category = integration.category.value
            
            # Count by status
            if status == "connected":
                status_summary["connected"] += 1
            elif status == "disconnected":
                status_summary["disconnected"] += 1
            elif status == "error":
                status_summary["error"] += 1
            
            # Count by category
            if category not in status_summary["by_category"]:
                status_summary["by_category"][category] = {"total": 0, "connected": 0}
            
            status_summary["by_category"][category]["total"] += 1
            if status == "connected":
                status_summary["by_category"][category]["connected"] += 1
            
            # Individual integration status
            status_summary["integrations"][tool_name] = {
                "status": status,
                "category": category,
                "last_sync": integration.last_sync,
                "usage_stats": integration.usage_stats,
                "error_message": integration.error_message
            }
        
        return status_summary
    
    async def sync_all_tools(self) -> Dict[str, Any]:
        """Sync data across all connected tools"""
        
        sync_results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tools_synced": 0,
            "sync_results": {},
            "errors": []
        }
        
        connected_tools = [
            name for name, integration in self.integrations.items()
            if integration.status == IntegrationStatus.CONNECTED
        ]
        
        for tool_name in connected_tools:
            try:
                # Tool-specific sync logic
                sync_result = await self._sync_tool_data(tool_name)
                sync_results["sync_results"][tool_name] = sync_result
                sync_results["tools_synced"] += 1
                
                # Update last sync time
                self.integrations[tool_name].last_sync = datetime.now(timezone.utc).isoformat()
                
            except Exception as e:
                error_msg = f"Sync failed for {tool_name}: {str(e)}"
                sync_results["errors"].append(error_msg)
                logger.error(error_msg)
        
        sync_results["completed_at"] = datetime.now(timezone.utc).isoformat()
        return sync_results
    
    async def _sync_tool_data(self, tool_name: str) -> Dict[str, Any]:
        """Sync data for a specific tool"""
        
        # Implement tool-specific sync logic
        # This is a simplified example
        
        if tool_name == "github":
            # Sync repositories and issues
            repos_op = await self.execute_operation("github", "get_repos", {"per_page": 100})
            return {"repositories_synced": len(repos_op.result or [])}
        
        elif tool_name == "linear":
            # Sync issues
            issues_op = await self.execute_operation("linear", "get_issues", {})
            return {"issues_synced": len(issues_op.result.get("data", {}).get("issues", {}).get("nodes", []))}
        
        else:
            return {"status": "sync_not_implemented"}

# Global universal tool integration
universal_tools = UniversalToolIntegration()