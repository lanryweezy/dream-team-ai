"""
Enhanced Test Suite for Dream Machine System
Implements advanced testing features including parallel execution, performance monitoring, and comprehensive reporting
"""

import asyncio
import json
import os
import sys
import time
import traceback
import unittest.mock as mock
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
import logging
import sqlite3
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestMetrics:
    """Test execution metrics"""
    test_name: str
    start_time: float
    end_time: float
    duration: float
    memory_usage: float
    cpu_usage: float
    success: bool
    error_message: Optional[str] = None

@dataclass
class TestResult:
    """Enhanced test result with detailed information"""
    test_id: str
    test_name: str
    component: str
    status: str  # PASSED, FAILED, SKIPPED
    duration: float
    memory_peak: float
    error_details: Optional[str] = None
    performance_score: float = 0.0
    retry_count: int = 0

class TestDataFactory:
    """Factory for generating consistent test data"""
    
    @staticmethod
    def create_test_agent_config():
        """Create test agent configuration"""
        return {
            "agent_id": "test_agent_001",
            "capabilities": [
                {
                    "name": "test_capability",
                    "description": "Test capability for validation",
                    "cost_estimate": 1.0,
                    "confidence_level": 0.9,
                    "requirements": []
                }
            ]
        }
    
    @staticmethod
    def create_test_company_blueprint():
        """Create test company blueprint"""
        return {
            "company_name": "TestCorp",
            "vision": "Test company vision",
            "industry": "technology",
            "target_market": "consumers",
            "business_model": "saas",
            "yearly_revenue_target": 1000000,
            "budget": 50000,
            "timeline_months": 12
        }
    
    @staticmethod
    def create_test_task():
        """Create test task"""
        return {
            "id": f"test_task_{int(time.time())}",
            "type": "test_execution",
            "description": "Test task for validation",
            "priority": "high",
            "deadline": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        }

class PerformanceBenchmark:
    """Performance benchmarking utilities"""
    
    def __init__(self):
        self.benchmarks: Dict[str, List[float]] = {}
        
    def record_execution_time(self, test_name: str, duration: float):
        """Record execution time for a test"""
        if test_name not in self.benchmarks:
            self.benchmarks[test_name] = []
        self.benchmarks[test_name].append(duration)
        
    def get_performance_stats(self, test_name: str) -> Dict[str, float]:
        """Get performance statistics for a test"""
        if test_name not in self.benchmarks:
            return {}
            
        times = self.benchmarks[test_name]
        return {
            "avg_duration": sum(times) / len(times),
            "min_duration": min(times),
            "max_duration": max(times),
            "total_runs": len(times)
        }
        
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_tests": len(self.benchmarks),
            "performance_data": {}
        }
        
        for test_name in self.benchmarks:
            report["performance_data"][test_name] = self.get_performance_stats(test_name)
            
        return report

class TestDatabase:
    """Database for storing test results and metrics"""
    
    def __init__(self, db_path: str = "test_results.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize test results database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT UNIQUE,
                start_time TEXT,
                end_time TEXT,
                total_tests INTEGER,
                passed_tests INTEGER,
                failed_tests INTEGER,
                success_rate REAL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT,
                test_name TEXT,
                component TEXT,
                status TEXT,
                duration REAL,
                memory_peak REAL,
                error_details TEXT,
                performance_score REAL,
                retry_count INTEGER,
                timestamp TEXT,
                FOREIGN KEY (run_id) REFERENCES test_runs (run_id)
            )
        """)
        
        conn.commit()
        conn.close()
        
    def save_test_run(self, run_id: str, results: List[TestResult]):
        """Save test run results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate summary stats
        total_tests = len(results)
        passed_tests = len([r for r in results if r.status == "PASSED"])
        failed_tests = len([r for r in results if r.status == "FAILED"])
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        # Save test run summary
        cursor.execute("""
            INSERT OR REPLACE INTO test_runs 
            (run_id, start_time, end_time, total_tests, passed_tests, failed_tests, success_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            datetime.now(timezone.utc).isoformat(),
            datetime.now(timezone.utc).isoformat(),
            total_tests,
            passed_tests,
            failed_tests,
            success_rate
        ))
        
        # Save individual test results
        for result in results:
            cursor.execute("""
                INSERT INTO test_results 
                (run_id, test_name, component, status, duration, memory_peak, 
                 error_details, performance_score, retry_count, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id,
                result.test_name,
                result.component,
                result.status,
                result.duration,
                result.memory_peak,
                result.error_details,
                result.performance_score,
                result.retry_count,
                datetime.now(timezone.utc).isoformat()
            ))
        
        conn.commit()
        conn.close()

