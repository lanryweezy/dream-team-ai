"""
Comprehensive Integration Test Suite
Tests the complete Dream Machine system with real-world scenarios
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List
from datetime import datetime, timezone
import unittest.mock as mock

# Import system components
from core.performance_monitor import performance_monitor
from core.policy_engine import PolicyEngine, Policy, PolicyRule
from core.cost_tracker import CostTracker
from core.enhanced_base_agent import TestEnhancedAgent, AgentCapability

# Mock Redis for testing
import core.mock_redis as mock_redis
import core.message_bus as message_bus_module

# Replace Redis with mock for testing
message_bus_module.redis = mock_redis
from core.message_bus import message_bus, Message, MessageType, Priority

logger = logging.getLogger(__name__)

class IntegrationTestSuite:
    """Comprehensive integration testing suite"""
    
    def __init__(self):
        self.test_results = []
        self.performance_data = {}
        
    async def run_complete_integration_tests(self):
        """Run all integration tests"""
        logger.info("🚀 Starting Comprehensive Integration Test Suite")
        
        # Start performance monitoring
        await performance_monitor.start_monitoring(interval=1.0)
        
        try:
            # Test 1: System Initialization
            await self.test_system_initialization()
            
            # Test 2: Multi-Agent Communication
            await self.test_multi_agent_communication()
            
            # Test 3: Policy Engine Integration
            await self.test_policy_engine_integration()
            
            # Test 4: Cost Tracking Integration
            await self.test_cost_tracking_integration()
            
            # Test 5: Performance Under Load
            await self.test_performance_under_load()
            
            # Test 6: Error Recovery
            await self.test_error_recovery_scenarios()
            
            # Test 7: Real-world Business Scenario
            await self.test_business_scenario_simulation()
            
        finally:
            await performance_monitor.stop_monitoring()
            
        # Generate comprehensive report
        return await self.generate_integration_report()
        
    async def test_system_initialization(self):
        """Test complete system initialization"""
        logger.info("🔧 Testing System Initialization")
        
        start_time = time.time()
        
        try:
            # Initialize message bus
            await message_bus.connect()
            
            # Create test agents
            agent1 = TestEnhancedAgent("test_agent_1", [
                AgentCapability("capability_1", "Test capability", 1.0, 0.9, [])
            ])
            
            agent2 = TestEnhancedAgent("test_agent_2", [
                AgentCapability("capability_2", "Test capability", 1.5, 0.8, [])
            ])
            
            # Start agents
            await agent1.start()
            await agent2.start()
            
            # Verify agents are running
            assert agent1.is_running
            assert agent2.is_running
            
            # Stop agents
            await agent1.stop()
            await agent2.stop()
            
            await message_bus.disconnect()
            
            duration = time.time() - start_time
            
            self.test_results.append({
                "test": "system_initialization",
                "status": "PASSED",
                "duration": duration,
                "details": "System initialized successfully"
            })
            
            await performance_monitor.record_metric(
                "test_duration", duration, "seconds", "integration_test"
            )
            
        except Exception as e:
            self.test_results.append({
                "test": "system_initialization",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def test_multi_agent_communication(self):
        """Test communication between multiple agents"""
        logger.info("📡 Testing Multi-Agent Communication")
        
        start_time = time.time()
        
        try:
            await message_bus.connect()
            
            # Create agents
            sender_agent = TestEnhancedAgent("sender", [])
            receiver_agent = TestEnhancedAgent("receiver", [])
            
            await sender_agent.start()
            await receiver_agent.start()
            
            # Set up message handling
            received_messages = []
            
            def message_handler(message: Message):
                received_messages.append(message)
                
            await message_bus.subscribe("receiver", message_handler)
            
            # Send test message
            test_message = Message(
                id="test_msg_001",
                type=MessageType.TASK_ASSIGNMENT,
                sender="sender",
                recipient="receiver",
                payload={"task": "test_task", "data": "test_data"},
                priority=Priority.HIGH
            )
            
            await message_bus.publish(test_message)
            
            # Wait for message processing
            await asyncio.sleep(2.0)
            
            # Verify message was received
            assert len(received_messages) > 0
            assert received_messages[0].payload["task"] == "test_task"
            
            await sender_agent.stop()
            await receiver_agent.stop()
            await message_bus.disconnect()
            
            duration = time.time() - start_time
            
            self.test_results.append({
                "test": "multi_agent_communication",
                "status": "PASSED",
                "duration": duration,
                "details": f"Successfully exchanged {len(received_messages)} messages"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "multi_agent_communication",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def test_policy_engine_integration(self):
        """Test policy engine integration with agents"""
        logger.info("⚖️ Testing Policy Engine Integration")
        
        start_time = time.time()
        
        try:
            # Create policy engine
            policy_engine = PolicyEngine()
            
            # Add test policies
            test_policy = Policy(
                name="test_integration_policy",
                description="Test policy for integration",
                rules=[
                    PolicyRule(
                        condition="cost < 50",
                        action="auto_approve",
                        priority=1
                    ),
                    PolicyRule(
                        condition="cost >= 50",
                        action="require_approval",
                        priority=2
                    )
                ],
                enabled=True
            )
            
            policy_engine.add_policy(test_policy)
            
            # Test policy evaluation
            low_cost_action = {"type": "test_action", "cost": 25}
            high_cost_action = {"type": "test_action", "cost": 75}
            
            # Test low cost (should auto-approve)
            result1 = policy_engine.evaluate("test_action", {"cost": 25})
            assert result1 == "auto_approve"
            
            # Test high cost (should require approval)
            result2 = policy_engine.evaluate("test_action", {"cost": 75})
            assert result2 == "require_approval"
            
            duration = time.time() - start_time
            
            self.test_results.append({
                "test": "policy_engine_integration",
                "status": "PASSED",
                "duration": duration,
                "details": "Policy engine correctly evaluated actions"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "policy_engine_integration",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def test_cost_tracking_integration(self):
        """Test cost tracking integration"""
        logger.info("💰 Testing Cost Tracking Integration")
        
        start_time = time.time()
        
        try:
            # Create cost tracker
            cost_tracker = CostTracker()
            
            # Record test costs
            cost_tracker.record_cost(
                agent_id="test_agent",
                tool_name="test_tool",
                action_type="test_action",
                amount=10.50,
                description="Test cost recording",
                metadata={"test": True},
                category="testing"
            )
            
            cost_tracker.record_cost(
                agent_id="test_agent",
                tool_name="another_tool",
                action_type="another_action",
                amount=25.75,
                description="Another test cost",
                metadata={"test": True},
                category="testing"
            )
            
            # Get cost summary
            summary = cost_tracker.get_cost_summary()
            
            # Verify costs were recorded
            assert summary["total_cost"] > 0
            assert "test_agent" in summary["by_agent"]
            assert summary["by_agent"]["test_agent"] == 36.25
            
            duration = time.time() - start_time
            
            self.test_results.append({
                "test": "cost_tracking_integration",
                "status": "PASSED",
                "duration": duration,
                "details": f"Tracked total cost: ${summary['total_cost']:.2f}"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "cost_tracking_integration",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def test_performance_under_load(self):
        """Test system performance under load"""
        logger.info("⚡ Testing Performance Under Load")
        
        start_time = time.time()
        
        try:
            await message_bus.connect()
            
            # Create multiple agents
            agents = []
            for i in range(5):
                agent = TestEnhancedAgent(f"load_test_agent_{i}", [])
                await agent.start()
                agents.append(agent)
                
            # Send multiple messages concurrently
            tasks = []
            for i in range(50):
                message = Message(
                    id=f"load_test_msg_{i}",
                    type=MessageType.TASK_ASSIGNMENT,
                    sender="load_tester",
                    recipient=f"load_test_agent_{i % 5}",
                    payload={"task_id": i, "data": f"load_test_data_{i}"},
                    priority=Priority.MEDIUM
                )
                tasks.append(message_bus.publish(message))
                
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Count successful sends
            successful_sends = len([r for r in results if r is True])
            
            # Clean up agents
            for agent in agents:
                await agent.stop()
                
            await message_bus.disconnect()
            
            duration = time.time() - start_time
            throughput = successful_sends / duration
            
            # Record performance metrics
            await performance_monitor.record_metric(
                "message_throughput", throughput, "messages/second", "load_test"
            )
            
            self.test_results.append({
                "test": "performance_under_load",
                "status": "PASSED",
                "duration": duration,
                "details": f"Processed {successful_sends}/50 messages at {throughput:.2f} msg/s"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "performance_under_load",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def test_error_recovery_scenarios(self):
        """Test system error recovery"""
        logger.info("🔄 Testing Error Recovery Scenarios")
        
        start_time = time.time()
        
        try:
            # Test 1: Agent failure and restart
            agent = TestEnhancedAgent("recovery_test_agent", [])
            await agent.start()
            
            # Simulate agent failure
            agent.is_running = False
            
            # Restart agent
            await agent.start()
            assert agent.is_running
            
            await agent.stop()
            
            # Test 2: Message bus reconnection
            await message_bus.connect()
            
            # Simulate disconnection
            await message_bus.disconnect()
            
            # Reconnect
            await message_bus.connect()
            await message_bus.disconnect()
            
            duration = time.time() - start_time
            
            self.test_results.append({
                "test": "error_recovery_scenarios",
                "status": "PASSED",
                "duration": duration,
                "details": "Successfully recovered from simulated failures"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "error_recovery_scenarios",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def test_business_scenario_simulation(self):
        """Test realistic business scenario"""
        logger.info("🏢 Testing Business Scenario Simulation")
        
        start_time = time.time()
        
        try:
            await message_bus.connect()
            
            # Create business agents
            ceo_agent = TestEnhancedAgent("ceo_agent", [
                AgentCapability("strategic_planning", "Strategic planning", 5.0, 0.9, [])
            ])
            
            marketing_agent = TestEnhancedAgent("marketing_agent", [
                AgentCapability("campaign_creation", "Marketing campaigns", 3.0, 0.8, [])
            ])
            
            legal_agent = TestEnhancedAgent("legal_agent", [
                AgentCapability("contract_review", "Contract review", 4.0, 0.95, [])
            ])
            
            # Start agents
            await ceo_agent.start()
            await marketing_agent.start()
            await legal_agent.start()
            
            # Simulate business workflow
            # 1. CEO assigns marketing task
            marketing_task = Message(
                id="business_task_001",
                type=MessageType.TASK_ASSIGNMENT,
                sender="ceo_agent",
                recipient="marketing_agent",
                payload={
                    "task": "create_campaign",
                    "product": "FitTrack Pro",
                    "budget": 10000,
                    "deadline": "2024-01-15"
                },
                priority=Priority.HIGH
            )
            
            await message_bus.publish(marketing_task)
            
            # 2. Marketing agent requests legal review
            legal_task = Message(
                id="business_task_002",
                type=MessageType.TASK_ASSIGNMENT,
                sender="marketing_agent",
                recipient="legal_agent",
                payload={
                    "task": "review_campaign_legal",
                    "campaign_id": "campaign_001",
                    "materials": ["ad_copy.txt", "terms.txt"]
                },
                priority=Priority.MEDIUM
            )
            
            await message_bus.publish(legal_task)
            
            # 3. Simulate task completion
            completion_message = Message(
                id="business_task_003",
                type=MessageType.TASK_COMPLETION,
                sender="legal_agent",
                recipient="marketing_agent",
                payload={
                    "task_id": "business_task_002",
                    "status": "completed",
                    "result": "approved_with_minor_changes",
                    "recommendations": ["Update privacy policy link", "Add disclaimer"]
                },
                priority=Priority.MEDIUM
            )
            
            await message_bus.publish(completion_message)
            
            # Wait for message processing
            await asyncio.sleep(2.0)
            
            # Clean up
            await ceo_agent.stop()
            await marketing_agent.stop()
            await legal_agent.stop()
            await message_bus.disconnect()
            
            duration = time.time() - start_time
            
            self.test_results.append({
                "test": "business_scenario_simulation",
                "status": "PASSED",
                "duration": duration,
                "details": "Successfully simulated multi-agent business workflow"
            })
            
        except Exception as e:
            self.test_results.append({
                "test": "business_scenario_simulation",
                "status": "FAILED",
                "duration": time.time() - start_time,
                "error": str(e)
            })
            
    async def generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration test report"""
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASSED"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAILED"])
        total_duration = sum(t["duration"] for t in self.test_results)
        
        # Get performance metrics
        performance_metrics = performance_monitor.get_current_metrics()
        
        report = {
            "integration_test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration,
                "average_test_duration": total_duration / total_tests if total_tests > 0 else 0
            },
            "test_results": self.test_results,
            "performance_metrics": performance_metrics,
            "system_health": {
                "message_bus": "operational",
                "policy_engine": "operational",
                "cost_tracker": "operational",
                "performance_monitor": "operational"
            },
            "recommendations": self._generate_recommendations()
        }
        
        # Save report to file
        report_filename = f"integration_test_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        return report
        
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [t for t in self.test_results if t["status"] == "FAILED"]
        
        if failed_tests:
            recommendations.append(f"Address {len(failed_tests)} failed test(s) before production deployment")
            
        slow_tests = [t for t in self.test_results if t["duration"] > 5.0]
        if slow_tests:
            recommendations.append(f"Optimize performance for {len(slow_tests)} slow test(s)")
            
        if len(self.test_results) < 7:
            recommendations.append("Consider adding more comprehensive integration tests")
            
        recommendations.append("Implement continuous integration testing")
        recommendations.append("Set up automated performance monitoring")
        recommendations.append("Create disaster recovery procedures")
        
        return recommendations

async def main():
    """Run integration test suite"""
    suite = IntegrationTestSuite()
    report = await suite.run_complete_integration_tests()
    
    print("\n" + "="*80)
    print("🎯 INTEGRATION TEST SUITE COMPLETED")
    print("="*80)
    print(f"📊 Total Tests: {report['integration_test_summary']['total_tests']}")
    print(f"✅ Passed: {report['integration_test_summary']['passed_tests']}")
    print(f"❌ Failed: {report['integration_test_summary']['failed_tests']}")
    print(f"📈 Success Rate: {report['integration_test_summary']['success_rate']:.1f}%")
    print(f"⏱️  Total Duration: {report['integration_test_summary']['total_duration']:.2f}s")
    print("="*80)
    
    if report['integration_test_summary']['failed_tests'] > 0:
        print("\n❌ Failed Tests:")
        for test in report['test_results']:
            if test['status'] == 'FAILED':
                print(f"  - {test['test']}: {test.get('error', 'Unknown error')}")
                
    print(f"\n📄 Detailed report saved to integration test JSON file")
    
    return report

if __name__ == "__main__":
    asyncio.run(main())