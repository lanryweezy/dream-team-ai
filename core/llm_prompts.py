"""
LLM Prompt Templates for Dream Machine System
Centralized prompt management for consistent LLM interactions
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class PromptTemplate:
    """Base class for prompt templates"""
    
    def __init__(self, template: str, required_vars: List[str] = None):
        self.template = template
        self.required_vars = required_vars or []
        
    def format(self, **kwargs) -> str:
        """Format template with provided variables"""
        # Check required variables
        missing_vars = [var for var in self.required_vars if var not in kwargs]
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
            
        return self.template.format(**kwargs)

class CEOPrompts:
    """Prompts for CEO Agent"""
    
    BLUEPRINT_CREATION = PromptTemplate(
        """You are an expert business strategist and CEO. Based on the founder's dream and vision, create a comprehensive company blueprint.

Founder's Dream: {dream}

Additional Context:
- Industry preferences: {industry_preferences}
- Budget constraints: {budget_constraints}
- Timeline: {timeline}
- Target market hints: {target_market_hints}

Please create a detailed company blueprint that includes:
1. Company name and tagline
2. Clear vision and mission statements
3. Industry classification
4. Target market analysis
5. Business model and revenue streams
6. Core product/service features
7. Competitive advantages
8. Go-to-market strategy
9. Financial projections (high-level)
10. Team structure recommendations
11. Technology stack suggestions
12. Key milestones and timeline

Make sure the blueprint is realistic, actionable, and aligned with the founder's vision while being commercially viable.""",
        required_vars=["dream", "industry_preferences", "budget_constraints", "timeline", "target_market_hints"]
    )
    
    DAILY_BRIEFING = PromptTemplate(
        """You are the CEO of {company_name}. Prepare a comprehensive daily briefing based on the current company status.

Current Status:
- Company Stage: {company_stage}
- Active Agents: {active_agents}
- Recent Achievements: {achievements}
- Current Budget: {budget_status}
- Pending Issues: {pending_issues}
- Market Conditions: {market_conditions}

Please provide:
1. Executive Summary (2-3 sentences)
2. Key Achievements from yesterday
3. Today's Priority Actions
4. Budget and Financial Status
5. Team Performance Insights
6. Market Opportunities
7. Risk Assessment
8. Strategic Recommendations
9. Decisions Needed
10. Tomorrow's Focus Areas

Keep it concise but comprehensive, focusing on actionable insights.""",
        required_vars=["company_name", "company_stage", "active_agents", "achievements", "budget_status", "pending_issues", "market_conditions"]
    )
    
    AGENT_COORDINATION = PromptTemplate(
        """You are coordinating work between multiple AI agents in your company. Analyze the current situation and provide coordination instructions.

Current Agent Status:
{agent_status}

Pending Tasks:
{pending_tasks}

Dependencies:
{task_dependencies}

Resource Constraints:
{resource_constraints}

Please provide:
1. Task prioritization and sequencing
2. Agent assignments and workload distribution
3. Dependency resolution plan
4. Resource allocation recommendations
5. Timeline adjustments if needed
6. Risk mitigation strategies
7. Communication plan between agents
8. Success metrics and checkpoints

Focus on efficiency, avoiding conflicts, and ensuring smooth collaboration.""",
        required_vars=["agent_status", "pending_tasks", "task_dependencies", "resource_constraints"]
    )