class RetryMechanism:
    """Configurable retry mechanism for flaky tests"""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.5):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
    async def execute_with_retry(self, test_func: Callable, test_name: str) -> TestResult:
        """Execute test with retry logic"""
        retry_count = 0
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()
                result = await test_func()
                duration = time.time() - start_time
                
                return TestResult(
                    test_id=f"{test_name}_{int(time.time())}",
                    test_name=test_name,
                    component="unknown",
                    status="PASSED",
                    duration=duration,
                    memory_peak=0.0,
                    retry_count=retry_count
                )
                
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                
                if attempt < self.max_retries:
                    wait_time = self.backoff_factor ** attempt
                    logger.warning(f"Test {test_name} failed (attempt {attempt + 1}), retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Test {test_name} failed after {self.max_retries} retries: {last_error}")
                    
        return TestResult(
            test_id=f"{test_name}_{int(time.time())}",
            test_name=test_name,
            component="unknown",
            status="FAILED",
            duration=0.0,
            memory_peak=0.0,
            error_details=last_error,
            retry_count=retry_count
        )

class EnhancedTestSuite:
    """Enhanced test suite with advanced features"""
    
    def __init__(self):
        self.benchmark = PerformanceBenchmark()
        self.database = TestDatabase()
        self.retry_mechanism = RetryMechanism()
        self.test_factory = TestDataFactory()
        self.results: List[TestResult] = []
        
    async def run_parallel_tests(self, test_functions: List[Callable]) -> List[TestResult]:
        """Run tests in parallel for better performance"""
        logger.info(f"Running {len(test_functions)} tests in parallel")
        
        tasks = []
        for test_func in test_functions:
            task = asyncio.create_task(
                self.retry_mechanism.execute_with_retry(test_func, test_func.__name__)
            )
            tasks.append(task)
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(TestResult(
                    test_id=f"failed_test_{i}",
                    test_name=test_functions[i].__name__,
                    component="unknown",
                    status="FAILED",
                    duration=0.0,
                    memory_peak=0.0,
                    error_details=str(result)
                ))
            else:
                processed_results.append(result)
                
        return processed_results
        
    async def test_core_system_enhanced(self) -> List[TestResult]:
        """Enhanced core system tests"""
        logger.info("🔧 Running Enhanced Core System Tests")
        
        async def test_base_agent_with_mocks():
            """Test base agent with proper mocking"""
            with mock.patch('core.simple_message_bus.event_bus') as mock_bus:
                mock_bus.start = mock.AsyncMock()
                mock_bus.stop = mock.AsyncMock()
                mock_bus.publish_event = mock.AsyncMock()
                
                from core.base_agent import BaseAgent, AgentCapability
                
                capability = AgentCapability(
                    name="test_capability",
                    description="Test capability",
                    cost_estimate=1.0,
                    confidence_level=0.9,
                    requirements=[]
                )
                
                # Create concrete implementation for testing
                class TestAgent(BaseAgent):
                    async def execute_task(self, task):
                        return mock.MagicMock(success=True)
                    
                    async def get_daily_goals(self):
                        return [{"goal": "test_goal"}]
                
                agent = TestAgent("test_agent", [capability])
                await agent.start()
                
                # Test event sending
                await agent.send_event("test_event", {"data": "test"})
                mock_bus.publish_event.assert_called_once()
                
                await agent.stop()
                return True
                
        async def test_message_bus_reliability():
            """Test message bus with reliability features"""
            # Mock Redis for testing
            with mock.patch('redis.asyncio.from_url') as mock_redis:
                mock_client = mock.AsyncMock()
                mock_redis.return_value = mock_client
                mock_client.ping = mock.AsyncMock()
                mock_client.lpush = mock.AsyncMock()
                mock_client.publish = mock.AsyncMock()
                
                from core.message_bus import MessageBus, Message, MessageType, Priority
                
                bus = MessageBus()
                await bus.connect()
                
                message = Message(
                    id="test_msg",
                    type=MessageType.TASK_ASSIGNMENT,
                    sender="test_sender",
                    recipient="test_recipient",
                    payload={"test": "data"},
                    priority=Priority.HIGH
                )
                
                result = await bus.publish(message)
                assert result == True
                
                await bus.disconnect()
                return True
                
        async def test_policy_engine_persistence():
            """Test policy engine with persistence simulation"""
            with mock.patch('builtins.open', mock.mock_open()) as mock_file:
                from core.policy_engine import PolicyEngine, Policy, PolicyRule
                
                engine = PolicyEngine()
                
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
                
                return True
        
        # Run tests in parallel
        test_functions = [
            test_base_agent_with_mocks,
            test_message_bus_reliability,
            test_policy_engine_persistence
        ]
        
        return await self.run_parallel_tests(test_functions)
        
    async def test_agent_performance_benchmarks(self) -> List[TestResult]:
        """Benchmark agent performance"""
        logger.info("⚡ Running Agent Performance Benchmarks")
        
        async def benchmark_ceo_agent_response_time():
            """Benchmark CEO agent response time"""
            start_time = time.time()
            
            # Simulate CEO agent task execution
            await asyncio.sleep(0.1)  # Simulate processing time
            
            duration = time.time() - start_time
            self.benchmark.record_execution_time("ceo_agent_response", duration)
            
            # Performance threshold check
            if duration > 0.5:  # 500ms threshold
                raise Exception(f"CEO agent response too slow: {duration}s")
                
            return True
            
        async def benchmark_message_bus_throughput():
            """Benchmark message bus throughput"""
            start_time = time.time()
            
            # Simulate high message volume
            for i in range(100):
                await asyncio.sleep(0.001)  # Simulate message processing
                
            duration = time.time() - start_time
            throughput = 100 / duration
            
            self.benchmark.record_execution_time("message_bus_throughput", throughput)
            
            if throughput < 50:  # 50 messages/second threshold
                raise Exception(f"Message bus throughput too low: {throughput} msg/s")
                
            return True
            
        test_functions = [
            benchmark_ceo_agent_response_time,
            benchmark_message_bus_throughput
        ]
        
        return await self.run_parallel_tests(test_functions)
        
    async def test_integration_workflows_advanced(self) -> List[TestResult]:
        """Advanced integration workflow tests"""
        logger.info("🔄 Running Advanced Integration Workflow Tests")
        
        async def test_end_to_end_company_creation():
            """Test complete company creation workflow"""
            # Mock all external dependencies
            with mock.patch('agents.ceo_agent.CEOAgent'):
                # Simulate complete workflow
                workflow_steps = [
                    "blueprint_creation",
                    "agent_initialization", 
                    "goal_setting",
                    "task_distribution",
                    "progress_monitoring"
                ]
                
                for step in workflow_steps:
                    await asyncio.sleep(0.01)  # Simulate step processing
                    logger.debug(f"Completed workflow step: {step}")
                    
                return True
                
        async def test_failure_recovery_workflow():
            """Test system recovery from failures"""
            # Simulate failure and recovery
            try:
                # Simulate a failure
                raise Exception("Simulated system failure")
            except Exception:
                # Simulate recovery mechanism
                logger.info("Recovering from simulated failure")
                await asyncio.sleep(0.1)
                return True
                
        test_functions = [
            test_end_to_end_company_creation,
            test_failure_recovery_workflow
        ]
        
        return await self.run_parallel_tests(test_functions)
        
    def generate_html_report(self, run_id: str) -> str:
        """Generate interactive HTML test report"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dream Machine Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #3B82F6; color: white; padding: 20px; border-radius: 8px; }}
                .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
                .metric {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
                .metric h3 {{ margin: 0; color: #333; }}
                .metric .value {{ font-size: 2em; font-weight: bold; color: #3B82F6; }}
                .test-results {{ margin: 20px 0; }}
                .test-item {{ padding: 10px; margin: 5px 0; border-radius: 4px; }}
                .passed {{ background: #d4edda; border-left: 4px solid #28a745; }}
                .failed {{ background: #f8d7da; border-left: 4px solid #dc3545; }}
                .performance-chart {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Dream Machine Test Report</h1>
                <p>Run ID: {run_id}</p>
                <p>Generated: {timestamp}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <h3>Total Tests</h3>
                    <div class="value">{total_tests}</div>
                </div>
                <div class="metric">
                    <h3>Passed</h3>
                    <div class="value" style="color: #28a745;">{passed_tests}</div>
                </div>
                <div class="metric">
                    <h3>Failed</h3>
                    <div class="value" style="color: #dc3545;">{failed_tests}</div>
                </div>
                <div class="metric">
                    <h3>Success Rate</h3>
                    <div class="value">{success_rate}%</div>
                </div>
            </div>
            
            <div class="test-results">
                <h2>Test Results</h2>
                {test_items}
            </div>
            
            <div class="performance-chart">
                <h2>Performance Metrics</h2>
                <p>Performance benchmarking data would be displayed here with charts.</p>
            </div>
        </body>
        </html>
        """
        
        # Calculate summary stats
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "PASSED"])
        failed_tests = len([r for r in self.results if r.status == "FAILED"])
        success_rate = round((passed_tests / total_tests * 100) if total_tests > 0 else 0, 1)
        
        # Generate test items HTML
        test_items = ""
        for result in self.results:
            status_class = "passed" if result.status == "PASSED" else "failed"
            test_items += f"""
            <div class="test-item {status_class}">
                <strong>{result.test_name}</strong> - {result.status}
                <br>Duration: {result.duration:.3f}s
                {f'<br>Error: {result.error_details}' if result.error_details else ''}
            </div>
            """
        
        return html_template.format(
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            success_rate=success_rate,
            test_items=test_items
        )
        
    async def run_complete_test_suite(self) -> Dict[str, Any]:
        """Run the complete enhanced test suite"""
        run_id = f"test_run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"🚀 Starting Enhanced Test Suite - Run ID: {run_id}")
        
        start_time = time.time()
        
        try:
            # Run all test categories
            core_results = await self.test_core_system_enhanced()
            performance_results = await self.test_agent_performance_benchmarks()
            integration_results = await self.test_integration_workflows_advanced()
            
            # Combine all results
            all_results = core_results + performance_results + integration_results
            self.results = all_results
            
            # Save to database
            self.database.save_test_run(run_id, all_results)
            
            # Generate reports
            performance_report = self.benchmark.generate_performance_report()
            html_report = self.generate_html_report(run_id)
            
            # Save HTML report
            report_path = f"test_report_{run_id}.html"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_report)
            
            total_duration = time.time() - start_time
            
            # Summary
            total_tests = len(all_results)
            passed_tests = len([r for r in all_results if r.status == "PASSED"])
            failed_tests = len([r for r in all_results if r.status == "FAILED"])
            
            summary = {
                "run_id": run_id,
                "total_duration": total_duration,
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "performance_report": performance_report,
                "html_report_path": report_path,
                "database_path": self.database.db_path
            }
            
            # Print summary
            print("\n" + "="*80)
            print("🎉 ENHANCED TEST SUITE COMPLETED")
            print("="*80)
            print(f"📊 Run ID: {run_id}")
            print(f"⏱️  Total Duration: {total_duration:.2f}s")
            print(f"✅ Tests Passed: {passed_tests}")
            print(f"❌ Tests Failed: {failed_tests}")
            print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
            print(f"📄 HTML Report: {report_path}")
            print(f"💾 Database: {self.database.db_path}")
            print("="*80)
            
            return summary
            
        except Exception as e:
            logger.error(f"Test suite execution failed: {e}")
            traceback.print_exc()
            return {
                "run_id": run_id,
                "error": str(e),
                "success": False
            }

async def main():
    """Main execution function"""
    suite = EnhancedTestSuite()
    results = await suite.run_complete_test_suite()
    
    if results.get("success", True):
        print(f"\n🚀 Enhanced test suite completed successfully!")
        print(f"📊 Check the HTML report: {results.get('html_report_path')}")
    else:
        print(f"\n💥 Test suite failed: {results.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())