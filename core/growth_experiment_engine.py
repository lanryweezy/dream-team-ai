"""
Growth Experiment Manager Engine
A/B testing framework, growth hack tracking, and conversion optimization
Provides comprehensive growth experimentation and optimization capabilities
"""

import json
import logging
import asyncio
import random
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics
import math

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class ExperimentType(Enum):
    AB_TEST = "ab_test"
    MULTIVARIATE = "multivariate"
    SPLIT_URL = "split_url"
    FEATURE_FLAG = "feature_flag"
    GROWTH_HACK = "growth_hack"
    FUNNEL_OPTIMIZATION = "funnel_optimization"

class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ExperimentCategory(Enum):
    ACQUISITION = "acquisition"
    ACTIVATION = "activation"
    RETENTION = "retention"
    REVENUE = "revenue"
    REFERRAL = "referral"
    ONBOARDING = "onboarding"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"

class StatisticalSignificance(Enum):
    NOT_SIGNIFICANT = "not_significant"
    TRENDING = "trending"
    SIGNIFICANT = "significant"
    HIGHLY_SIGNIFICANT = "highly_significant"

@dataclass
class ExperimentVariant:
    """Individual experiment variant"""
    variant_id: str
    name: str
    description: str
    traffic_allocation: float  # 0.0 to 1.0
    
    # Implementation details
    changes: List[str] = field(default_factory=list)
    assets: Dict[str, str] = field(default_factory=dict)  # URLs, images, copy
    
    # Results
    visitors: int = 0
    conversions: int = 0
    conversion_rate: float = 0.0
    revenue: float = 0.0
    
    # Statistical analysis
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    p_value: float = 1.0
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class GrowthExperiment:
    """Complete growth experiment"""
    experiment_id: str
    name: str
    description: str
    hypothesis: str
    
    # Configuration
    experiment_type: ExperimentType
    category: ExperimentCategory
    status: ExperimentStatus = ExperimentStatus.DRAFT
    
    # Targeting
    target_audience: str = "all_users"
    traffic_percentage: float = 1.0  # Percentage of traffic to include
    
    # Variants
    variants: List[ExperimentVariant] = field(default_factory=list)
    
    # Success metrics
    primary_metric: str = "conversion_rate"
    secondary_metrics: List[str] = field(default_factory=list)
    success_criteria: Dict[str, float] = field(default_factory=dict)
    
    # Timeline
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: int = 14
    
    # Results
    total_visitors: int = 0
    statistical_significance: StatisticalSignificance = StatisticalSignificance.NOT_SIGNIFICANT
    winner_variant: Optional[str] = None
    lift_percentage: float = 0.0
    
    # Analysis
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Metadata
    created_by: str = "system"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class GrowthHack:
    """Individual growth hack or tactic"""
    hack_id: str
    name: str
    description: str
    category: ExperimentCategory
    
    # Implementation
    implementation_effort: str  # "low", "medium", "high"
    expected_impact: str  # "low", "medium", "high"
    time_to_implement: int  # days
    
    # Requirements
    required_resources: List[str] = field(default_factory=list)
    technical_requirements: List[str] = field(default_factory=list)
    
    # Tracking
    status: str = "idea"  # "idea", "planned", "implementing", "testing", "deployed", "retired"
    implemented_date: Optional[str] = None
    
    # Results
    impact_metrics: Dict[str, float] = field(default_factory=dict)
    success_score: float = 0.0  # 0-10
    
    # Learning
    lessons_learned: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class FunnelAnalysis:
    """Funnel conversion analysis"""
    funnel_id: str
    name: str
    steps: List[str]
    
    # Data
    step_conversions: Dict[str, int] = field(default_factory=dict)
    step_conversion_rates: Dict[str, float] = field(default_factory=dict)
    drop_off_points: List[str] = field(default_factory=list)
    
    # Analysis
    overall_conversion_rate: float = 0.0
    biggest_drop_off: str = ""
    optimization_opportunities: List[str] = field(default_factory=list)
    
    analysis_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class GrowthExperimentEngine:
    """
    Comprehensive growth experimentation and optimization system that provides:
    - A/B testing and multivariate testing framework
    - Growth hack ideation and tracking
    - Funnel analysis and optimization
    - Statistical significance testing
    - Conversion rate optimization
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.experiments: Dict[str, GrowthExperiment] = {}
        self.growth_hacks: Dict[str, GrowthHack] = {}
        self.funnel_analyses: Dict[str, FunnelAnalysis] = {}
        
        # Configuration
        self.significance_threshold = 0.05  # p-value threshold
        self.minimum_sample_size = 100
        self.minimum_conversions = 10
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample experiment data"""
        
        # Sample experiments
        sample_experiments = [
            GrowthExperiment(
                experiment_id="exp_001",
                name="Landing Page Headline Test",
                description="Test different headlines on the main landing page to improve conversion rates",
                hypothesis="A more benefit-focused headline will increase sign-up conversions by 15%",
                experiment_type=ExperimentType.AB_TEST,
                category=ExperimentCategory.CONVERSION,
                status=ExperimentStatus.RUNNING,
                primary_metric="sign_up_rate",
                secondary_metrics=["time_on_page", "bounce_rate"],
                success_criteria={"sign_up_rate": 0.15},  # 15% improvement
                duration_days=14,
                start_date=(datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
                variants=[
                    ExperimentVariant(
                        variant_id="control",
                        name="Control",
                        description="Original headline: 'Powerful Analytics for Your Business'",
                        traffic_allocation=0.5,
                        visitors=1250,
                        conversions=87,
                        conversion_rate=6.96,
                        changes=["Original headline"]
                    ),
                    ExperimentVariant(
                        variant_id="variant_a",
                        name="Benefit-Focused",
                        description="New headline: 'Increase Revenue by 30% with AI-Powered Analytics'",
                        traffic_allocation=0.5,
                        visitors=1180,
                        conversions=102,
                        conversion_rate=8.64,
                        changes=["New benefit-focused headline", "Updated subheading"]
                    )
                ],
                total_visitors=2430,
                statistical_significance=StatisticalSignificance.SIGNIFICANT,
                winner_variant="variant_a",
                lift_percentage=24.1
            ),
            GrowthExperiment(
                experiment_id="exp_002",
                name="Onboarding Flow Optimization",
                description="Simplify the onboarding process to reduce drop-off rates",
                hypothesis="Reducing onboarding steps from 5 to 3 will improve completion rate by 25%",
                experiment_type=ExperimentType.FUNNEL_OPTIMIZATION,
                category=ExperimentCategory.ACTIVATION,
                status=ExperimentStatus.RUNNING,
                primary_metric="onboarding_completion_rate",
                secondary_metrics=["time_to_complete", "user_satisfaction"],
                success_criteria={"onboarding_completion_rate": 0.25},
                duration_days=21,
                start_date=(datetime.now(timezone.utc) - timedelta(days=10)).isoformat(),
                variants=[
                    ExperimentVariant(
                        variant_id="control",
                        name="5-Step Onboarding",
                        description="Current 5-step onboarding process",
                        traffic_allocation=0.5,
                        visitors=890,
                        conversions=623,
                        conversion_rate=70.0
                    ),
                    ExperimentVariant(
                        variant_id="variant_a",
                        name="3-Step Onboarding",
                        description="Simplified 3-step onboarding process",
                        traffic_allocation=0.5,
                        visitors=920,
                        conversions=736,
                        conversion_rate=80.0
                    )
                ],
                total_visitors=1810,
                statistical_significance=StatisticalSignificance.HIGHLY_SIGNIFICANT,
                winner_variant="variant_a",
                lift_percentage=14.3
            ),
            GrowthExperiment(
                experiment_id="exp_003",
                name="Pricing Page CTA Test",
                description="Test different call-to-action buttons on pricing page",
                hypothesis="A more urgent CTA will increase trial sign-ups by 20%",
                experiment_type=ExperimentType.AB_TEST,
                category=ExperimentCategory.CONVERSION,
                status=ExperimentStatus.COMPLETED,
                primary_metric="trial_sign_up_rate",
                duration_days=14,
                start_date=(datetime.now(timezone.utc) - timedelta(days=21)).isoformat(),
                end_date=(datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
                variants=[
                    ExperimentVariant(
                        variant_id="control",
                        name="Standard CTA",
                        description="'Start Free Trial' button",
                        traffic_allocation=0.5,
                        visitors=2100,
                        conversions=147,
                        conversion_rate=7.0
                    ),
                    ExperimentVariant(
                        variant_id="variant_a",
                        name="Urgent CTA",
                        description="'Start Free Trial - Limited Time' button",
                        traffic_allocation=0.5,
                        visitors=2050,
                        conversions=164,
                        conversion_rate=8.0
                    )
                ],
                total_visitors=4150,
                statistical_significance=StatisticalSignificance.SIGNIFICANT,
                winner_variant="variant_a",
                lift_percentage=14.3,
                insights=[
                    "Urgency messaging increases conversion rates",
                    "Users respond well to time-sensitive offers",
                    "CTA button color and text both matter"
                ],
                recommendations=[
                    "Implement winning variant across all CTAs",
                    "Test additional urgency messaging",
                    "Consider limited-time offers for new users"
                ]
            )
        ]
        
        for experiment in sample_experiments:
            self.experiments[experiment.experiment_id] = experiment
        
        # Sample growth hacks
        sample_hacks = [
            GrowthHack(
                hack_id="hack_001",
                name="Referral Program Launch",
                description="Implement a referral program giving existing users credits for successful referrals",
                category=ExperimentCategory.REFERRAL,
                implementation_effort="medium",
                expected_impact="high",
                time_to_implement=21,
                required_resources=["Product Manager", "Engineer", "Designer"],
                technical_requirements=["Referral tracking system", "Credit management", "Email notifications"],
                status="implementing",
                impact_metrics={"new_user_acquisition": 0.25, "user_engagement": 0.15}
            ),
            GrowthHack(
                hack_id="hack_002",
                name="Exit-Intent Popup",
                description="Show a special offer popup when users are about to leave the pricing page",
                category=ExperimentCategory.CONVERSION,
                implementation_effort="low",
                expected_impact="medium",
                time_to_implement=3,
                required_resources=["Developer"],
                technical_requirements=["Exit-intent detection", "Popup modal"],
                status="testing",
                implemented_date=(datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
                impact_metrics={"conversion_rate": 0.12},
                success_score=7.5
            ),
            GrowthHack(
                hack_id="hack_003",
                name="Social Proof Notifications",
                description="Display real-time notifications of other users signing up or upgrading",
                category=ExperimentCategory.CONVERSION,
                implementation_effort="low",
                expected_impact="medium",
                time_to_implement=5,
                required_resources=["Developer", "Designer"],
                technical_requirements=["Real-time notification system", "User activity tracking"],
                status="deployed",
                implemented_date=(datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),
                impact_metrics={"conversion_rate": 0.18, "time_on_site": 0.22},
                success_score=8.2,
                lessons_learned=[
                    "Social proof significantly increases trust",
                    "Real-time notifications create urgency",
                    "Placement on page matters for effectiveness"
                ]
            )
        ]
        
        for hack in sample_hacks:
            self.growth_hacks[hack.hack_id] = hack
    
    async def create_experiment(self, experiment_data: Dict[str, Any]) -> GrowthExperiment:
        """Create a new growth experiment"""
        
        try:
            logger.info(f"Creating experiment: {experiment_data.get('name')}")
            
            experiment = GrowthExperiment(
                experiment_id=f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=experiment_data["name"],
                description=experiment_data["description"],
                hypothesis=experiment_data["hypothesis"],
                experiment_type=ExperimentType(experiment_data["experiment_type"]),
                category=ExperimentCategory(experiment_data["category"]),
                primary_metric=experiment_data["primary_metric"],
                secondary_metrics=experiment_data.get("secondary_metrics", []),
                success_criteria=experiment_data.get("success_criteria", {}),
                duration_days=experiment_data.get("duration_days", 14),
                target_audience=experiment_data.get("target_audience", "all_users"),
                traffic_percentage=experiment_data.get("traffic_percentage", 1.0)
            )
            
            # Create variants
            for variant_data in experiment_data.get("variants", []):
                variant = ExperimentVariant(
                    variant_id=variant_data["variant_id"],
                    name=variant_data["name"],
                    description=variant_data["description"],
                    traffic_allocation=variant_data["traffic_allocation"],
                    changes=variant_data.get("changes", []),
                    assets=variant_data.get("assets", {})
                )
                experiment.variants.append(variant)
            
            # Validate experiment
            await self._validate_experiment(experiment)
            
            # Store experiment
            self.experiments[experiment.experiment_id] = experiment
            
            logger.info(f"Created experiment: {experiment.experiment_id}")
            return experiment
            
        except Exception as e:
            logger.error(f"Failed to create experiment: {e}")
            raise
    
    async def _validate_experiment(self, experiment: GrowthExperiment):
        """Validate experiment configuration"""
        
        # Check traffic allocation
        total_allocation = sum(variant.traffic_allocation for variant in experiment.variants)
        if abs(total_allocation - 1.0) > 0.01:
            raise ValueError(f"Traffic allocation must sum to 1.0, got {total_allocation}")
        
        # Check minimum variants
        if len(experiment.variants) < 2:
            raise ValueError("Experiment must have at least 2 variants")
        
        # Check success criteria
        if not experiment.success_criteria:
            logger.warning(f"No success criteria defined for experiment {experiment.experiment_id}")
    
    async def start_experiment(self, experiment_id: str) -> bool:
        """Start running an experiment"""
        
        try:
            if experiment_id not in self.experiments:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment = self.experiments[experiment_id]
            
            if experiment.status != ExperimentStatus.DRAFT:
                raise ValueError(f"Can only start experiments in draft status, current: {experiment.status}")
            
            experiment.status = ExperimentStatus.RUNNING
            experiment.start_date = datetime.now(timezone.utc).isoformat()
            experiment.updated_at = datetime.now(timezone.utc).isoformat()
            
            logger.info(f"Started experiment: {experiment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start experiment {experiment_id}: {e}")
            raise
    
    async def record_experiment_data(self, experiment_id: str, variant_id: str, visitor_count: int, conversion_count: int, revenue: float = 0.0):
        """Record experiment data for analysis"""
        
        try:
            if experiment_id not in self.experiments:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment = self.experiments[experiment_id]
            
            # Find variant
            variant = None
            for v in experiment.variants:
                if v.variant_id == variant_id:
                    variant = v
                    break
            
            if not variant:
                raise ValueError(f"Variant {variant_id} not found in experiment {experiment_id}")
            
            # Update variant data
            variant.visitors += visitor_count
            variant.conversions += conversion_count
            variant.revenue += revenue
            variant.conversion_rate = (variant.conversions / variant.visitors * 100) if variant.visitors > 0 else 0.0
            
            # Update experiment totals
            experiment.total_visitors = sum(v.visitors for v in experiment.variants)
            experiment.updated_at = datetime.now(timezone.utc).isoformat()
            
            # Perform statistical analysis
            await self._analyze_experiment_results(experiment)
            
            logger.info(f"Recorded data for experiment {experiment_id}, variant {variant_id}")
            
        except Exception as e:
            logger.error(f"Failed to record experiment data: {e}")
            raise
    
    async def _analyze_experiment_results(self, experiment: GrowthExperiment):
        """Perform statistical analysis on experiment results"""
        
        if len(experiment.variants) != 2:
            return  # Only handle A/B tests for now
        
        control = experiment.variants[0]
        variant = experiment.variants[1]
        
        # Check minimum sample size
        if control.visitors < self.minimum_sample_size or variant.visitors < self.minimum_sample_size:
            experiment.statistical_significance = StatisticalSignificance.NOT_SIGNIFICANT
            return
        
        # Check minimum conversions
        if control.conversions < self.minimum_conversions or variant.conversions < self.minimum_conversions:
            experiment.statistical_significance = StatisticalSignificance.NOT_SIGNIFICANT
            return
        
        # Calculate statistical significance using z-test
        p1 = control.conversions / control.visitors
        p2 = variant.conversions / variant.visitors
        
        # Pooled proportion
        p_pool = (control.conversions + variant.conversions) / (control.visitors + variant.visitors)
        
        # Standard error
        se = math.sqrt(p_pool * (1 - p_pool) * (1/control.visitors + 1/variant.visitors))
        
        # Z-score
        z_score = (p2 - p1) / se if se > 0 else 0
        
        # P-value (two-tailed test)
        p_value = 2 * (1 - self._normal_cdf(abs(z_score)))
        
        # Update variant p-values
        variant.p_value = p_value
        
        # Determine significance
        if p_value < 0.001:
            experiment.statistical_significance = StatisticalSignificance.HIGHLY_SIGNIFICANT
        elif p_value < self.significance_threshold:
            experiment.statistical_significance = StatisticalSignificance.SIGNIFICANT
        elif p_value < 0.1:
            experiment.statistical_significance = StatisticalSignificance.TRENDING
        else:
            experiment.statistical_significance = StatisticalSignificance.NOT_SIGNIFICANT
        
        # Calculate lift
        if p1 > 0:
            experiment.lift_percentage = ((p2 - p1) / p1) * 100
        
        # Determine winner
        if experiment.statistical_significance in [StatisticalSignificance.SIGNIFICANT, StatisticalSignificance.HIGHLY_SIGNIFICANT]:
            if p2 > p1:
                experiment.winner_variant = variant.variant_id
            else:
                experiment.winner_variant = control.variant_id
        
        # Calculate confidence intervals
        for v in experiment.variants:
            if v.visitors > 0:
                p = v.conversions / v.visitors
                se = math.sqrt(p * (1 - p) / v.visitors)
                margin = 1.96 * se  # 95% confidence interval
                v.confidence_interval = (max(0, p - margin), min(1, p + margin))
    
    def _normal_cdf(self, x: float) -> float:
        """Approximate normal cumulative distribution function"""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    async def complete_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Complete an experiment and generate final results"""
        
        try:
            if experiment_id not in self.experiments:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment = self.experiments[experiment_id]
            
            if experiment.status != ExperimentStatus.RUNNING:
                raise ValueError(f"Can only complete running experiments, current: {experiment.status}")
            
            experiment.status = ExperimentStatus.COMPLETED
            experiment.end_date = datetime.now(timezone.utc).isoformat()
            experiment.updated_at = datetime.now(timezone.utc).isoformat()
            
            # Generate insights and recommendations
            await self._generate_experiment_insights(experiment)
            
            # Create results summary
            results = {
                "experiment_id": experiment.experiment_id,
                "name": experiment.name,
                "status": experiment.status.value,
                "statistical_significance": experiment.statistical_significance.value,
                "winner_variant": experiment.winner_variant,
                "lift_percentage": experiment.lift_percentage,
                "total_visitors": experiment.total_visitors,
                "variants": [
                    {
                        "variant_id": v.variant_id,
                        "name": v.name,
                        "visitors": v.visitors,
                        "conversions": v.conversions,
                        "conversion_rate": v.conversion_rate,
                        "confidence_interval": v.confidence_interval,
                        "p_value": v.p_value
                    }
                    for v in experiment.variants
                ],
                "insights": experiment.insights,
                "recommendations": experiment.recommendations
            }
            
            logger.info(f"Completed experiment: {experiment_id}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to complete experiment {experiment_id}: {e}")
            raise
    
    async def _generate_experiment_insights(self, experiment: GrowthExperiment):
        """Generate insights and recommendations from experiment results"""
        
        insights = []
        recommendations = []
        
        # Statistical significance insights
        if experiment.statistical_significance == StatisticalSignificance.HIGHLY_SIGNIFICANT:
            insights.append(f"Results are highly statistically significant (p < 0.001)")
            recommendations.append("Implement winning variant immediately")
        elif experiment.statistical_significance == StatisticalSignificance.SIGNIFICANT:
            insights.append(f"Results are statistically significant (p < 0.05)")
            recommendations.append("Implement winning variant with confidence")
        elif experiment.statistical_significance == StatisticalSignificance.TRENDING:
            insights.append("Results show a trending pattern but not statistically significant")
            recommendations.append("Consider running experiment longer or with larger sample size")
        else:
            insights.append("No statistically significant difference found")
            recommendations.append("Keep current version or test more dramatic changes")
        
        # Lift insights
        if abs(experiment.lift_percentage) > 20:
            insights.append(f"Large effect size detected: {experiment.lift_percentage:.1f}% lift")
        elif abs(experiment.lift_percentage) > 10:
            insights.append(f"Moderate effect size: {experiment.lift_percentage:.1f}% lift")
        elif abs(experiment.lift_percentage) > 5:
            insights.append(f"Small but meaningful effect: {experiment.lift_percentage:.1f}% lift")
        
        # Sample size insights
        total_visitors = experiment.total_visitors
        if total_visitors < 1000:
            insights.append("Small sample size - consider running longer for more reliable results")
        elif total_visitors > 10000:
            insights.append("Large sample size provides high confidence in results")
        
        # Category-specific recommendations
        if experiment.category == ExperimentCategory.CONVERSION:
            if experiment.winner_variant:
                recommendations.append("Apply learnings to other conversion points in the funnel")
            recommendations.append("Test additional conversion optimization tactics")
        
        elif experiment.category == ExperimentCategory.ONBOARDING:
            if experiment.winner_variant:
                recommendations.append("Monitor long-term user engagement and retention")
            recommendations.append("Test additional onboarding improvements")
        
        elif experiment.category == ExperimentCategory.RETENTION:
            recommendations.append("Track long-term retention metrics beyond experiment period")
            recommendations.append("Consider personalization based on user segments")
        
        experiment.insights = insights
        experiment.recommendations = recommendations
    
    async def create_growth_hack(self, hack_data: Dict[str, Any]) -> GrowthHack:
        """Create a new growth hack"""
        
        try:
            hack = GrowthHack(
                hack_id=f"hack_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=hack_data["name"],
                description=hack_data["description"],
                category=ExperimentCategory(hack_data["category"]),
                implementation_effort=hack_data["implementation_effort"],
                expected_impact=hack_data["expected_impact"],
                time_to_implement=hack_data["time_to_implement"],
                required_resources=hack_data.get("required_resources", []),
                technical_requirements=hack_data.get("technical_requirements", [])
            )
            
            self.growth_hacks[hack.hack_id] = hack
            
            logger.info(f"Created growth hack: {hack.hack_id}")
            return hack
            
        except Exception as e:
            logger.error(f"Failed to create growth hack: {e}")
            raise
    
    async def analyze_funnel(self, funnel_data: Dict[str, Any]) -> FunnelAnalysis:
        """Analyze conversion funnel"""
        
        try:
            logger.info(f"Analyzing funnel: {funnel_data.get('name')}")
            
            analysis = FunnelAnalysis(
                funnel_id=f"funnel_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                name=funnel_data["name"],
                steps=funnel_data["steps"],
                step_conversions=funnel_data["step_conversions"]
            )
            
            # Calculate conversion rates
            total_users = analysis.step_conversions[analysis.steps[0]]
            
            for i, step in enumerate(analysis.steps):
                conversions = analysis.step_conversions[step]
                if i == 0:
                    rate = 100.0  # First step is 100%
                else:
                    prev_conversions = analysis.step_conversions[analysis.steps[i-1]]
                    rate = (conversions / prev_conversions * 100) if prev_conversions > 0 else 0
                
                analysis.step_conversion_rates[step] = rate
            
            # Overall conversion rate
            final_conversions = analysis.step_conversions[analysis.steps[-1]]
            analysis.overall_conversion_rate = (final_conversions / total_users * 100) if total_users > 0 else 0
            
            # Find biggest drop-off
            biggest_drop = 0
            biggest_drop_step = ""
            
            for i in range(1, len(analysis.steps)):
                current_rate = analysis.step_conversion_rates[analysis.steps[i]]
                if 100 - current_rate > biggest_drop:
                    biggest_drop = 100 - current_rate
                    biggest_drop_step = analysis.steps[i]
            
            analysis.biggest_drop_off = biggest_drop_step
            
            # Identify drop-off points (conversion rate < 70%)
            for step, rate in analysis.step_conversion_rates.items():
                if rate < 70 and step != analysis.steps[0]:
                    analysis.drop_off_points.append(step)
            
            # Generate optimization opportunities
            analysis.optimization_opportunities = await self._generate_funnel_opportunities(analysis)
            
            self.funnel_analyses[analysis.funnel_id] = analysis
            
            logger.info(f"Completed funnel analysis: {analysis.funnel_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze funnel: {e}")
            raise
    
    async def _generate_funnel_opportunities(self, analysis: FunnelAnalysis) -> List[str]:
        """Generate optimization opportunities for funnel"""
        
        opportunities = []
        
        # Low conversion rate opportunities
        for step, rate in analysis.step_conversion_rates.items():
            if rate < 50 and step != analysis.steps[0]:
                opportunities.append(f"Critical: Optimize '{step}' step (only {rate:.1f}% conversion)")
            elif rate < 70 and step != analysis.steps[0]:
                opportunities.append(f"Improve '{step}' step conversion rate ({rate:.1f}%)")
        
        # Overall funnel opportunities
        if analysis.overall_conversion_rate < 5:
            opportunities.append("Overall funnel conversion is very low - consider major redesign")
        elif analysis.overall_conversion_rate < 15:
            opportunities.append("Overall funnel has room for improvement - test incremental changes")
        
        # Specific recommendations
        if analysis.biggest_drop_off:
            opportunities.append(f"Focus on biggest drop-off point: '{analysis.biggest_drop_off}'")
        
        opportunities.extend([
            "A/B test different messaging at each step",
            "Reduce friction by removing unnecessary form fields",
            "Add progress indicators to show completion status",
            "Implement exit-intent popups at drop-off points",
            "Test different page layouts and designs"
        ])
        
        return opportunities[:5]  # Return top 5 opportunities
    
    async def get_growth_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive growth experiment dashboard data"""
        
        try:
            # Experiment overview
            total_experiments = len(self.experiments)
            running_experiments = len([e for e in self.experiments.values() if e.status == ExperimentStatus.RUNNING])
            completed_experiments = len([e for e in self.experiments.values() if e.status == ExperimentStatus.COMPLETED])
            
            # Success metrics
            successful_experiments = len([
                e for e in self.experiments.values() 
                if e.status == ExperimentStatus.COMPLETED and e.statistical_significance in [StatisticalSignificance.SIGNIFICANT, StatisticalSignificance.HIGHLY_SIGNIFICANT]
            ])
            
            success_rate = (successful_experiments / max(completed_experiments, 1)) * 100
            
            # Recent experiments
            recent_experiments = sorted(
                self.experiments.values(),
                key=lambda x: x.updated_at,
                reverse=True
            )[:5]
            
            # Growth hacks overview
            total_hacks = len(self.growth_hacks)
            deployed_hacks = len([h for h in self.growth_hacks.values() if h.status == "deployed"])
            testing_hacks = len([h for h in self.growth_hacks.values() if h.status == "testing"])
            
            # Average impact
            deployed_hack_scores = [h.success_score for h in self.growth_hacks.values() if h.status == "deployed" and h.success_score > 0]
            avg_hack_impact = statistics.mean(deployed_hack_scores) if deployed_hack_scores else 0
            
            # Category distribution
            category_distribution = {}
            for category in ExperimentCategory:
                count = len([e for e in self.experiments.values() if e.category == category])
                if count > 0:
                    category_distribution[category.value] = count
            
            # Recent results
            recent_results = []
            for experiment in recent_experiments:
                if experiment.status == ExperimentStatus.COMPLETED:
                    recent_results.append({
                        "experiment_name": experiment.name,
                        "category": experiment.category.value,
                        "lift_percentage": experiment.lift_percentage,
                        "statistical_significance": experiment.statistical_significance.value,
                        "winner_variant": experiment.winner_variant,
                        "total_visitors": experiment.total_visitors
                    })
            
            # Active experiments
            active_experiments = [
                {
                    "experiment_id": e.experiment_id,
                    "name": e.name,
                    "category": e.category.value,
                    "status": e.status.value,
                    "total_visitors": e.total_visitors,
                    "days_running": (datetime.now(timezone.utc) - datetime.fromisoformat(e.start_date.replace('Z', '+00:00'))).days if e.start_date else 0,
                    "statistical_significance": e.statistical_significance.value
                }
                for e in self.experiments.values()
                if e.status == ExperimentStatus.RUNNING
            ]
            
            # Growth hack pipeline
            hack_pipeline = {}
            for status in ["idea", "planned", "implementing", "testing", "deployed"]:
                count = len([h for h in self.growth_hacks.values() if h.status == status])
                if count > 0:
                    hack_pipeline[status] = count
            
            dashboard_data = {
                "experiment_overview": {
                    "total_experiments": total_experiments,
                    "running_experiments": running_experiments,
                    "completed_experiments": completed_experiments,
                    "success_rate": round(success_rate, 1)
                },
                "growth_hack_overview": {
                    "total_hacks": total_hacks,
                    "deployed_hacks": deployed_hacks,
                    "testing_hacks": testing_hacks,
                    "average_impact_score": round(avg_hack_impact, 1)
                },
                "category_distribution": category_distribution,
                "recent_results": recent_results,
                "active_experiments": active_experiments,
                "growth_hack_pipeline": hack_pipeline,
                "recommendations": await self._generate_dashboard_recommendations()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get growth dashboard data: {e}")
            raise
    
    async def _generate_dashboard_recommendations(self) -> List[str]:
        """Generate dashboard-specific recommendations"""
        
        recommendations = []
        
        # Experiment recommendations
        running_count = len([e for e in self.experiments.values() if e.status == ExperimentStatus.RUNNING])
        
        if running_count == 0:
            recommendations.append("🚀 No experiments running - start testing to drive growth")
        elif running_count > 5:
            recommendations.append("⚠️ Many experiments running - ensure proper traffic allocation")
        
        # Success rate recommendations
        completed = [e for e in self.experiments.values() if e.status == ExperimentStatus.COMPLETED]
        if len(completed) >= 3:
            successful = len([e for e in completed if e.statistical_significance in [StatisticalSignificance.SIGNIFICANT, StatisticalSignificance.HIGHLY_SIGNIFICANT]])
            success_rate = successful / len(completed)
            
            if success_rate < 0.3:
                recommendations.append("📊 Low experiment success rate - test more dramatic changes")
            elif success_rate > 0.7:
                recommendations.append("🎯 High success rate - consider testing more ambitious hypotheses")
        
        # Growth hack recommendations
        deployed_hacks = [h for h in self.growth_hacks.values() if h.status == "deployed"]
        if len(deployed_hacks) < 3:
            recommendations.append("💡 Implement more growth hacks to accelerate growth")
        
        # Category recommendations
        category_counts = {}
        for e in self.experiments.values():
            category_counts[e.category] = category_counts.get(e.category, 0) + 1
        
        if category_counts.get(ExperimentCategory.RETENTION, 0) < 2:
            recommendations.append("🔄 Focus more on retention experiments - they compound over time")
        
        if category_counts.get(ExperimentCategory.REFERRAL, 0) == 0:
            recommendations.append("🤝 Test referral programs - they can provide sustainable growth")
        
        # Default recommendations
        if not recommendations:
            recommendations = [
                "📈 Continue systematic experimentation across all growth areas",
                "🎯 Focus on experiments with highest potential impact",
                "📊 Ensure proper statistical rigor in all tests"
            ]
        
        return recommendations

# Global growth experiment engine
growth_experiments = GrowthExperimentEngine()