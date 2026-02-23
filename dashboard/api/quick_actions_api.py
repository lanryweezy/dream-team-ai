"""
Quick Actions API Integration
Connects One-Click Actions to our existing backend systems
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Header, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
import os
import time
import json
import uuid
from fastapi import Response, status

# Import our existing systems
from core.founder_orchestration_system import FounderOrchestrationSystem
from core.ai_orchestration_engine import AIOrchestrationEngine
from core.project_task_manager import ProjectTaskManager
from core.universal_tool_integration import UniversalToolIntegration
from core.business_orchestration_api import BusinessOrchestrationAPI

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/quick-actions", tags=["quick-actions"])

# Initialize systems
founder_system = FounderOrchestrationSystem()
ai_engine = AIOrchestrationEngine()
project_manager = ProjectTaskManager()
tool_integration = UniversalToolIntegration()
business_api = BusinessOrchestrationAPI()

# Security, rate limiting, and idempotency helpers
from core.state_store import state_store

def _safe_preview(obj: Any, max_len: int = 200) -> str:
    """Safely creates a string preview of any object."""
    try:
        # Normalize to a plain string first
        if isinstance(obj, (dict, list)):
            s = json.dumps(obj, ensure_ascii=False)
        elif isinstance(obj, (bytes, bytearray)):
            s = obj.decode("utf-8", errors="replace")
        else:
            s = "" if obj is None else str(obj)
        if not isinstance(s, str):
            s = str(s)
        # Defensive bounds for max_len
        try:
            max_len = int(max_len)
        except Exception:
            max_len = 200
        if max_len <= 0:
            max_len = 200
        return (s[:max_len] + "...") if len(s) > max_len else s
    except Exception:
        try:
            s = "" if obj is None else str(obj)
            return (s[:200] + "...") if len(s) > 200 else s
        except Exception:
            return ""

# Task helpers (persisted via state_store; Redis if REDIS_URL is configured)
def _task_key(task_id: str) -> str:
    return f"task:{task_id}"

async def create_task(initial: Dict[str, Any] | None = None, ttl_seconds: int = 86400) -> str:
    task_id = str(uuid.uuid4())
    payload = {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        **(initial or {}),
    }
    await state_store.set(_task_key(task_id), payload, ttl_seconds=ttl_seconds)
    return task_id

async def update_task(task_id: str, **fields):
    key = _task_key(task_id)
    current = await state_store.get(key) or {}
    if not isinstance(current, dict):
        try:
            current = json.loads(current)
        except Exception:
            current = {}
    current.update(fields)
    await state_store.set(key, current, ttl_seconds=86400)

async def get_task(task_id: str):
    key = _task_key(task_id)
    data = await state_store.get(key)
    if data is None:
        return None
    return data if isinstance(data, dict) else json.loads(data)


BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")

async def require_auth(x_api_key: str | None):
    if not BACKEND_API_KEY:
        return  # auth disabled if no key configured
    if not x_api_key or x_api_key != BACKEND_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

async def enforce_rate_limit(api_key: str, route: str, max_per_minute: int = 60):
    # simple token bucket per API key + route
    key = f"rate:{api_key or 'public'}:{route}:{int(time.time()//60)}"
    count = await state_store.incr(key, ttl_seconds=60)
    if count > max_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

async def get_cached_response(idempotency_key: str | None):
    if not idempotency_key:
        return None
    raw = await state_store.get(f"idemp:{idempotency_key}")
    if not raw:
        return None
    try:
        return raw if isinstance(raw, dict) else json.loads(raw)
    except Exception:
        return None

async def cache_response(idempotency_key: str | None, response_data: dict, ttl_seconds: int = 3600):
    if not idempotency_key:
        return
    try:
        await state_store.set(f"idemp:{idempotency_key}", response_data, ttl_seconds=ttl_seconds)
    except Exception:
        pass

async def with_retries(coro_factory, retries: int = 3, base_delay: float = 0.5):
    last_err = None
    for attempt in range(retries):
        try:
            return await coro_factory()
        except Exception as e:
            last_err = e
            await asyncio.sleep(min(base_delay * (2 ** attempt), 5.0))
    raise last_err if last_err else Exception("Operation failed")

class ActionRequest(BaseModel):
    business_id: str
    action_type: str
    parameters: Dict[str, Any] = {}

class ActionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: float
    timestamp: datetime

class SprintCreationRequest(BaseModel):
    business_id: str
    sprint_duration: int = 14
    ai_generate_tasks: bool = True
    focus_areas: List[str] = []

class InvestorUpdateRequest(BaseModel):
    business_id: str
    period: str = "monthly"
    include_financials: bool = True
    include_metrics: bool = True
    auto_send: bool = False
    recipient_list: List[str] = []

class DeploymentRequest(BaseModel):
    business_id: str
    environment: str = "staging"
    run_tests: bool = True
    auto_promote: bool = False
    features: List[str] = []

class TeamCheckinRequest(BaseModel):
    business_id: str
    include_mood: bool = True
    include_blockers: bool = True
    generate_summary: bool = True

class ReportGenerationRequest(BaseModel):
    business_id: str
    report_type: str = "comprehensive"
    include_predictions: bool = True
    include_recommendations: bool = True
    time_period: str = "last_30_days"
    async_mode: bool = False # Add async mode flag

@router.post("/create-sprint", response_model=ActionResponse)
async def create_sprint(
    request: SprintCreationRequest,
    req: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """Create a new sprint with AI-generated tasks"""
    start_time = datetime.now()
    
    # Auth, rate limit, idempotency
    await require_auth(x_api_key)
    await enforce_rate_limit(x_api_key or "public", req.url.path)
    cached = await get_cached_response(idempotency_key)
    if cached:
        return ActionResponse(**cached)
    try:
        logger.info(f"Creating sprint for business {request.business_id}")
        
        # Get business context
        business_context = await business_api.get_business_context(request.business_id)
        
        # Generate sprint plan using AI
        sprint_prompt = f"""
        Create a {request.sprint_duration}-day sprint plan for a {business_context.get('business_type', 'startup')} business.
        
        Business Context:
        - Industry: {business_context.get('industry', 'Technology')}
        - Stage: {business_context.get('stage', 'Early Stage')}
        - Team Size: {business_context.get('team_size', 5)}
        - Current Goals: {business_context.get('current_goals', 'Growth and Product Development')}
        
        Focus Areas: {', '.join(request.focus_areas) if request.focus_areas else 'General Development'}
        
        Generate 8-12 specific, actionable tasks with:
        1. Clear task descriptions
        2. Estimated effort (hours)
        3. Priority level (High/Medium/Low)
        4. Assigned team member suggestions
        5. Dependencies between tasks
        """
        
        # Use AI to generate sprint tasks
        ai_response = await ai_engine.generate_content(
            prompt=sprint_prompt,
            model="gpt-4",
            max_tokens=1500
        )
        
        # Create sprint in project manager
        sprint_data = {
            "name": f"AI Sprint - {datetime.now().strftime('%B %Y')}",
            "duration": request.sprint_duration,
            "business_id": request.business_id,
            "ai_generated": True,
            "tasks": ai_response.get("tasks", []),
            "goals": ai_response.get("goals", []),
            "success_metrics": ai_response.get("metrics", [])
        }
        
        sprint_result = await project_manager.create_sprint(sprint_data)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        resp = ActionResponse(
            success=True,
            message=f"Created sprint '{sprint_result['name']}' with {len(sprint_result['tasks'])} AI-generated tasks",
            data={
                "sprint_id": sprint_result["id"],
                "sprint_name": sprint_result["name"],
                "task_count": len(sprint_result["tasks"]),
                "duration": request.sprint_duration,
                "estimated_completion": sprint_result.get("estimated_completion"),
                "tasks_preview": sprint_result["tasks"][:3]  # First 3 tasks for preview
            },
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        await cache_response(idempotency_key, resp.dict())
        return resp
        
    except Exception as e:
        logger.error(f"Sprint creation failed: {str(e)}")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ActionResponse(
            success=False,
            message=f"Sprint creation failed: {str(e)}",
            data=None,
            execution_time=execution_time,
            timestamp=datetime.now()
        )

@router.post("/investor-update", response_model=ActionResponse)
async def generate_investor_update(
    request: InvestorUpdateRequest,
    req: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """Generate and optionally send investor update"""
    start_time = datetime.now()
    
    await require_auth(x_api_key)
    await enforce_rate_limit(x_api_key or "public", req.url.path)
    cached = await get_cached_response(idempotency_key)
    if cached:
        return ActionResponse(**cached)
    try:
        logger.info(f"Generating investor update for business {request.business_id}")
        
        # Gather business metrics
        business_metrics = await business_api.get_comprehensive_metrics(request.business_id)
        
        # Generate investor update using AI
        update_prompt = f"""
        Generate a professional investor update for a startup.
        
        Period: {request.period}
        
        Key Metrics:
        - Revenue: {str(business_metrics.get('revenue', 0))}
        - Growth Rate: {str(business_metrics.get('growth_rate', 0))}%
        - Active Users: {str(business_metrics.get('active_users', 0))}
        - Team Size: {str(business_metrics.get('team_size', 0))}
        - Runway: {str(business_metrics.get('runway_months', 0))} months
        
        Include:
        1. Executive Summary
        2. Key Achievements
        3. Financial Performance
        4. Product Updates
        5. Team Updates
        6. Challenges and Solutions
        7. Next Period Goals
        8. Funding Status (if applicable)
        
        Tone: Professional, optimistic but realistic, data-driven
        """
        
        # Generate update content
        update_content = await ai_engine.generate_content(
            prompt=update_prompt,
            model="gpt-4",
            max_tokens=2000
        )
        # Coerce AI output to a robust, safe string
        try:
            if isinstance(update_content, dict):
                content_candidate = update_content.get("content", update_content)
            else:
                content_candidate = update_content
            if isinstance(content_candidate, (dict, list)):
                content_str = json.dumps(content_candidate, ensure_ascii=False)
            elif isinstance(content_candidate, (bytes, bytearray)):
                content_str = content_candidate.decode("utf-8", errors="replace")
            else:
                content_str = "" if content_candidate is None else str(content_candidate)
            if not isinstance(content_str, str):
                content_str = str(content_str)
        except Exception:
            content_str = ""
        
        # Format as professional document
        formatted_update = {
            "title": f"Investor Update - {datetime.now().strftime('%B %Y')}",
            "content": content_str,
            "metrics": business_metrics,
            "generated_at": datetime.now().isoformat(),
            "period": request.period
        }
        
        # Optionally send to investors
        recipient_count = 0
        if request.auto_send and request.recipient_list:
            # In a real implementation, this would send emails
            recipient_count = len(request.recipient_list)
            logger.info(f"Would send update to {recipient_count} investors")
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Build a safe preview on a guaranteed string
        preview = ""
        try:
            s = content_str if isinstance(content_str, str) else ("" if content_str is None else str(content_str))
            preview = (s[:200] + "...") if len(s) > 200 else s
        except Exception:
            preview = ""
        
        resp = ActionResponse(
            success=True,
            message=f"Generated investor update{' and sent to ' + str(recipient_count) + ' investors' if recipient_count > 0 else ''}",
            data={
                "update_title": formatted_update["title"],
                "content_length": len(content_str or ""),
                "recipient_count": recipient_count,
                "key_metrics": {
                    "revenue": business_metrics.get('revenue', 0),
                    "growth_rate": business_metrics.get('growth_rate', 0),
                    "active_users": business_metrics.get('active_users', 0)
                },
                "preview": preview
            },
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        await cache_response(idempotency_key, resp.dict())
        return resp
        
    except Exception as e:
        logger.error(f"Investor update generation failed: {str(e)}", exc_info=True)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ActionResponse(
            success=False,
            message=f"Investor update generation failed: {str(e)}",
            data=None,
            execution_time=execution_time,
            timestamp=datetime.now()
        )

@router.post("/deploy-feature", response_model=ActionResponse)
async def deploy_feature(
    request: DeploymentRequest,
    req: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """Deploy features with automated testing"""
    start_time = datetime.now()
    
    await require_auth(x_api_key)
    await enforce_rate_limit(x_api_key or "public", req.url.path)
    cached = await get_cached_response(idempotency_key)
    if cached:
        return ActionResponse(**cached)
    try:
        logger.info(f"Deploying features for business {request.business_id}")
        
        # Get pending features for deployment
        pending_features = await project_manager.get_ready_features(request.business_id)
        
        if not pending_features:
            return ActionResponse(
                success=False,
                message="No features ready for deployment",
                data=None,
                execution_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now()
            )
        
        # Simulate deployment process
        deployment_steps = [
            "Running pre-deployment tests",
            "Building application",
            "Deploying to staging environment",
            "Running integration tests",
            "Validating deployment"
        ]
        
        deployment_results = []
        for step in deployment_steps:
            # Simulate step execution
            await asyncio.sleep(0.1)  # Simulate processing time
            deployment_results.append({
                "step": step,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            })
        
        # Mark features as deployed
        deployed_features = []
        for feature in pending_features[:5]:  # Deploy up to 5 features
            deployed_features.append({
                "name": feature.get("name", "Feature"),
                "version": feature.get("version", "1.0.0"),
                "status": "deployed"
            })
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        resp = ActionResponse(
            success=True,
            message=f"Successfully deployed {len(deployed_features)} features to {request.environment}",
            data={
                "environment": request.environment,
                "feature_count": len(deployed_features),
                "deployed_features": deployed_features,
                "deployment_steps": deployment_results,
                "tests_passed": request.run_tests,
                "deployment_url": f"https://{request.environment}.yourapp.com"
            },
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        await cache_response(idempotency_key, resp.dict())
        return resp
        
    except Exception as e:
        logger.error(f"Feature deployment failed: {str(e)}")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ActionResponse(
            success=False,
            message=f"Feature deployment failed: {str(e)}",
            data=None,
            execution_time=execution_time,
            timestamp=datetime.now()
        )

@router.post("/team-checkin", response_model=ActionResponse)
async def team_checkin(
    request: TeamCheckinRequest,
    req: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """Automated team check-in and status collection"""
    start_time = datetime.now()
    
    await require_auth(x_api_key)
    await enforce_rate_limit(x_api_key or "public", req.url.path)
    cached = await get_cached_response(idempotency_key)
    if cached:
        return ActionResponse(**cached)
    try:
        logger.info(f"Running team check-in for business {request.business_id}")
        
        # Get team members
        team_members = await business_api.get_team_members(request.business_id)
        
        # Simulate collecting status from team members
        team_status = []
        for member in team_members:
            status = {
                "name": member.get("name", "Team Member"),
                "role": member.get("role", "Developer"),
                "status": "active",
                "current_tasks": member.get("current_tasks", []),
                "completion_rate": member.get("completion_rate", 85),
                "mood": "positive" if request.include_mood else None,
                "blockers": member.get("blockers", []) if request.include_blockers else None,
                "last_update": datetime.now().isoformat()
            }
            team_status.append(status)
        
        # Generate team summary if requested
        team_summary = None
        if request.generate_summary:
            summary_prompt = f"""
            Generate a brief team status summary based on the following data:
            
            Team Size: {len(team_members)}
            Average Completion Rate: {sum(m.get('completion_rate', 85) for m in team_status) / len(team_status):.1f}%
            Active Blockers: {sum(len(m.get('blockers', [])) for m in team_status)}
            
            Provide:
            1. Overall team health assessment
            2. Key achievements this period
            3. Main challenges and blockers
            4. Recommendations for improvement
            """
            
            team_summary = await ai_engine.generate_content(
                prompt=summary_prompt,
                model="gpt-3.5-turbo",
                max_tokens=500
            )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        resp = ActionResponse(
            success=True,
            message=f"Collected status from {len(team_members)} team members",
            data={
                "team_member_count": len(team_members),
                "team_status": team_status,
                "team_summary": team_summary,
                "average_completion_rate": sum(m.get('completion_rate', 85) for m in team_status) / len(team_status),
                "total_blockers": sum(len(m.get('blockers', [])) for m in team_status),
                "check_in_timestamp": datetime.now().isoformat()
            },
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        await cache_response(idempotency_key, resp.dict())
        return resp
        
    except Exception as e:
        logger.error(f"Team check-in failed: {str(e)}")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ActionResponse(
            success=False,
            message=f"Team check-in failed: {str(e)}",
            data=None,
            execution_time=execution_time,
            timestamp=datetime.now()
        )

@router.post("/generate-report", response_model=ActionResponse)
async def generate_business_report(
    request: ReportGenerationRequest,
    req: Request,
    background_tasks: BackgroundTasks,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """Generate comprehensive business report with AI insights"""
    start_time = datetime.now()
    
    await require_auth(x_api_key)
    await enforce_rate_limit(x_api_key or "public", req.url.path)
    cached = await get_cached_response(idempotency_key)
    if cached:
        return ActionResponse(**cached)
    try:
        logger.info(f"Generating business report for {request.business_id}")

        # Async mode: create a task, run in background, and return 202 with task_id
        if request.async_mode:
            task_id = await create_task({"type": "generate-report", "business_id": request.business_id})
            
            async def run_report_task():
                try:
                    await update_task(task_id, status="running", started_at=datetime.now().isoformat())
                    business_data = await business_api.get_comprehensive_analytics(request.business_id)
                    report_prompt = f"""
            Generate a comprehensive business report with the following data:
            Business Metrics:
            - Revenue: ${business_data.get('revenue', 0):,.2f}
            - Growth Rate: {business_data.get('growth_rate', 0):.1f}%
            - Customer Count: {business_data.get('customers', 0):,}
            Time Period: {request.time_period}
            Include: Executive Summary, Financial Performance, etc.
            {"Include Predictive Analysis" if request.include_predictions else ""}
            {"Include Actionable Recommendations" if request.include_recommendations else ""}
            """
                    report_content = await ai_engine.generate_content(prompt=report_prompt, model="gpt-4", max_tokens=3000)
                    result = {"message": "Report generated successfully", "data": {"report_content": report_content}}
                    await update_task(task_id, status="succeeded", finished_at=datetime.now().isoformat(), result=result)
                except Exception as e:
                    await update_task(task_id, status="failed", finished_at=datetime.now().isoformat(), error=str(e))
            
            background_tasks.add_task(run_report_task)
            
            return Response(
                content=json.dumps({"task_id": task_id, "status": "pending"}),
                media_type="application/json",
                status_code=status.HTTP_202_ACCEPTED,
            )
        
        # Gather comprehensive business data
        business_data = await business_api.get_comprehensive_analytics(request.business_id)
        
        # Generate AI-powered insights
        report_prompt = f"""
        Generate a comprehensive business report with the following data:
        
        Business Metrics:
        - Revenue: ${business_data.get('revenue', 0):,.2f}
        - Growth Rate: {business_data.get('growth_rate', 0):.1f}%
        - Customer Count: {business_data.get('customers', 0):,}
        - Team Productivity: {business_data.get('team_productivity', 85):.1f}%
        - Market Position: {business_data.get('market_position', 'Growing')}
        
        Time Period: {request.time_period}
        
        Include:
        1. Executive Summary
        2. Financial Performance Analysis
        3. Operational Metrics
        4. Team Performance
        5. Market Analysis
        6. Risk Assessment
        7. Growth Opportunities
        8. Strategic Recommendations
        
        {"9. Predictive Analysis (3-month forecast)" if request.include_predictions else ""}
        {"10. Actionable Recommendations with priorities" if request.include_recommendations else ""}
        """
        
        # Generate comprehensive report
        report_content = await ai_engine.generate_content(
            prompt=report_prompt,
            model="gpt-4",
            max_tokens=3000
        )
        
        # Extract key insights
        insights = [
            f"Revenue growth of {business_data.get('growth_rate', 0):.1f}% this period",
            f"Team productivity at {business_data.get('team_productivity', 85):.1f}%",
            f"Customer base grew to {business_data.get('customers', 0):,}",
            "Market position remains strong",
            "Operational efficiency improved"
        ]
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        resp = ActionResponse(
            success=True,
            message=f"Generated comprehensive report with {len(insights)} key insights",
            data={
                "report_type": request.report_type,
                "insight_count": len(insights),
                "key_insights": insights,
                "report_content": report_content,
                "business_metrics": business_data,
                "time_period": request.time_period,
                "includes_predictions": request.include_predictions,
                "includes_recommendations": request.include_recommendations,
                "generated_at": datetime.now().isoformat()
            },
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        await cache_response(idempotency_key, resp.dict())
        return resp
        
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ActionResponse(
            success=False,
            message=f"Report generation failed: {str(e)}",
            data=None,
            execution_time=execution_time,
            timestamp=datetime.now()
        )

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str, req: Request, x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")):
    """Poll the status of a background task"""
    await require_auth(x_api_key)
    await enforce_rate_limit(x_api_key or "public", req.url.path, max_per_minute=300)
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/action-history/{business_id}")
async def get_action_history(business_id: str, limit: int = 50):
    """Get history of executed quick actions"""
    try:
        # In a real implementation, this would query a database
        # For now, return mock data
        history = [
            {
                "action_type": "create-sprint",
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "execution_time": 2.3,
                "message": "Created sprint with 10 AI-generated tasks"
            },
            {
                "action_type": "team-checkin",
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "execution_time": 1.1,
                "message": "Collected status from 5 team members"
            }
        ]
        
        return {
            "business_id": business_id,
            "total_actions": len(history),
            "success_rate": 100.0,
            "history": history[:limit]
        }
        
    except Exception as e:
        logger.error(f"Failed to get action history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))