"""
Enhanced Goal Planner with correct parameter names
Fixes Milestone parameter mismatch issues
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class GoalStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Milestone:
    """Milestone with correct parameter names"""
    milestone_id: str  # Changed from 'id' to 'milestone_id'
    title: str
    description: str
    target_date: str
    status: str = "pending"
    dependencies: List[str] = field(default_factory=list)
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    completion_date: Optional[str] = None
    notes: str = ""
    
@dataclass
class Goal:
    """Enhanced goal definition"""
    goal_id: str
    title: str
    description: str
    priority: Priority
    status: GoalStatus = GoalStatus.PENDING
    milestones: List[Milestone] = field(default_factory=list)
    target_date: Optional[str] = None
    created_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    assigned_agent: Optional[str] = None
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    completion_percentage: float = 0.0
    tags: List[str] = field(default_factory=list)
    
class EnhancedGoalPlanner:
    """Enhanced goal planner with comprehensive functionality"""
    
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.daily_tasks: Dict[str, List[Dict[str, Any]]] = {}
        
    def add_goal(self, goal: Goal) -> bool:
        """Add a new goal"""
        try:
            self.goals[goal.goal_id] = goal
            
            # Add milestones to milestone tracking
            for milestone in goal.milestones:
                self.milestones[milestone.milestone_id] = milestone
                
            logger.info(f"Added goal: {goal.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add goal: {e}")
            return False
            
    def update_goal(self, goal_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing goal"""
        try:
            if goal_id not in self.goals:
                logger.warning(f"Goal {goal_id} not found")
                return False
                
            goal = self.goals[goal_id]
            
            # Update fields
            for field, value in updates.items():
                if hasattr(goal, field):
                    setattr(goal, field, value)
                    
            goal.updated_date = datetime.now(timezone.utc).isoformat()
            
            # Recalculate completion percentage
            self._update_completion_percentage(goal_id)
            
            logger.info(f"Updated goal: {goal.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update goal: {e}")
            return False
            
    def add_milestone(self, goal_id: str, milestone: Milestone) -> bool:
        """Add a milestone to a goal"""
        try:
            if goal_id not in self.goals:
                logger.warning(f"Goal {goal_id} not found")
                return False
                
            goal = self.goals[goal_id]
            goal.milestones.append(milestone)
            self.milestones[milestone.milestone_id] = milestone
            
            # Update goal's updated date
            goal.updated_date = datetime.now(timezone.utc).isoformat()
            
            logger.info(f"Added milestone {milestone.title} to goal {goal.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add milestone: {e}")
            return False
            
    def complete_milestone(self, milestone_id: str) -> bool:
        """Mark a milestone as completed"""
        try:
            if milestone_id not in self.milestones:
                logger.warning(f"Milestone {milestone_id} not found")
                return False
                
            milestone = self.milestones[milestone_id]
            milestone.status = "completed"
            milestone.completion_date = datetime.now(timezone.utc).isoformat()
            
            # Find and update the parent goal
            for goal in self.goals.values():
                if any(m.milestone_id == milestone_id for m in goal.milestones):
                    self._update_completion_percentage(goal.goal_id)
                    break
                    
            logger.info(f"Completed milestone: {milestone.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to complete milestone: {e}")
            return False
            
    def _update_completion_percentage(self, goal_id: str):
        """Update goal completion percentage based on milestones"""
        try:
            goal = self.goals[goal_id]
            
            if not goal.milestones:
                return
                
            completed_milestones = sum(
                1 for milestone in goal.milestones 
                if milestone.status == "completed"
            )
            
            goal.completion_percentage = (completed_milestones / len(goal.milestones)) * 100
            
            # Update goal status based on completion
            if goal.completion_percentage == 100:
                goal.status = GoalStatus.COMPLETED
            elif goal.completion_percentage > 0:
                goal.status = GoalStatus.IN_PROGRESS
                
        except Exception as e:
            logger.error(f"Failed to update completion percentage: {e}")
            
    def _calculate_days_overdue(self, target_date: str) -> int:
        """Safely calculate days overdue for a target date"""
        try:
            # Parse target date and make it timezone-aware if needed
            if 'T' in target_date:
                # ISO format with time
                target_dt = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
            else:
                # Date only format
                target_dt = datetime.strptime(target_date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            
            # Ensure target_dt is timezone-aware
            if target_dt.tzinfo is None:
                target_dt = target_dt.replace(tzinfo=timezone.utc)
                
            current_dt = datetime.now(timezone.utc)
            return (current_dt - target_dt).days
            
        except (ValueError, TypeError, AttributeError):
            return 0  # Return 0 for invalid dates
            
    def get_goals(self, status: Optional[GoalStatus] = None, 
                  agent_id: Optional[str] = None) -> List[Goal]:
        """Get goals with optional filtering"""
        goals = list(self.goals.values())
        
        if status:
            goals = [goal for goal in goals if goal.status == status]
            
        if agent_id:
            goals = [goal for goal in goals if goal.assigned_agent == agent_id]
            
        return goals
        
    def get_daily_tasks(self, agent_id: Optional[str] = None, 
                       date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get daily tasks for agent or date"""
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
        if agent_id:
            return self.daily_tasks.get(f"{agent_id}_{date}", [])
        else:
            # Return all tasks for the date
            all_tasks = []
            for key, tasks in self.daily_tasks.items():
                if key.endswith(f"_{date}"):
                    all_tasks.extend(tasks)
            return all_tasks
            
    def generate_daily_tasks(self, agent_id: str, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate daily tasks for an agent based on their goals"""
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
        tasks = []
        
        # Get agent's goals
        agent_goals = self.get_goals(agent_id=agent_id)
        
        for goal in agent_goals:
            if goal.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]:
                # Find milestones due today or overdue
                for milestone in goal.milestones:
                    if milestone.status == "pending":
                        milestone_date = milestone.target_date[:10]  # YYYY-MM-DD
                        
                        if milestone_date <= date:
                            tasks.append({
                                "id": f"task_{milestone.milestone_id}_{date}",
                                "title": f"Work on: {milestone.title}",
                                "description": milestone.description,
                                "goal_id": goal.goal_id,
                                "milestone_id": milestone.milestone_id,
                                "priority": goal.priority.value,
                                "estimated_duration": "2 hours",
                                "due_date": milestone.target_date,
                                "status": "pending"
                            })
                            
        # Store generated tasks
        task_key = f"{agent_id}_{date}"
        self.daily_tasks[task_key] = tasks
        
        return tasks
        
    def get_goal_progress_report(self, goal_id: str) -> Dict[str, Any]:
        """Get detailed progress report for a goal"""
        if goal_id not in self.goals:
            return {}
            
        goal = self.goals[goal_id]
        
        completed_milestones = [m for m in goal.milestones if m.status == "completed"]
        pending_milestones = [m for m in goal.milestones if m.status == "pending"]
        overdue_milestones = []
        
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        for milestone in pending_milestones:
            try:
                milestone_date = milestone.target_date[:10]
                if milestone_date < current_date:
                    overdue_milestones.append(milestone)
            except (ValueError, TypeError, AttributeError):
                # Skip milestones with invalid dates
                continue
                
        return {
            "goal_id": goal_id,
            "title": goal.title,
            "status": goal.status.value,
            "completion_percentage": goal.completion_percentage,
            "total_milestones": len(goal.milestones),
            "completed_milestones": len(completed_milestones),
            "pending_milestones": len(pending_milestones),
            "overdue_milestones": len(overdue_milestones),
            "estimated_cost": goal.estimated_cost,
            "actual_cost": goal.actual_cost,
            "cost_variance": goal.actual_cost - goal.estimated_cost,
            "created_date": goal.created_date,
            "updated_date": goal.updated_date,
            "target_date": goal.target_date,
            "overdue_milestone_details": [
                {
                    "milestone_id": m.milestone_id,
                    "title": m.title,
                    "target_date": m.target_date,
                    "days_overdue": self._calculate_days_overdue(m.target_date)
                }
                for m in overdue_milestones
            ]
        }
        
    def export_goals_to_json(self, filename: str) -> bool:
        """Export all goals to JSON file"""
        try:
            data = {
                "goals": [
                    {
                        "goal_id": goal.goal_id,
                        "title": goal.title,
                        "description": goal.description,
                        "priority": goal.priority.value,
                        "status": goal.status.value,
                        "completion_percentage": goal.completion_percentage,
                        "milestones": [
                            {
                                "milestone_id": m.milestone_id,
                                "title": m.title,
                                "description": m.description,
                                "target_date": m.target_date,
                                "status": m.status,
                                "estimated_cost": m.estimated_cost,
                                "actual_cost": m.actual_cost
                            }
                            for m in goal.milestones
                        ],
                        "target_date": goal.target_date,
                        "created_date": goal.created_date,
                        "updated_date": goal.updated_date,
                        "assigned_agent": goal.assigned_agent,
                        "estimated_cost": goal.estimated_cost,
                        "actual_cost": goal.actual_cost,
                        "tags": goal.tags
                    }
                    for goal in self.goals.values()
                ],
                "exported_at": datetime.now(timezone.utc).isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Goals exported to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export goals: {e}")
            return False

# Global enhanced goal planner instance
enhanced_goal_planner = EnhancedGoalPlanner()