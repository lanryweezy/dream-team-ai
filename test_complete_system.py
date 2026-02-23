"""
Comprehensive Test Suite for Dream Machine
Tests all components: Core, Agents, Toolkit, and Integration workflows
"""

import asyncio
import json
import os
import sys
from datetime import datetime
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 Starting Complete Dream Machine System Tests...")
print("=" * 80)

# Test Results Tracker
test_results = {
    "core_tests": {},
    "agent_tests": {},
    "toolkit_tests": {},
    "integration_tests": {},
    "total_passed": 0,
    "total_failed": 0,
    "errors": []
}

async def test_core_system():
    """Test all core system components"""
    print("\n🔧 TESTING CORE SYSTEM COMPONENTS")
    print("-" * 50)
    
    core_results = {}
    
    # Test Base Agent
    try:
        print("📋 Testing Base Agent...")
        from core.base_agent import BaseAgent, AgentCapability, TaskResult
        
        # Create test capability
        capability = AgentCapability(
            name="test_capability",
            description="Test capability",
            cost_estimate=1.0,
            confidence_level=0.9,
            requirements=[]
        )
        
        # Create test agent
        agent = BaseAgent("test_agent", [capability])
        await agent.start()
        
        # Test task execution
        test_task = {"type": "test", "data": "test_data"}
        result = await agent.execute_task(test_task)
        
        await agent.stop()
        
        core_results["base_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Base Agent: PASSED")
        
    except Exception as e:
        core_results["base_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Base Agent: {str(e)}")
        print(f"   ❌ Base Agent: FAILED - {str(e)}")
    
    # Test Message Bus
    try:
        print("📨 Testing Message Bus...")
        from core.message_bus import MessageBus, Message
        
        bus = MessageBus()
        await bus.start()
        
        # Test message publishing and subscribing
        received_messages = []
        
        async def test_handler(message):
            received_messages.append(message)
        
        await bus.subscribe("test_topic", test_handler)
        
        test_message = Message(
            id="test_msg_1",
            sender="test_sender",
            recipient="test_recipient",
            message_type="test",
            content={"test": "data"},
            priority=1
        )
        
        await bus.publish("test_topic", test_message)
        await asyncio.sleep(0.1)  # Allow message processing
        
        await bus.stop()
        
        if len(received_messages) > 0:
            core_results["message_bus"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Message Bus: PASSED")
        else:
            raise Exception("No messages received")
            
    except Exception as e:
        core_results["message_bus"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Message Bus: {str(e)}")
        print(f"   ❌ Message Bus: FAILED - {str(e)}")
    
    # Test Policy Engine
    try:
        print("🛡️ Testing Policy Engine...")
        from core.policy_engine import PolicyEngine, Policy, PolicyRule
        
        engine = PolicyEngine()
        
        # Create test policy
        rule = PolicyRule(
            condition="cost < 100",
            action="auto_approve",
            priority=1
        )
        
        policy = Policy(
            name="test_policy",
            description="Test policy",
            rules=[rule],
            enabled=True
        )
        
        engine.add_policy(policy)
        
        # Test policy evaluation
        context = {"cost": 50, "action": "test_action"}
        result = engine.evaluate("test_action", context)
        
        core_results["policy_engine"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Policy Engine: PASSED")
        
    except Exception as e:
        core_results["policy_engine"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Policy Engine: {str(e)}")
        print(f"   ❌ Policy Engine: FAILED - {str(e)}")
    
    # Test Cost Tracker
    try:
        print("💰 Testing Cost Tracker...")
        from core.cost_tracker import CostTracker, CostEntry
        
        tracker = CostTracker()
        
        # Add test cost entries
        entry1 = CostEntry(
            agent_id="test_agent",
            action="test_action",
            cost=25.50,
            currency="USD",
            description="Test cost entry"
        )
        
        tracker.add_cost(entry1)
        
        # Test cost retrieval
        total_cost = tracker.get_total_cost()
        agent_costs = tracker.get_agent_costs("test_agent")
        
        if total_cost > 0 and len(agent_costs) > 0:
            core_results["cost_tracker"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Cost Tracker: PASSED")
        else:
            raise Exception("Cost tracking failed")
            
    except Exception as e:
        core_results["cost_tracker"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Cost Tracker: {str(e)}")
        print(f"   ❌ Cost Tracker: FAILED - {str(e)}")
    
    # Test Goal Planner
    try:
        print("🎯 Testing Goal Planner...")
        from core.goal_planner import GoalPlanner, Goal, Milestone
        
        planner = GoalPlanner()
        
        # Create test goal with milestones
        milestone1 = Milestone(
            id="m1",
            title="First milestone",
            description="Complete initial setup",
            due_date=datetime.now(),
            dependencies=[],
            estimated_cost=100.0
        )
        
        goal = Goal(
            id="test_goal",
            title="Test Goal",
            description="Test goal for validation",
            priority=1,
            milestones=[milestone1],
            target_date=datetime.now()
        )
        
        planner.add_goal(goal)
        
        # Test goal retrieval and planning
        goals = planner.get_goals()
        daily_tasks = planner.get_daily_tasks()
        
        if len(goals) > 0:
            core_results["goal_planner"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Goal Planner: PASSED")
        else:
            raise Exception("Goal planning failed")
            
    except Exception as e:
        core_results["goal_planner"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Goal Planner: {str(e)}")
        print(f"   ❌ Goal Planner: FAILED - {str(e)}")
    
    # Test Company Blueprint
    try:
        print("📋 Testing Company Blueprint...")
        from core.company_blueprint import CompanyBlueprint, BusinessModel, TargetMarket
        
        # Create test target market
        target_market = TargetMarket(
            segment="Tech Startups",
            size=1000000,
            demographics={"age": "25-45", "income": "high"},
            pain_points=["Time management", "Cost optimization"]
        )
        
        # Create test business model
        business_model = BusinessModel(
            type="SaaS",
            revenue_streams=["Subscription", "Premium features"],
            cost_structure=["Development", "Marketing", "Operations"],
            key_partnerships=["Cloud providers", "Payment processors"]
        )
        
        # Create company blueprint
        blueprint = CompanyBlueprint(
            company_name="Test Company",
            vision="Test vision",
            mission="Test mission",
            target_market=target_market,
            business_model=business_model,
            initial_budget=50000.0
        )
        
        # Test blueprint operations
        blueprint_dict = blueprint.to_dict()
        
        if blueprint_dict and "company_name" in blueprint_dict:
            core_results["company_blueprint"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Company Blueprint: PASSED")
        else:
            raise Exception("Blueprint creation failed")
            
    except Exception as e:
        core_results["company_blueprint"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Company Blueprint: {str(e)}")
        print(f"   ❌ Company Blueprint: FAILED - {str(e)}")
    
    test_results["core_tests"] = core_results
    return core_results

async def test_all_agents():
    """Test all agent components"""
    print("\n🤖 TESTING ALL AGENT COMPONENTS")
    print("-" * 50)
    
    agent_results = {}
    
    # Test CEO Agent
    try:
        print("👔 Testing CEO Agent...")
        from agents.ceo_agent import CEOAgent
        
        ceo = CEOAgent()
        await ceo.start()
        
        # Test company creation task
        company_task = {
            "type": "create_company",
            "dream": "I want to build a fitness tracking app",
            "budget": 10000,
            "timeline": "3 months"
        }
        
        result = await ceo.execute_task(company_task)
        await ceo.stop()
        
        agent_results["ceo_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ CEO Agent: PASSED")
        
    except Exception as e:
        agent_results["ceo_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"CEO Agent: {str(e)}")
        print(f"   ❌ CEO Agent: FAILED - {str(e)}")
    
    # Test Finance Agent
    try:
        print("💰 Testing Finance Agent...")
        from agents.finance_agent import FinanceAgent
        
        finance = FinanceAgent()
        await finance.start()
        
        # Test budget analysis
        budget_task = {
            "type": "budget_analysis",
            "revenue": 50000,
            "expenses": [
                {"category": "development", "amount": 15000},
                {"category": "marketing", "amount": 10000}
            ]
        }
        
        result = await finance.execute_task(budget_task)
        await finance.stop()
        
        agent_results["finance_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Finance Agent: PASSED")
        
    except Exception as e:
        agent_results["finance_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Finance Agent: {str(e)}")
        print(f"   ❌ Finance Agent: FAILED - {str(e)}")
    
    # Test Marketing Agent
    try:
        print("📢 Testing Marketing Agent...")
        from agents.marketing_agent import MarketingAgent
        
        marketing = MarketingAgent()
        await marketing.start()
        
        # Test campaign creation
        campaign_task = {
            "type": "create_campaign",
            "product": "Fitness App",
            "target_audience": "Health-conscious millennials",
            "budget": 5000,
            "channels": ["social_media", "content_marketing"]
        }
        
        result = await marketing.execute_task(campaign_task)
        await marketing.stop()
        
        agent_results["marketing_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Marketing Agent: PASSED")
        
    except Exception as e:
        agent_results["marketing_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Marketing Agent: {str(e)}")
        print(f"   ❌ Marketing Agent: FAILED - {str(e)}")
    
    # Test Product Agent
    try:
        print("🛠️ Testing Product Agent...")
        from agents.product_agent import ProductAgent
        
        product = ProductAgent()
        await product.start()
        
        # Test feature planning
        feature_task = {
            "type": "plan_features",
            "product_type": "mobile_app",
            "target_users": "fitness enthusiasts",
            "core_functionality": "workout tracking"
        }
        
        result = await product.execute_task(feature_task)
        await product.stop()
        
        agent_results["product_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Product Agent: PASSED")
        
    except Exception as e:
        agent_results["product_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Product Agent: {str(e)}")
        print(f"   ❌ Product Agent: FAILED - {str(e)}")
    
    # Test Sales Agent
    try:
        print("💼 Testing Sales Agent...")
        from agents.sales_agent import SalesAgent
        
        sales = SalesAgent()
        await sales.start()
        
        # Test lead generation
        lead_task = {
            "type": "generate_leads",
            "target_market": "fitness centers",
            "product": "fitness tracking app",
            "lead_count": 50
        }
        
        result = await sales.execute_task(lead_task)
        await sales.stop()
        
        agent_results["sales_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Sales Agent: PASSED")
        
    except Exception as e:
        agent_results["sales_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Sales Agent: {str(e)}")
        print(f"   ❌ Sales Agent: FAILED - {str(e)}")
    
    # Test Investor Agent
    try:
        print("💎 Testing Investor Agent...")
        from agents.investor_agent import InvestorAgent
        
        investor = InvestorAgent()
        await investor.start()
        
        # Test investor matching
        investor_task = {
            "type": "find_investors",
            "industry": "fitness_tech",
            "stage": "seed",
            "funding_amount": 500000,
            "location": "USA"
        }
        
        result = await investor.execute_task(investor_task)
        await investor.stop()
        
        agent_results["investor_agent"] = "✅ PASSED"
        test_results["total_passed"] += 1
        print("   ✅ Investor Agent: PASSED")
        
    except Exception as e:
        agent_results["investor_agent"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Investor Agent: {str(e)}")
        print(f"   ❌ Investor Agent: FAILED - {str(e)}")
    
    test_results["agent_tests"] = agent_results
    return agent_results

async def test_toolkit():
    """Test all toolkit components"""
    print("\n🧰 TESTING TOOLKIT COMPONENTS")
    print("-" * 50)
    
    toolkit_results = {}
    
    # Test Landing Page Generator
    try:
        print("🌐 Testing Landing Page Generator...")
        from toolkit.landing_page_generator import LandingPageGenerator
        
        generator = LandingPageGenerator()
        
        # Test landing page creation
        page_config = {
            "company_name": "FitTrack Pro",
            "tagline": "Track your fitness journey",
            "description": "The ultimate fitness tracking app",
            "features": ["Workout tracking", "Progress analytics", "Social sharing"]
        }
        
        result = generator.generate_landing_page(page_config)
        
        if result.get("success") and result.get("files"):
            toolkit_results["landing_page_generator"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Landing Page Generator: PASSED")
        else:
            raise Exception("Landing page generation failed")
            
    except Exception as e:
        toolkit_results["landing_page_generator"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Landing Page Generator: {str(e)}")
        print(f"   ❌ Landing Page Generator: FAILED - {str(e)}")
    
    # Test Repo Manager
    try:
        print("📁 Testing Repo Manager...")
        from toolkit.repo_manager import RepoManager
        
        manager = RepoManager()
        
        # Test project initialization
        result = manager.initialize_project("./test_project", "web", "react")
        
        if result.get("success") and result.get("files_created"):
            toolkit_results["repo_manager"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Repo Manager: PASSED")
        else:
            raise Exception("Repo structure creation failed")
            
    except Exception as e:
        toolkit_results["repo_manager"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Repo Manager: {str(e)}")
        print(f"   ❌ Repo Manager: FAILED - {str(e)}")
    
    # Test Email Manager
    try:
        print("📧 Testing Email Manager...")
        from toolkit.email_manager import EmailManager
        
        manager = EmailManager()
        
        # Test waitlist email creation
        result = manager.create_waitlist_email("FitTrack Pro", "FitTrack App")
        
        if result.get("success") and result.get("subject") and result.get("content"):
            toolkit_results["email_manager"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Email Manager: PASSED")
        else:
            raise Exception("Email template creation failed")
            
    except Exception as e:
        toolkit_results["email_manager"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Email Manager: {str(e)}")
        print(f"   ❌ Email Manager: FAILED - {str(e)}")
    
    # Test Deployment Manager
    try:
        print("🚀 Testing Deployment Manager...")
        from toolkit.deployment_manager import DeploymentManager
        
        manager = DeploymentManager()
        
        # Test deployment configuration
        deploy_config = {
            "app_name": "fittrack-pro",
            "platform": "vercel",
            "environment": "production",
            "domain": "fittrackpro.com"
        }
        
        deployment_plan = manager.create_deployment_plan(deploy_config)
        
        if deployment_plan and "steps" in deployment_plan:
            toolkit_results["deployment_manager"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Deployment Manager: PASSED")
        else:
            raise Exception("Deployment plan creation failed")
            
    except Exception as e:
        toolkit_results["deployment_manager"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Deployment Manager: {str(e)}")
        print(f"   ❌ Deployment Manager: FAILED - {str(e)}")
    
    test_results["toolkit_tests"] = toolkit_results
    return toolkit_results

async def test_integration_workflows():
    """Test end-to-end integration workflows"""
    print("\n🔄 TESTING INTEGRATION WORKFLOWS")
    print("-" * 50)
    
    integration_results = {}
    
    # Test Complete Company Creation Workflow
    try:
        print("🏢 Testing Complete Company Creation Workflow...")
        
        # This would test the full dream-to-company pipeline
        # For now, we'll test the coordination between components
        
        from agents.ceo_agent import CEOAgent
        from agents.legal_agent import LegalAgent
        from agents.accounting_agent import AccountingAgent
        from toolkit.landing_page_generator import LandingPageGenerator
        
        # Initialize components
        ceo = CEOAgent()
        legal = LegalAgent()
        accounting = AccountingAgent()
        landing_gen = LandingPageGenerator()
        
        await ceo.start()
        await legal.start()
        await accounting.start()
        
        # Simulate company creation workflow
        dream = "I want to build a fitness tracking app for millennials"
        
        # CEO creates company blueprint
        company_task = {
            "type": "create_company",
            "dream": dream,
            "budget": 50000,
            "timeline": "6 months"
        }
        
        ceo_result = await ceo.execute_task(company_task)
        
        # Legal handles incorporation
        legal_task = {
            "type": "incorporation_guidance",
            "business_type": "SaaS",
            "jurisdiction": "USA"
        }
        
        legal_result = await legal.execute_task(legal_task)
        
        # Accounting sets up financial structure
        accounting_task = {
            "type": "tax_calculation",
            "income": 0,  # New company
            "business_type": "LLC",
            "deductions": []
        }
        
        accounting_result = await accounting.execute_task(accounting_task)
        
        # Generate landing page
        page_config = {
            "company_name": "FitTrack Pro",
            "tagline": "Your fitness journey starts here",
            "description": "Track workouts, monitor progress, achieve goals",
            "features": ["Workout Tracking", "Progress Analytics", "Goal Setting"],
            "cta_text": "Join Waitlist"
        }
        
        landing_page = landing_gen.generate_landing_page(page_config)
        
        await ceo.stop()
        await legal.stop()
        await accounting.stop()
        
        # Check if all components worked together
        if (ceo_result.success and legal_result.success and 
            accounting_result.success and landing_page):
            integration_results["company_creation_workflow"] = "✅ PASSED"
            test_results["total_passed"] += 1
            print("   ✅ Company Creation Workflow: PASSED")
        else:
            raise Exception("Workflow integration failed")
            
    except Exception as e:
        integration_results["company_creation_workflow"] = f"❌ FAILED: {str(e)}"
        test_results["total_failed"] += 1
        test_results["errors"].append(f"Company Creation Workflow: {str(e)}")
        print(f"   ❌ Company Creation Workflow: FAILED - {str(e)}")
    
    test_results["integration_tests"] = integration_results
    return integration_results

async def run_all_tests():
    """Run all tests and generate comprehensive report"""
    
    try:
        # Run all test suites
        core_results = await test_core_system()
        agent_results = await test_all_agents()
        toolkit_results = await test_toolkit()
        integration_results = await test_integration_workflows()
        
        # Generate final report
        print("\n" + "=" * 80)
        print("📊 COMPLETE SYSTEM TEST RESULTS")
        print("=" * 80)
        
        print(f"\n📈 SUMMARY:")
        print(f"   ✅ Tests Passed: {test_results['total_passed']}")
        print(f"   ❌ Tests Failed: {test_results['total_failed']}")
        print(f"   📊 Success Rate: {(test_results['total_passed'] / (test_results['total_passed'] + test_results['total_failed']) * 100):.1f}%")
        
        print(f"\n🔧 CORE SYSTEM RESULTS:")
        for component, result in core_results.items():
            print(f"   {component}: {result}")
        
        print(f"\n🤖 AGENT SYSTEM RESULTS:")
        for agent, result in agent_results.items():
            print(f"   {agent}: {result}")
        
        print(f"\n🧰 TOOLKIT RESULTS:")
        for tool, result in toolkit_results.items():
            print(f"   {tool}: {result}")
        
        print(f"\n🔄 INTEGRATION RESULTS:")
        for workflow, result in integration_results.items():
            print(f"   {workflow}: {result}")
        
        if test_results["errors"]:
            print(f"\n❌ ERRORS ENCOUNTERED:")
            for error in test_results["errors"]:
                print(f"   • {error}")
        
        # Save test results to file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        results_file = f"test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(test_results, f, indent=2, default=str)
        
        print(f"\n📁 Test results saved to: {results_file}")
        
        # Overall system status
        if test_results["total_failed"] == 0:
            print("\n🎉 ALL SYSTEMS OPERATIONAL - DREAM MACHINE READY!")
        elif test_results["total_failed"] < test_results["total_passed"]:
            print("\n⚠️  MOSTLY OPERATIONAL - SOME ISSUES NEED ATTENTION")
        else:
            print("\n🚨 CRITICAL ISSUES - SYSTEM NEEDS MAJOR FIXES")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n💥 CRITICAL TEST FAILURE: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_tests())