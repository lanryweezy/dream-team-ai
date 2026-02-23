"""
Cost Tracker
Monitors and tracks costs across all agents and tools
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class CostEntry:
    id: str
    agent_id: str
    tool_name: str
    action_type: str
    amount: float
    currency: str
    description: str
    metadata: Dict[str, Any]
    timestamp: str
    category: str = "general"

@dataclass
class BudgetAlert:
    id: str
    alert_type: str  # "threshold", "limit", "projection"
    message: str
    severity: str  # "info", "warning", "critical"
    current_amount: float
    threshold_amount: float
    period: str
    timestamp: str

class CostTracker:
    def __init__(self, db_path: str = "cost_tracking.db"):
        self.db_path = db_path
        self.budget_limits = {
            "daily": 100.0,
            "weekly": 500.0,
            "monthly": 2000.0,
            "yearly": 20000.0
        }
        self.alert_thresholds = {
            "daily": 0.8,  # Alert at 80% of daily budget
            "weekly": 0.75,
            "monthly": 0.7,
            "yearly": 0.6
        }
        
        # Tool cost estimates (per API call or usage)
        self.tool_costs = {
            "openai_gpt4": 0.03,  # per 1k tokens
            "openai_gpt3": 0.002,
            "sendgrid": 0.0001,  # per email
            "stripe": 0.029,  # 2.9% + 30¢ per transaction
            "github_api": 0.0,  # Free tier
            "vercel_deployment": 0.0,  # Free tier
            "aws_s3": 0.023,  # per GB
            "domain_registration": 12.0,  # per year
            "ssl_certificate": 0.0,  # Let's Encrypt free
        }
        
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for cost tracking"""
        
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create costs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS costs (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                description TEXT,
                metadata TEXT,
                category TEXT DEFAULT 'general',
                timestamp TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create budget_alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget_alerts (
                id TEXT PRIMARY KEY,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL,
                current_amount REAL NOT NULL,
                threshold_amount REAL NOT NULL,
                period TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                acknowledged BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_costs_timestamp ON costs(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_costs_agent ON costs(agent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_costs_tool ON costs(tool_name)")
        
        conn.commit()
        conn.close()
        
    def record_cost(self, 
                   agent_id: str,
                   tool_name: str,
                   action_type: str,
                   amount: float,
                   description: str = "",
                   metadata: Dict[str, Any] = None,
                   category: str = "general") -> str:
        """Record a cost entry"""
        
        cost_entry = CostEntry(
            id=f"cost_{datetime.utcnow().timestamp()}",
            agent_id=agent_id,
            tool_name=tool_name,
            action_type=action_type,
            amount=amount,
            currency="USD",
            description=description,
            metadata=metadata or {},
            timestamp=datetime.utcnow().isoformat(),
            category=category
        )
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO costs (id, agent_id, tool_name, action_type, amount, currency, 
                             description, metadata, category, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cost_entry.id,
            cost_entry.agent_id,
            cost_entry.tool_name,
            cost_entry.action_type,
            cost_entry.amount,
            cost_entry.currency,
            cost_entry.description,
            json.dumps(cost_entry.metadata),
            cost_entry.category,
            cost_entry.timestamp
        ))
        
        conn.commit()
        conn.close()
        
        # Check for budget alerts
        self._check_budget_alerts()
        
        logger.info(f"Recorded cost: {cost_entry.agent_id} - {cost_entry.tool_name} - ${cost_entry.amount:.4f}")
        
        return cost_entry.id
        
    def estimate_cost(self, tool_name: str, usage_params: Dict[str, Any]) -> float:
        """Estimate cost for a tool usage"""
        
        base_cost = self.tool_costs.get(tool_name, 0.0)
        
        if tool_name.startswith("openai"):
            # Estimate based on tokens
            tokens = usage_params.get("tokens", 1000)
            return (tokens / 1000) * base_cost
            
        elif tool_name == "sendgrid":
            # Cost per email
            email_count = usage_params.get("email_count", 1)
            return email_count * base_cost
            
        elif tool_name == "stripe":
            # Percentage + fixed fee
            transaction_amount = usage_params.get("amount", 0)
            return (transaction_amount * 0.029) + 0.30
            
        elif tool_name == "aws_s3":
            # Cost per GB
            storage_gb = usage_params.get("storage_gb", 0.1)
            return storage_gb * base_cost
            
        else:
            # Default flat rate
            return base_cost
            
    def get_spending_summary(self, period: str = "monthly") -> Dict[str, Any]:
        """Get spending summary for a period"""
        
        end_date = datetime.utcnow()
        
        if period == "daily":
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            start_date = end_date - timedelta(days=7)
        elif period == "monthly":
            start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "yearly":
            start_date = end_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = end_date - timedelta(days=30)
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total spending
        cursor.execute("""
            SELECT SUM(amount) FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
        """, (start_date.isoformat(), end_date.isoformat()))
        
        total_spent = cursor.fetchone()[0] or 0.0
        
        # Spending by agent
        cursor.execute("""
            SELECT agent_id, SUM(amount) FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY agent_id
            ORDER BY SUM(amount) DESC
        """, (start_date.isoformat(), end_date.isoformat()))
        
        spending_by_agent = dict(cursor.fetchall())
        
        # Spending by tool
        cursor.execute("""
            SELECT tool_name, SUM(amount) FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY tool_name
            ORDER BY SUM(amount) DESC
        """, (start_date.isoformat(), end_date.isoformat()))
        
        spending_by_tool = dict(cursor.fetchall())
        
        # Spending by category
        cursor.execute("""
            SELECT category, SUM(amount) FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (start_date.isoformat(), end_date.isoformat()))
        
        spending_by_category = dict(cursor.fetchall())
        
        conn.close()
        
        budget_limit = self.budget_limits.get(period, 0)
        remaining_budget = budget_limit - total_spent
        utilization = (total_spent / budget_limit * 100) if budget_limit > 0 else 0
        
        return {
            "period": period,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_spent": total_spent,
            "budget_limit": budget_limit,
            "remaining_budget": remaining_budget,
            "utilization_percent": utilization,
            "spending_by_agent": spending_by_agent,
            "spending_by_tool": spending_by_tool,
            "spending_by_category": spending_by_category
        }
        
    def get_cost_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get cost trends over time"""
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Daily spending trend
        cursor.execute("""
            SELECT DATE(timestamp) as date, SUM(amount) as daily_total
            FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        """, (start_date.isoformat(), end_date.isoformat()))
        
        daily_trends = [
            {"date": row[0], "amount": row[1]}
            for row in cursor.fetchall()
        ]
        
        # Tool usage trends
        cursor.execute("""
            SELECT tool_name, DATE(timestamp) as date, SUM(amount) as daily_total
            FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY tool_name, DATE(timestamp)
            ORDER BY tool_name, date
        """, (start_date.isoformat(), end_date.isoformat()))
        
        tool_trends = defaultdict(list)
        for row in cursor.fetchall():
            tool_trends[row[0]].append({
                "date": row[1],
                "amount": row[2]
            })
            
        conn.close()
        
        return {
            "period_days": days,
            "daily_trends": daily_trends,
            "tool_trends": dict(tool_trends)
        }
        
    def _check_budget_alerts(self):
        """Check for budget threshold alerts"""
        
        for period in self.budget_limits:
            summary = self.get_spending_summary(period)
            
            threshold = self.alert_thresholds.get(period, 0.8)
            threshold_amount = summary["budget_limit"] * threshold
            
            if summary["total_spent"] >= threshold_amount:
                severity = "critical" if summary["utilization_percent"] >= 95 else "warning"
                
                alert = BudgetAlert(
                    id=f"alert_{datetime.utcnow().timestamp()}",
                    alert_type="threshold",
                    message=f"{period.title()} budget at {summary['utilization_percent']:.1f}% (${summary['total_spent']:.2f} of ${summary['budget_limit']:.2f})",
                    severity=severity,
                    current_amount=summary["total_spent"],
                    threshold_amount=threshold_amount,
                    period=period,
                    timestamp=datetime.utcnow().isoformat()
                )
                
                self._save_alert(alert)
                
    def _save_alert(self, alert: BudgetAlert):
        """Save budget alert to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if similar alert already exists (avoid spam)
        cursor.execute("""
            SELECT id FROM budget_alerts 
            WHERE alert_type = ? AND period = ? AND severity = ?
            AND timestamp >= ?
            AND acknowledged = FALSE
        """, (
            alert.alert_type,
            alert.period,
            alert.severity,
            (datetime.utcnow() - timedelta(hours=1)).isoformat()  # Within last hour
        ))
        
        if cursor.fetchone():
            conn.close()
            return  # Similar alert already exists
            
        cursor.execute("""
            INSERT INTO budget_alerts (id, alert_type, message, severity, 
                                     current_amount, threshold_amount, period, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert.id,
            alert.alert_type,
            alert.message,
            alert.severity,
            alert.current_amount,
            alert.threshold_amount,
            alert.period,
            alert.timestamp
        ))
        
        conn.commit()
        conn.close()
        
        logger.warning(f"Budget alert: {alert.message}")
        
    def get_active_alerts(self) -> List[BudgetAlert]:
        """Get active budget alerts"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, alert_type, message, severity, current_amount, 
                   threshold_amount, period, timestamp
            FROM budget_alerts 
            WHERE acknowledged = FALSE
            ORDER BY timestamp DESC
        """)
        
        alerts = []
        for row in cursor.fetchall():
            alert = BudgetAlert(
                id=row[0],
                alert_type=row[1],
                message=row[2],
                severity=row[3],
                current_amount=row[4],
                threshold_amount=row[5],
                period=row[6],
                timestamp=row[7]
            )
            alerts.append(alert)
            
        conn.close()
        return alerts
        
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a budget alert"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE budget_alerts 
            SET acknowledged = TRUE 
            WHERE id = ?
        """, (alert_id,))
        
        conn.commit()
        conn.close()
        
    def update_budget_limits(self, limits: Dict[str, float]):
        """Update budget limits"""
        
        for period, limit in limits.items():
            if period in self.budget_limits:
                self.budget_limits[period] = limit
                logger.info(f"Updated {period} budget limit to ${limit:.2f}")
                
    def export_costs(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Export cost data for a date range"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, agent_id, tool_name, action_type, amount, currency,
                   description, metadata, category, timestamp
            FROM costs 
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
        """, (start_date, end_date))
        
        costs = []
        for row in cursor.fetchall():
            cost = {
                "id": row[0],
                "agent_id": row[1],
                "tool_name": row[2],
                "action_type": row[3],
                "amount": row[4],
                "currency": row[5],
                "description": row[6],
                "metadata": json.loads(row[7]) if row[7] else {},
                "category": row[8],
                "timestamp": row[9]
            }
            costs.append(cost)
            
        conn.close()
        return costs
        
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total cost
        cursor.execute("SELECT SUM(amount) FROM costs")
        total_result = cursor.fetchone()
        total_cost = total_result[0] if total_result[0] else 0.0
        
        # Get cost by agent
        cursor.execute("SELECT agent_id, SUM(amount) FROM costs GROUP BY agent_id")
        agent_results = cursor.fetchall()
        by_agent = {agent_id: amount for agent_id, amount in agent_results}
        
        # Get cost by category
        cursor.execute("SELECT category, SUM(amount) FROM costs GROUP BY category")
        category_results = cursor.fetchall()
        by_category = {category: amount for category, amount in category_results}
        
        # Get cost by tool
        cursor.execute("SELECT tool_name, SUM(amount) FROM costs GROUP BY tool_name")
        tool_results = cursor.fetchall()
        by_tool = {tool_name: amount for tool_name, amount in tool_results}
        
        conn.close()
        
        return {
            "total_cost": total_cost,
            "by_agent": by_agent,
            "by_category": by_category,
            "by_tool": by_tool,
            "summary_generated_at": datetime.utcnow().isoformat()
        }

# Example usage
def main():
    """Example usage of CostTracker"""
    
    cost_tracker = CostTracker()
    
    # Record some costs
    cost_tracker.record_cost(
        agent_id="marketing_agent",
        tool_name="sendgrid",
        action_type="send_email",
        amount=0.05,
        description="Welcome email campaign",
        category="marketing"
    )
    
    cost_tracker.record_cost(
        agent_id="engineering_agent",
        tool_name="openai_gpt4",
        action_type="code_generation",
        amount=1.20,
        description="Generate React components",
        category="development"
    )
    
    # Get spending summary
    summary = cost_tracker.get_spending_summary("monthly")
    print("Monthly spending summary:")
    print(json.dumps(summary, indent=2))
    
    # Get active alerts
    alerts = cost_tracker.get_active_alerts()
    print(f"\nActive alerts: {len(alerts)}")
    for alert in alerts:
        print(f"- {alert.severity.upper()}: {alert.message}")

if __name__ == "__main__":
    main()