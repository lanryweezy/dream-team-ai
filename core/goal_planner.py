"""
Goal Planning System
Manages hierarchical goals (Yearly → Quarterly → Monthly → Daily)
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class GoalStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class GoalPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Goal:
    def __init__(self, 
                 goal_id: str,
                 title: str,
                 description: str,
                 goal_type: str,  # yearly, quarterly, monthly, daily
                 target_date: datetime,
                 priority: GoalPriority = GoalPriority.MEDIUM,
                 parent_goal_id: Optional[str] = None,
                 metrics: Optional[Dict[str, Any]] = None):
        self.goal_id = goal_id
        self.title = title
        self.description = description
        self.goal_type = goal_type
        self.target_date = target_date
        self.priority = priority
        self.parent_goal_id = parent_goal_id
        self.metrics = metrics or {}
        self.status = GoalStatus.PENDING
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.progress = 0.0
        self.sub_goals: List[str] = []
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "goal_type": self.goal_type,
            "target_date": self.target_date.isoformat(),
            "priority": self.priority.value,
            "parent_goal_id": self.parent_goal_id,
            "metrics": self.metrics,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "progress": self.progress,
            "sub_goals": self.sub_goals
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Goal':
        goal = cls(
            goal_id=data["goal_id"],
            title=data["title"],
            description=data["description"],
            goal_type=data["goal_type"],
            target_date=datetime.fromisoformat(data["target_date"]),
            priority=GoalPriority(data["priority"]),
            parent_goal_id=data.get("parent_goal_id"),
            metrics=data.get("metrics", {})
        )
        goal.status = GoalStatus(data["status"])
        goal.created_at = datetime.fromisoformat(data["created_at"])
        goal.updated_at = datetime.fromisoformat(data["updated_at"])
        goal.progress = data["progress"]
        goal.sub_goals = data["sub_goals"]
        return goal

class Milestone:
    def __init__(self,
                 milestone_id: str,
                 title: str,
                 description: str,
                 due_date: datetime,
                 goal_id: str,
                 deliverables: List[str] = None):
        self.milestone_id = milestone_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.goal_id = goal_id
        self.deliverables = deliverables or []
        self.status = GoalStatus.PENDING
        self.created_at = datetime.utcnow()
        self.completed_at: Optional[datetime] = None
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "milestone_id": self.milestone_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "goal_id": self.goal_id,
            "deliverables": self.deliverables,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class GoalPlanner:
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.milestones: Dict[str, Milestone] = {}
        
    def create_yearly_goal(self, 
                          title: str,
                          description: str,
                          target_metrics: Dict[str, Any],
                          year: int = None) -> Goal:
        """Create a yearly goal"""
        
        if year is None:
            year = datetime.utcnow().year
            
        goal_id = f"yearly_{year}_{len(self.goals)}"
        target_date = datetime(year, 12, 31)
        
        goal = Goal(
            goal_id=goal_id,
            title=title,
            description=description,
            goal_type="yearly",
            target_date=target_date,
            priority=GoalPriority.HIGH,
            metrics=target_metrics
        )
        
        self.goals[goal_id] = goal
        return goal
        
    def create_quarterly_goal(self,
                            title: str,
                            description: str,
                            quarter: int,
                            year: int,
                            parent_yearly_goal_id: str,
                            target_metrics: Dict[str, Any] = None) -> Goal:
        """Create a quarterly goal"""
        
        goal_id = f"quarterly_{year}_q{quarter}_{len(self.goals)}"
        
        # Calculate quarter end date
        quarter_end_months = {1: 3, 2: 6, 3: 9, 4: 12}
        end_month = quarter_end_months[quarter]
        target_date = datetime(year, end_month, 28)  # Safe end of month
        
        goal = Goal(
            goal_id=goal_id,
            title=title,
            description=description,
            goal_type="quarterly",
            target_date=target_date,
            priority=GoalPriority.HIGH,
            parent_goal_id=parent_yearly_goal_id,
            metrics=target_metrics or {}
        )
        
        # Add to parent goal's sub_goals
        if parent_yearly_goal_id in self.goals:
            self.goals[parent_yearly_goal_id].sub_goals.append(goal_id)
            
        self.goals[goal_id] = goal
        return goal
        
    def create_monthly_goal(self,
                          title: str,
                          description: str,
                          month: int,
                          year: int,
                          parent_quarterly_goal_id: str,
                          target_metrics: Dict[str, Any] = None) -> Goal:
        """Create a monthly goal"""
        
        goal_id = f"monthly_{year}_{month:02d}_{len(self.goals)}"
        
        # Calculate month end date
        if month == 12:
            target_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            target_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
        goal = Goal(
            goal_id=goal_id,
            title=title,
            description=description,
            goal_type="monthly",
            target_date=target_date,
            priority=GoalPriority.MEDIUM,
            parent_goal_id=parent_quarterly_goal_id,
            metrics=target_metrics or {}
        )
        
        # Add to parent goal's sub_goals
        if parent_quarterly_goal_id in self.goals:
            self.goals[parent_quarterly_goal_id].sub_goals.append(goal_id)
            
        self.goals[goal_id] = goal
        return goal
        
    def create_daily_goal(self,
                        title: str,
                        description: str,
                        target_date: datetime,
                        parent_monthly_goal_id: str,
                        assigned_agent: str = None) -> Goal:
        """Create a daily goal"""
        
        goal_id = f"daily_{target_date.strftime('%Y_%m_%d')}_{len(self.goals)}"
        
        goal = Goal(
            goal_id=goal_id,
            title=title,
            description=description,
            goal_type="daily",
            target_date=target_date,
            priority=GoalPriority.MEDIUM,
            parent_goal_id=parent_monthly_goal_id,
            metrics={"assigned_agent": assigned_agent} if assigned_agent else {}
        )
        
        # Add to parent goal's sub_goals
        if parent_monthly_goal_id in self.goals:
            self.goals[parent_monthly_goal_id].sub_goals.append(goal_id)
            
        self.goals[goal_id] = goal
        return goal
        
    def update_goal_progress(self, goal_id: str, progress: float) -> bool:
        """Update goal progress (0.0 to 1.0)"""
        
        if goal_id not in self.goals:
            return False
            
        goal = self.goals[goal_id]
        goal.progress = max(0.0, min(1.0, progress))
        goal.updated_at = datetime.utcnow()
        
        if progress >= 1.0:
            goal.status = GoalStatus.COMPLETED
            
        # Update parent goal progress
        if goal.parent_goal_id:
            self._update_parent_progress(goal.parent_goal_id)
            
        return True
        
    def _update_parent_progress(self, parent_goal_id: str) -> None:
        """Update parent goal progress based on sub-goals"""
        
        if parent_goal_id not in self.goals:
            return
            
        parent_goal = self.goals[parent_goal_id]
        
        if not parent_goal.sub_goals:
            return
            
        # Calculate average progress of sub-goals
        total_progress = 0.0
        completed_sub_goals = 0
        
        for sub_goal_id in parent_goal.sub_goals:
            if sub_goal_id in self.goals:
                sub_goal = self.goals[sub_goal_id]
                total_progress += sub_goal.progress
                if sub_goal.status == GoalStatus.COMPLETED:
                    completed_sub_goals += 1
                    
        if parent_goal.sub_goals:
            parent_goal.progress = total_progress / len(parent_goal.sub_goals)
            parent_goal.updated_at = datetime.utcnow()
            
            # Update parent's parent recursively
            if parent_goal.parent_goal_id:
                self._update_parent_progress(parent_goal.parent_goal_id)
                
    def get_daily_goals_for_date(self, date: datetime) -> List[Goal]:
        """Get all daily goals for a specific date"""
        
        daily_goals = []
        date_str = date.strftime('%Y_%m_%d')
        
        for goal in self.goals.values():
            if (goal.goal_type == "daily" and 
                date_str in goal.goal_id and
                goal.status != GoalStatus.COMPLETED):
                daily_goals.append(goal)
                
        return sorted(daily_goals, key=lambda g: g.priority.value, reverse=True)
        
    def get_goals_by_type(self, goal_type: str) -> List[Goal]:
        """Get all goals of a specific type"""
        
        return [goal for goal in self.goals.values() if goal.goal_type == goal_type]
        
    def get_overdue_goals(self) -> List[Goal]:
        """Get all overdue goals"""
        
        now = datetime.utcnow()
        overdue = []
        
        for goal in self.goals.values():
            if (goal.target_date < now and 
                goal.status not in [GoalStatus.COMPLETED, GoalStatus.CANCELLED]):
                overdue.append(goal)
                
        return sorted(overdue, key=lambda g: g.target_date)
        
    def create_milestone(self,
                        title: str,
                        description: str,
                        due_date: datetime,
                        goal_id: str,
                        deliverables: List[str] = None) -> Milestone:
        """Create a milestone for a goal"""
        
        milestone_id = f"milestone_{goal_id}_{len(self.milestones)}"
        
        milestone = Milestone(
            milestone_id=milestone_id,
            title=title,
            description=description,
            due_date=due_date,
            goal_id=goal_id,
            deliverables=deliverables or []
        )
        
        self.milestones[milestone_id] = milestone
        return milestone
        
    def complete_milestone(self, milestone_id: str) -> bool:
        """Mark a milestone as completed"""
        
        if milestone_id not in self.milestones:
            return False
            
        milestone = self.milestones[milestone_id]
        milestone.status = GoalStatus.COMPLETED
        milestone.completed_at = datetime.utcnow()
        
        # Update associated goal progress
        goal_milestones = [m for m in self.milestones.values() if m.goal_id == milestone.goal_id]
        completed_milestones = [m for m in goal_milestones if m.status == GoalStatus.COMPLETED]
        
        if goal_milestones:
            progress = len(completed_milestones) / len(goal_milestones)
            self.update_goal_progress(milestone.goal_id, progress)
            
        return True
        
    def generate_goal_hierarchy_from_vision(self, 
                                          company_vision: str,
                                          industry: str,
                                          target_year: int = None) -> Dict[str, Any]:
        """Generate a complete goal hierarchy from company vision"""
        
        if target_year is None:
            target_year = datetime.utcnow().year
            
        # Create yearly goal
        yearly_goal = self.create_yearly_goal(
            title=f"{company_vision} - {target_year}",
            description=f"Achieve the company vision in the {industry} industry",
            target_metrics={
                "revenue": 1000000,  # $1M ARR
                "users": 10000,      # 10K users
                "team_size": 25      # 25 employees
            },
            year=target_year
        )
        
        # Create quarterly goals
        quarterly_goals = []
        quarterly_themes = [
            ("Foundation & MVP", "Build core product and initial user base"),
            ("Growth & Scale", "Scale user acquisition and improve product"),
            ("Expansion & Optimization", "Expand features and optimize operations"),
            ("Consolidation & Planning", "Consolidate gains and plan next year")
        ]
        
        for quarter, (theme, description) in enumerate(quarterly_themes, 1):
            quarterly_goal = self.create_quarterly_goal(
                title=f"Q{quarter}: {theme}",
                description=description,
                quarter=quarter,
                year=target_year,
                parent_yearly_goal_id=yearly_goal.goal_id,
                target_metrics={
                    "revenue": yearly_goal.metrics["revenue"] * quarter / 4,
                    "users": yearly_goal.metrics["users"] * quarter / 4,
                    "team_size": yearly_goal.metrics["team_size"] * quarter / 4
                }
            )
            quarterly_goals.append(quarterly_goal)
            
        return {
            "yearly_goal": yearly_goal.to_dict(),
            "quarterly_goals": [q.to_dict() for q in quarterly_goals],
            "total_goals_created": 1 + len(quarterly_goals)
        }
        
    def save_to_file(self, filename: str) -> bool:
        """Save goals and milestones to file"""
        
        try:
            data = {
                "goals": {goal_id: goal.to_dict() for goal_id, goal in self.goals.items()},
                "milestones": {m_id: milestone.to_dict() for m_id, milestone in self.milestones.items()},
                "saved_at": datetime.utcnow().isoformat()
            }
            
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to save goals to file: {e}")
            return False
            
    def load_from_file(self, filename: str) -> bool:
        """Load goals and milestones from file"""
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                
            # Load goals
            self.goals = {}
            for goal_id, goal_data in data.get("goals", {}).items():
                self.goals[goal_id] = Goal.from_dict(goal_data)
                
            # Load milestones
            self.milestones = {}
            for m_id, milestone_data in data.get("milestones", {}).items():
                milestone = Milestone(
                    milestone_id=milestone_data["milestone_id"],
                    title=milestone_data["title"],
                    description=milestone_data["description"],
                    due_date=datetime.fromisoformat(milestone_data["due_date"]),
                    goal_id=milestone_data["goal_id"],
                    deliverables=milestone_data["deliverables"]
                )
                milestone.status = GoalStatus(milestone_data["status"])
                milestone.created_at = datetime.fromisoformat(milestone_data["created_at"])
                if milestone_data["completed_at"]:
                    milestone.completed_at = datetime.fromisoformat(milestone_data["completed_at"])
                    
                self.milestones[m_id] = milestone
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to load goals from file: {e}")
            return False

# Example usage
def main():
    """Example usage of GoalPlanner"""
    
    planner = GoalPlanner()
    
    # Generate goal hierarchy
    result = planner.generate_goal_hierarchy_from_vision(
        company_vision="Revolutionary AI-powered fashion platform",
        industry="fashion-tech"
    )
    
    print("Goal hierarchy created:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()