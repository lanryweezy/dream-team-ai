"""
Test script for Accounting Agent functionality
Tests tax calculations, expense categorization, payroll processing across different jurisdictions
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the base agent since we're testing in isolation
class MockTaskResult:
    def __init__(self, success=True, output=None, cost_incurred=0.0, evidence=None, next_steps=None, error_message=None):
        self.success = success
        self.output = output or {}
        self.cost_incurred = cost_incurred
        self.evidence = evidence or []
        self.next_steps = next_steps or []
        self.error_message = error_message

class MockAgentCapability:
    def __init__(self, name, description, cost_estimate, confidence_level, requirements):
        self.name = name
        self.description = description
        self.cost_estimate = cost_estimate
        self.confidence_level = confidence_level
        self.requirements = requirements

class MockBaseAgent:
    def __init__(self, agent_id, capabilities):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.is_running = False
        
    async def start(self):
        self.is_running = True
        print(f"✅ {self.agent_id} started")
        
    async def stop(self):
        self.is_running = False
        print(f"🛑 {self.agent_id} stopped")
        
    async def request_approval(self, action, estimated_cost):
        """Mock approval - auto-approve for testing"""
        print(f"📋 Approval requested for {action.get('type', 'unknown')} - Cost: ${estimated_cost}")
        return True  # Auto-approve for testing

# Patch the imports
import sys
sys.modules['core.base_agent'] = type('MockModule', (), {
    'BaseAgent': MockBaseAgent,
    'AgentCapability': MockAgentCapability,
    'TaskResult': MockTaskResult
})()

# Now import our accounting agent
from agents.accounting_agent import (
    AccountingAgent, USAAccountingAgent, IndiaAccountingAgent, UKAccountingAgent,
    NigeriaAccountingAgent, SouthAfricaAccountingAgent, EgyptAccountingAgent, KenyaAccountingAgent
)

async def test_usa_accounting_agent():
    """Test USA Accounting Agent functionality"""
    print("\n🇺🇸 Testing USA Accounting Agent...")
    
    usa_agent = USAAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 150000,
        "business_type": "LLC",
        "deductions": [
            {"description": "Office rent", "amount": 24000},
            {"description": "Professional services", "amount": 8000},
            {"description": "Equipment", "amount": 5000}
        ],
        "state": "California"
    }
    
    result = await usa_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))
    
    # Test expense categorization
    expense_task = {
        "type": "expense_categorization",
        "expenses": [
            {"description": "Office supplies", "amount": 500, "date": "2024-01-15"},
            {"description": "Business lunch with client", "amount": 120, "date": "2024-01-20"},
            {"description": "Legal consultation", "amount": 2000, "date": "2024-01-25"},
            {"description": "Google Ads campaign", "amount": 800, "date": "2024-02-01"},
            {"description": "New laptop for development", "amount": 2500, "date": "2024-02-05"},
            {"description": "Office rent", "amount": 2000, "date": "2024-02-01"}
        ]
    }
    
    result = await usa_agent.handle_task(expense_task)
    print("✅ Expense categorization:", json.dumps(result, indent=2))
    
    # Test payroll taxes
    payroll_task = {
        "type": "payroll_taxes",
        "employees": [
            {"name": "John Doe", "annual_wages": 80000},
            {"name": "Jane Smith", "annual_wages": 95000},
            {"name": "Bob Johnson", "annual_wages": 120000}
        ]
    }
    
    result = await usa_agent.handle_task(payroll_task)
    print("✅ Payroll taxes:", json.dumps(result, indent=2))

async def test_india_accounting_agent():
    """Test India Accounting Agent functionality"""
    print("\n🇮🇳 Testing India Accounting Agent...")
    
    india_agent = IndiaAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 1500000,  # ₹15 lakhs
        "business_type": "Private Limited",
        "deductions": [
            {"description": "Section 80C investments", "amount": 150000},
            {"description": "Health insurance premium", "amount": 25000}
        ]
    }
    
    result = await india_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))
    
    # Test GST calculation
    gst_task = {
        "type": "gst_calculation",
        "transactions": [
            {"type": "sale", "amount": 100000, "gst_rate": 0.18},
            {"type": "sale", "amount": 50000, "gst_rate": 0.12},
            {"type": "purchase", "amount": 30000, "gst_rate": 0.18},
            {"type": "purchase", "amount": 20000, "gst_rate": 0.12}
        ],
        "business_type": "services"
    }
    
    result = await india_agent.handle_task(gst_task)
    print("✅ GST calculation:", json.dumps(result, indent=2))
    
    # Test TDS calculation
    tds_task = {
        "type": "tds_calculation",
        "payments": [
            {"type": "professional_fees", "amount": 50000, "recipient_pan": "ABCDE1234F"},
            {"type": "contractor_payment", "amount": 100000, "recipient_pan": "FGHIJ5678K"},
            {"type": "rent", "amount": 25000, "recipient_pan": ""}  # No PAN
        ]
    }
    
    result = await india_agent.handle_task(tds_task)
    print("✅ TDS calculation:", json.dumps(result, indent=2))

async def test_uk_accounting_agent():
    """Test UK Accounting Agent functionality"""
    print("\n🇬🇧 Testing UK Accounting Agent...")
    
    uk_agent = UKAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 75000,  # £75,000
        "business_type": "Limited Company",
        "deductions": [
            {"description": "Pension contributions", "amount": 5000},
            {"description": "Professional subscriptions", "amount": 500}
        ]
    }
    
    result = await uk_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))
    
    # Test VAT calculation
    vat_task = {
        "type": "vat_calculation",
        "transactions": [
            {"type": "sale", "amount": 10000, "vat_rate": 0.20},
            {"type": "sale", "amount": 5000, "vat_rate": 0.05},  # Reduced rate
            {"type": "purchase", "amount": 3000, "vat_rate": 0.20},
            {"type": "purchase", "amount": 1000, "vat_rate": 0.20}
        ]
    }
    
    result = await uk_agent.handle_task(vat_task)
    print("✅ VAT calculation:", json.dumps(result, indent=2))
    
    # Test corporation tax
    corp_tax_task = {
        "type": "corporation_tax",
        "profit": 180000  # £180,000
    }
    
    result = await uk_agent.handle_task(corp_tax_task)
    print("✅ Corporation tax:", json.dumps(result, indent=2))

async def test_nigeria_accounting_agent():
    """Test Nigeria Accounting Agent functionality"""
    print("\n🇳🇬 Testing Nigeria Accounting Agent...")
    
    nigeria_agent = NigeriaAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 5000000,  # ₦5 million
        "business_type": "Limited Company",
        "deductions": [
            {"description": "Office rent", "amount": 600000},
            {"description": "Professional services", "amount": 200000}
        ]
    }
    
    result = await nigeria_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))
    
    # Test VAT calculation
    vat_task = {
        "type": "vat_calculation",
        "transactions": [
            {"type": "sale", "amount": 1000000},
            {"type": "sale", "amount": 500000},
            {"type": "purchase", "amount": 300000},
            {"type": "purchase", "amount": 200000}
        ]
    }
    
    result = await nigeria_agent.handle_task(vat_task)
    print("✅ VAT calculation:", json.dumps(result, indent=2))

async def test_south_africa_accounting_agent():
    """Test South Africa Accounting Agent functionality"""
    print("\n🇿🇦 Testing South Africa Accounting Agent...")
    
    sa_agent = SouthAfricaAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 800000,  # R800,000
        "business_type": "Pty Ltd",
        "deductions": [
            {"description": "Retirement annuity", "amount": 50000},
            {"description": "Medical aid", "amount": 30000}
        ]
    }
    
    result = await sa_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))
    
    # Test VAT calculation
    vat_task = {
        "type": "vat_calculation",
        "transactions": [
            {"type": "sale", "amount": 100000},
            {"type": "purchase", "amount": 50000}
        ]
    }
    
    result = await sa_agent.handle_task(vat_task)
    print("✅ VAT calculation:", json.dumps(result, indent=2))

async def test_egypt_accounting_agent():
    """Test Egypt Accounting Agent functionality"""
    print("\n🇪🇬 Testing Egypt Accounting Agent...")
    
    egypt_agent = EgyptAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 250000,  # E£250,000
        "business_type": "Joint Stock",
        "deductions": [
            {"description": "Business expenses", "amount": 30000}
        ]
    }
    
    result = await egypt_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))

async def test_kenya_accounting_agent():
    """Test Kenya Accounting Agent functionality"""
    print("\n🇰🇪 Testing Kenya Accounting Agent...")
    
    kenya_agent = KenyaAccountingAgent()
    
    # Test tax calculation
    tax_task = {
        "type": "tax_calculation",
        "income": 1200000,  # KSh 1.2 million
        "business_type": "Limited",
        "deductions": [
            {"description": "Business expenses", "amount": 150000}
        ]
    }
    
    result = await kenya_agent.handle_task(tax_task)
    print("✅ Tax calculation:", json.dumps(result, indent=2))

async def test_accounting_agent_main():
    """Test main Accounting Agent with multi-jurisdiction capabilities"""
    print("\n🌍 Testing Main Accounting Agent...")
    
    accounting_agent = AccountingAgent()
    await accounting_agent.start()
    
    # Test multi-jurisdiction tax calculation
    multi_tax_task = {
        "type": "multi_jurisdiction_tax_calculation",
        "jurisdictions": ["USA", "India", "UK", "Nigeria"],
        "income": 100000,
        "business_type": "LLC",
        "deductions": [
            {"description": "Office expenses", "amount": 15000},
            {"description": "Professional development", "amount": 5000},
            {"description": "Travel expenses", "amount": 8000}
        ]
    }
    
    result = await accounting_agent.execute_task(multi_tax_task)
    print("✅ Multi-jurisdiction tax calculation:")
    print(f"   Success: {result.success}")
    print(f"   Cost: ${result.cost_incurred}")
    print(f"   Evidence files: {result.evidence}")
    print(f"   Supported jurisdictions: {result.output.get('supported_jurisdictions', 0)}")
    
    await accounting_agent.stop()

async def test_tax_scenarios():
    """Test various tax scenarios across jurisdictions"""
    print("\n💰 Testing Tax Scenarios...")
    
    scenarios = [
        {
            "name": "Startup Founder (Low Income)",
            "income": 50000,
            "business_type": "LLC",
            "deductions": [{"description": "Home office", "amount": 3000}]
        },
        {
            "name": "Growing Business (Medium Income)",
            "income": 150000,
            "business_type": "LLC", 
            "deductions": [
                {"description": "Equipment", "amount": 15000},
                {"description": "Marketing", "amount": 8000}
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📊 {scenario['name']}:")
        
        # Test USA
        usa_agent = USAAccountingAgent()
        usa_calc = usa_agent.calculate_taxes(
            scenario["income"], 
            scenario["business_type"], 
            scenario["deductions"]
        )
        print(f"   USA: ${usa_calc['total_federal_tax']:,.2f} ({usa_calc['effective_tax_rate']:.1f}%)")
        
        # Test Nigeria
        nigeria_agent = NigeriaAccountingAgent()
        nigeria_income = scenario["income"] * 1600  # Rough USD to NGN conversion
        nigeria_deductions = [{"description": d["description"], "amount": d["amount"] * 1600} for d in scenario["deductions"]]
        nigeria_calc = nigeria_agent.calculate_taxes(nigeria_income, "Limited Company", nigeria_deductions)
        print(f"   Nigeria: ₦{nigeria_calc['total_tax']:,.2f} ({nigeria_calc['effective_tax_rate']:.1f}%)")

async def main():
    """Run all accounting agent tests"""
    print("🧮 Starting Accounting Agent Tests...")
    print("=" * 60)
    
    try:
        # Test individual sub-agents
        await test_usa_accounting_agent()
        await test_india_accounting_agent()
        await test_uk_accounting_agent()
        
        # Test African countries
        await test_nigeria_accounting_agent()
        await test_south_africa_accounting_agent()
        await test_egypt_accounting_agent()
        await test_kenya_accounting_agent()
        
        # Test main accounting agent
        await test_accounting_agent_main()
        
        # Test various tax scenarios
        await test_tax_scenarios()
        
        print("\n" + "=" * 60)
        print("✅ All Accounting Agent tests completed successfully!")
        print("🌍 African countries (Nigeria, South Africa, Egypt, Kenya) now supported!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())