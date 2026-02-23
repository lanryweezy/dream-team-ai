"""
Performance Monitoring System for Dream Machine
Tracks system performance, resource usage, and provides real-time insights
"""

import asyncio
import logging
import time
import psutil
import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    component: str
    metadata: Dict[str, Any] = None

@dataclass
class SystemSnapshot:
    """System performance snapshot"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_usage_percent: float
    network_io_bytes: int
    active_processes: int
    agent_count: int
    message_queue_size: int

@dataclass
class AgentPerformance:
    """Agent-specific performance metrics"""
    agent_id: str
    task_completion_rate: float
    average_response_time: float
    error_rate: float
    resource_utilization: float
    last_activity: datetime

class PerformanceMonitor:
    """Real-time performance monitoring system"""
    
    def __init__(self, db_path: str = "performance_metrics.db"):
        self.db_path = db_path
        self.metrics_buffer: deque = deque(maxlen=1000)
        self.system_snapshots: deque = deque(maxlen=100)
        self.agent_metrics: Dict[str, AgentPerformance] = {}
        self.alert_thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_usage_percent": 90.0,
            "error_rate": 0.1,
            "response_time_ms": 5000
        }
        self.alert_callbacks: List[Callable] = []
        self.monitoring_active = False
        self.init_database()
        
    def init_database(self):
        """Initialize performance metrics database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                metric_name TEXT,
                value REAL,
                unit TEXT,
                component TEXT,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_percent REAL,
                memory_percent REAL,
                memory_used_mb REAL,
                disk_usage_percent REAL,
                network_io_bytes INTEGER,
                active_processes INTEGER,
                agent_count INTEGER,
                message_queue_size INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                timestamp TEXT,
                task_completion_rate REAL,
                average_response_time REAL,
                error_rate REAL,
                resource_utilization REAL,
                last_activity TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                alert_type TEXT,
                severity TEXT,
                message TEXT,
                component TEXT,
                resolved BOOLEAN DEFAULT FALSE,
                resolved_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    async def start_monitoring(self, interval: float = 5.0):
        """Start continuous performance monitoring"""
        self.monitoring_active = True
        logger.info("Performance monitoring started")
        
        # Start monitoring tasks
        asyncio.create_task(self._system_monitor_loop(interval))
        asyncio.create_task(self._metrics_processor_loop())
        asyncio.create_task(self._alert_checker_loop())
        
    async def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        logger.info("Performance monitoring stopped")
        
    async def _system_monitor_loop(self, interval: float):
        """Main system monitoring loop"""
        while self.monitoring_active:
            try:
                snapshot = await self._capture_system_snapshot()
                self.system_snapshots.append(snapshot)
                await self._save_system_snapshot(snapshot)
                
                # Check for alerts
                await self._check_system_alerts(snapshot)
                
            except Exception as e:
                logger.error(f"System monitoring error: {e}")
                
            await asyncio.sleep(interval)
            
    async def _capture_system_snapshot(self) -> SystemSnapshot:
        """Capture current system performance snapshot"""
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        return SystemSnapshot(
            timestamp=datetime.now(timezone.utc),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            disk_usage_percent=disk.percent,
            network_io_bytes=network.bytes_sent + network.bytes_recv,
            active_processes=len(psutil.pids()),
            agent_count=len(self.agent_metrics),
            message_queue_size=0  # Would be populated from message bus
        )
        
    async def _save_system_snapshot(self, snapshot: SystemSnapshot):
        """Save system snapshot to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO system_snapshots 
            (timestamp, cpu_percent, memory_percent, memory_used_mb, 
             disk_usage_percent, network_io_bytes, active_processes, 
             agent_count, message_queue_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            snapshot.timestamp.isoformat(),
            snapshot.cpu_percent,
            snapshot.memory_percent,
            snapshot.memory_used_mb,
            snapshot.disk_usage_percent,
            snapshot.network_io_bytes,
            snapshot.active_processes,
            snapshot.agent_count,
            snapshot.message_queue_size
        ))
        
        conn.commit()
        conn.close()
        
    async def record_metric(self, metric_name: str, value: float, unit: str, 
                          component: str, metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(timezone.utc),
            metric_name=metric_name,
            value=value,
            unit=unit,
            component=component,
            metadata=metadata or {}
        )
        
        self.metrics_buffer.append(metric)
        
    async def _metrics_processor_loop(self):
        """Process and save metrics from buffer"""
        while self.monitoring_active:
            try:
                if self.metrics_buffer:
                    # Process batch of metrics
                    batch_size = min(50, len(self.metrics_buffer))
                    metrics_batch = []
                    
                    for _ in range(batch_size):
                        if self.metrics_buffer:
                            metrics_batch.append(self.metrics_buffer.popleft())
                    
                    if metrics_batch:
                        await self._save_metrics_batch(metrics_batch)
                        
            except Exception as e:
                logger.error(f"Metrics processing error: {e}")
                
            await asyncio.sleep(1.0)
            
    async def _save_metrics_batch(self, metrics: List[PerformanceMetric]):
        """Save batch of metrics to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for metric in metrics:
            cursor.execute("""
                INSERT INTO performance_metrics 
                (timestamp, metric_name, value, unit, component, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                metric.timestamp.isoformat(),
                metric.metric_name,
                metric.value,
                metric.unit,
                metric.component,
                json.dumps(metric.metadata)
            ))
        
        conn.commit()
        conn.close()
        
    async def update_agent_performance(self, agent_id: str, 
                                     task_completion_rate: float = None,
                                     response_time: float = None,
                                     error_rate: float = None,
                                     resource_utilization: float = None):
        """Update agent performance metrics"""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentPerformance(
                agent_id=agent_id,
                task_completion_rate=0.0,
                average_response_time=0.0,
                error_rate=0.0,
                resource_utilization=0.0,
                last_activity=datetime.now(timezone.utc)
            )
            
        agent_perf = self.agent_metrics[agent_id]
        
        # Update metrics with exponential moving average
        alpha = 0.3  # Smoothing factor
        
        if task_completion_rate is not None:
            agent_perf.task_completion_rate = (
                alpha * task_completion_rate + 
                (1 - alpha) * agent_perf.task_completion_rate
            )
            
        if response_time is not None:
            agent_perf.average_response_time = (
                alpha * response_time + 
                (1 - alpha) * agent_perf.average_response_time
            )
            
        if error_rate is not None:
            agent_perf.error_rate = (
                alpha * error_rate + 
                (1 - alpha) * agent_perf.error_rate
            )
            
        if resource_utilization is not None:
            agent_perf.resource_utilization = (
                alpha * resource_utilization + 
                (1 - alpha) * agent_perf.resource_utilization
            )
            
        agent_perf.last_activity = datetime.now(timezone.utc)
        
        # Save to database
        await self._save_agent_performance(agent_perf)
        
    async def _save_agent_performance(self, agent_perf: AgentPerformance):
        """Save agent performance to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_performance 
            (agent_id, timestamp, task_completion_rate, average_response_time, 
             error_rate, resource_utilization, last_activity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            agent_perf.agent_id,
            datetime.now(timezone.utc).isoformat(),
            agent_perf.task_completion_rate,
            agent_perf.average_response_time,
            agent_perf.error_rate,
            agent_perf.resource_utilization,
            agent_perf.last_activity.isoformat()
        ))
        
        conn.commit()
        conn.close()
        
    async def _check_system_alerts(self, snapshot: SystemSnapshot):
        """Check system metrics against alert thresholds"""
        alerts = []
        
        if snapshot.cpu_percent > self.alert_thresholds["cpu_percent"]:
            alerts.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"CPU usage at {snapshot.cpu_percent:.1f}%",
                "component": "system"
            })
            
        if snapshot.memory_percent > self.alert_thresholds["memory_percent"]:
            alerts.append({
                "type": "high_memory",
                "severity": "warning",
                "message": f"Memory usage at {snapshot.memory_percent:.1f}%",
                "component": "system"
            })
            
        if snapshot.disk_usage_percent > self.alert_thresholds["disk_usage_percent"]:
            alerts.append({
                "type": "high_disk",
                "severity": "critical",
                "message": f"Disk usage at {snapshot.disk_usage_percent:.1f}%",
                "component": "system"
            })
            
        for alert in alerts:
            await self._trigger_alert(alert)
            
    async def _alert_checker_loop(self):
        """Check agent performance for alerts"""
        while self.monitoring_active:
            try:
                for agent_id, agent_perf in self.agent_metrics.items():
                    # Check error rate
                    if agent_perf.error_rate > self.alert_thresholds["error_rate"]:
                        await self._trigger_alert({
                            "type": "high_error_rate",
                            "severity": "warning",
                            "message": f"Agent {agent_id} error rate: {agent_perf.error_rate:.2%}",
                            "component": agent_id
                        })
                        
                    # Check response time
                    if agent_perf.average_response_time > self.alert_thresholds["response_time_ms"]:
                        await self._trigger_alert({
                            "type": "slow_response",
                            "severity": "warning",
                            "message": f"Agent {agent_id} slow response: {agent_perf.average_response_time:.0f}ms",
                            "component": agent_id
                        })
                        
            except Exception as e:
                logger.error(f"Alert checking error: {e}")
                
            await asyncio.sleep(30.0)  # Check every 30 seconds
            
    async def _trigger_alert(self, alert: Dict[str, Any]):
        """Trigger performance alert"""
        # Save alert to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO performance_alerts 
            (timestamp, alert_type, severity, message, component)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            alert["type"],
            alert["severity"],
            alert["message"],
            alert["component"]
        ))
        
        conn.commit()
        conn.close()
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")
                
        logger.warning(f"Performance Alert: {alert['message']}")
        
    def add_alert_callback(self, callback: Callable):
        """Add callback for performance alerts"""
        self.alert_callbacks.append(callback)
        
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics summary"""
        if not self.system_snapshots:
            return {"error": "No metrics available"}
            
        latest_snapshot = self.system_snapshots[-1]
        
        return {
            "system": {
                "cpu_percent": latest_snapshot.cpu_percent,
                "memory_percent": latest_snapshot.memory_percent,
                "memory_used_mb": latest_snapshot.memory_used_mb,
                "disk_usage_percent": latest_snapshot.disk_usage_percent,
                "active_processes": latest_snapshot.active_processes,
                "timestamp": latest_snapshot.timestamp.isoformat()
            },
            "agents": {
                agent_id: {
                    "task_completion_rate": perf.task_completion_rate,
                    "average_response_time": perf.average_response_time,
                    "error_rate": perf.error_rate,
                    "resource_utilization": perf.resource_utilization,
                    "last_activity": perf.last_activity.isoformat()
                }
                for agent_id, perf in self.agent_metrics.items()
            },
            "summary": {
                "total_agents": len(self.agent_metrics),
                "healthy_agents": len([p for p in self.agent_metrics.values() 
                                     if p.error_rate < 0.05]),
                "average_response_time": sum(p.average_response_time 
                                           for p in self.agent_metrics.values()) / 
                                         len(self.agent_metrics) if self.agent_metrics else 0
            }
        }
        
    async def generate_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get system metrics
        cursor.execute("""
            SELECT * FROM system_snapshots 
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
        """, (start_time.isoformat(), end_time.isoformat()))
        
        system_data = cursor.fetchall()
        
        # Get agent performance
        cursor.execute("""
            SELECT * FROM agent_performance 
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
        """, (start_time.isoformat(), end_time.isoformat()))
        
        agent_data = cursor.fetchall()
        
        # Get alerts
        cursor.execute("""
            SELECT * FROM performance_alerts 
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp DESC
        """, (start_time.isoformat(), end_time.isoformat()))
        
        alerts_data = cursor.fetchall()
        
        conn.close()
        
        return {
            "report_period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "duration_hours": hours
            },
            "system_performance": {
                "data_points": len(system_data),
                "avg_cpu": sum(row[2] for row in system_data) / len(system_data) if system_data else 0,
                "avg_memory": sum(row[3] for row in system_data) / len(system_data) if system_data else 0,
                "peak_cpu": max(row[2] for row in system_data) if system_data else 0,
                "peak_memory": max(row[3] for row in system_data) if system_data else 0
            },
            "agent_performance": {
                "total_records": len(agent_data),
                "unique_agents": len(set(row[1] for row in agent_data)),
                "avg_completion_rate": sum(row[3] for row in agent_data) / len(agent_data) if agent_data else 0,
                "avg_response_time": sum(row[4] for row in agent_data) / len(agent_data) if agent_data else 0
            },
            "alerts": {
                "total_alerts": len(alerts_data),
                "critical_alerts": len([a for a in alerts_data if a[3] == "critical"]),
                "warning_alerts": len([a for a in alerts_data if a[3] == "warning"]),
                "recent_alerts": alerts_data[:10]  # Last 10 alerts
            }
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()