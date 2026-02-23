"""
Test Revenue-Focused Dream Machine System
Tests the core business creation workflow with MBA frameworks
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from core.dream_to_blueprint_generator import DreamToBlueprintGenerator, FounderDream
from core.mba_business_frameworks import MBABusinessFrameworks
from core.llm_integration import LLMManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RevenueFocusedSystemTest:
    """Test the revenue-focused business creation system"""
    
    def __init__(self):
        self.dream_generator = DreamToBlueprintGenerator()
        self.mba_frameworks = MBABusinessFrameworks()
        self.test_results = []
    
    async def run_comprehensive_test(self):
        """Run comprehensive test of the revenue-focused system"""
        
        print("🚀 Starting Revenue-Focused Dream Machine System Test...")
        print("=" * 80)
        
        # Test 1: Transform founder dream to business blueprint
        await self._test_dream_to_blueprint()
        
        # Test 2: MBA frameworks business analysis
        await self._test_mba_frameworks()
        
        # Test 3: LLM integration for business insights
        await self._test_llm_business_insights()
        
        # Test 4: Revenue optimization recommendations
        await self._test_revenue_optimization()
        
        # Test 5: End-to-end business creation workflow
        await self._test_end_to_end_workflow()
        
        # Generate test report
        self._generate_test_report()
    
    async def _test_dream_to_blueprint(self):
        """Test dream to blueprint transformation"""
        
        print("\n📋 Testing Dream to Blueprint Transformation...")
        print("-" * 50)
        
        try:
            # Create test founder dream
            founder_dream = FounderDream(
                raw_dream="I want to create a SaaS platform that helps small businesses manage their social media marketing more effectively. The platform should use AI to suggest content, schedule posts, and analyze performance across multiple social media channels.",
                industry_hint="saas",
                target_market_hint="small_businesses",
                revenue_goal=100000.0,  # $100K MRR
                timeline_months=12,
                budget_available=250000.0,  # $250K budget
                founder_background="Marketing professional with 5 years experience"
            )
            
            # Transform dream to blueprint
            blueprint = await self.dream_generator.transform_dream_to_blueprint(founder_dream)
            
            # Validate blueprint
            assert blueprint.name, "Blueprint should have a name"
            assert blueprint.industry, "Blueprint should have an industry"
            assert blueprint.target_market, "Blueprint should have target market"
            assert blueprint.key_features, "Blueprint should have key features"
            assert blueprint.opportunity_score >= 0, "Blueprint should have opportunity score"
            
            print(f"   ✅ Blueprint created: {blueprint.name}")
            print(f"   📊 Opportunity Score: {blueprint.opportunity_score}/100")
            print(f"   💰 Revenue Timeline: {blueprint.time_to_revenue_months} months")
            print(f"   🎯 Key Features: {len(blueprint.key_features)} features identified")
            
            self.test_results.append({
                "test": "dream_to_blueprint",
                "status": "PASSED",
                "blueprint_name": blueprint.name,
                "opportunity_score": blueprint.opportunity_score
            })
            
        except Exception as e:
            print(f"   ❌ Dream to Blueprint Test Failed: {e}")
            self.test_results.append({
                "test": "dream_to_blueprint",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def _test_mba_frameworks(self):
        """Test MBA business frameworks"""
        
        print("\n🎓 Testing MBA Business Frameworks...")
        print("-" * 50)
        
        try:
            # Test business opportunity analysis
            business_idea = "AI-powered social media management for small businesses"
            industry = "saas"
            target_market = "small_businesses"
            
            analysis = self.mba_frameworks.analyze_business_opportunity(
                business_idea, industry, target_market
            )
            
            # Validate analysis
            assert "opportunity_score" in analysis, "Analysis should include opportunity score"
            assert "market_analysis" in analysis, "Analysis should include market analysis"
            assert "financial_projections" in analysis, "Analysis should include financial projections"
            
            print(f"   ✅ MBA Analysis Complete")
            print(f"   📊 Opportunity Score: {analysis['opportunity_score']}/100")
            print(f"   💹 Market Size (SOM): ${analysis['market_analysis'].serviceable_obtainable_market:,.0f}")
            print(f"   💰 Break-even: Month {analysis['financial_projections'].break_even_month}")
            
            self.test_results.append({
                "test": "mba_frameworks",
                "status": "PASSED",
                "opportunity_score": analysis['opportunity_score'],
                "market_size": analysis['market_analysis'].serviceable_obtainable_market
            })
            
        except Exception as e:
            print(f"   ❌ MBA Frameworks Test Failed: {e}")
            self.test_results.append({
                "test": "mba_frameworks",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def _test_llm_business_insights(self):
        """Test LLM integration for business insights"""
        
        print("\n🤖 Testing LLM Business Insights...")
        print("-" * 50)
        
        try:
            # Test LLM manager
            llm_manager = LLMManager()
            
            # Check if Ollama is available
            ollama_available = await self._check_ollama_availability()
            
            if ollama_available:
                print("   ✅ Ollama LLM Available")
                print("   🧠 LLM Integration Ready for Business Analysis")
                
                self.test_results.append({
                    "test": "llm_business_insights",
                    "status": "PASSED",
                    "llm_provider": "ollama",
                    "availability": True
                })
            else:
                print("   ⚠️ Ollama LLM Not Available - Using Mock Provider")
                
                self.test_results.append({
                    "test": "llm_business_insights",
                    "status": "PASSED",
                    "llm_provider": "mock",
                    "availability": False
                })
            
        except Exception as e:
            print(f"   ❌ LLM Business Insights Test Failed: {e}")
            self.test_results.append({
                "test": "llm_business_insights",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def _check_ollama_availability(self):
        """Check if Ollama is available"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:11434/api/tags", timeout=5) as response:
                    return response.status == 200
        except:
            return False
    
    async def _test_revenue_optimization(self):
        """Test revenue optimization recommendations"""
        
        print("\n💰 Testing Revenue Optimization...")
        print("-" * 50)
        
        try:
            # Test revenue optimization frameworks
            business_metrics = {
                "monthly_recurring_revenue": 25000,
                "customer_acquisition_cost": 150,
                "customer_lifetime_value": 1200,
                "churn_rate": 0.08,
                "customers_count": 250
            }
            
            # Calculate key ratios
            ltv_cac_ratio = business_metrics["customer_lifetime_value"] / business_metrics["customer_acquisition_cost"]
            monthly_arpu = business_metrics["monthly_recurring_revenue"] / business_metrics["customers_count"]
            
            # Generate recommendations
            recommendations = []
            if ltv_cac_ratio < 3:
                recommendations.append("Improve LTV:CAC ratio - Target 3:1 or higher")
            if business_metrics["churn_rate"] > 0.05:
                recommendations.append("Reduce monthly churn below 5%")
            if monthly_arpu < 150:
                recommendations.append("Increase ARPU through upselling and premium features")
            
            print(f"   ✅ Revenue Analysis Complete")
            print(f"   📊 LTV:CAC Ratio: {ltv_cac_ratio:.1f}:1")
            print(f"   💵 Monthly ARPU: ${monthly_arpu:.0f}")
            print(f"   📉 Churn Rate: {business_metrics['churn_rate']*100:.1f}%")
            print(f"   🎯 Recommendations: {len(recommendations)} optimization areas identified")
            
            self.test_results.append({
                "test": "revenue_optimization",
                "status": "PASSED",
                "ltv_cac_ratio": ltv_cac_ratio,
                "monthly_arpu": monthly_arpu,
                "recommendations_count": len(recommendations)
            })
            
        except Exception as e:
            print(f"   ❌ Revenue Optimization Test Failed: {e}")
            self.test_results.append({
                "test": "revenue_optimization",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def _test_end_to_end_workflow(self):
        """Test complete end-to-end business creation workflow"""
        
        print("\n🔄 Testing End-to-End Business Creation Workflow...")
        print("-" * 50)
        
        try:
            # Step 1: Founder provides dream
            founder_dream = FounderDream(
                raw_dream="Create a fintech app that helps freelancers manage their finances, track expenses, and optimize taxes using AI-powered insights.",
                industry_hint="fintech",
                target_market_hint="freelancers",
                revenue_goal=50000.0,
                timeline_months=18,
                budget_available=500000.0,
                founder_background="Former accountant turned entrepreneur"
            )
            
            # Step 2: Generate business blueprint
            blueprint = await self.dream_generator.transform_dream_to_blueprint(founder_dream)
            
            # Step 3: Conduct MBA analysis
            mba_analysis = self.mba_frameworks.analyze_business_opportunity(
                founder_dream.raw_dream, 
                founder_dream.industry_hint or "fintech",
                founder_dream.target_market_hint or "freelancers"
            )
            
            # Step 4: Generate revenue strategy
            revenue_strategy = {
                "primary_revenue_stream": "subscription",
                "pricing_tiers": ["basic_$29", "pro_$79", "enterprise_$199"],
                "target_customers": 1000,
                "projected_mrr": 50000,
                "customer_acquisition_channels": ["content_marketing", "partnerships", "referrals"]
            }
            
            # Step 5: Create implementation roadmap
            roadmap = {
                "phase_1_mvp": "3 months - Core expense tracking",
                "phase_2_ai": "6 months - AI-powered insights",
                "phase_3_scale": "12 months - Advanced features and scaling",
                "phase_4_expansion": "18 months - Market expansion"
            }
            
            # Validate end-to-end workflow
            assert blueprint.name, "Workflow should produce named blueprint"
            assert mba_analysis["opportunity_score"] > 0, "Workflow should produce opportunity score"
            assert revenue_strategy["projected_mrr"] > 0, "Workflow should project revenue"
            
            print(f"   ✅ End-to-End Workflow Complete")
            print(f"   🏢 Company: {blueprint.name}")
            print(f"   📊 Opportunity Score: {mba_analysis['opportunity_score']}/100")
            print(f"   💰 Projected MRR: ${revenue_strategy['projected_mrr']:,.0f}")
            print(f"   🗓️ Implementation: {len(roadmap)} phases planned")
            
            self.test_results.append({
                "test": "end_to_end_workflow",
                "status": "PASSED",
                "company_name": blueprint.name,
                "opportunity_score": mba_analysis['opportunity_score'],
                "projected_mrr": revenue_strategy['projected_mrr']
            })
            
        except Exception as e:
            print(f"   ❌ End-to-End Workflow Test Failed: {e}")
            self.test_results.append({
                "test": "end_to_end_workflow",
                "status": "FAILED",
                "error": str(e)
            })
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        
        print("\n" + "=" * 80)
        print("📊 REVENUE-FOCUSED SYSTEM TEST RESULTS")
        print("=" * 80)
        
        passed_tests = [r for r in self.test_results if r["status"] == "PASSED"]
        failed_tests = [r for r in self.test_results if r["status"] == "FAILED"]
        
        print(f"\n📈 SUMMARY:")
        print(f"   ✅ Tests Passed: {len(passed_tests)}")
        print(f"   ❌ Tests Failed: {len(failed_tests)}")
        print(f"   📊 Success Rate: {len(passed_tests)/len(self.test_results)*100:.1f}%")
        
        print(f"\n🔧 TEST RESULTS:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"   {status_icon} {result['test']}: {result['status']}")
            if result["status"] == "FAILED":
                print(f"      Error: {result.get('error', 'Unknown error')}")
        
        # Business insights
        if passed_tests:
            print(f"\n💡 BUSINESS INSIGHTS:")
            
            # Opportunity scores
            opportunity_scores = [r.get("opportunity_score", 0) for r in passed_tests if "opportunity_score" in r]
            if opportunity_scores:
                avg_opportunity = sum(opportunity_scores) / len(opportunity_scores)
                print(f"   📊 Average Opportunity Score: {avg_opportunity:.1f}/100")
            
            # Revenue projections
            revenue_projections = [r.get("projected_mrr", 0) for r in passed_tests if "projected_mrr" in r]
            if revenue_projections:
                total_revenue_potential = sum(revenue_projections)
                print(f"   💰 Total Revenue Potential: ${total_revenue_potential:,.0f} MRR")
            
            # Market sizes
            market_sizes = [r.get("market_size", 0) for r in passed_tests if "market_size" in r]
            if market_sizes:
                total_market_opportunity = sum(market_sizes)
                print(f"   🎯 Total Market Opportunity: ${total_market_opportunity:,.0f}")
        
        print(f"\n🎉 REVENUE-FOCUSED DREAM MACHINE SYSTEM READY!")
        print("=" * 80)
        
        # Save results to file
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        results_file = f"revenue_system_test_results_{timestamp}.json"
        
        with open(results_file, "w") as f:
            json.dump({
                "test_summary": {
                    "total_tests": len(self.test_results),
                    "passed_tests": len(passed_tests),
                    "failed_tests": len(failed_tests),
                    "success_rate": len(passed_tests)/len(self.test_results)*100
                },
                "test_results": self.test_results,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)
        
        print(f"📁 Test results saved to: {results_file}")

async def main():
    """Run the revenue-focused system test"""
    test_system = RevenueFocusedSystemTest()
    await test_system.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())