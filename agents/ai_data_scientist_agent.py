"""
AI Data Scientist Agent
Advanced data analysis, machine learning, and predictive analytics
Provides data-driven insights and automated model development
"""

import json
import logging
import asyncio
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from core.enhanced_base_agent import EnhancedBaseAgent
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

@dataclass
class DataAnalysis:
    """Data analysis result"""
    analysis_id: str
    dataset_name: str
    analysis_type: str  # descriptive, predictive, prescriptive
    
    # Analysis results
    key_findings: List[str]
    statistical_summary: Dict[str, Any]
    correlations: Dict[str, float]
    anomalies: List[Dict[str, Any]]
    
    # Insights and recommendations
    insights: List[str]
    recommendations: List[str]
    confidence_score: float  # 0-1
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    processing_time: Optional[float] = None

@dataclass
class MLModel:
    """Machine learning model tracking"""
    model_id: str
    model_name: str
    model_type: str  # regression, classification, clustering, forecasting
    
    # Performance metrics
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    rmse: Optional[float] = None
    
    # Model details
    features: List[str] = field(default_factory=list)
    target_variable: Optional[str] = None
    training_data_size: int = 0
    
    # Status
    status: str = "training"  # training, deployed, retired
    deployment_date: Optional[str] = None
    last_retrained: Optional[str] = None
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AIDataScientistAgent(EnhancedBaseAgent):
    """
    AI Data Scientist Agent that provides:
    - Automated data analysis and insights
    - Machine learning model development
    - Predictive analytics and forecasting
    - Statistical analysis and hypothesis testing
    - Data quality assessment and cleaning
    - Business intelligence and reporting
    """
    
    def __init__(self):
        super().__init__(
            agent_id="ai_data_scientist",
            name="AI Data Scientist",
            description="Advanced data analysis and machine learning automation",
            capabilities=[
                "data_analysis",
                "machine_learning",
                "predictive_modeling",
                "statistical_analysis",
                "data_visualization",
                "business_intelligence"
            ]
        )
        
        # Analysis history and models
        self.analyses: Dict[str, DataAnalysis] = {}
        self.models: Dict[str, MLModel] = {}
        
        # Sample business data for analysis
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize sample business data for analysis"""
        
        # Sample customer data
        self.sample_datasets = {
            "customer_metrics": {
                "monthly_revenue": [125000, 132000, 128000, 145000, 152000, 148000],
                "customer_count": [2847, 2965, 2892, 3124, 3287, 3156],
                "churn_rate": [0.05, 0.04, 0.06, 0.03, 0.04, 0.05],
                "avg_order_value": [43.9, 44.5, 44.2, 46.4, 46.2, 46.9],
                "customer_satisfaction": [8.2, 8.4, 8.1, 8.6, 8.5, 8.3]
            },
            "product_usage": {
                "daily_active_users": [1250, 1320, 1180, 1450, 1380, 1290],
                "session_duration": [12.5, 13.2, 11.8, 14.1, 13.7, 12.9],
                "feature_adoption": [0.65, 0.68, 0.62, 0.71, 0.69, 0.67],
                "conversion_rate": [0.034, 0.037, 0.032, 0.039, 0.036, 0.035]
            },
            "marketing_performance": {
                "cac": [45, 42, 48, 39, 41, 44],
                "ltv": [520, 535, 515, 550, 545, 530],
                "campaign_roi": [3.2, 3.8, 2.9, 4.1, 3.7, 3.4],
                "organic_traffic": [15600, 16200, 14800, 17100, 16800, 16400]
            }
        }
    
    async def analyze_business_data(self, dataset_name: str, analysis_type: str = "descriptive") -> DataAnalysis:
        """Perform comprehensive business data analysis"""
        
        try:
            logger.info(f"Analyzing dataset: {dataset_name}")
            
            if dataset_name not in self.sample_datasets:
                raise ValueError(f"Dataset {dataset_name} not found")
            
            start_time = datetime.now()
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            dataset = self.sample_datasets[dataset_name]
            
            # Perform statistical analysis
            statistical_summary = self._calculate_statistical_summary(dataset)
            correlations = self._calculate_correlations(dataset)
            anomalies = self._detect_anomalies(dataset)
            
            # Generate insights based on analysis type
            if analysis_type == "descriptive":
                insights, recommendations = await self._generate_descriptive_insights(dataset_name, dataset, statistical_summary)
            elif analysis_type == "predictive":
                insights, recommendations = await self._generate_predictive_insights(dataset_name, dataset)
            else:
                insights, recommendations = await self._generate_prescriptive_insights(dataset_name, dataset, statistical_summary)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(dataset, statistical_summary)
            
            # Create analysis result
            analysis = DataAnalysis(
                analysis_id=analysis_id,
                dataset_name=dataset_name,
                analysis_type=analysis_type,
                key_findings=self._extract_key_findings(dataset, statistical_summary),
                statistical_summary=statistical_summary,
                correlations=correlations,
                anomalies=anomalies,
                insights=insights,
                recommendations=recommendations,
                confidence_score=confidence_score,
                processing_time=(datetime.now() - start_time).total_seconds()
            )
            
            # Store analysis
            self.analyses[analysis_id] = analysis
            
            logger.info(f"Data analysis completed: {analysis_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze business data: {e}")
            raise
    
    def _calculate_statistical_summary(self, dataset: Dict[str, List[float]]) -> Dict[str, Any]:
        """Calculate statistical summary for dataset"""
        
        summary = {}
        
        for metric, values in dataset.items():
            if values:
                summary[metric] = {
                    "mean": round(np.mean(values), 2),
                    "median": round(np.median(values), 2),
                    "std": round(np.std(values), 2),
                    "min": round(min(values), 2),
                    "max": round(max(values), 2),
                    "trend": "increasing" if values[-1] > values[0] else "decreasing",
                    "volatility": round(np.std(values) / np.mean(values), 3) if np.mean(values) != 0 else 0
                }
        
        return summary
    
    def _calculate_correlations(self, dataset: Dict[str, List[float]]) -> Dict[str, float]:
        """Calculate correlations between metrics"""
        
        correlations = {}
        metrics = list(dataset.keys())
        
        for i, metric1 in enumerate(metrics):
            for metric2 in metrics[i+1:]:
                if len(dataset[metric1]) == len(dataset[metric2]):
                    corr = np.corrcoef(dataset[metric1], dataset[metric2])[0, 1]
                    if not np.isnan(corr):
                        correlations[f"{metric1}_vs_{metric2}"] = round(corr, 3)
        
        return correlations
    
    def _detect_anomalies(self, dataset: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Detect anomalies in the dataset"""
        
        anomalies = []
        
        for metric, values in dataset.items():
            if len(values) >= 3:
                mean_val = np.mean(values)
                std_val = np.std(values)
                
                for i, value in enumerate(values):
                    z_score = abs((value - mean_val) / std_val) if std_val > 0 else 0
                    
                    if z_score > 2:  # Anomaly threshold
                        anomalies.append({
                            "metric": metric,
                            "period": i,
                            "value": value,
                            "z_score": round(z_score, 2),
                            "severity": "high" if z_score > 3 else "medium"
                        })
        
        return anomalies
    
    def _extract_key_findings(self, dataset: Dict[str, List[float]], summary: Dict[str, Any]) -> List[str]:
        """Extract key findings from analysis"""
        
        findings = []
        
        for metric, stats in summary.items():
            # Trend findings
            if stats["trend"] == "increasing":
                findings.append(f"{metric.replace('_', ' ').title()} shows positive growth trend")
            else:
                findings.append(f"{metric.replace('_', ' ').title()} shows declining trend")
            
            # Volatility findings
            if stats["volatility"] > 0.2:
                findings.append(f"{metric.replace('_', ' ').title()} exhibits high volatility ({stats['volatility']})")
            elif stats["volatility"] < 0.05:
                findings.append(f"{metric.replace('_', ' ').title()} is highly stable ({stats['volatility']})")
        
        return findings[:5]  # Return top 5 findings
    
    async def _generate_descriptive_insights(self, dataset_name: str, dataset: Dict[str, List[float]], 
                                           summary: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Generate descriptive insights and recommendations"""
        
        insights = []
        recommendations = []
        
        if dataset_name == "customer_metrics":
            # Revenue insights
            if "monthly_revenue" in summary:
                revenue_trend = summary["monthly_revenue"]["trend"]
                if revenue_trend == "increasing":
                    insights.append("Revenue growth is positive, indicating healthy business expansion")
                    recommendations.append("Maintain current growth strategies and scale successful initiatives")
                else:
                    insights.append("Revenue decline detected, requires immediate attention")
                    recommendations.append("Analyze revenue drivers and implement recovery strategies")
            
            # Customer insights
            if "customer_count" in summary and "churn_rate" in summary:
                avg_churn = summary["churn_rate"]["mean"]
                if avg_churn < 0.05:
                    insights.append("Low churn rate indicates strong customer retention")
                    recommendations.append("Document and replicate retention best practices")
                else:
                    insights.append("Churn rate above optimal levels")
                    recommendations.append("Implement customer success programs to reduce churn")
        
        elif dataset_name == "product_usage":
            # User engagement insights
            if "daily_active_users" in summary:
                dau_trend = summary["daily_active_users"]["trend"]
                if dau_trend == "increasing":
                    insights.append("User engagement is growing, indicating product-market fit")
                    recommendations.append("Focus on user experience optimization and feature development")
            
            # Feature adoption insights
            if "feature_adoption" in summary:
                adoption_rate = summary["feature_adoption"]["mean"]
                if adoption_rate > 0.6:
                    insights.append("Strong feature adoption indicates good product design")
                    recommendations.append("Analyze successful features for replication in new development")
        
        elif dataset_name == "marketing_performance":
            # CAC/LTV insights
            if "cac" in summary and "ltv" in summary:
                avg_cac = summary["cac"]["mean"]
                avg_ltv = summary["ltv"]["mean"]
                ltv_cac_ratio = avg_ltv / avg_cac if avg_cac > 0 else 0
                
                if ltv_cac_ratio > 3:
                    insights.append(f"Excellent LTV:CAC ratio of {ltv_cac_ratio:.1f} indicates efficient marketing")
                    recommendations.append("Scale marketing spend while maintaining efficiency")
                else:
                    insights.append(f"LTV:CAC ratio of {ltv_cac_ratio:.1f} needs improvement")
                    recommendations.append("Optimize marketing channels and improve customer lifetime value")
        
        return insights, recommendations
    
    async def _generate_predictive_insights(self, dataset_name: str, 
                                          dataset: Dict[str, List[float]]) -> Tuple[List[str], List[str]]:
        """Generate predictive insights using simple forecasting"""
        
        insights = []
        recommendations = []
        
        # Simple trend-based predictions
        for metric, values in dataset.items():
            if len(values) >= 3:
                # Calculate trend
                recent_trend = (values[-1] - values[-3]) / 2
                predicted_next = values[-1] + recent_trend
                
                change_percent = (predicted_next - values[-1]) / values[-1] * 100 if values[-1] != 0 else 0
                
                if abs(change_percent) > 5:
                    direction = "increase" if change_percent > 0 else "decrease"
                    insights.append(f"{metric.replace('_', ' ').title()} predicted to {direction} by {abs(change_percent):.1f}% next period")
                    
                    if change_percent > 10:
                        recommendations.append(f"Prepare for significant growth in {metric.replace('_', ' ')}")
                    elif change_percent < -10:
                        recommendations.append(f"Implement mitigation strategies for declining {metric.replace('_', ' ')}")
        
        return insights, recommendations
    
    async def _generate_prescriptive_insights(self, dataset_name: str, dataset: Dict[str, List[float]], 
                                            summary: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Generate prescriptive insights with actionable recommendations"""
        
        insights = []
        recommendations = []
        
        # Optimization opportunities
        for metric, stats in summary.items():
            if stats["volatility"] > 0.15:
                insights.append(f"{metric.replace('_', ' ').title()} shows high variability - optimization opportunity")
                recommendations.append(f"Implement process controls to stabilize {metric.replace('_', ' ')}")
            
            if stats["trend"] == "decreasing":
                insights.append(f"{metric.replace('_', ' ').title()} declining - intervention required")
                recommendations.append(f"Develop action plan to reverse {metric.replace('_', ' ')} decline")
        
        # Cross-metric optimization
        if dataset_name == "customer_metrics":
            recommendations.extend([
                "Implement customer segmentation for targeted retention",
                "Develop predictive churn model for proactive intervention",
                "Optimize pricing strategy based on customer value analysis"
            ])
        
        return insights, recommendations
    
    def _calculate_confidence_score(self, dataset: Dict[str, List[float]], 
                                  summary: Dict[str, Any]) -> float:
        """Calculate confidence score for analysis"""
        
        # Base confidence on data quality factors
        data_points = sum(len(values) for values in dataset.values())
        completeness = data_points / (len(dataset) * 6)  # Assuming 6 periods expected
        
        # Adjust for data consistency
        consistency_score = 1.0
        for metric, stats in summary.items():
            if stats["volatility"] > 0.5:  # High volatility reduces confidence
                consistency_score *= 0.9
        
        confidence = min(completeness * consistency_score, 1.0)
        return round(confidence, 2)
    
    async def build_predictive_model(self, model_name: str, model_type: str, 
                                   features: List[str], target: str) -> MLModel:
        """Build and train a predictive model"""
        
        try:
            logger.info(f"Building predictive model: {model_name}")
            
            model_id = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Simulate model training (in real implementation, would use actual ML libraries)
            model = MLModel(
                model_id=model_id,
                model_name=model_name,
                model_type=model_type,
                features=features,
                target_variable=target,
                training_data_size=1000,  # Simulated
                status="training"
            )
            
            # Simulate training process
            await asyncio.sleep(2)  # Simulate training time
            
            # Generate realistic performance metrics based on model type
            if model_type == "classification":
                model.accuracy = round(np.random.uniform(0.75, 0.95), 3)
                model.precision = round(np.random.uniform(0.70, 0.90), 3)
                model.recall = round(np.random.uniform(0.70, 0.90), 3)
                model.f1_score = round(2 * (model.precision * model.recall) / (model.precision + model.recall), 3)
            elif model_type == "regression":
                model.rmse = round(np.random.uniform(0.05, 0.20), 3)
                model.accuracy = round(1 - model.rmse, 3)  # R-squared approximation
            
            # Update model status
            model.status = "deployed"
            model.deployment_date = datetime.now(timezone.utc).isoformat()
            
            # Store model
            self.models[model_id] = model
            
            logger.info(f"Model training completed: {model_name}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to build predictive model: {e}")
            raise
    
    async def generate_business_forecast(self, metric: str, periods: int = 6) -> Dict[str, Any]:
        """Generate business forecast for specific metric"""
        
        try:
            logger.info(f"Generating forecast for {metric}")
            
            # Find dataset containing the metric
            dataset_name = None
            for name, data in self.sample_datasets.items():
                if metric in data:
                    dataset_name = name
                    break
            
            if not dataset_name:
                raise ValueError(f"Metric {metric} not found in datasets")
            
            historical_data = self.sample_datasets[dataset_name][metric]
            
            # Simple trend-based forecasting
            forecast_values = []
            trend = (historical_data[-1] - historical_data[0]) / (len(historical_data) - 1)
            
            for i in range(periods):
                next_value = historical_data[-1] + trend * (i + 1)
                # Add some realistic variance
                variance = np.std(historical_data) * 0.1
                next_value += np.random.normal(0, variance)
                forecast_values.append(round(next_value, 2))
            
            # Calculate confidence intervals
            std_dev = np.std(historical_data)
            confidence_intervals = []
            
            for i, value in enumerate(forecast_values):
                # Confidence decreases with distance
                confidence_factor = 1 - (i * 0.1)
                interval_width = std_dev * confidence_factor
                
                confidence_intervals.append({
                    "lower": round(value - interval_width, 2),
                    "upper": round(value + interval_width, 2),
                    "confidence": round(confidence_factor * 100, 1)
                })
            
            forecast_result = {
                "metric": metric,
                "historical_data": historical_data,
                "forecast_periods": periods,
                "forecast_values": forecast_values,
                "confidence_intervals": confidence_intervals,
                "trend_direction": "increasing" if trend > 0 else "decreasing",
                "trend_strength": abs(trend),
                "forecast_accuracy": "medium",  # Would be based on model validation
                "key_assumptions": [
                    "Historical trend continues",
                    "No major external disruptions",
                    "Current business conditions remain stable"
                ],
                "risk_factors": [
                    "Market volatility",
                    "Competitive changes",
                    "Economic conditions"
                ]
            }
            
            logger.info(f"Forecast generated for {metric}")
            return forecast_result
            
        except Exception as e:
            logger.error(f"Failed to generate business forecast: {e}")
            raise
    
    async def get_data_insights(self) -> Dict[str, Any]:
        """Get comprehensive data science insights"""
        
        try:
            # Analyze all available datasets
            insights_summary = {
                "data_health_score": 0.0,
                "datasets_analyzed": len(self.sample_datasets),
                "models_deployed": len([m for m in self.models.values() if m.status == "deployed"]),
                "key_insights": [],
                "recommendations": [],
                "data_quality": {},
                "model_performance": {},
                "business_impact": []
            }
            
            # Calculate data health score
            total_quality = 0
            for dataset_name, dataset in self.sample_datasets.items():
                completeness = sum(1 for values in dataset.values() if len(values) >= 5) / len(dataset)
                consistency = 1 - np.mean([np.std(values) / np.mean(values) for values in dataset.values() if np.mean(values) != 0])
                quality_score = (completeness + max(consistency, 0)) / 2
                
                insights_summary["data_quality"][dataset_name] = {
                    "completeness": round(completeness * 100, 1),
                    "consistency": round(max(consistency, 0) * 100, 1),
                    "quality_score": round(quality_score * 100, 1)
                }
                
                total_quality += quality_score
            
            insights_summary["data_health_score"] = round((total_quality / len(self.sample_datasets)) * 100, 1)
            
            # Model performance summary
            if self.models:
                avg_accuracy = np.mean([m.accuracy for m in self.models.values() if m.accuracy])
                insights_summary["model_performance"] = {
                    "average_accuracy": round(avg_accuracy * 100, 1) if avg_accuracy else 0,
                    "models_in_production": len([m for m in self.models.values() if m.status == "deployed"]),
                    "total_models": len(self.models)
                }
            
            # Generate key insights
            if insights_summary["data_health_score"] >= 80:
                insights_summary["key_insights"].append("📊 High-quality data enables reliable analytics")
                insights_summary["recommendations"].append("Leverage data for advanced ML initiatives")
            else:
                insights_summary["key_insights"].append("⚠️ Data quality issues may impact analysis reliability")
                insights_summary["recommendations"].append("Implement data quality improvement processes")
            
            # Business impact insights
            recent_analyses = [a for a in self.analyses.values() 
                             if (datetime.now(timezone.utc) - datetime.fromisoformat(a.created_at.replace('Z', '+00:00'))).days <= 7]
            
            if recent_analyses:
                insights_summary["business_impact"].extend([
                    f"Generated {len(recent_analyses)} actionable insights this week",
                    "Data-driven recommendations implemented across departments",
                    "Predictive models supporting strategic decision making"
                ])
            
            # Strategic recommendations
            insights_summary["recommendations"].extend([
                "Expand data collection for deeper customer insights",
                "Implement real-time analytics dashboards",
                "Develop automated anomaly detection systems",
                "Create predictive models for key business metrics"
            ])
            
            return insights_summary
            
        except Exception as e:
            logger.error(f"Failed to get data insights: {e}")
            raise

# Global AI data scientist agent
ai_data_scientist = AIDataScientistAgent()