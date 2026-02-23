"""
Company Blueprint System
Defines the master plan and business model for the company
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
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

class BusinessModel:
    def __init__(self,
                 model_type: BusinessModelType,
                 revenue_streams: List[RevenueStream],
                 target_market: str,
                 value_proposition: str,
                 pricing_strategy: Dict[str, Any]):
        self.model_type = model_type
        self.revenue_streams = revenue_streams
        self.target_market = target_market
        self.value_proposition = value_proposition
        self.pricing_strategy = pricing_strategy
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_type": self.model_type.value,
            "revenue_streams": [stream.value for stream in self.revenue_streams],
            "target_market": self.target_market,
            "value_proposition": self.value_proposition,
            "pricing_strategy": self.pricing_strategy,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BusinessModel':
        model = cls(
            model_type=BusinessModelType(data["model_type"]),
            revenue_streams=[RevenueStream(stream) for stream in data["revenue_streams"]],
            target_market=data["target_market"],
            value_proposition=data["value_proposition"],
            pricing_strategy=data["pricing_strategy"]
        )
        model.created_at = datetime.fromisoformat(data["created_at"])
        model.updated_at = datetime.fromisoformat(data["updated_at"])
        return model

class CompanyBlueprint:
    def __init__(self):
        self.company_name: Optional[str] = None
        self.vision: Optional[str] = None
        self.mission: Optional[str] = None
        self.industry: Optional[str] = None
        self.business_model: Optional[BusinessModel] = None
        self.target_customers: List[Dict[str, Any]] = []
        self.core_features: List[str] = []
        self.competitive_advantages: List[str] = []
        self.financial_projections: Dict[str, Any] = {}
        self.team_structure: Dict[str, Any] = {}
        self.technology_stack: Dict[str, List[str]] = {}
        self.go_to_market_strategy: Dict[str, Any] = {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def set_company_basics(self,
                          company_name: str,
                          vision: str,
                          mission: str,
                          industry: str) -> None:
        """Set basic company information"""
        
        self.company_name = company_name
        self.vision = vision
        self.mission = mission
        self.industry = industry
        self.updated_at = datetime.utcnow()
        
    def set_business_model(self,
                          model_type: BusinessModelType,
                          revenue_streams: List[RevenueStream],
                          target_market: str,
                          value_proposition: str,
                          pricing_strategy: Dict[str, Any]) -> None:
        """Set the business model"""
        
        self.business_model = BusinessModel(
            model_type=model_type,
            revenue_streams=revenue_streams,
            target_market=target_market,
            value_proposition=value_proposition,
            pricing_strategy=pricing_strategy
        )
        self.updated_at = datetime.utcnow()
        
    def add_target_customer(self,
                           segment_name: str,
                           demographics: Dict[str, Any],
                           pain_points: List[str],
                           buying_behavior: Dict[str, Any]) -> None:
        """Add a target customer segment"""
        
        customer_segment = {
            "segment_name": segment_name,
            "demographics": demographics,
            "pain_points": pain_points,
            "buying_behavior": buying_behavior,
            "added_at": datetime.utcnow().isoformat()
        }
        
        self.target_customers.append(customer_segment)
        self.updated_at = datetime.utcnow()
        
    def set_core_features(self, features: List[str]) -> None:
        """Set core product features"""
        
        self.core_features = features
        self.updated_at = datetime.utcnow()
        
    def set_competitive_advantages(self, advantages: List[str]) -> None:
        """Set competitive advantages"""
        
        self.competitive_advantages = advantages
        self.updated_at = datetime.utcnow()
        
    def set_financial_projections(self,
                                 year_1_revenue: float,
                                 year_3_revenue: float,
                                 initial_funding_needed: float,
                                 break_even_month: int,
                                 customer_acquisition_cost: float,
                                 lifetime_value: float) -> None:
        """Set financial projections"""
        
        self.financial_projections = {
            "year_1_revenue": year_1_revenue,
            "year_3_revenue": year_3_revenue,
            "initial_funding_needed": initial_funding_needed,
            "break_even_month": break_even_month,
            "customer_acquisition_cost": customer_acquisition_cost,
            "lifetime_value": lifetime_value,
            "ltv_cac_ratio": lifetime_value / customer_acquisition_cost if customer_acquisition_cost > 0 else 0,
            "updated_at": datetime.utcnow().isoformat()
        }
        self.updated_at = datetime.utcnow()
        
    def set_technology_stack(self,
                           frontend: List[str],
                           backend: List[str],
                           database: List[str],
                           infrastructure: List[str],
                           ai_ml: List[str] = None) -> None:
        """Set technology stack"""
        
        self.technology_stack = {
            "frontend": frontend,
            "backend": backend,
            "database": database,
            "infrastructure": infrastructure,
            "ai_ml": ai_ml or [],
            "updated_at": datetime.utcnow().isoformat()
        }
        self.updated_at = datetime.utcnow()
        
    def set_go_to_market_strategy(self,
                                 launch_strategy: str,
                                 marketing_channels: List[str],
                                 sales_strategy: str,
                                 partnership_strategy: str,
                                 pricing_model: str) -> None:
        """Set go-to-market strategy"""
        
        self.go_to_market_strategy = {
            "launch_strategy": launch_strategy,
            "marketing_channels": marketing_channels,
            "sales_strategy": sales_strategy,
            "partnership_strategy": partnership_strategy,
            "pricing_model": pricing_model,
            "updated_at": datetime.utcnow().isoformat()
        }
        self.updated_at = datetime.utcnow()
        
    def set_team_structure(self,
                          founding_team: List[Dict[str, str]],
                          hiring_plan: Dict[str, Any],
                          advisory_board: List[Dict[str, str]] = None) -> None:
        """Set team structure and hiring plan"""
        
        self.team_structure = {
            "founding_team": founding_team,
            "hiring_plan": hiring_plan,
            "advisory_board": advisory_board or [],
            "updated_at": datetime.utcnow().isoformat()
        }
        self.updated_at = datetime.utcnow()
        
    def generate_from_vision(self, vision: str, industry: str) -> Dict[str, Any]:
        """Generate a complete blueprint from vision and industry"""
        
        # Extract company name from vision (simple heuristic)
        company_name = self._extract_company_name_from_vision(vision)
        
        # Set basic info
        self.set_company_basics(
            company_name=company_name,
            vision=vision,
            mission=f"To revolutionize the {industry} industry through innovative technology",
            industry=industry
        )
        
        # Determine business model based on industry
        business_model_mapping = {
            "saas": BusinessModelType.SAAS,
            "software": BusinessModelType.SAAS,
            "ecommerce": BusinessModelType.ECOMMERCE,
            "retail": BusinessModelType.ECOMMERCE,
            "marketplace": BusinessModelType.MARKETPLACE,
            "fintech": BusinessModelType.SAAS,
            "healthtech": BusinessModelType.SAAS,
            "edtech": BusinessModelType.FREEMIUM,
            "media": BusinessModelType.ADVERTISING,
            "consulting": BusinessModelType.CONSULTING
        }
        
        model_type = business_model_mapping.get(industry.lower(), BusinessModelType.SAAS)
        
        # Set business model
        revenue_streams = self._get_revenue_streams_for_model(model_type)
        pricing_strategy = self._get_pricing_strategy_for_model(model_type)
        
        self.set_business_model(
            model_type=model_type,
            revenue_streams=revenue_streams,
            target_market=f"{industry.title()} professionals and businesses",
            value_proposition=f"Streamline and optimize {industry} operations with cutting-edge technology",
            pricing_strategy=pricing_strategy
        )
        
        # Set core features based on industry
        core_features = self._get_core_features_for_industry(industry)
        self.set_core_features(core_features)
        
        # Set competitive advantages
        advantages = [
            "AI-powered automation",
            "User-friendly interface",
            "Scalable architecture",
            "24/7 customer support",
            "Competitive pricing"
        ]
        self.set_competitive_advantages(advantages)
        
        # Set financial projections
        self.set_financial_projections(
            year_1_revenue=500000,  # $500K
            year_3_revenue=5000000,  # $5M
            initial_funding_needed=1000000,  # $1M
            break_even_month=18,
            customer_acquisition_cost=200,
            lifetime_value=2400
        )
        
        # Set technology stack
        tech_stack = self._get_tech_stack_for_industry(industry)
        self.set_technology_stack(**tech_stack)
        
        # Set go-to-market strategy
        self.set_go_to_market_strategy(
            launch_strategy="Beta launch with early adopters",
            marketing_channels=["Content marketing", "Social media", "Industry events", "Partnerships"],
            sales_strategy="Inside sales with product-led growth",
            partnership_strategy="Strategic partnerships with industry leaders",
            pricing_model="Freemium with premium tiers"
        )
        
        # Add target customer segments
        self._add_default_customer_segments(industry)
        
        return {
            "success": True,
            "company_name": self.company_name,
            "industry": self.industry,
            "business_model": self.business_model.model_type.value if self.business_model else None,
            "core_features_count": len(self.core_features),
            "customer_segments_count": len(self.target_customers)
        }
        
    def _extract_company_name_from_vision(self, vision: str) -> str:
        """Extract a company name from the vision statement"""
        
        # Simple heuristic - look for key words and create a name
        vision_lower = vision.lower()
        
        if "fashion" in vision_lower:
            return "StyleTech"
        elif "food" in vision_lower or "restaurant" in vision_lower:
            return "FoodieApp"
        elif "health" in vision_lower or "medical" in vision_lower:
            return "HealthTech"
        elif "education" in vision_lower or "learning" in vision_lower:
            return "EduPlatform"
        elif "finance" in vision_lower or "payment" in vision_lower:
            return "FinanceFlow"
        elif "music" in vision_lower or "audio" in vision_lower:
            return "SoundWave"
        elif "travel" in vision_lower or "booking" in vision_lower:
            return "TravelEase"
        else:
            return "InnovateCorp"
            
    def _get_revenue_streams_for_model(self, model_type: BusinessModelType) -> List[RevenueStream]:
        """Get appropriate revenue streams for business model type"""
        
        mapping = {
            BusinessModelType.SAAS: [RevenueStream.SUBSCRIPTION],
            BusinessModelType.ECOMMERCE: [RevenueStream.ONE_TIME, RevenueStream.COMMISSION],
            BusinessModelType.MARKETPLACE: [RevenueStream.COMMISSION, RevenueStream.SUBSCRIPTION],
            BusinessModelType.FREEMIUM: [RevenueStream.FREEMIUM, RevenueStream.SUBSCRIPTION],
            BusinessModelType.SUBSCRIPTION: [RevenueStream.SUBSCRIPTION],
            BusinessModelType.ADVERTISING: [RevenueStream.ADVERTISING],
            BusinessModelType.TRANSACTION: [RevenueStream.COMMISSION],
            BusinessModelType.CONSULTING: [RevenueStream.ONE_TIME, RevenueStream.SUBSCRIPTION]
        }
        
        return mapping.get(model_type, [RevenueStream.SUBSCRIPTION])
        
    def _get_pricing_strategy_for_model(self, model_type: BusinessModelType) -> Dict[str, Any]:
        """Get pricing strategy for business model type"""
        
        if model_type == BusinessModelType.SAAS:
            return {
                "model": "tiered_subscription",
                "tiers": [
                    {"name": "Starter", "price": 29, "features": ["Basic features", "Email support"]},
                    {"name": "Professional", "price": 99, "features": ["Advanced features", "Priority support", "API access"]},
                    {"name": "Enterprise", "price": 299, "features": ["All features", "24/7 support", "Custom integrations"]}
                ]
            }
        elif model_type == BusinessModelType.FREEMIUM:
            return {
                "model": "freemium",
                "free_tier": {"features": ["Basic features", "Limited usage"]},
                "paid_tiers": [
                    {"name": "Pro", "price": 19, "features": ["Unlimited usage", "Premium features"]},
                    {"name": "Business", "price": 49, "features": ["Team features", "Advanced analytics"]}
                ]
            }
        else:
            return {
                "model": "custom",
                "description": "Pricing varies based on usage and requirements"
            }
            
    def _get_core_features_for_industry(self, industry: str) -> List[str]:
        """Get core features based on industry"""
        
        feature_mapping = {
            "saas": ["User management", "Dashboard", "Analytics", "API", "Integrations"],
            "ecommerce": ["Product catalog", "Shopping cart", "Payment processing", "Order management", "Inventory tracking"],
            "fintech": ["Account management", "Transaction processing", "Security", "Compliance", "Reporting"],
            "healthtech": ["Patient management", "Appointment scheduling", "Medical records", "Telemedicine", "Billing"],
            "edtech": ["Course management", "Student tracking", "Assessment tools", "Video conferencing", "Progress analytics"],
            "fashion": ["Product showcase", "Size guide", "Style recommendations", "Inventory management", "Order tracking"]
        }
        
        return feature_mapping.get(industry.lower(), ["Core functionality", "User interface", "Data management", "Security", "Analytics"])
        
    def _get_tech_stack_for_industry(self, industry: str) -> Dict[str, List[str]]:
        """Get technology stack recommendations for industry"""
        
        return {
            "frontend": ["React", "TypeScript", "Tailwind CSS"],
            "backend": ["Node.js", "Express", "Python", "FastAPI"],
            "database": ["PostgreSQL", "Redis"],
            "infrastructure": ["AWS", "Docker", "Kubernetes"],
            "ai_ml": ["OpenAI API", "TensorFlow", "Scikit-learn"] if industry.lower() in ["ai", "ml", "data"] else []
        }
        
    def _add_default_customer_segments(self, industry: str) -> None:
        """Add default customer segments for industry"""
        
        if industry.lower() == "saas":
            self.add_target_customer(
                segment_name="Small Businesses",
                demographics={"size": "1-50 employees", "revenue": "$100K-$1M"},
                pain_points=["Manual processes", "Lack of automation", "Limited resources"],
                buying_behavior={"decision_maker": "Owner/Manager", "budget": "$100-$500/month"}
            )
            
            self.add_target_customer(
                segment_name="Enterprise",
                demographics={"size": "500+ employees", "revenue": "$10M+"},
                pain_points=["Scalability issues", "Integration challenges", "Compliance requirements"],
                buying_behavior={"decision_maker": "IT Director", "budget": "$1000+/month"}
            )
        else:
            # Generic segments
            self.add_target_customer(
                segment_name="Early Adopters",
                demographics={"age": "25-40", "tech_savvy": True},
                pain_points=["Current solutions are outdated", "Looking for innovation"],
                buying_behavior={"decision_speed": "Fast", "price_sensitivity": "Low"}
            )
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert blueprint to dictionary"""
        
        return {
            "company_name": self.company_name,
            "vision": self.vision,
            "mission": self.mission,
            "industry": self.industry,
            "business_model": self.business_model.to_dict() if self.business_model else None,
            "target_customers": self.target_customers,
            "core_features": self.core_features,
            "competitive_advantages": self.competitive_advantages,
            "financial_projections": self.financial_projections,
            "team_structure": self.team_structure,
            "technology_stack": self.technology_stack,
            "go_to_market_strategy": self.go_to_market_strategy,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
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
            
    def load_from_file(self, filename: str) -> bool:
        """Load blueprint from file"""
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                
            self.company_name = data.get("company_name")
            self.vision = data.get("vision")
            self.mission = data.get("mission")
            self.industry = data.get("industry")
            
            if data.get("business_model"):
                self.business_model = BusinessModel.from_dict(data["business_model"])
                
            self.target_customers = data.get("target_customers", [])
            self.core_features = data.get("core_features", [])
            self.competitive_advantages = data.get("competitive_advantages", [])
            self.financial_projections = data.get("financial_projections", {})
            self.team_structure = data.get("team_structure", {})
            self.technology_stack = data.get("technology_stack", {})
            self.go_to_market_strategy = data.get("go_to_market_strategy", {})
            
            if data.get("created_at"):
                self.created_at = datetime.fromisoformat(data["created_at"])
            if data.get("updated_at"):
                self.updated_at = datetime.fromisoformat(data["updated_at"])
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to load blueprint: {e}")
            return False

# Example usage
def main():
    """Example usage of CompanyBlueprint"""
    
    blueprint = CompanyBlueprint()
    
    # Generate blueprint from vision
    result = blueprint.generate_from_vision(
        vision="Revolutionary AI-powered fashion platform that helps people discover their perfect style",
        industry="fashion"
    )
    
    print("Company blueprint created:")
    print(json.dumps(result, indent=2))
    
    # Save blueprint
    blueprint.save_to_file("company_blueprint.json")

if __name__ == "__main__":
    main()