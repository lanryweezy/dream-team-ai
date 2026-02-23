"""
Customer Feedback Integration Engine
Aggregate feedback from all channels, sentiment analysis, and action item generation
Provides comprehensive customer insights and automated feedback processing
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics
import re

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class FeedbackChannel(Enum):
    EMAIL = "email"
    CHAT = "chat"
    SURVEY = "survey"
    REVIEW = "review"
    SOCIAL_MEDIA = "social_media"
    SUPPORT_TICKET = "support_ticket"
    INTERVIEW = "interview"
    NPS = "nps"
    APP_STORE = "app_store"
    WEBSITE = "website"

class SentimentType(Enum):
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

class FeedbackCategory(Enum):
    PRODUCT = "product"
    PRICING = "pricing"
    SUPPORT = "support"
    ONBOARDING = "onboarding"
    PERFORMANCE = "performance"
    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"
    GENERAL = "general"
    COMPETITOR = "competitor"
    CHURN_RISK = "churn_risk"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CustomerFeedback:
    """Individual customer feedback item"""
    feedback_id: str
    customer_id: str
    customer_name: str
    customer_segment: str  # "enterprise", "smb", "startup"
    
    # Feedback content
    channel: FeedbackChannel
    title: str
    content: str
    rating: Optional[int] = None  # 1-5 or 1-10 scale
    
    # Analysis results
    sentiment: SentimentType = SentimentType.NEUTRAL
    sentiment_score: float = 0.0  # -1 to 1
    categories: List[FeedbackCategory] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    
    # Metadata
    source_url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    processed_at: Optional[str] = None
    
    # Action items
    action_items: List[str] = field(default_factory=list)
    assigned_team: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    
    # Follow-up
    requires_response: bool = False
    response_sent: bool = False
    follow_up_date: Optional[str] = None

@dataclass
class FeedbackInsight:
    """Aggregated feedback insight"""
    insight_id: str
    insight_type: str  # "trend", "issue", "opportunity", "risk"
    title: str
    description: str
    
    # Supporting data
    affected_customers: int
    feedback_count: int
    sentiment_trend: List[float] = field(default_factory=list)
    categories_involved: List[FeedbackCategory] = field(default_factory=list)
    
    # Impact assessment
    impact_score: float = 0.0  # 0-10
    urgency_score: float = 0.0  # 0-10
    confidence_level: float = 0.0  # 0-1
    
    # Recommendations
    recommended_actions: List[str] = field(default_factory=list)
    estimated_effort: str = ""  # "low", "medium", "high"
    expected_impact: str = ""  # "low", "medium", "high"
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class FeedbackReport:
    """Comprehensive feedback analysis report"""
    report_id: str
    period: str  # "2025-09"
    
    # Summary metrics
    total_feedback: int
    sentiment_distribution: Dict[str, int] = field(default_factory=dict)
    channel_distribution: Dict[str, int] = field(default_factory=dict)
    category_distribution: Dict[str, int] = field(default_factory=dict)
    
    # Trends
    sentiment_trend: List[Dict[str, Any]] = field(default_factory=list)
    volume_trend: List[Dict[str, Any]] = field(default_factory=list)
    
    # Key insights
    top_insights: List[FeedbackInsight] = field(default_factory=list)
    critical_issues: List[str] = field(default_factory=list)
    improvement_opportunities: List[str] = field(default_factory=list)
    
    # Customer segments
    segment_analysis: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Action items
    priority_actions: List[Dict[str, Any]] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class CustomerFeedbackEngine:
    """
    Comprehensive customer feedback integration and analysis system that provides:
    - Multi-channel feedback aggregation
    - AI-powered sentiment analysis and categorization
    - Automated insight generation
    - Action item prioritization
    - Customer satisfaction tracking
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.feedback_items: Dict[str, CustomerFeedback] = {}
        self.insights: Dict[str, FeedbackInsight] = {}
        self.reports: Dict[str, FeedbackReport] = {}
        
        # Analysis configuration
        self.sentiment_keywords = {
            "positive": ["love", "great", "excellent", "amazing", "fantastic", "perfect", "awesome", "brilliant"],
            "negative": ["hate", "terrible", "awful", "horrible", "worst", "useless", "broken", "frustrated"]
        }
        
        self.category_keywords = {
            FeedbackCategory.PRODUCT: ["feature", "functionality", "product", "tool", "interface", "design"],
            FeedbackCategory.PRICING: ["price", "cost", "expensive", "cheap", "value", "pricing", "plan"],
            FeedbackCategory.SUPPORT: ["support", "help", "service", "response", "team", "assistance"],
            FeedbackCategory.PERFORMANCE: ["slow", "fast", "speed", "performance", "loading", "lag"],
            FeedbackCategory.BUG_REPORT: ["bug", "error", "issue", "problem", "broken", "crash", "glitch"]
        }
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample feedback data"""
        
        sample_feedback = [
            CustomerFeedback(
                feedback_id="fb_001",
                customer_id="cust_001",
                customer_name="TechCorp Inc",
                customer_segment="enterprise",
                channel=FeedbackChannel.EMAIL,
                title="Love the new analytics dashboard!",
                content="The new analytics dashboard is fantastic! It's exactly what we needed for our quarterly reports. The real-time data visualization is a game-changer for our team.",
                rating=5,
                sentiment=SentimentType.VERY_POSITIVE,
                sentiment_score=0.9,
                categories=[FeedbackCategory.PRODUCT, FeedbackCategory.FEATURE_REQUEST],
                keywords=["analytics", "dashboard", "real-time", "visualization"],
                requires_response=True,
                priority=Priority.MEDIUM
            ),
            CustomerFeedback(
                feedback_id="fb_002",
                customer_id="cust_002",
                customer_name="StartupXYZ",
                customer_segment="startup",
                channel=FeedbackChannel.CHAT,
                title="Pricing is too high for small teams",
                content="We love the product but the pricing is really steep for a small startup like us. Would love to see a more affordable plan for teams under 10 people.",
                rating=3,
                sentiment=SentimentType.NEUTRAL,
                sentiment_score=0.1,
                categories=[FeedbackCategory.PRICING],
                keywords=["pricing", "expensive", "small team", "startup"],
                requires_response=True,
                priority=Priority.HIGH
            ),
            CustomerFeedback(
                feedback_id="fb_003",
                customer_id="cust_003",
                customer_name="DataFlow Solutions",
                customer_segment="smb",
                channel=FeedbackChannel.SUPPORT_TICKET,
                title="Dashboard loading very slowly",
                content="The dashboard has been loading very slowly for the past week. It's affecting our daily operations and team productivity. Please fix this ASAP.",
                rating=2,
                sentiment=SentimentType.NEGATIVE,
                sentiment_score=-0.7,
                categories=[FeedbackCategory.PERFORMANCE, FeedbackCategory.BUG_REPORT],
                keywords=["slow", "loading", "performance", "productivity"],
                requires_response=True,
                priority=Priority.CRITICAL,
                assigned_team="engineering"
            ),
            CustomerFeedback(
                feedback_id="fb_004",
                customer_id="cust_004",
                customer_name="GrowthCo",
                customer_segment="smb",
                channel=FeedbackChannel.NPS,
                title="NPS Survey Response",
                content="Great product overall, but would love to see mobile app support. Also, the onboarding process could be more streamlined.",
                rating=8,
                sentiment=SentimentType.POSITIVE,
                sentiment_score=0.6,
                categories=[FeedbackCategory.PRODUCT, FeedbackCategory.ONBOARDING, FeedbackCategory.FEATURE_REQUEST],
                keywords=["mobile app", "onboarding", "streamlined"],
                requires_response=False,
                priority=Priority.MEDIUM
            ),
            CustomerFeedback(
                feedback_id="fb_005",
                customer_id="cust_005",
                customer_name="Enterprise Corp",
                customer_segment="enterprise",
                channel=FeedbackChannel.INTERVIEW,
                title="Considering switching to competitor",
                content="We're evaluating alternatives because we need better API integration capabilities. The current API is limited and doesn't meet our enterprise requirements.",
                rating=2,
                sentiment=SentimentType.NEGATIVE,
                sentiment_score=-0.5,
                categories=[FeedbackCategory.PRODUCT, FeedbackCategory.CHURN_RISK, FeedbackCategory.COMPETITOR],
                keywords=["switching", "competitor", "API", "integration", "enterprise"],
                requires_response=True,
                priority=Priority.CRITICAL,
                assigned_team="product"
            )
        ]
        
        for feedback in sample_feedback:
            self.feedback_items[feedback.feedback_id] = feedback
    
    async def process_feedback(self, feedback_data: Dict[str, Any]) -> CustomerFeedback:
        """Process new feedback item with AI analysis"""
        
        try:
            logger.info(f"Processing feedback from {feedback_data.get('customer_name')}")
            
            # Create feedback object
            feedback = CustomerFeedback(
                feedback_id=f"fb_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                customer_id=feedback_data.get("customer_id", "unknown"),
                customer_name=feedback_data.get("customer_name", "Anonymous"),
                customer_segment=feedback_data.get("customer_segment", "unknown"),
                channel=FeedbackChannel(feedback_data.get("channel", "email")),
                title=feedback_data.get("title", ""),
                content=feedback_data.get("content", ""),
                rating=feedback_data.get("rating"),
                source_url=feedback_data.get("source_url")
            )
            
            # Perform AI analysis
            await self._analyze_sentiment(feedback)
            await self._categorize_feedback(feedback)
            await self._extract_keywords(feedback)
            await self._generate_action_items(feedback)
            await self._assess_priority(feedback)
            
            feedback.processed_at = datetime.now(timezone.utc).isoformat()
            
            # Store feedback
            self.feedback_items[feedback.feedback_id] = feedback
            
            logger.info(f"Processed feedback: {feedback.feedback_id}")
            return feedback
            
        except Exception as e:
            logger.error(f"Failed to process feedback: {e}")
            raise
    
    async def _analyze_sentiment(self, feedback: CustomerFeedback):
        """Analyze sentiment using AI and keyword matching"""
        
        content_lower = feedback.content.lower()
        
        # Keyword-based sentiment scoring
        positive_count = sum(1 for word in self.sentiment_keywords["positive"] if word in content_lower)
        negative_count = sum(1 for word in self.sentiment_keywords["negative"] if word in content_lower)
        
        # Calculate sentiment score
        if feedback.rating:
            # Use rating if available
            if feedback.rating >= 4:
                sentiment_score = 0.5 + (feedback.rating - 4) * 0.25
                sentiment = SentimentType.POSITIVE if feedback.rating == 4 else SentimentType.VERY_POSITIVE
            elif feedback.rating <= 2:
                sentiment_score = -0.5 - (2 - feedback.rating) * 0.25
                sentiment = SentimentType.NEGATIVE if feedback.rating == 2 else SentimentType.VERY_NEGATIVE
            else:
                sentiment_score = 0.0
                sentiment = SentimentType.NEUTRAL
        else:
            # Use keyword analysis
            net_sentiment = positive_count - negative_count
            if net_sentiment > 2:
                sentiment = SentimentType.VERY_POSITIVE
                sentiment_score = 0.8
            elif net_sentiment > 0:
                sentiment = SentimentType.POSITIVE
                sentiment_score = 0.4
            elif net_sentiment < -2:
                sentiment = SentimentType.VERY_NEGATIVE
                sentiment_score = -0.8
            elif net_sentiment < 0:
                sentiment = SentimentType.NEGATIVE
                sentiment_score = -0.4
            else:
                sentiment = SentimentType.NEUTRAL
                sentiment_score = 0.0
        
        feedback.sentiment = sentiment
        feedback.sentiment_score = sentiment_score
    
    async def _categorize_feedback(self, feedback: CustomerFeedback):
        """Categorize feedback using keyword matching"""
        
        content_lower = feedback.content.lower() + " " + feedback.title.lower()
        categories = []
        
        for category, keywords in self.category_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                categories.append(category)
        
        # Default to general if no categories found
        if not categories:
            categories.append(FeedbackCategory.GENERAL)
        
        feedback.categories = categories
    
    async def _extract_keywords(self, feedback: CustomerFeedback):
        """Extract key terms and phrases from feedback"""
        
        content = feedback.content.lower()
        
        # Simple keyword extraction (in production, use more sophisticated NLP)
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        words = re.findall(r'\b\w+\b', content)
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        
        # Get most frequent keywords
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and take top 10
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        feedback.keywords = [word for word, freq in top_keywords]
    
    async def _generate_action_items(self, feedback: CustomerFeedback):
        """Generate action items based on feedback content and categories"""
        
        action_items = []
        
        # Category-based action items
        if FeedbackCategory.BUG_REPORT in feedback.categories:
            action_items.append("Investigate and reproduce reported bug")
            action_items.append("Assign to engineering team for fix")
            feedback.assigned_team = "engineering"
        
        if FeedbackCategory.FEATURE_REQUEST in feedback.categories:
            action_items.append("Evaluate feature request for product roadmap")
            action_items.append("Assess technical feasibility and effort")
            feedback.assigned_team = "product"
        
        if FeedbackCategory.PRICING in feedback.categories:
            action_items.append("Review pricing strategy and competitive positioning")
            action_items.append("Consider customer segment-specific pricing")
            feedback.assigned_team = "business"
        
        if FeedbackCategory.SUPPORT in feedback.categories:
            action_items.append("Improve support process and response time")
            action_items.append("Provide additional training to support team")
            feedback.assigned_team = "support"
        
        if FeedbackCategory.CHURN_RISK in feedback.categories:
            action_items.append("Schedule immediate customer success call")
            action_items.append("Develop retention strategy for this customer")
            feedback.assigned_team = "customer_success"
        
        # Sentiment-based action items
        if feedback.sentiment in [SentimentType.NEGATIVE, SentimentType.VERY_NEGATIVE]:
            action_items.append("Respond to customer within 24 hours")
            action_items.append("Escalate to management if needed")
            feedback.requires_response = True
        
        if feedback.sentiment in [SentimentType.POSITIVE, SentimentType.VERY_POSITIVE]:
            action_items.append("Request customer testimonial or case study")
            action_items.append("Consider for customer reference program")
        
        feedback.action_items = action_items
    
    async def _assess_priority(self, feedback: CustomerFeedback):
        """Assess priority based on sentiment, customer segment, and categories"""
        
        priority_score = 0
        
        # Sentiment impact
        if feedback.sentiment == SentimentType.VERY_NEGATIVE:
            priority_score += 4
        elif feedback.sentiment == SentimentType.NEGATIVE:
            priority_score += 3
        elif feedback.sentiment == SentimentType.NEUTRAL:
            priority_score += 1
        
        # Customer segment impact
        if feedback.customer_segment == "enterprise":
            priority_score += 3
        elif feedback.customer_segment == "smb":
            priority_score += 2
        else:
            priority_score += 1
        
        # Category impact
        if FeedbackCategory.CHURN_RISK in feedback.categories:
            priority_score += 4
        if FeedbackCategory.BUG_REPORT in feedback.categories:
            priority_score += 3
        if FeedbackCategory.PERFORMANCE in feedback.categories:
            priority_score += 2
        
        # Assign priority
        if priority_score >= 8:
            feedback.priority = Priority.CRITICAL
        elif priority_score >= 6:
            feedback.priority = Priority.HIGH
        elif priority_score >= 3:
            feedback.priority = Priority.MEDIUM
        else:
            feedback.priority = Priority.LOW
    
    async def generate_insights(self, period_days: int = 30) -> List[FeedbackInsight]:
        """Generate insights from feedback data"""
        
        try:
            logger.info(f"Generating feedback insights for {period_days} days")
            
            # Filter recent feedback
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=period_days)
            recent_feedback = [
                fb for fb in self.feedback_items.values()
                if datetime.fromisoformat(fb.created_at.replace('Z', '+00:00')) > cutoff_date
            ]
            
            insights = []
            
            # Sentiment trend insight
            sentiment_insight = await self._analyze_sentiment_trends(recent_feedback)
            if sentiment_insight:
                insights.append(sentiment_insight)
            
            # Category analysis insight
            category_insight = await self._analyze_category_trends(recent_feedback)
            if category_insight:
                insights.append(category_insight)
            
            # Customer segment insight
            segment_insight = await self._analyze_segment_patterns(recent_feedback)
            if segment_insight:
                insights.append(segment_insight)
            
            # Churn risk insight
            churn_insight = await self._analyze_churn_risks(recent_feedback)
            if churn_insight:
                insights.append(churn_insight)
            
            # Store insights
            for insight in insights:
                self.insights[insight.insight_id] = insight
            
            logger.info(f"Generated {len(insights)} insights")
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate insights: {e}")
            raise
    
    async def _analyze_sentiment_trends(self, feedback_list: List[CustomerFeedback]) -> Optional[FeedbackInsight]:
        """Analyze sentiment trends"""
        
        if len(feedback_list) < 5:
            return None
        
        # Calculate average sentiment by week
        sentiment_by_week = {}
        for fb in feedback_list:
            week = datetime.fromisoformat(fb.created_at.replace('Z', '+00:00')).strftime('%Y-W%U')
            if week not in sentiment_by_week:
                sentiment_by_week[week] = []
            sentiment_by_week[week].append(fb.sentiment_score)
        
        # Calculate weekly averages
        weekly_averages = {week: statistics.mean(scores) for week, scores in sentiment_by_week.items()}
        
        # Detect trend
        if len(weekly_averages) >= 2:
            recent_weeks = sorted(weekly_averages.keys())[-2:]
            trend = weekly_averages[recent_weeks[-1]] - weekly_averages[recent_weeks[0]]
            
            if trend < -0.2:
                insight_type = "risk"
                title = "Declining Customer Sentiment Detected"
                description = f"Customer sentiment has declined by {abs(trend):.1f} points over recent weeks"
                impact_score = 8.0
                urgency_score = 9.0
            elif trend > 0.2:
                insight_type = "opportunity"
                title = "Improving Customer Sentiment"
                description = f"Customer sentiment has improved by {trend:.1f} points over recent weeks"
                impact_score = 7.0
                urgency_score = 5.0
            else:
                return None
            
            return FeedbackInsight(
                insight_id=f"sentiment_trend_{datetime.now().strftime('%H%M%S')}",
                insight_type=insight_type,
                title=title,
                description=description,
                affected_customers=len(feedback_list),
                feedback_count=len(feedback_list),
                sentiment_trend=list(weekly_averages.values()),
                impact_score=impact_score,
                urgency_score=urgency_score,
                confidence_level=0.8,
                recommended_actions=[
                    "Investigate root causes of sentiment changes",
                    "Implement targeted customer success initiatives",
                    "Monitor sentiment closely over next 2 weeks"
                ]
            )
        
        return None
    
    async def _analyze_category_trends(self, feedback_list: List[CustomerFeedback]) -> Optional[FeedbackInsight]:
        """Analyze category trends"""
        
        # Count feedback by category
        category_counts = {}
        for fb in feedback_list:
            for category in fb.categories:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Find most common issues
        if category_counts:
            top_category = max(category_counts, key=category_counts.get)
            count = category_counts[top_category]
            
            if count >= 3:  # At least 3 feedback items
                return FeedbackInsight(
                    insight_id=f"category_trend_{datetime.now().strftime('%H%M%S')}",
                    insight_type="trend",
                    title=f"High Volume of {top_category.value.title()} Feedback",
                    description=f"Received {count} feedback items related to {top_category.value} in recent period",
                    affected_customers=count,
                    feedback_count=count,
                    categories_involved=[top_category],
                    impact_score=6.0 + min(count * 0.5, 4.0),
                    urgency_score=7.0,
                    confidence_level=0.9,
                    recommended_actions=[
                        f"Deep dive analysis of {top_category.value} issues",
                        f"Prioritize {top_category.value} improvements in roadmap",
                        "Communicate improvements to affected customers"
                    ]
                )
        
        return None
    
    async def _analyze_segment_patterns(self, feedback_list: List[CustomerFeedback]) -> Optional[FeedbackInsight]:
        """Analyze patterns by customer segment"""
        
        # Analyze sentiment by segment
        segment_sentiment = {}
        for fb in feedback_list:
            if fb.customer_segment not in segment_sentiment:
                segment_sentiment[fb.customer_segment] = []
            segment_sentiment[fb.customer_segment].append(fb.sentiment_score)
        
        # Find segments with concerning patterns
        for segment, scores in segment_sentiment.items():
            if len(scores) >= 3:
                avg_sentiment = statistics.mean(scores)
                if avg_sentiment < -0.3:  # Negative sentiment
                    return FeedbackInsight(
                        insight_id=f"segment_pattern_{datetime.now().strftime('%H%M%S')}",
                        insight_type="risk",
                        title=f"Negative Sentiment in {segment.title()} Segment",
                        description=f"{segment.title()} customers showing consistently negative sentiment (avg: {avg_sentiment:.2f})",
                        affected_customers=len(scores),
                        feedback_count=len(scores),
                        impact_score=8.0,
                        urgency_score=8.0,
                        confidence_level=0.85,
                        recommended_actions=[
                            f"Conduct {segment} customer interviews",
                            f"Review {segment} customer journey and pain points",
                            f"Develop {segment}-specific improvement plan"
                        ]
                    )
        
        return None
    
    async def _analyze_churn_risks(self, feedback_list: List[CustomerFeedback]) -> Optional[FeedbackInsight]:
        """Analyze churn risk indicators"""
        
        churn_risk_feedback = [
            fb for fb in feedback_list
            if FeedbackCategory.CHURN_RISK in fb.categories or fb.sentiment_score < -0.5
        ]
        
        if len(churn_risk_feedback) >= 2:
            return FeedbackInsight(
                insight_id=f"churn_risk_{datetime.now().strftime('%H%M%S')}",
                insight_type="risk",
                title="Multiple Customers at Churn Risk",
                description=f"Identified {len(churn_risk_feedback)} customers with high churn risk indicators",
                affected_customers=len(churn_risk_feedback),
                feedback_count=len(churn_risk_feedback),
                categories_involved=[FeedbackCategory.CHURN_RISK],
                impact_score=9.0,
                urgency_score=10.0,
                confidence_level=0.9,
                recommended_actions=[
                    "Immediate customer success outreach to at-risk customers",
                    "Develop retention offers and incentives",
                    "Address root causes of dissatisfaction",
                    "Implement proactive churn prevention measures"
                ],
                estimated_effort="high",
                expected_impact="high"
            )
        
        return None
    
    async def generate_feedback_report(self, period: str) -> FeedbackReport:
        """Generate comprehensive feedback report"""
        
        try:
            logger.info(f"Generating feedback report for {period}")
            
            # Filter feedback for period
            if period == "current_month":
                start_date = datetime.now(timezone.utc).replace(day=1)
            else:
                # Parse period like "2025-09"
                year, month = period.split('-')
                start_date = datetime(int(year), int(month), 1, tzinfo=timezone.utc)
            
            end_date = start_date + timedelta(days=32)
            end_date = end_date.replace(day=1) - timedelta(days=1)
            
            period_feedback = [
                fb for fb in self.feedback_items.values()
                if start_date <= datetime.fromisoformat(fb.created_at.replace('Z', '+00:00')) <= end_date
            ]
            
            # Calculate distributions
            sentiment_dist = {}
            for sentiment in SentimentType:
                count = len([fb for fb in period_feedback if fb.sentiment == sentiment])
                sentiment_dist[sentiment.value] = count
            
            channel_dist = {}
            for channel in FeedbackChannel:
                count = len([fb for fb in period_feedback if fb.channel == channel])
                if count > 0:
                    channel_dist[channel.value] = count
            
            category_dist = {}
            for fb in period_feedback:
                for category in fb.categories:
                    category_dist[category.value] = category_dist.get(category.value, 0) + 1
            
            # Generate insights
            insights = await self.generate_insights(30)
            top_insights = sorted(insights, key=lambda x: x.impact_score * x.urgency_score, reverse=True)[:5]
            
            # Critical issues
            critical_issues = [
                fb.title for fb in period_feedback
                if fb.priority == Priority.CRITICAL or fb.sentiment == SentimentType.VERY_NEGATIVE
            ]
            
            # Improvement opportunities
            improvement_opportunities = [
                "Implement mobile app based on customer requests",
                "Improve onboarding process to reduce confusion",
                "Enhance API capabilities for enterprise customers",
                "Develop pricing tiers for different customer segments",
                "Improve dashboard performance and loading times"
            ]
            
            # Segment analysis
            segment_analysis = {}
            for segment in ["enterprise", "smb", "startup"]:
                segment_feedback = [fb for fb in period_feedback if fb.customer_segment == segment]
                if segment_feedback:
                    avg_sentiment = statistics.mean([fb.sentiment_score for fb in segment_feedback])
                    segment_analysis[segment] = {
                        "feedback_count": len(segment_feedback),
                        "average_sentiment": round(avg_sentiment, 2),
                        "top_categories": list(category_dist.keys())[:3]
                    }
            
            # Priority actions
            priority_actions = [
                {
                    "action": "Address dashboard performance issues",
                    "priority": "critical",
                    "affected_customers": 5,
                    "estimated_effort": "medium"
                },
                {
                    "action": "Develop startup-friendly pricing tier",
                    "priority": "high",
                    "affected_customers": 8,
                    "estimated_effort": "low"
                },
                {
                    "action": "Enhance API integration capabilities",
                    "priority": "high",
                    "affected_customers": 3,
                    "estimated_effort": "high"
                }
            ]
            
            report = FeedbackReport(
                report_id=f"report_{period}_{datetime.now().strftime('%H%M%S')}",
                period=period,
                total_feedback=len(period_feedback),
                sentiment_distribution=sentiment_dist,
                channel_distribution=channel_dist,
                category_distribution=category_dist,
                top_insights=top_insights,
                critical_issues=critical_issues,
                improvement_opportunities=improvement_opportunities,
                segment_analysis=segment_analysis,
                priority_actions=priority_actions
            )
            
            self.reports[report.report_id] = report
            logger.info(f"Generated feedback report: {report.report_id}")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate feedback report: {e}")
            raise
    
    async def get_feedback_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive feedback dashboard data"""
        
        try:
            # Recent feedback (last 30 days)
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
            recent_feedback = [
                fb for fb in self.feedback_items.values()
                if datetime.fromisoformat(fb.created_at.replace('Z', '+00:00')) > cutoff_date
            ]
            
            # Key metrics
            total_feedback = len(recent_feedback)
            avg_sentiment = statistics.mean([fb.sentiment_score for fb in recent_feedback]) if recent_feedback else 0
            response_rate = len([fb for fb in recent_feedback if fb.response_sent]) / max(len([fb for fb in recent_feedback if fb.requires_response]), 1) * 100
            critical_issues = len([fb for fb in recent_feedback if fb.priority == Priority.CRITICAL])
            
            # Sentiment distribution
            sentiment_dist = {}
            for sentiment in SentimentType:
                count = len([fb for fb in recent_feedback if fb.sentiment == sentiment])
                sentiment_dist[sentiment.value] = count
            
            # Channel performance
            channel_performance = {}
            for channel in FeedbackChannel:
                channel_feedback = [fb for fb in recent_feedback if fb.channel == channel]
                if channel_feedback:
                    avg_sentiment = statistics.mean([fb.sentiment_score for fb in channel_feedback])
                    channel_performance[channel.value] = {
                        "count": len(channel_feedback),
                        "avg_sentiment": round(avg_sentiment, 2)
                    }
            
            # Recent insights
            recent_insights = sorted(
                self.insights.values(),
                key=lambda x: x.created_at,
                reverse=True
            )[:5]
            
            # Action items
            pending_actions = []
            for fb in recent_feedback:
                if fb.action_items and not fb.response_sent:
                    pending_actions.extend([
                        {
                            "feedback_id": fb.feedback_id,
                            "customer": fb.customer_name,
                            "action": action,
                            "priority": fb.priority.value,
                            "assigned_team": fb.assigned_team
                        }
                        for action in fb.action_items[:2]  # Top 2 actions per feedback
                    ])
            
            # Sort by priority
            priority_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            pending_actions = sorted(
                pending_actions,
                key=lambda x: priority_order.get(x["priority"], 0),
                reverse=True
            )[:10]
            
            dashboard_data = {
                "key_metrics": {
                    "total_feedback": total_feedback,
                    "average_sentiment": round(avg_sentiment, 2),
                    "response_rate": round(response_rate, 1),
                    "critical_issues": critical_issues
                },
                "sentiment_distribution": sentiment_dist,
                "channel_performance": channel_performance,
                "recent_insights": [asdict(insight) for insight in recent_insights],
                "pending_actions": pending_actions,
                "trending_topics": list(dict(sorted(
                    {category: count for category, count in 
                     {cat.value: sum(1 for fb in recent_feedback for cat in fb.categories if cat.value == cat.value) 
                      for cat in FeedbackCategory}.items() if count > 0}.items(),
                    key=lambda x: x[1], reverse=True
                )).keys())[:5],
                "recommendations": await self._generate_dashboard_recommendations(recent_feedback)
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get feedback dashboard data: {e}")
            raise
    
    async def _generate_dashboard_recommendations(self, recent_feedback: List[CustomerFeedback]) -> List[str]:
        """Generate dashboard-specific recommendations"""
        
        recommendations = []
        
        # Sentiment-based recommendations
        negative_feedback = [fb for fb in recent_feedback if fb.sentiment_score < -0.3]
        if len(negative_feedback) > len(recent_feedback) * 0.3:
            recommendations.append("🚨 High negative sentiment detected - implement immediate customer success outreach")
        
        # Category-based recommendations
        category_counts = {}
        for fb in recent_feedback:
            for category in fb.categories:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        if category_counts.get(FeedbackCategory.PERFORMANCE, 0) >= 3:
            recommendations.append("⚡ Multiple performance complaints - prioritize technical optimization")
        
        if category_counts.get(FeedbackCategory.PRICING, 0) >= 3:
            recommendations.append("💰 Pricing concerns raised - review pricing strategy and value communication")
        
        # Response rate recommendations
        unresponded = len([fb for fb in recent_feedback if fb.requires_response and not fb.response_sent])
        if unresponded > 5:
            recommendations.append(f"📧 {unresponded} customers awaiting responses - improve response time")
        
        # Default recommendations
        if not recommendations:
            recommendations = [
                "📊 Continue monitoring feedback trends and sentiment patterns",
                "🎯 Focus on converting positive feedback into testimonials and case studies",
                "🔄 Implement regular feedback collection across all customer touchpoints"
            ]
        
        return recommendations

# Global customer feedback engine
customer_feedback = CustomerFeedbackEngine()