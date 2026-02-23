"""
Test script for Legal Agent functionality
Tests various legal agent capabilities across different jurisdictions
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

# Now import our legal agent
from agents.legal_agent import LegalAgent, USALegalAgent, IndiaLegalAgent, ChinaLegalAgent

async def test_usa_legal_agent():
    """Test USA Legal Agent functionality"""
    print("\n🇺🇸 Testing USA Legal Agent...")
    
    usa_agent = USALegalAgent()
    
    # Test incorporation
    incorporation_task = {
        "type": "incorporation",
        "business_type": "LLC",
        "state": "Delaware",
        "seeking_investment": True
    }
    
    result = await usa_agent.handle_task(incorporation_task)
    print("✅ Incorporation guidance:", json.dumps(result, indent=2))
    
    # Test compliance check
    compliance_task = {
        "type": "compliance_check",
        "business_type": "fintech"
    }
    
    result = await usa_agent.handle_task(compliance_task)
    print("✅ Compliance requirements:", json.dumps(result, indent=2))
    
    # Test IP protection
    ip_task = {
        "type": "ip_protection",
        "ip_type": "trademark"
    }
    
    result = await usa_agent.handle_task(ip_task)
    print("✅ IP protection guidance:", json.dumps(result, indent=2))

async def test_india_legal_agent():
    """Test India Legal Agent functionality"""
    print("\n🇮🇳 Testing India Legal Agent...")
    
    india_agent = IndiaLegalAgent()
    
    # Test incorporation
    incorporation_task = {
        "type": "incorporation",
        "business_type": "Private Limited"
    }
    
    result = await india_agent.handle_task(incorporation_task)
    print("✅ Incorporation guidance:", json.dumps(result, indent=2))
    
    # Test GST compliance
    gst_task = {
        "type": "gst_compliance",
        "annual_turnover": 6000000  # 60 lakhs
    }
    
    result = await india_agent.handle_task(gst_task)
    print("✅ GST compliance:", json.dumps(result, indent=2))

async def test_legal_agent_main():
    """Test main Legal Agent with multi-jurisdiction capabilities"""
    print("\n🌍 Testing Main Legal Agent...")
    
    legal_agent = LegalAgent()
    await legal_agent.start()
    
    # Test multi-jurisdiction compliance
    multi_jurisdiction_task = {
        "type": "multi_jurisdiction_compliance",
        "jurisdictions": ["USA", "India", "UK", "Nigeria"],
        "business_type": "SaaS"
    }
    
    result = await legal_agent.execute_task(multi_jurisdiction_task)
    print("✅ Multi-jurisdiction compliance:")
    print(f"   Success: {result.success}")
    print(f"   Cost: ${result.cost_incurred}")
    print(f"   Evidence files: {result.evidence}")
    print(f"   Next steps: {result.next_steps}")
    
    # Test contract generation
    contract_task = {
        "type": "contract_generation",
        "contract_type": "service_agreement",
        "jurisdiction": "USA",
        "parties": {
            "client_name": "Acme Corp",
            "client_address": "123 Business St, New York, NY",
            "provider_name": "Dream Team LLC",
            "provider_address": "456 Tech Ave, San Francisco, CA",
            "service_description": "Software development services",
            "total_fee": "$50,000",
            "payment_schedule": "Net 30 days",
            "ip_owner": "Client",
            "termination_notice": "30",
            "governing_state": "California"
        }
    }
    
    result = await legal_agent.execute_task(contract_task)
    print("✅ Contract generation:")
    print(f"   Success: {result.success}")
    print(f"   Contract file: {result.output.get('contract_file', 'N/A')}")
    print(f"   Missing fields: {result.output.get('missing_fields', [])}")
    
    # Test IP protection analysis
    ip_task = {
        "type": "ip_protection",
        "ip_type": "patent",
        "jurisdiction": "USA",
        "asset_details": {
            "invention_name": "AI-Powered Legal Assistant",
            "description": "Machine learning system for legal document analysis"
        }
    }
    
    result = await legal_agent.execute_task(ip_task)
    print("✅ IP protection analysis:")
    print(f"   Success: {result.success}")
    print(f"   Analysis: {json.dumps(result.output, indent=2)}")
    
    # Test regulatory analysis
    regulatory_task = {
        "type": "regulatory_analysis",
        "industry": "fintech",
        "jurisdiction": "USA",
        "business_model": "Digital payments"
    }
    
    result = await legal_agent.execute_task(regulatory_task)
    print("✅ Regulatory analysis:")
    print(f"   Success: {result.success}")
    print(f"   Framework: {result.output.get('regulatory_framework', {}).get('primary_regulators', [])}")
    print(f"   Compliance costs: {result.output.get('regulatory_framework', {}).get('compliance_costs', 'N/A')}")
    
    await legal_agent.stop()

async def test_document_review():
    """Test document review functionality"""
    print("\n📄 Testing Document Review...")
    
    legal_agent = LegalAgent()
    await legal_agent.start()
    
    # Test contract review
    review_task = {
        "type": "legal_document_review",
        "document_type": "contract",
        "jurisdiction": "USA",
        "document_content": """
        This Service Agreement is between Client Corp and Provider LLC.
        Services: Software development and maintenance.
        Payment: $10,000 monthly, net 30 days.
        Liability: Provider shall be liable for all damages without limitation.
        Termination: Either party may terminate immediately without notice.
        """
    }
    
    result = await legal_agent.execute_task(review_task)
    print("✅ Document review:")
    print(f"   Success: {result.success}")
    print(f"   Risk level: {result.output.get('risk_level', 'N/A')}")
    print(f"   Recommendations: {result.output.get('recommendations', [])}")
    
    await legal_agent.stop()

async def test_compliance_requirements():
    """Test compliance requirements for different business types"""
    print("\n📋 Testing Compliance Requirements...")
    
    legal_agent = LegalAgent()
    
    # Test different business types across jurisdictions
    business_types = ["SaaS", "fintech", "e-commerce", "healthcare"]
    jurisdictions = ["USA", "India", "UK"]
    
    for business_type in business_types:
        print(f"\n📊 {business_type.upper()} Compliance Requirements:")
        
        for jurisdiction in jurisdictions:
            if jurisdiction in legal_agent.sub_agents:
                sub_agent = legal_agent.sub_agents[jurisdiction]
                requirements = sub_agent.get_compliance_requirements(business_type)
                
                print(f"   {jurisdiction}:")
                for req in requirements[:3]:  # Show first 3 requirements
                    print(f"     - {req['requirement']}: {req['cost']} ({req['urgency']} priority)")

def check_generated_files():
    """Check if legal analysis files were generated"""
    print("\n📁 Checking Generated Files...")
    
    legal_data_dir = "legal_data"
    if os.path.exists(legal_data_dir):
        for root, dirs, files in os.walk(legal_data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f"   ✅ {file_path} ({file_size} bytes)")
    else:
        print("   ⚠️  No legal_data directory found")

async def main():
    """Run all legal agent tests"""
    print("🧪 Starting Legal Agent Tests...")
    print("=" * 50)
    
    try:
        # Test individual sub-agents
        await test_usa_legal_agent()
        await test_india_legal_agent()
        
        # Test main legal agent
        await test_legal_agent_main()
        
        # Test document review
        await test_document_review()
        
        # Test compliance requirements
        await test_compliance_requirements()
        
        # Check generated files
        check_generated_files()
        
        print("\n" + "=" * 50)
        print("✅ All Legal Agent tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())