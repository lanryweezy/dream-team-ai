"""
Test Ollama Integration with Dream Machine
"""

import asyncio
import logging
from core.llm_integration import llm_manager, initialize_llm_providers, LLMProvider, LLMMessage, LLMRole
from core.ollama_provider import ollama_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_ollama_basic():
    """Test basic Ollama functionality"""
    print("🔍 Testing Ollama Basic Functionality")
    print("=" * 50)
    
    try:
        # Initialize LLM providers
        await initialize_llm_providers()
        
        # Check if Ollama is available
        if LLMProvider.LOCAL not in llm_manager.providers:
            print("❌ Ollama not available. Make sure Ollama is running with: ollama serve")
            print("💡 Install a model with: ollama pull llama2")
            return False
            
        print("✅ Ollama provider initialized successfully")
        
        # Test simple question
        print("\n📝 Testing simple question...")
        response = await llm_manager.generate_response(
            messages=[
                LLMMessage(role=LLMRole.USER, content="What is 2+2? Please answer briefly.")
            ],
            provider=LLMProvider.LOCAL
        )
        
        print(f"Response: {response.content}")
        print(f"Tokens used: {response.tokens_used}")
        print(f"Response time: {response.response_time:.2f}s")
        print(f"Cost: ${response.cost_estimate:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

async def test_ollama_structured():
    """Test Ollama structured response"""
    print("\n🏗️ Testing Ollama Structured Response")
    print("=" * 50)
    
    try:
        # Test structured response for company blueprint
        schema = {
            "type": "object",
            "properties": {
                "company_name": {"type": "string"},
                "industry": {"type": "string"},
                "vision": {"type": "string"},
                "key_features": {"type": "array", "items": {"type": "string"}},
                "target_market": {"type": "string"}
            }
        }
        
        messages = [
            LLMMessage(
                role=LLMRole.SYSTEM,
                content="You are a business strategist helping create company blueprints."
            ),
            LLMMessage(
                role=LLMRole.USER,
                content="Create a company blueprint for a productivity app that helps remote teams collaborate better."
            )
        ]
        
        print("📋 Requesting structured response...")
        structured_response = await llm_manager.generate_structured_response(
            messages=messages,
            schema=schema,
            provider=LLMProvider.LOCAL
        )
        
        print("✅ Structured Response:")
        import json
        print(json.dumps(structured_response, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing structured response: {e}")
        return False

async def test_ceo_blueprint_creation():
    """Test CEO agent blueprint creation with Ollama"""
    print("\n👔 Testing CEO Blueprint Creation with Ollama")
    print("=" * 50)
    
    try:
        from agents.ceo_agent import CEOAgent
        from core.enhanced_message_bus import enhanced_message_bus
        from core.enhanced_policy_engine import enhanced_policy_engine
        
        # Start message bus
        await enhanced_message_bus.start()
        
        # Create CEO agent
        ceo = CEOAgent("ceo_001", enhanced_message_bus, enhanced_policy_engine)
        
        # Test blueprint creation
        dream = """
        I want to create a revolutionary fitness tracking app that uses AI to provide 
        personalized workout recommendations. The app should help people achieve their 
        fitness goals through smart coaching and community features. I want to target 
        health-conscious millennials and gen-z users who are tech-savvy.
        """
        
        print("🎯 Creating blueprint from dream...")
        print(f"Dream: {dream[:100]}...")
        
        blueprint = await ceo._create_blueprint_from_dream(dream)
        
        print("✅ Blueprint Created:")
        print(f"Company Name: {blueprint.company_name}")
        print(f"Vision: {blueprint.vision}")
        print(f"Mission: {blueprint.mission}")
        print(f"Industry: {blueprint.industry}")
        print(f"Target Market: {blueprint.business_model.target_market}")
        
        # Stop message bus
        await enhanced_message_bus.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing CEO blueprint creation: {e}")
        return False

async def test_ollama_models():
    """Test available Ollama models"""
    print("\n🔧 Testing Available Ollama Models")
    print("=" * 50)
    
    try:
        # Check available models
        models = await ollama_manager.ollama_manager.list_models() if hasattr(ollama_manager, 'ollama_manager') else []
        
        if not models:
            provider = ollama_manager.get_provider()
            if provider:
                models = await provider.list_models()
        
        if models:
            print("✅ Available models:")
            for model in models:
                print(f"  - {model}")
        else:
            print("❌ No models found")
            print("💡 Try: ollama pull llama2")
            
        return len(models) > 0
        
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

async def main():
    """Run all Ollama tests"""
    print("🚀 Dream Machine - Ollama Integration Tests")
    print("=" * 60)
    
    results = []
    
    # Test basic functionality
    results.append(await test_ollama_basic())
    
    # Test available models
    results.append(await test_ollama_models())
    
    # Test structured response
    if results[-1]:  # Only if basic test passed
        results.append(await test_ollama_structured())
        
        # Test CEO blueprint creation
        results.append(await test_ceo_blueprint_creation())
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ollama integration is working perfectly.")
    elif passed > 0:
        print("⚠️ Some tests passed. Check the errors above.")
    else:
        print("❌ All tests failed. Make sure Ollama is running:")
        print("   1. Install Ollama: https://ollama.ai")
        print("   2. Start Ollama: ollama serve")
        print("   3. Pull a model: ollama pull llama2")

if __name__ == "__main__":
    asyncio.run(main())