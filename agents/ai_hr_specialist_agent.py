"""
AI HR Specialist Agent
Comprehensive human resources management with AI-powered insights
Handles recruitment, performance management, employee engagement, and compliance
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from core.enhanced_base_agent import EnhancedBaseAgent
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

@dataclass
class Employee:
    """Employee profile and data"""
    employee_id: str
    name: str
    email: str
    position: str
    department: str
    hire_date: str
    
    # Performance data
    performance_score: float  # 0-10
    goals_completion: float  # 0-100%
    last_review_date: Optional[str] = None
    
    # Engagement metrics
    engagement_score: float = 7.5  # 0-10
    satisfaction_score: float = 8.0  # 0-10
    retention_risk: str = "low"  # low, medium, high
    
    # Career development
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    career_goals: List[str] = field(default_factory=list)
    
    # Status
    status: str = "active"  # active, on_leave, terminated
    manager: Optional[str] = None
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class JobPosting:
    """Job posting and recruitment tracking"""
    job_id: str
    title: str
    department: str
    description: str
    requirements: List[str]
    
    # Recruitment metrics
    applications_received: int = 0
    interviews_scheduled: int = 0
    offers_made: int = 0
    hires_completed: int = 0
    
    # Status and timeline
    status: str = "active"  # active, paused, filled, cancelled
    posted_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_hire_date: Optional[str] = None
    
    # AI insights
    predicted_time_to_fill: Optional[int] = None  # days
    recommended_salary_range: Optional[Tuple[int, int]] = None
    skill_match_score: float = 0.0

class AIHRSpecialistAgent(EnhancedBaseAgent):
    """
    AI HR Specialist Agent that provides:
    - Employee lifecycle management
    - Performance tracking and reviews
    - Recruitment and talent acquisition
    - Employee engagement monitoring
    - HR compliance and policy management
    - Career development planning
    """
    
    def __init__(self):
        super().__init__(
            agent_id="ai_hr_specialist",
            name="AI HR Specialist",
            description="Comprehensive human resources management with AI insights",
            capabilities=[
                "employee_management",
                "performance_tracking",
                "recruitment_optimization",
                "engagement_monitoring",
                "compliance_management",
                "career_development"
            ]
        )
        
        # Employee database
        self.employees: Dict[str, Employee] = {}
        self.job_postings: Dict[str, JobPosting] = {}
        
        # HR metrics and benchmarks
        self.hr_benchmarks = {
            "engagement_target": 8.0,
            "performance_target": 7.5,
            "retention_rate_target": 0.90,
            "time_to_fill_target": 30,  # days
            "employee_satisfaction_target": 8.5
        }
        
        # Initialize sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize sample employee and job data"""
        
        # Sample employees
        sample_employees = [
            {
                "employee_id": "emp_001",
                "name": "Sarah Chen",
                "email": "sarah.chen@company.com",
                "position": "Product Manager",
                "department": "Product",
                "hire_date": "2023-03-15",
                "performance_score": 8.5,
                "goals_completion": 85.0,
                "engagement_score": 9.0,
                "satisfaction_score": 8.8,
                "retention_risk": "low",
                "skills": ["Product Strategy", "User Research", "Data Analysis"],
                "manager": "VP Product"
            },
            {
                "employee_id": "emp_002", 
                "name": "Alex Rodriguez",
                "email": "alex.rodriguez@company.com",
                "position": "Senior Developer",
                "department": "Engineering",
                "hire_date": "2022-08-20",
                "performance_score": 9.2,
                "goals_completion": 92.0,
                "engagement_score": 8.5,
                "satisfaction_score": 9.0,
                "retention_risk": "low",
                "skills": ["React", "Node.js", "Python", "AWS"],
                "manager": "Engineering Manager"
            },
            {
                "employee_id": "emp_003",
                "name": "Maya Patel",
                "email": "maya.patel@company.com", 
                "position": "Marketing Manager",
                "department": "Marketing",
                "hire_date": "2023-01-10",
                "performance_score": 7.8,
                "goals_completion": 78.0,
                "engagement_score": 7.2,
                "satisfaction_score": 7.5,
                "retention_risk": "medium",
                "skills": ["Digital Marketing", "Content Strategy", "Analytics"],
                "manager": "VP Marketing"
            }
        ]
        
        for emp_data in sample_employees:
            employee = Employee(**emp_data)
            self.employees[employee.employee_id] = employee
        
        # Sample job postings
        sample_jobs = [
            {
                "job_id": "job_001",
                "title": "Senior Frontend Developer",
                "department": "Engineering",
                "description": "Lead frontend development for our core product",
                "requirements": ["React", "TypeScript", "5+ years experience"],
                "applications_received": 45,
                "interviews_scheduled": 8,
                "offers_made": 2,
                "target_hire_date": "2025-11-15",
                "predicted_time_to_fill": 25,
                "recommended_salary_range": (120000, 150000)
            },
            {
                "job_id": "job_002",
                "title": "Customer Success Manager",
                "department": "Customer Success",
                "description": "Drive customer adoption and retention",
                "requirements": ["Customer Success experience", "SaaS background", "Communication skills"],
                "applications_received": 32,
                "interviews_scheduled": 6,
                "offers_made": 1,
                "target_hire_date": "2025-10-30",
                "predicted_time_to_fill": 20,
                "recommended_salary_range": (80000, 100000)
            }
        ]
        
        for job_data in sample_jobs:
            job = JobPosting(**job_data)
            self.job_postings[job.job_id] = job
    
    async def analyze_employee_performance(self, employee_id: str) -> Dict[str, Any]:
        """Analyze individual employee performance and provide insights"""
        
        try:
            if employee_id not in self.employees:
                raise ValueError(f"Employee {employee_id} not found")
            
            employee = self.employees[employee_id]
            
            # Performance analysis
            performance_analysis = {
                "employee_id": employee_id,
                "name": employee.name,
                "current_performance": {
                    "performance_score": employee.performance_score,
                    "goals_completion": employee.goals_completion,
                    "engagement_score": employee.engagement_score,
                    "satisfaction_score": employee.satisfaction_score
                },
                "performance_trend": "improving",  # Would calculate from historical data
                "strengths": [],
                "improvement_areas": [],
                "recommendations": [],
                "retention_risk": employee.retention_risk,
                "career_development": {
                    "current_skills": employee.skills,
                    "skill_gaps": [],
                    "recommended_training": [],
                    "career_path_options": []
                }
            }
            
            # Analyze performance levels
            if employee.performance_score >= 9.0:
                performance_analysis["strengths"].extend([
                    "Exceptional performance consistently",
                    "Exceeds expectations in key areas",
                    "Strong leadership potential"
                ])
                performance_analysis["recommendations"].extend([
                    "Consider for promotion opportunities",
                    "Assign stretch projects and leadership roles",
                    "Explore career advancement paths"
                ])
            elif employee.performance_score >= 7.5:
                performance_analysis["strengths"].extend([
                    "Solid performance across responsibilities",
                    "Meets expectations consistently",
                    "Reliable team contributor"
                ])
                performance_analysis["recommendations"].extend([
                    "Provide skill development opportunities",
                    "Set challenging but achievable goals",
                    "Consider lateral growth opportunities"
                ])
            else:
                performance_analysis["improvement_areas"].extend([
                    "Performance below expectations",
                    "Goals completion needs improvement",
                    "May benefit from additional support"
                ])
                performance_analysis["recommendations"].extend([
                    "Develop performance improvement plan",
                    "Provide additional training and mentoring",
                    "Schedule regular check-ins with manager"
                ])
            
            # Engagement analysis
            if employee.engagement_score < 7.0:
                performance_analysis["improvement_areas"].append("Low engagement score")
                performance_analysis["recommendations"].extend([
                    "Conduct engagement survey to identify issues",
                    "Explore role adjustment or new challenges",
                    "Improve manager-employee relationship"
                ])
            
            # Retention risk analysis
            if employee.retention_risk == "high":
                performance_analysis["recommendations"].extend([
                    "URGENT: Schedule retention conversation",
                    "Review compensation and benefits",
                    "Explore career development opportunities",
                    "Address any workplace concerns"
                ])
            elif employee.retention_risk == "medium":
                performance_analysis["recommendations"].extend([
                    "Monitor engagement closely",
                    "Provide growth opportunities",
                    "Regular career development discussions"
                ])
            
            # Career development recommendations
            if employee.department == "Engineering":
                performance_analysis["career_development"]["skill_gaps"] = [
                    "Cloud Architecture", "Machine Learning", "Leadership"
                ]
                performance_analysis["career_development"]["recommended_training"] = [
                    "AWS Solutions Architect Certification",
                    "Technical Leadership Course",
                    "Advanced Python for ML"
                ]
                performance_analysis["career_development"]["career_path_options"] = [
                    "Senior Developer → Tech Lead → Engineering Manager",
                    "Senior Developer → Principal Engineer → Staff Engineer",
                    "Senior Developer → Solutions Architect → VP Engineering"
                ]
            elif employee.department == "Product":
                performance_analysis["career_development"]["skill_gaps"] = [
                    "Data Science", "Growth Marketing", "Strategic Planning"
                ]
                performance_analysis["career_development"]["recommended_training"] = [
                    "Product Analytics Certification",
                    "Growth Product Management",
                    "Strategic Product Leadership"
                ]
            
            logger.info(f"Performance analysis completed for {employee.name}")
            return performance_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze employee performance: {e}")
            raise
    
    async def optimize_recruitment_process(self, job_id: str) -> Dict[str, Any]:
        """Optimize recruitment process with AI insights"""
        
        try:
            if job_id not in self.job_postings:
                raise ValueError(f"Job posting {job_id} not found")
            
            job = self.job_postings[job_id]
            
            # Calculate recruitment metrics
            application_to_interview_rate = (job.interviews_scheduled / max(job.applications_received, 1)) * 100
            interview_to_offer_rate = (job.offers_made / max(job.interviews_scheduled, 1)) * 100
            
            optimization_analysis = {
                "job_id": job_id,
                "job_title": job.title,
                "current_metrics": {
                    "applications_received": job.applications_received,
                    "interviews_scheduled": job.interviews_scheduled,
                    "offers_made": job.offers_made,
                    "application_to_interview_rate": round(application_to_interview_rate, 1),
                    "interview_to_offer_rate": round(interview_to_offer_rate, 1)
                },
                "benchmarks": {
                    "target_application_to_interview_rate": 20.0,
                    "target_interview_to_offer_rate": 30.0,
                    "target_time_to_fill": self.hr_benchmarks["time_to_fill_target"]
                },
                "optimization_recommendations": [],
                "process_improvements": [],
                "sourcing_strategies": [],
                "predicted_outcomes": {}
            }
            
            # Analyze application quality
            if application_to_interview_rate < 15.0:
                optimization_analysis["optimization_recommendations"].extend([
                    "Improve job description clarity and requirements",
                    "Enhance employer branding and company visibility",
                    "Optimize job posting on relevant platforms"
                ])
                optimization_analysis["sourcing_strategies"].extend([
                    "Target specialized job boards for this role",
                    "Leverage employee referral programs",
                    "Partner with technical recruiters"
                ])
            elif application_to_interview_rate > 30.0:
                optimization_analysis["optimization_recommendations"].extend([
                    "Tighten screening criteria to improve quality",
                    "Add pre-screening assessments",
                    "Refine job requirements to attract better matches"
                ])
            
            # Analyze interview conversion
            if interview_to_offer_rate < 20.0:
                optimization_analysis["process_improvements"].extend([
                    "Review interview process for candidate experience",
                    "Provide interview training for hiring managers",
                    "Streamline decision-making process"
                ])
            elif interview_to_offer_rate > 50.0:
                optimization_analysis["process_improvements"].extend([
                    "Raise interview standards and assessment rigor",
                    "Add technical assessments or case studies",
                    "Include more stakeholders in interview process"
                ])
            
            # Time to fill optimization
            if job.predicted_time_to_fill and job.predicted_time_to_fill > self.hr_benchmarks["time_to_fill_target"]:
                optimization_analysis["process_improvements"].extend([
                    "Accelerate interview scheduling",
                    "Reduce decision-making delays",
                    "Prepare offer packages in advance"
                ])
            
            # Salary competitiveness analysis
            if job.recommended_salary_range:
                min_salary, max_salary = job.recommended_salary_range
                market_position = "competitive"  # Would analyze against market data
                
                optimization_analysis["predicted_outcomes"] = {
                    "salary_competitiveness": market_position,
                    "estimated_acceptance_rate": 75.0,
                    "recommended_offer_strategy": "Target 75th percentile for top candidates"
                }
            
            # Department-specific recommendations
            if job.department == "Engineering":
                optimization_analysis["sourcing_strategies"].extend([
                    "Post on Stack Overflow Jobs and GitHub Jobs",
                    "Attend tech meetups and conferences",
                    "Partner with coding bootcamps and universities"
                ])
            elif job.department == "Marketing":
                optimization_analysis["sourcing_strategies"].extend([
                    "Leverage marketing professional networks",
                    "Post on marketing-specific job boards",
                    "Reach out through LinkedIn and industry groups"
                ])
            
            logger.info(f"Recruitment optimization completed for {job.title}")
            return optimization_analysis
            
        except Exception as e:
            logger.error(f"Failed to optimize recruitment process: {e}")
            raise
    
    async def monitor_employee_engagement(self) -> Dict[str, Any]:
        """Monitor and analyze employee engagement across the organization"""
        
        try:
            engagement_analysis = {
                "overall_metrics": {
                    "total_employees": len(self.employees),
                    "average_engagement": 0.0,
                    "average_satisfaction": 0.0,
                    "high_risk_employees": 0,
                    "engagement_trend": "stable"
                },
                "department_breakdown": {},
                "engagement_drivers": [],
                "risk_factors": [],
                "recommendations": [],
                "action_items": []
            }
            
            # Calculate overall metrics
            if self.employees:
                total_engagement = sum(emp.engagement_score for emp in self.employees.values())
                total_satisfaction = sum(emp.satisfaction_score for emp in self.employees.values())
                
                engagement_analysis["overall_metrics"]["average_engagement"] = round(total_engagement / len(self.employees), 1)
                engagement_analysis["overall_metrics"]["average_satisfaction"] = round(total_satisfaction / len(self.employees), 1)
                
                # Count high-risk employees
                high_risk_count = len([emp for emp in self.employees.values() if emp.retention_risk == "high"])
                engagement_analysis["overall_metrics"]["high_risk_employees"] = high_risk_count
            
            # Department breakdown
            departments = {}
            for employee in self.employees.values():
                dept = employee.department
                if dept not in departments:
                    departments[dept] = {
                        "employee_count": 0,
                        "total_engagement": 0.0,
                        "total_satisfaction": 0.0,
                        "high_risk_count": 0
                    }
                
                departments[dept]["employee_count"] += 1
                departments[dept]["total_engagement"] += employee.engagement_score
                departments[dept]["total_satisfaction"] += employee.satisfaction_score
                
                if employee.retention_risk == "high":
                    departments[dept]["high_risk_count"] += 1
            
            # Calculate department averages
            for dept, data in departments.items():
                if data["employee_count"] > 0:
                    engagement_analysis["department_breakdown"][dept] = {
                        "employee_count": data["employee_count"],
                        "average_engagement": round(data["total_engagement"] / data["employee_count"], 1),
                        "average_satisfaction": round(data["total_satisfaction"] / data["employee_count"], 1),
                        "high_risk_employees": data["high_risk_count"],
                        "risk_percentage": round((data["high_risk_count"] / data["employee_count"]) * 100, 1)
                    }
            
            # Identify engagement drivers and risk factors
            avg_engagement = engagement_analysis["overall_metrics"]["average_engagement"]
            
            if avg_engagement >= self.hr_benchmarks["engagement_target"]:
                engagement_analysis["engagement_drivers"].extend([
                    "Strong leadership and management quality",
                    "Clear career development opportunities",
                    "Positive company culture and values alignment",
                    "Competitive compensation and benefits"
                ])
            else:
                engagement_analysis["risk_factors"].extend([
                    "Below-target engagement scores",
                    "Potential management or leadership issues",
                    "Limited growth opportunities",
                    "Workplace culture concerns"
                ])
            
            # Generate recommendations
            if high_risk_count > 0:
                engagement_analysis["recommendations"].extend([
                    f"URGENT: Address {high_risk_count} high-risk employees immediately",
                    "Conduct exit interviews to understand retention issues",
                    "Review compensation and benefits competitiveness"
                ])
                engagement_analysis["action_items"].extend([
                    "Schedule one-on-one meetings with high-risk employees",
                    "Develop retention strategies for at-risk talent",
                    "Implement stay interviews for key employees"
                ])
            
            if avg_engagement < self.hr_benchmarks["engagement_target"]:
                engagement_analysis["recommendations"].extend([
                    "Conduct comprehensive employee engagement survey",
                    "Implement manager training programs",
                    "Review and improve internal communication"
                ])
                engagement_analysis["action_items"].extend([
                    "Launch pulse surveys for regular feedback",
                    "Create employee resource groups",
                    "Establish mentorship programs"
                ])
            
            # Department-specific recommendations
            for dept, data in engagement_analysis["department_breakdown"].items():
                if data["average_engagement"] < 7.0:
                    engagement_analysis["recommendations"].append(f"{dept} department needs focused engagement improvement")
                    engagement_analysis["action_items"].append(f"Conduct {dept} team building and culture initiatives")
            
            logger.info("Employee engagement monitoring completed")
            return engagement_analysis
            
        except Exception as e:
            logger.error(f"Failed to monitor employee engagement: {e}")
            raise
    
    async def generate_hr_insights(self) -> Dict[str, Any]:
        """Generate comprehensive HR insights and recommendations"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Calculate key HR metrics
            total_employees = len(self.employees)
            active_jobs = len([job for job in self.job_postings.values() if job.status == "active"])
            
            # Performance distribution
            high_performers = len([emp for emp in self.employees.values() if emp.performance_score >= 8.5])
            low_performers = len([emp for emp in self.employees.values() if emp.performance_score < 6.5])
            
            # Engagement metrics
            avg_engagement = sum(emp.engagement_score for emp in self.employees.values()) / max(total_employees, 1)
            avg_satisfaction = sum(emp.satisfaction_score for emp in self.employees.values()) / max(total_employees, 1)
            
            # Retention risk
            high_risk_retention = len([emp for emp in self.employees.values() if emp.retention_risk == "high"])
            medium_risk_retention = len([emp for emp in self.employees.values() if emp.retention_risk == "medium"])
            
            hr_insights = {
                "hr_health_score": 0.0,
                "workforce_metrics": {
                    "total_employees": total_employees,
                    "active_job_postings": active_jobs,
                    "high_performers_percentage": round((high_performers / max(total_employees, 1)) * 100, 1),
                    "low_performers_percentage": round((low_performers / max(total_employees, 1)) * 100, 1),
                    "average_engagement": round(avg_engagement, 1),
                    "average_satisfaction": round(avg_satisfaction, 1),
                    "retention_risk_high": high_risk_retention,
                    "retention_risk_medium": medium_risk_retention
                },
                "key_insights": [],
                "priority_actions": [],
                "trends": {
                    "engagement_trend": "stable",
                    "performance_trend": "improving",
                    "retention_trend": "stable"
                },
                "recommendations": []
            }
            
            # Calculate HR health score
            engagement_score = min(avg_engagement / self.hr_benchmarks["engagement_target"] * 25, 25)
            satisfaction_score = min(avg_satisfaction / self.hr_benchmarks["employee_satisfaction_target"] * 25, 25)
            performance_score = min((high_performers / max(total_employees, 1)) * 100 / 30 * 25, 25)  # 30% high performers target
            retention_score = max(25 - (high_risk_retention / max(total_employees, 1)) * 100 * 2.5, 0)  # Penalty for retention risk
            
            hr_insights["hr_health_score"] = round(engagement_score + satisfaction_score + performance_score + retention_score, 1)
            
            # Generate key insights
            if high_performers / max(total_employees, 1) > 0.3:
                hr_insights["key_insights"].append("🌟 Strong talent pool with high percentage of top performers")
            
            if avg_engagement >= self.hr_benchmarks["engagement_target"]:
                hr_insights["key_insights"].append("💪 Employee engagement meets or exceeds targets")
            else:
                hr_insights["key_insights"].append("⚠️ Employee engagement below target - needs attention")
                hr_insights["priority_actions"].append("Implement engagement improvement initiatives")
            
            if high_risk_retention > 0:
                hr_insights["key_insights"].append(f"🚨 {high_risk_retention} employees at high risk of leaving")
                hr_insights["priority_actions"].append("Address retention risks immediately")
            
            if low_performers > 0:
                hr_insights["key_insights"].append(f"📈 {low_performers} employees need performance improvement")
                hr_insights["priority_actions"].append("Develop performance improvement plans")
            
            # Generate recommendations
            if hr_insights["hr_health_score"] >= 80:
                hr_insights["recommendations"].extend([
                    "HR operations are performing excellently",
                    "Focus on maintaining high standards",
                    "Consider expanding team and capabilities"
                ])
            elif hr_insights["hr_health_score"] >= 60:
                hr_insights["recommendations"].extend([
                    "HR performance is good with room for improvement",
                    "Focus on engagement and retention initiatives",
                    "Strengthen performance management processes"
                ])
            else:
                hr_insights["recommendations"].extend([
                    "HR performance needs significant improvement",
                    "Conduct comprehensive HR audit",
                    "Implement immediate retention and engagement programs"
                ])
            
            # Recruitment insights
            if active_jobs > 0:
                hr_insights["key_insights"].append(f"📋 {active_jobs} active job postings - growth phase")
                hr_insights["recommendations"].append("Optimize recruitment processes for efficiency")
            
            logger.info("HR insights generation completed")
            return hr_insights
            
        except Exception as e:
            logger.error(f"Failed to generate HR insights: {e}")
            raise

# Global AI HR specialist agent
ai_hr_specialist = AIHRSpecialistAgent()