class FinancePrompts:
    """Prompts for Finance Agent"""
    
    EXPENSE_CATEGORIZATION = PromptTemplate(
        """You are a financial analyst. Categorize and analyze the following expense:

Expense Details:
- Amount: ${amount}
- Description: {description}
- Vendor: {vendor}
- Date: {date}
- Context: {context}

Please provide:
1. Primary category (e.g., Marketing, Development, Operations, Legal, etc.)
2. Subcategory (more specific classification)
3. Business justification assessment
4. Tax deductibility status
5. Recurring vs. one-time classification
6. Priority level (Essential, Important, Optional)
7. Cost optimization suggestions
8. Approval recommendation

Be thorough but concise in your analysis.""",
        required_vars=["amount", "description", "vendor", "date", "context"]
    )
    
    BUDGET_ANALYSIS = PromptTemplate(
        """You are a CFO analyzing the company's financial position. Create a comprehensive budget analysis.

Financial Data:
- Current Balance: ${current_balance}
- Monthly Revenue: ${monthly_revenue}
- Monthly Expenses: ${monthly_expenses}
- Expense Breakdown: {expense_breakdown}
- Revenue Trends: {revenue_trends}
- Upcoming Expenses: {upcoming_expenses}
- Business Goals: {business_goals}

Please provide:
1. Current Financial Health Assessment
2. Cash Flow Analysis
3. Burn Rate Calculation
4. Runway Estimation
5. Budget Allocation Recommendations
6. Cost Optimization Opportunities
7. Revenue Growth Strategies
8. Risk Assessment
9. Funding Requirements (if any)
10. Financial Milestones and KPIs

Include specific numbers and actionable recommendations.""",
        required_vars=["current_balance", "monthly_revenue", "monthly_expenses", "expense_breakdown", "revenue_trends", "upcoming_expenses", "business_goals"]
    )

class MarketingPrompts:
    """Prompts for Marketing Agent"""
    
    CAMPAIGN_STRATEGY = PromptTemplate(
        """You are a marketing strategist. Develop a comprehensive marketing campaign strategy.

Product/Service: {product_description}
Target Audience: {target_audience}
Budget: ${budget}
Timeline: {timeline}
Goals: {campaign_goals}
Competitors: {competitors}
Unique Value Proposition: {value_proposition}

Please create:
1. Campaign Objectives and KPIs
2. Target Audience Segmentation
3. Key Messaging and Positioning
4. Channel Strategy (digital, traditional, etc.)
5. Content Strategy and Calendar
6. Budget Allocation by Channel
7. Timeline and Milestones
8. Creative Direction Guidelines
9. Measurement and Analytics Plan
10. Risk Mitigation Strategies

Focus on ROI and measurable outcomes.""",
        required_vars=["product_description", "target_audience", "budget", "timeline", "campaign_goals", "competitors", "value_proposition"]
    )
    
    CONTENT_CREATION = PromptTemplate(
        """You are a content marketing expert. Create engaging content for the specified platform and audience.

Content Type: {content_type}
Platform: {platform}
Target Audience: {target_audience}
Key Message: {key_message}
Call to Action: {call_to_action}
Brand Voice: {brand_voice}
Content Goals: {content_goals}

Please create:
1. Compelling headline/title
2. Engaging opening hook
3. Main content body
4. Strong call-to-action
5. Relevant hashtags (if applicable)
6. Visual content suggestions
7. Engagement optimization tips
8. Performance metrics to track

Ensure the content is authentic, valuable, and aligned with brand voice.""",
        required_vars=["content_type", "platform", "target_audience", "key_message", "call_to_action", "brand_voice", "content_goals"]
    )

