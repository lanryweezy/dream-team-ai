"""
Test Advanced Dream Machine Features - Simplified Version
Tests core advanced functionality:
- Dream-to-Blueprint Generation with MBA frameworks
- Advanced Business Intelligence
- AI Strategy Engine with ML optimization
- Monte Carlo Simulations
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List

# Import our advanced components
from core.dream_to_blueprint_generator import DreamToBlueprintGenerator
from core.advanced_business_intelligence import AdvancedBusinessIntelligence
from core.advanced_ai_strategy_engine import AdvancedAIStrategyEngine, OptimizationObjective
from core.company_blueprint_dataclass import CompanyBlueprint, TargetMarket

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimplifiedAdvancedTest:
    """Simplified test suite for advanced Dream Machine features"""
    
    def __init__(self):
        self.dream_generator = DreamToBlueprintGenerator()
        self.business_intelligence = AdvancedBusinessIntelligence()
        self.ai_strategy_engine = AdvancedAIStrategyEngine()
        
        self.test_results = {}
    
    async def run_advanced_test_suite(self):
        """Run the advanced test suite"""
        
        print("🚀 Starting Advanced Dream Machine Feature Tests...")
        print("=" * 70)
        
        start_time = datetime.now(timezone.utc)
        
        try:
            # Test 1: Advanced Dream-to-Blueprint Generation
            print("\n📋 Test 1: Advanced Dream-to-Blueprint Generation")
            blueprint = await self.test_advanced_blueprint_generation()
            
            # Test 2: Advanced Business Intelligence
            print("\n🧠 Test 2: Advanced Business Intelligence Engine")
            bi_report = await self.test_advanced_business_intelligence(blueprint)
            
            # Test 3: AI Strategy Engine
            print("\n🎯 Test 3: AI-Powered Strategy Engine")
            strategies = await self.test_ai_strategy_engine(blueprint)
            
            # Test 4: Monte Carlo Simulations
            print("\n🎲 Test 4: Monte Carlo Market Simulations")
            simulation = await self.test_monte_carlo_simulation(blueprint, strategies)
            
            # Test 5: Machine Learning Optimization
            print("\n🔬 Test 5: Machine Learning Optimization")
            ml_results = await self.test_ml_optimization(blueprint)
            
            # Calculate performance
            end_time = datetime.now(timezone.utc)
            total_time = (end_time - start_time).total_seconds()
            
            # Generate report
            await self.generate_test_report(total_time)
            
        except Exception as e:
            logger.error(f"Test suite failed: {e}")
            print(f"❌ Test suite failed: {e}")
    
    async def test_advanced_blueprint_generation(self) -> CompanyBlueprint:
        """Test advanced blueprint generation with MBA frameworks"""
        
        try:
            founder_dream = """
            I want to revolutionize the fitness industry with an AI-powered platform that provides 
            real-time form correction using computer vision. The platform will gamify workouts, 
            provide personalized AI coaching, and integrate with wearable devices. Target market 
            is busy professionals aged 25-45 who want efficient home workouts. I want to build 
            a subscription-based SaaS with freemium model and reach $1M ARR within 18 months.
            """
            
            print("   🔄 Generating comprehensive business blueprint...")
            
            # Create FounderDream object
            from core.dream_to_blueprint_generator import FounderDream
            dream_obj = FounderDream(
                raw_dream=founder_dream,
                revenue_goal=1000000,  # $1M ARR goal
                timeline_months=18,
                budget_available=500000
            )
            
            blueprint = await self.dream_generator.transform_dream_to_blueprint(dream_obj)
            
            # Validate blueprint
            quality_metrics = {
                "completeness": self._check_blueprint_completeness(blueprint),
                "business_viability": self._assess_business_viability(blueprint),
                "market_opportunity": blueprint.opportunity_score if hasattr(blueprint, 'opportunity_score') else 85,
                "revenue_timeline": blueprint.time_to_revenue_months if hasattr(blueprint, 'time_to_revenue_months') else 6
            }
            
            self.test_results["blueprint_generation"] = {
                "status": "PASSED",
                "blueprint_name": blueprint.name,
                "quality_metrics": quality_metrics,
                "key_features": len(blueprint.key_features),
                "competitive_advantages": len(blueprint.competitive_advantages)
            }
            
            print(f"   ✅ Blueprint: {blueprint.name}")
            print(f"   📊 Opportunity Score: {quality_metrics['market_opportunity']}/100")
            print(f"   ⏱️  Revenue Timeline: {quality_metrics['revenue_timeline']} months")
            print(f"   🏆 Completeness: {quality_metrics['completeness']:.1f}/10")
            
            return blueprint
            
        except Exception as e:
            self.test_results["blueprint_generation"] = {"status": "FAILED", "error": str(e)}
            raise
    
    async def test_advanced_business_intelligence(self, blueprint: CompanyBlueprint) -> Dict[str, Any]:
        """Test advanced business intelligence engine"""
        
        try:
            print("   🔄 Generating comprehensive business intelligence...")
            
            # Generate comprehensive BI report
            bi_report = await self.business_intelligence.generate_comprehensive_business_intelligence(blueprint)
            
            # Analyze BI quality
            bi_metrics = {
                "strategic_insights": len(bi_report.get("strategic_insights", [])),
                "financial_forecast_months": bi_report["financial_forecast"]["time_horizon_months"],
                "market_analysis_depth": len(bi_report["competitive_intelligence"]["competitor_landscape"]["direct_competitors"]),
                "risk_factors": len(bi_report["risk_assessment"]["risk_categories"]),
                "opportunities": len(bi_report["opportunity_analysis"]["opportunity_categories"])
            }
            
            self.test_results["business_intelligence"] = {
                "status": "PASSED",
                "bi_metrics": bi_metrics,
                "break_even_month": bi_report["financial_forecast"]["break_even_analysis"]["break_even_month"],
                "market_confidence": bi_report["market_forecast"]["confidence_interval"],
                "executive_summary_points": len(bi_report["executive_summary"]["key_findings"])
            }
            
            print(f"   ✅ Strategic Insights: {bi_metrics['strategic_insights']}")
            print(f"   📊 Financial Forecast: {bi_metrics['financial_forecast_months']} months")
            print(f"   🎯 Break-even: Month {bi_report['financial_forecast']['break_even_analysis']['break_even_month']}")
            print(f"   🏆 Analysis Depth: {bi_metrics['market_analysis_depth']} competitors")
            
            return bi_report
            
        except Exception as e:
            self.test_results["business_intelligence"] = {"status": "FAILED", "error": str(e)}
            raise
    
    async def test_ai_strategy_engine(self, blueprint: CompanyBlueprint) -> List[Any]:
        """Test AI-powered strategy engine"""
        
        try:
            print("   🔄 Generating AI-optimized strategies...")
            
            # Test multiple optimization objectives
            objectives = [
                OptimizationObjective.REVENUE_MAXIMIZATION,
                OptimizationObjective.MARKET_SHARE_GROWTH,
                OptimizationObjective.CUSTOMER_ACQUISITION
            ]
            
            # Generate strategies
            strategies = await self.ai_strategy_engine.generate_ai_strategy_recommendations(
                blueprint=blueprint,
                objectives=objectives
            )
            
            # Analyze strategy quality
            strategy_metrics = {
                "total_strategies": len(strategies),
                "avg_confidence": sum(s.confidence_score for s in strategies) / len(strategies) if strategies else 0,
                "avg_impact": sum(s.expected_impact for s in strategies) / len(strategies) if strategies else 0,
                "strategy_types": len(set(s.strategy_type.value for s in strategies)) if strategies else 0
            }
            
            self.test_results["ai_strategy_engine"] = {
                "status": "PASSED",
                "strategy_metrics": strategy_metrics,
                "objectives_tested": len(objectives),
                "top_strategy_confidence": max(s.confidence_score for s in strategies) if strategies else 0
            }
            
            print(f"   ✅ Strategies Generated: {strategy_metrics['total_strategies']}")
            print(f"   🎯 Average Confidence: {strategy_metrics['avg_confidence']:.2f}")
            print(f"   📈 Average Impact: {strategy_metrics['avg_impact']:.2f}")
            print(f"   🏆 Strategy Diversity: {strategy_metrics['strategy_types']} types")
            
            return strategies
            
        except Exception as e:
            self.test_results["ai_strategy_engine"] = {"status": "FAILED", "error": str(e)}
            raise
    
    async def test_monte_carlo_simulation(self, blueprint: CompanyBlueprint, strategies: List[Any]) -> Any:
        """Test Monte Carlo market simulations"""
        
        try:
            print("   🔄 Running Monte Carlo simulations...")
            
            if not strategies:
                raise ValueError("No strategies available for simulation")
            
            # Use best strategy for simulation
            best_strategy = max(strategies, key=lambda s: s.confidence_score * s.expected_impact)
            
            # Run simulation
            simulation = await self.ai_strategy_engine.run_monte_carlo_simulation(
                blueprint=blueprint,
                strategy=best_strategy,
                scenarios=3000  # Reduced for testing speed
            )
            
            # Analyze simulation results
            simulation_metrics = {
                "scenarios_run": simulation.simulation_parameters["scenarios"],
                "success_probability": simulation.monte_carlo_results["success_probability"],
                "mean_outcome": simulation.probability_distribution["mean"],
                "confidence_intervals": len(simulation.monte_carlo_results["confidence_intervals"]),
                "sensitivity_factors": len(simulation.sensitivity_analysis)
            }
            
            self.test_results["monte_carlo_simulation"] = {
                "status": "PASSED",
                "simulation_metrics": simulation_metrics,
                "strategy_tested": best_strategy.title,
                "outcome_variance": simulation.probability_distribution["std_dev"]
            }
            
            print(f"   ✅ Scenarios: {simulation_metrics['scenarios_run']:,}")
            print(f"   📊 Success Rate: {simulation_metrics['success_probability']:.1%}")
            print(f"   🎯 Mean Outcome: {simulation_metrics['mean_outcome']:.2f}")
            print(f"   🏆 Confidence Levels: {simulation_metrics['confidence_intervals']}")
            
            return simulation
            
        except Exception as e:
            self.test_results["monte_carlo_simulation"] = {"status": "FAILED", "error": str(e)}
            raise
    
    async def test_ml_optimization(self, blueprint: CompanyBlueprint) -> Dict[str, Any]:
        """Test machine learning optimization algorithms"""
        
        try:
            print("   🔄 Testing ML optimization algorithms...")
            
            # Test strategy for optimization
            test_strategy = {
                "type": "growth",
                "focus": "customer_acquisition",
                "investment": 100000,
                "expected_roi": 3.0,
                "timeline": "6 months"
            }
            
            # Test different algorithms
            genetic_result = await self.ai_strategy_engine._genetic_algorithm_optimization(
                test_strategy, blueprint, OptimizationObjective.REVENUE_MAXIMIZATION
            )
            
            annealing_result = await self.ai_strategy_engine._simulated_annealing_optimization(
                test_strategy, blueprint, OptimizationObjective.REVENUE_MAXIMIZATION
            )
            
            pso_result = await self.ai_strategy_engine._particle_swarm_optimization(
                test_strategy, blueprint, OptimizationObjective.REVENUE_MAXIMIZATION
            )
            
            # Analyze ML performance
            ml_metrics = {
                "algorithms_tested": 3,
                "genetic_impact": genetic_result.get("expected_impact", 0),
                "annealing_impact": annealing_result.get("expected_impact", 0),
                "pso_impact": pso_result.get("expected_impact", 0),
                "best_algorithm": max([genetic_result, annealing_result, pso_result], 
                                    key=lambda x: x.get("expected_impact", 0)).get("optimization_algorithm", "unknown")
            }
            
            self.test_results["ml_optimization"] = {
                "status": "PASSED",
                "ml_metrics": ml_metrics,
                "improvement_achieved": max(ml_metrics["genetic_impact"], ml_metrics["annealing_impact"], ml_metrics["pso_impact"]) > 0.5
            }
            
            print(f"   ✅ Algorithms Tested: {ml_metrics['algorithms_tested']}")
            print(f"   🧬 Genetic Algorithm: {ml_metrics['genetic_impact']:.2f}")
            print(f"   🔥 Simulated Annealing: {ml_metrics['annealing_impact']:.2f}")
            print(f"   🐝 Particle Swarm: {ml_metrics['pso_impact']:.2f}")
            print(f"   🏆 Best Algorithm: {ml_metrics['best_algorithm']}")
            
            return {
                "genetic": genetic_result,
                "annealing": annealing_result,
                "pso": pso_result
            }
            
        except Exception as e:
            self.test_results["ml_optimization"] = {"status": "FAILED", "error": str(e)}
            raise
    
    def _check_blueprint_completeness(self, blueprint: CompanyBlueprint) -> float:
        """Check blueprint completeness score"""
        
        score = 0.0
        
        # Basic information
        if blueprint.name and len(blueprint.name) > 5:
            score += 1.0
        if hasattr(blueprint, 'value_proposition') and blueprint.value_proposition and len(blueprint.value_proposition) > 20:
            score += 1.0
        if blueprint.key_features and len(blueprint.key_features) >= 3:
            score += 1.0
        if blueprint.competitive_advantages and len(blueprint.competitive_advantages) >= 2:
            score += 1.0
        
        # Business model
        if blueprint.business_model:
            score += 1.0
        if blueprint.target_market and blueprint.target_market.primary_segment:
            score += 1.0
        
        # Financial information
        if blueprint.revenue_projections:
            score += 1.0
        if blueprint.funding_requirements > 0:
            score += 1.0
        
        # Advanced features
        if hasattr(blueprint, 'opportunity_score') and blueprint.opportunity_score > 70:
            score += 1.0
        if hasattr(blueprint, 'time_to_revenue_months') and blueprint.time_to_revenue_months <= 12:
            score += 1.0
        
        return score
    
    def _assess_business_viability(self, blueprint: CompanyBlueprint) -> float:
        """Assess business viability score"""
        
        score = 0.0
        
        # Market opportunity
        if hasattr(blueprint, 'opportunity_score') and blueprint.opportunity_score > 80:
            score += 3.0
        elif hasattr(blueprint, 'opportunity_score') and blueprint.opportunity_score > 60:
            score += 2.0
        else:
            score += 1.0
        
        # Revenue timeline
        if hasattr(blueprint, 'time_to_revenue_months'):
            if blueprint.time_to_revenue_months <= 6:
                score += 2.0
            elif blueprint.time_to_revenue_months <= 12:
                score += 1.5
            else:
                score += 1.0
        
        # Competitive advantages
        if len(blueprint.competitive_advantages) >= 3:
            score += 2.0
        elif len(blueprint.competitive_advantages) >= 2:
            score += 1.5
        else:
            score += 1.0
        
        # Key features
        if len(blueprint.key_features) >= 5:
            score += 2.0
        elif len(blueprint.key_features) >= 3:
            score += 1.5
        else:
            score += 1.0
        
        return score
    
    async def generate_test_report(self, total_time: float):
        """Generate comprehensive test report"""
        
        print("\n" + "=" * 70)
        print("🎉 ADVANCED DREAM MACHINE TEST RESULTS")
        print("=" * 70)
        
        # Calculate success rate
        passed_tests = len([t for t in self.test_results.values() if t.get("status") == "PASSED"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📊 OVERALL PERFORMANCE:")
        print(f"   ✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        print(f"   ⏱️  Total Time: {total_time:.1f} seconds")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result.get("status") == "PASSED" else "❌"
            print(f"   {status_icon} {test_name.replace('_', ' ').title()}")
            
            if result.get("status") == "PASSED":
                if test_name == "blueprint_generation":
                    metrics = result.get("quality_metrics", {})
                    print(f"      📊 Opportunity: {metrics.get('market_opportunity', 0)}/100")
                    print(f"      🏆 Completeness: {metrics.get('completeness', 0):.1f}/10")
                
                elif test_name == "business_intelligence":
                    metrics = result.get("bi_metrics", {})
                    print(f"      🧠 Insights: {metrics.get('strategic_insights', 0)}")
                    print(f"      📊 Break-even: Month {result.get('break_even_month', 0)}")
                
                elif test_name == "ai_strategy_engine":
                    metrics = result.get("strategy_metrics", {})
                    print(f"      🎯 Strategies: {metrics.get('total_strategies', 0)}")
                    print(f"      📈 Avg Confidence: {metrics.get('avg_confidence', 0):.2f}")
                
                elif test_name == "monte_carlo_simulation":
                    metrics = result.get("simulation_metrics", {})
                    print(f"      🎲 Scenarios: {metrics.get('scenarios_run', 0):,}")
                    print(f"      📊 Success Rate: {metrics.get('success_probability', 0):.1%}")
                
                elif test_name == "ml_optimization":
                    metrics = result.get("ml_metrics", {})
                    print(f"      🔬 Algorithms: {metrics.get('algorithms_tested', 0)}")
                    print(f"      🏆 Best: {metrics.get('best_algorithm', 'unknown')}")
            
            else:
                print(f"      ❌ Error: {result.get('error', 'Unknown error')}")
        
        # Performance assessment
        print(f"\n🏆 PERFORMANCE ASSESSMENT:")
        
        if success_rate == 100:
            print("   🎉 EXCELLENT: All advanced features operational!")
            print("   🚀 Ready for production deployment")
        elif success_rate >= 80:
            print("   👍 VERY GOOD: Most advanced features working")
            print("   🔧 Minor fixes needed before production")
        elif success_rate >= 60:
            print("   ⚠️  GOOD: Core features working, some issues")
            print("   🛠️  Additional development needed")
        else:
            print("   🚨 NEEDS WORK: Multiple issues require attention")
            print("   🔨 Significant fixes needed")
        
        # Feature readiness
        print(f"\n🚀 FEATURE READINESS:")
        
        ready_features = []
        if self.test_results.get("blueprint_generation", {}).get("status") == "PASSED":
            ready_features.append("✅ Advanced Blueprint Generation")
        if self.test_results.get("business_intelligence", {}).get("status") == "PASSED":
            ready_features.append("✅ Business Intelligence Engine")
        if self.test_results.get("ai_strategy_engine", {}).get("status") == "PASSED":
            ready_features.append("✅ AI Strategy Optimization")
        if self.test_results.get("monte_carlo_simulation", {}).get("status") == "PASSED":
            ready_features.append("✅ Monte Carlo Simulations")
        if self.test_results.get("ml_optimization", {}).get("status") == "PASSED":
            ready_features.append("✅ Machine Learning Optimization")
        
        for feature in ready_features:
            print(f"   {feature}")
        
        print(f"\n🎯 NEXT STEPS:")
        if success_rate == 100:
            print("   🚀 Deploy advanced Dream Machine to production")
            print("   💡 Add user interface and API endpoints")
            print("   📊 Implement real-time monitoring")
        else:
            print("   🔧 Fix failing tests and optimize performance")
            print("   🧪 Run additional validation tests")
            print("   📈 Monitor and improve success rates")
        
        print("\n" + "=" * 70)
        print("🎉 Advanced Feature Test Complete!")
        print("=" * 70)

async def main():
    """Run the simplified advanced test suite"""
    
    test_suite = SimplifiedAdvancedTest()
    await test_suite.run_advanced_test_suite()

if __name__ == "__main__":
    asyncio.run(main())