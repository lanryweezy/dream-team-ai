"""
Finance Agent
Handles payments, accounting, budgeting, and financial tracking
"""

import asyncio
import logging
import json
import sqlite3
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

from core.base_agent import BaseAgent, AgentCapability, TaskResult

logger = logging.getLogger(__name__)

class FinanceAgent(BaseAgent):

    def __init__(self):
        self.db_path = "finance_agent.db"
        self._init_db()
        capabilities = [
            AgentCapability(
                name="setup_payments",
                description="Setup payment processing (Stripe, PayPal, etc.)",
                cost_estimate=0.0,
                confidence_level=0.9,
                requirements=["business_info", "bank_account"]
            ),
            AgentCapability(
                name="track_expenses",
                description="Track and categorize business expenses",
                cost_estimate=0.0,
                confidence_level=0.95,
                requirements=["expense_data"]
            ),
            AgentCapability(
                name="generate_reports",
                description="Generate financial reports and forecasts",
                cost_estimate=1.0,
                confidence_level=0.85,
                requirements=["financial_data"]
            ),
            AgentCapability(
                name="manage_subscriptions",
                description="Track and manage SaaS subscriptions",
                cost_estimate=0.0,
                confidence_level=0.9,
                requirements=["subscription_list"]
            ),
            AgentCapability(
                name="budget_planning",
                description="Create and monitor budgets",
                cost_estimate=0.0,
                confidence_level=0.8,
                requirements=["revenue_projections", "expense_history"]
            )
        ]
        
        super().__init__("finance_agent", capabilities)
        self.financial_data = {}
        self.subscriptions = {}
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute finance tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "setup_payments":
                return await self._setup_payments(task)
            elif task_type == "track_expenses":
                return await self._track_expenses(task)
            elif task_type == "generate_reports":
                return await self._generate_reports(task)
            elif task_type == "manage_subscriptions":
                return await self._manage_subscriptions(task)
            elif task_type == "budget_planning":
                return await self._budget_planning(task)
            else:
                return TaskResult(
                    success=False,
                    output={},
                    cost_incurred=0.0,
                    evidence=[],
                    next_steps=[],
                    error_message=f"Unknown task type: {task_type}"
                )
                
        except Exception as e:
            logger.error(f"Finance task failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def _setup_payments(self, task: Dict[str, Any]) -> TaskResult:
        """Setup payment processing"""
        business_info = task.get("business_info", {})
        provider = task.get("provider", "stripe")
        
        # This would integrate with payment provider APIs
        # For now, we'll simulate the setup process
        
        payment_config = {
            "provider": provider,
            "business_name": business_info.get("name", "DreamCorp"),
            "currency": business_info.get("currency", "USD"),
            "account_id": f"{provider}_{datetime.utcnow().timestamp()}",
            "webhook_url": f"https://{business_info.get('domain', 'example.com')}/webhooks/{provider}",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Save payment configuration to DB
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO payment_configs (provider, config, created_at)
            VALUES (?, ?, ?)
        ''', (provider, json.dumps(payment_config), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
            
        return TaskResult(
            success=True,
            output={
                "provider": provider,
                "account_id": payment_config["account_id"],
                "webhook_url": payment_config["webhook_url"],
                "config_file": config_file
            },
            cost_incurred=0.0,
            evidence=[config_file],
            next_steps=[
                "Complete KYC verification",
                "Test payment flow",
                "Setup webhook handling",
                "Configure tax settings"
            ]
        )
        
    async def _track_expenses(self, task: Dict[str, Any]) -> TaskResult:
        """Track business expenses"""
        expenses = task.get("expenses", [])
        
        if not expenses:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Provide expense data"],
                error_message="No expenses to track"
            )
            
        # Process and categorize expenses
        categorized_expenses = []
        total_amount = 0.0
        
        for expense in expenses:
            amount = float(expense.get("amount", 0))
            category = self._categorize_expense(expense.get("description", ""))
            
            categorized_expense = {
                "id": expense.get("id", f"exp_{datetime.utcnow().timestamp()}"),
                "date": expense.get("date", datetime.utcnow().isoformat()),
                "amount": amount,
                "description": expense.get("description", ""),
                "category": category,
                "vendor": expense.get("vendor", "Unknown"),
                "receipt_url": expense.get("receipt_url", "")
            }
            
            categorized_expenses.append(categorized_expense)
            total_amount += amount
            
        # Save expense data to DB
        period = datetime.utcnow().strftime('%Y_%m')
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Load existing expenses
        c.execute('SELECT data FROM expenses WHERE period = ?', (period,))
        row = c.fetchone()
        existing_expenses = json.loads(row[0]) if row else []

        existing_expenses.extend(categorized_expenses)
        
        c.execute('''
            INSERT OR REPLACE INTO expenses (id, period, data)
            VALUES ((SELECT id FROM expenses WHERE period = ?), ?, ?)
        ''', (period, period, json.dumps(existing_expenses)))
        conn.commit()
        conn.close()
            
        return TaskResult(
            success=True,
            output={
                "total_expenses": len(categorized_expenses),
                "total_amount": total_amount,
                "categories": list(set(exp["category"] for exp in categorized_expenses)),
                "expense_file": expense_file
            },
            cost_incurred=0.0,
            evidence=[expense_file],
            next_steps=[
                "Review expense categories",
                "Generate monthly report",
                "Update budget forecasts"
            ]
        )
        
    def _categorize_expense(self, description: str) -> str:
        """Automatically categorize expenses based on description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["domain", "hosting", "server", "aws", "vercel"]):
            return "Infrastructure"
        elif any(word in description_lower for word in ["stripe", "paypal", "payment", "transaction"]):
            return "Payment Processing"
        elif any(word in description_lower for word in ["marketing", "ads", "advertising", "social"]):
            return "Marketing"
        elif any(word in description_lower for word in ["software", "saas", "subscription", "api"]):
            return "Software & Tools"
        elif any(word in description_lower for word in ["legal", "lawyer", "attorney", "compliance"]):
            return "Legal & Compliance"
        elif any(word in description_lower for word in ["office", "supplies", "equipment"]):
            return "Office & Equipment"
        else:
            return "Other"
            
    async def _generate_reports(self, task: Dict[str, Any]) -> TaskResult:
        """Generate financial reports"""
        report_type = task.get("report_type", "monthly")
        period = task.get("period", datetime.utcnow().strftime("%Y-%m"))
        
        # Load financial data
        expense_file = f"financial_data/expenses_{period.replace('-', '_')}.json"
        
        if not os.path.exists(expense_file):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Track expenses first", "Ensure data exists for period"],
                error_message=f"No financial data found for period {period}"
            )
            
        with open(expense_file, "r") as f:
            expenses = json.load(f)
            
        # Generate report
        report = await self._create_financial_report(expenses, report_type, period)
        
        # Save report
        report_file = f"financial_data/report_{report_type}_{period}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
            
        return TaskResult(
            success=True,
            output=report,
            cost_incurred=1.0,
            evidence=[report_file],
            next_steps=[
                "Review report with founder",
                "Identify cost optimization opportunities",
                "Update budget projections"
            ]
        )
        
    async def _create_financial_report(self, expenses: List[Dict], report_type: str, period: str) -> Dict[str, Any]:
        """Create a financial report from expense data"""
        total_expenses = sum(exp["amount"] for exp in expenses)
        
        # Group by category
        category_totals = {}
        for expense in expenses:
            category = expense["category"]
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]
            
        # Calculate trends (mock data for now)
        previous_period_total = total_expenses * 0.85  # Simulate 15% growth
        
        report = {
            "report_type": report_type,
            "period": period,
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_expenses": total_expenses,
                "total_transactions": len(expenses),
                "average_transaction": total_expenses / len(expenses) if expenses else 0,
                "previous_period_total": previous_period_total,
                "growth_rate": ((total_expenses - previous_period_total) / previous_period_total * 100) if previous_period_total > 0 else 0
            },
            "category_breakdown": category_totals,
            "top_expenses": sorted(expenses, key=lambda x: x["amount"], reverse=True)[:10],
            "recommendations": [
                "Consider negotiating better rates with top vendors",
                "Review recurring subscriptions for optimization",
                "Implement expense approval workflow for amounts over $100"
            ]
        }
        
        return report
        
    async def _manage_subscriptions(self, task: Dict[str, Any]) -> TaskResult:
        """Manage SaaS subscriptions"""
        action = task.get("action", "list")
        
        if action == "add":
            subscription = task.get("subscription", {})
            return await self._add_subscription(subscription)
        elif action == "list":
            return await self._list_subscriptions()
        elif action == "cancel":
            subscription_id = task.get("subscription_id")
            return await self._cancel_subscription(subscription_id)
        else:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Specify valid action: add, list, or cancel"],
                error_message=f"Unknown subscription action: {action}"
            )
            
    async def _add_subscription(self, subscription: Dict[str, Any]) -> TaskResult:
        """Add a new subscription"""
        subscription_id = f"sub_{datetime.utcnow().timestamp()}"
        
        subscription_data = {
            "id": subscription_id,
            "name": subscription.get("name", "Unknown Service"),
            "provider": subscription.get("provider", ""),
            "cost": float(subscription.get("cost", 0)),
            "billing_cycle": subscription.get("billing_cycle", "monthly"),
            "next_billing_date": subscription.get("next_billing_date", ""),
            "status": "active",
            "added_at": datetime.utcnow().isoformat()
        }
        
        # Save subscription to DB
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO subscriptions (id, name, provider, cost, billing_cycle, category, status, start_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (subscription_id, service_name, provider, cost, billing_cycle, category, "active", datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
            
        return TaskResult(
            success=True,
            output={
                "subscription_id": subscription_id,
                "subscription": subscription_data
            },
            cost_incurred=0.0,
            evidence=[subscriptions_file],
            next_steps=[
                "Set up billing alerts",
                "Review subscription usage",
                "Schedule periodic cost review"
            ]
        )
        
    async def _list_subscriptions(self) -> TaskResult:
        """List all subscriptions"""
        subscriptions_file = "financial_data/subscriptions.json"
        
        if not os.path.exists(subscriptions_file):
            return TaskResult(
                success=True,
                output={
                    "subscriptions": [],
                    "total_monthly_cost": 0.0,
                    "total_annual_cost": 0.0
                },
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Add subscriptions to track"]
            )
            
        with open(subscriptions_file, "r") as f:
            subscriptions = json.load(f)
            
        # Calculate costs
        monthly_cost = sum(
            sub["cost"] if sub["billing_cycle"] == "monthly" else sub["cost"] / 12
            for sub in subscriptions if sub["status"] == "active"
        )
        
        annual_cost = monthly_cost * 12
        
        return TaskResult(
            success=True,
            output={
                "subscriptions": subscriptions,
                "total_subscriptions": len(subscriptions),
                "active_subscriptions": len([s for s in subscriptions if s["status"] == "active"]),
                "total_monthly_cost": monthly_cost,
                "total_annual_cost": annual_cost
            },
            cost_incurred=0.0,
            evidence=[subscriptions_file],
            next_steps=[
                "Review high-cost subscriptions",
                "Check for unused services",
                "Negotiate better pricing"
            ]
        )
        
    async def _cancel_subscription(self, subscription_id: str) -> TaskResult:
        """Cancel a subscription"""
        subscriptions_file = "financial_data/subscriptions.json"
        
        if not os.path.exists(subscriptions_file):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Add subscriptions first"],
                error_message="No subscriptions found"
            )
            
        with open(subscriptions_file, "r") as f:
            subscriptions = json.load(f)
            
        # Find and cancel subscription
        for subscription in subscriptions:
            if subscription["id"] == subscription_id:
                subscription["status"] = "cancelled"
                subscription["cancelled_at"] = datetime.utcnow().isoformat()
                
                with open(subscriptions_file, "w") as f:
                    json.dump(subscriptions, f, indent=2)
                    
                return TaskResult(
                    success=True,
                    output={
                        "subscription_id": subscription_id,
                        "subscription": subscription
                    },
                    cost_incurred=0.0,
                    evidence=[subscriptions_file],
                    next_steps=[
                        "Confirm cancellation with provider",
                        "Update budget projections",
                        "Remove access credentials"
                    ]
                )
                
        return TaskResult(
            success=False,
            output={},
            cost_incurred=0.0,
            evidence=[],
            next_steps=["Check subscription ID"],
            error_message=f"Subscription {subscription_id} not found"
        )
        
    async def _budget_planning(self, task: Dict[str, Any]) -> TaskResult:
        """Create and monitor budgets"""
        budget_type = task.get("budget_type", "monthly")
        target_period = task.get("target_period", datetime.utcnow().strftime("%Y-%m"))
        
        # Create budget based on historical data and projections
        budget = await self._create_budget(budget_type, target_period)
        
        # Save budget to DB
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO budgets (budget_type, target_period, data)
            VALUES (?, ?, ?)
        ''', (budget_type, target_period, json.dumps(budget)))
        conn.commit()
        conn.close()
            
        return TaskResult(
            success=True,
            output=budget,
            cost_incurred=0.0,
            evidence=[budget_file],
            next_steps=[
                "Review budget with founder",
                "Set up budget alerts",
                "Monitor actual vs budgeted spend"
            ]
        )
        
    async def _create_budget(self, budget_type: str, target_period: str) -> Dict[str, Any]:
        """Create a budget based on historical data"""
        # This would analyze historical spending patterns
        # For now, we'll create a sample budget
        
        budget = {
            "budget_type": budget_type,
            "target_period": target_period,
            "created_at": datetime.utcnow().isoformat(),
            "categories": {
                "Infrastructure": 200.0,
                "Marketing": 500.0,
                "Software & Tools": 300.0,
                "Payment Processing": 100.0,
                "Legal & Compliance": 150.0,
                "Other": 100.0
            },
            "total_budget": 1350.0,
            "alerts": {
                "warning_threshold": 0.8,  # 80% of budget
                "critical_threshold": 0.95  # 95% of budget
            }
        }
        
        return budget
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily finance goals"""
        return [
            {
                "goal": "Review and categorize new expenses",
                "priority": "high",
                "estimated_time": "20 minutes"
            },
            {
                "goal": "Monitor subscription renewals",
                "priority": "medium",
                "estimated_time": "15 minutes"
            },
            {
                "goal": "Update financial forecasts",
                "priority": "low",
                "estimated_time": "30 minutes"
            }
        ]

# Example usage
async def main():
    """Example usage of FinanceAgent"""
    agent = FinanceAgent()
    await agent.start()
    
    # Test payment setup
    task = {
        "type": "setup_payments",
        "business_info": {
            "name": "DreamCorp",
            "currency": "USD",
            "domain": "dreamcorp.com"
        },
        "provider": "stripe"
    }
    
    result = await agent.execute_task(task)
    print("Payment setup result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())