class ProductPrompts:
    """Prompts for Product Agent"""
    
    FEATURE_SPECIFICATION = PromptTemplate(
        """You are a product manager. Create detailed specifications for a new feature.

Feature Request: {feature_request}
User Stories: {user_stories}
Business Goals: {business_goals}
Technical Constraints: {technical_constraints}
Timeline: {timeline}
Resources: {resources}

Please provide:
1. Feature Overview and Objectives
2. Detailed User Stories and Acceptance Criteria
3. Technical Requirements and Specifications
4. UI/UX Design Guidelines
5. API Requirements (if applicable)
6. Testing Strategy and Test Cases
7. Implementation Timeline and Milestones
8. Resource Requirements
9. Risk Assessment and Mitigation
10. Success Metrics and KPIs

Be specific and actionable for the development team.""",
        required_vars=["feature_request", "user_stories", "business_goals", "technical_constraints", "timeline", "resources"]
    )
    
    PRODUCT_ROADMAP = PromptTemplate(
        """You are a product strategist. Create a comprehensive product roadmap.

Current Product Status: {current_status}
Business Objectives: {business_objectives}
User Feedback: {user_feedback}
Market Trends: {market_trends}
Technical Debt: {technical_debt}
Resource Constraints: {resource_constraints}
Timeline: {timeline}

Please create:
1. Product Vision and Strategy
2. Quarterly Roadmap with Key Features
3. Feature Prioritization Matrix
4. Resource Allocation Plan
5. Technical Architecture Evolution
6. User Experience Improvements
7. Performance and Scalability Goals
8. Integration and Partnership Opportunities
9. Risk Assessment and Contingency Plans
10. Success Metrics and Milestones

Focus on user value and business impact.""",
        required_vars=["current_status", "business_objectives", "user_feedback", "market_trends", "technical_debt", "resource_constraints", "timeline"]
    )

class LegalPrompts:
    """Prompts for Legal Agent"""
    
    CONTRACT_ANALYSIS = PromptTemplate(
        """You are a legal expert. Analyze the following contract or legal document.

Document Type: {document_type}
Parties Involved: {parties}
Key Terms: {key_terms}
Business Context: {business_context}
Jurisdiction: {jurisdiction}

Please provide:
1. Document Summary and Purpose
2. Key Terms and Obligations Analysis
3. Risk Assessment and Red Flags
4. Compliance Requirements
5. Negotiation Points and Recommendations
6. Legal Implications and Consequences
7. Required Actions and Next Steps
8. Documentation and Record-keeping Requirements
9. Renewal and Termination Clauses
10. Legal Opinion and Recommendations

Focus on protecting business interests while ensuring compliance.""",
        required_vars=["document_type", "parties", "key_terms", "business_context", "jurisdiction"]
    )

class SalesPrompts:
    """Prompts for Sales Agent"""
    
    LEAD_QUALIFICATION = PromptTemplate(
        """You are a sales expert. Analyze and qualify the following lead.

Lead Information:
- Company: {company_name}
- Contact: {contact_info}
- Industry: {industry}
- Company Size: {company_size}
- Budget Indication: {budget}
- Pain Points: {pain_points}
- Current Solutions: {current_solutions}
- Timeline: {timeline}

Please provide:
1. Lead Qualification Score (1-10)
2. Fit Assessment (Product-Market Fit)
3. Decision Maker Identification
4. Budget Qualification
5. Timeline Assessment
6. Competitive Analysis
7. Value Proposition Alignment
8. Next Steps and Action Plan
9. Potential Deal Size Estimation
10. Success Probability and Risks

Be realistic and focus on conversion potential.""",
        required_vars=["company_name", "contact_info", "industry", "company_size", "budget", "pain_points", "current_solutions", "timeline"]
    )

# Prompt manager for easy access
class PromptManager:
    """Central manager for all prompt templates"""
    
    def __init__(self):
        self.ceo = CEOPrompts()
        self.finance = FinancePrompts()
        self.marketing = MarketingPrompts()
        self.product = ProductPrompts()
        self.legal = LegalPrompts()
        self.sales = SalesPrompts()
        
    def get_prompt(self, agent_type: str, prompt_name: str) -> PromptTemplate:
        """Get a specific prompt template"""
        agent_prompts = getattr(self, agent_type.lower(), None)
        if not agent_prompts:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        prompt = getattr(agent_prompts, prompt_name.upper(), None)
        if not prompt:
            raise ValueError(f"Unknown prompt: {prompt_name} for agent {agent_type}")
            
        return prompt

# Global prompt manager instance
prompt_manager = PromptManager()

# Convenience function
def get_prompt(agent_type: str, prompt_name: str, **kwargs) -> str:
    """Get formatted prompt"""
    template = prompt_manager.get_prompt(agent_type, prompt_name)
    return template.format(**kwargs)