"""
Company Blueprint System - Dataclass Version
Compatible with CEO Agent and LLM integration
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class BusinessModelType(Enum):
    SAAS = "saas"
    ECOMMERCE = "ecommerce"
    MARKETPLACE = "marketplace"
    FREEMIUM = "freemium"
    SUBSCRIPTION = "subscription"
    ADVERTISING = "advertising"
    TRANSACTION = "transaction"
    CONSULTING = "consulting"

class RevenueStream(Enum):
    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"
    COMMISSION = "commission"
    ADVERTISING = "advertising"
    LICENSING = "licensing"
    FREEMIUM = "freemium"

@dataclass
class TargetMarket:
    """Target market definition"""
    primary_segment: str
    demographics: List[str] = field(default_factory=list)
    psychographics: List[str] = field(default_factory=list)
    size_estimate: int = 0
    pain_points: List[str] = field(default_factory=list)
    secondary_segments: List[str] = field(default_factory=list)
    geographic_focus: List[str] = field(default_factory=lambda: ["Global"])
    market_size: Optional[str] = None

@dataclass
class BusinessModel:
    """Business model definition"""
    model_type: BusinessModelType = BusinessModelType.SAAS
    revenue_streams: List[RevenueStream] = field(default_factory=lambda: [RevenueStream.SUBSCRIPTION])
    target_market: str = "General market"
    value_proposition: str = "Innovative solution"
    pricing_strategy: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CompanyBlueprint:
    """Complete company blueprint with all business details"""
    name: str  # Changed from company_name to name
    vision: str
    mission: str
    industry: str
    target_market: TargetMarket
    key_features: List[str] = field(default_factory=list)  # Changed from core_features
    
    # Enhanced fields for comprehensive business planning
    business_model: str = "subscription"
    value_proposition: str = "Creating value for customers"
    competitive_advantages: List[str] = field(default_factory=list)
    revenue_projections: Dict[str, float] = field(default_factory=dict)
    funding_requirements: float = 0.0
    team_requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Opportunity assessment
    opportunity_score: float = 0.0
    risk_level: str = "medium"
    recommended_next_steps: List[str] = field(default_factory=list)
    time_to_revenue_months: int = 6
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    founder_dream: str = ""
    analysis_confidence: float = 0.8
    
    # Legacy fields for backward compatibility
    financial_projections: Dict[str, Any] = field(default_factory=dict)
    team_structure: Dict[str, Any] = field(default_factory=dict)
    technology_stack: Dict[str, List[str]] = field(default_factory=dict)
    go_to_market_strategy: Dict[str, Any] = field(default_factory=dict)
    target_customers: List[Dict[str, Any]] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def __post_init__(self):
        if self.business_model is None:
            self.business_model = BusinessModel()
        if self.target_market is None:
            self.target_market = TargetMarket(primary_segment="General Market")
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert blueprint to dictionary"""
        return {
            "company_name": self.company_name,
            "vision": self.vision,
            "mission": self.mission,
            "industry": self.industry,
            "business_model": {
                "model_type": self.business_model.model_type.value,
                "revenue_streams": [stream.value for stream in self.business_model.revenue_streams],
                "target_market": self.business_model.target_market,
                "value_proposition": self.business_model.value_proposition,
                "pricing_strategy": self.business_model.pricing_strategy
            } if self.business_model else None,
            "target_market": {
                "primary_segment": self.target_market.primary_segment,
                "secondary_segments": self.target_market.secondary_segments,
                "demographics": self.target_market.demographics,
                "geographic_focus": self.target_market.geographic_focus,
                "market_size": self.target_market.market_size
            } if self.target_market else None,
            "core_features": self.core_features,
            "competitive_advantages": self.competitive_advantages,
            "financial_projections": self.financial_projections,
            "team_structure": self.team_structure,
            "technology_stack": self.technology_stack,
            "go_to_market_strategy": self.go_to_market_strategy,
            "target_customers": self.target_customers,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
    def save_to_file(self, filename: str) -> bool:
        """Save blueprint to file"""
        try:
            with open(filename, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save blueprint: {e}")
            return False