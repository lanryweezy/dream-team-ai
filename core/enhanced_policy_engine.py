"""
Enhanced Policy Engine with Persistent Data and Advanced Rules
Addresses critical issues from improvement plan
"""

import json
import logging
import sqlite3
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import os

logger = logging.getLogger(__name__)

class ActionType(Enum):
    FINANCIAL_TRANSACTION = "financial_transaction"
    EXTERNAL_API_CALL = "external_api_call"
    EMAIL_SEND = "email_send"
    FILE_CREATION = "file_creation"
    SYSTEM_MODIFICATION = "system_modification"
    DATA_EXPORT = "data_export"
    LEGAL_FILING = "legal_filing"
    EXTERNAL_POST = "external_post"
    MARKETING_CAMPAIGN = "marketing_campaign"
    PRODUCT_RELEASE = "product_release"

class PolicyAction(Enum):
    AUTO_APPROVE = "auto_approve"
    REQUIRE_APPROVAL = "require_approval"
    DENY = "deny"
    ESCALATE = "escalate"

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class PolicyRule:
    id: str
    name: str
    description: str
    conditions: List[Dict[str, Any]]  # List of condition dictionaries
    action: PolicyAction
    risk_level: RiskLevel
    priority: int = 100
    active: bool = True
    created_at: str = None
    updated_at: str = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now(timezone.utc).isoformat()

@dataclass
class SpendingRecord:
    id: str
    agent_id: str
    action_type: str
    amount: float
    currency: str
    timestamp: str
    description: str
    approved: bool
    metadata: Dict[str, Any]

@dataclass
class PolicyDecision:
    decision_id: str
    rule_id: Optional[str]
    action_type: ActionType
    action_data: Dict[str, Any]
    decision: PolicyAction
    reason: str
    risk_level: RiskLevel
    timestamp: str
    agent_id: str
    estimated_cost: float

class EnhancedPolicyEngine:
    """Enhanced policy engine with persistent data and advanced rule evaluation"""
    
    def __init__(self, db_path: str = "policy_engine.db", approval_recipient: str = "founder"):
        self.db_path = db_path
        self.approval_recipient = approval_recipient
        self.rules: Dict[str, PolicyRule] = {}
        self.spending_limits = {
            "daily": 1000.0,
            "weekly": 5000.0,
            "monthly": 20000.0,
            "yearly": 200000.0
        }
        
        # Initialize database
        self._init_database()
        
        # Load rules and data
        self._load_rules()
        
        # Add default rules
        self._add_default_rules()
        
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS policy_rules (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    conditions TEXT,  -- JSON string
                    action TEXT NOT NULL,
                    risk_level INTEGER NOT NULL,
                    priority INTEGER DEFAULT 100,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS spending_records (
                    id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    timestamp TEXT NOT NULL,
                    description TEXT,
                    approved BOOLEAN NOT NULL,
                    metadata TEXT  -- JSON string
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS policy_decisions (
                    decision_id TEXT PRIMARY KEY,
                    rule_id TEXT,
                    action_type TEXT NOT NULL,
                    action_data TEXT,  -- JSON string
                    decision TEXT NOT NULL,
                    reason TEXT,
                    risk_level INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    estimated_cost REAL DEFAULT 0.0
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS spending_limits (
                    period TEXT PRIMARY KEY,
                    limit_amount REAL NOT NULL,
                    current_spend REAL DEFAULT 0.0,
                    last_reset TEXT
                )
            """)
            
            # Initialize spending limits if not exists
            for period, limit in self.spending_limits.items():
                cursor.execute("""
                    INSERT OR IGNORE INTO spending_limits (period, limit_amount, current_spend, last_reset)
                    VALUES (?, ?, 0.0, ?)
                """, (period, limit, datetime.now(timezone.utc).isoformat()))
            
            conn.commit()
            conn.close()
            
            logger.info("Policy engine database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize policy engine database: {e}")
            raise
            
    def _load_rules(self):
        """Load policy rules from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM policy_rules WHERE active = TRUE")
            rows = cursor.fetchall()
            
            for row in rows:
                rule = PolicyRule(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    conditions=json.loads(row[3]) if row[3] else [],
                    action=PolicyAction(row[4]),
                    risk_level=RiskLevel(row[5]),
                    priority=row[6],
                    active=bool(row[7]),
                    created_at=row[8],
                    updated_at=row[9]
                )
                self.rules[rule.id] = rule
                
            conn.close()
            logger.info(f"Loaded {len(self.rules)} policy rules")
            
        except Exception as e:
            logger.error(f"Failed to load policy rules: {e}")
            
    def _add_default_rules(self):
        """Add default policy rules if none exist"""
        if not self.rules:
            default_rules = [
                PolicyRule(
                    id="cost_approval_high",
                    name="High Cost Approval",
                    description="Require approval for high-cost actions",
                    conditions=[
                        {"field": "estimated_cost", "operator": ">", "value": 100.0}
                    ],
                    action=PolicyAction.REQUIRE_APPROVAL,
                    risk_level=RiskLevel.MEDIUM,
                    priority=50
                ),
                PolicyRule(
                    id="financial_transaction_approval",
                    name="Financial Transaction Approval",
                    description="All financial transactions require approval",
                    conditions=[
                        {"field": "action_type", "operator": "==", "value": "FINANCIAL_TRANSACTION"}
                    ],
                    action=PolicyAction.REQUIRE_APPROVAL,
                    risk_level=RiskLevel.HIGH,
                    priority=10
                ),
                PolicyRule(
                    id="external_api_moderate",
                    name="External API Moderate Risk",
                    description="External API calls require approval for sensitive operations",
                    conditions=[
                        {"field": "action_type", "operator": "==", "value": "EXTERNAL_API_CALL"},
                        {"field": "estimated_cost", "operator": ">", "value": 10.0}
                    ],
                    action=PolicyAction.REQUIRE_APPROVAL,
                    risk_level=RiskLevel.MEDIUM,
                    priority=30
                ),
                PolicyRule(
                    id="auto_approve_low_cost",
                    name="Auto Approve Low Cost",
                    description="Auto approve low-cost, low-risk actions",
                    conditions=[
                        {"field": "estimated_cost", "operator": "<=", "value": 5.0},
                        {"field": "action_type", "operator": "!=", "value": "FINANCIAL_TRANSACTION"}
                    ],
                    action=PolicyAction.AUTO_APPROVE,
                    risk_level=RiskLevel.LOW,
                    priority=90
                )
            ]
            
            for rule in default_rules:
                self.add_rule(rule)
                
    def add_rule(self, rule: PolicyRule) -> bool:
        """Add a new policy rule"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO policy_rules 
                (id, name, description, conditions, action, risk_level, priority, active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rule.id, rule.name, rule.description, json.dumps(rule.conditions),
                rule.action.value, rule.risk_level.value, rule.priority, rule.active,
                rule.created_at, rule.updated_at
            ))
            
            conn.commit()
            conn.close()
            
            self.rules[rule.id] = rule
            logger.info(f"Added policy rule: {rule.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add policy rule: {e}")
            return False
            
    def requires_approval(self, action: Dict[str, Any], estimated_cost: float = 0.0) -> bool:
        """Enhanced approval check with rule evaluation"""
        try:
            # Determine action type
            action_type = self._determine_action_type(action)
            
            # Create action context for rule evaluation
            action_context = {
                "action_type": action_type.value,
                "estimated_cost": estimated_cost,
                **action
            }
            
            # Evaluate rules in priority order
            applicable_rules = sorted(
                [rule for rule in self.rules.values() if rule.active],
                key=lambda r: r.priority
            )
            
            for rule in applicable_rules:
                if self._evaluate_rule_conditions(rule.conditions, action_context):
                    decision = PolicyDecision(
                        decision_id=f"decision_{datetime.now(timezone.utc).timestamp()}",
                        rule_id=rule.id,
                        action_type=action_type,
                        action_data=action,
                        decision=rule.action,
                        reason=f"Matched rule: {rule.name}",
                        risk_level=rule.risk_level,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        agent_id=action.get("agent_id", "unknown"),
                        estimated_cost=estimated_cost
                    )
                    
                    # Log decision
                    self._log_policy_decision(decision)
                    
                    # Check spending limits for financial actions
                    if action_type == ActionType.FINANCIAL_TRANSACTION:
                        if not self._check_spending_limits(estimated_cost):
                            logger.warning("Spending limit exceeded, requiring approval")
                            return True
                            
                    return rule.action == PolicyAction.REQUIRE_APPROVAL
                    
            # Default to require approval if no rules match
            logger.info("No matching rules found, defaulting to require approval")
            return True
            
        except Exception as e:
            logger.error(f"Error in approval check: {e}")
            return True  # Fail safe - require approval on error
            
    def _determine_action_type(self, action: Dict[str, Any]) -> ActionType:
        """Enhanced action type determination"""
        action_type_str = action.get("type", "").upper()
        
        # Direct mapping
        try:
            return ActionType(action_type_str.lower())
        except ValueError:
            pass
            
        # Keyword-based inference with improved logic
        action_str = str(action).lower()
        
        if any(keyword in action_str for keyword in ["payment", "transaction", "money", "cost", "expense"]):
            return ActionType.FINANCIAL_TRANSACTION
        elif any(keyword in action_str for keyword in ["api", "request", "call", "http"]):
            return ActionType.EXTERNAL_API_CALL
        elif any(keyword in action_str for keyword in ["email", "send", "message"]):
            return ActionType.EMAIL_SEND
        elif any(keyword in action_str for keyword in ["file", "create", "write", "save"]):
            return ActionType.FILE_CREATION
        elif any(keyword in action_str for keyword in ["system", "config", "modify"]):
            return ActionType.SYSTEM_MODIFICATION
        elif any(keyword in action_str for keyword in ["export", "download", "data"]):
            return ActionType.DATA_EXPORT
        elif any(keyword in action_str for keyword in ["legal", "filing", "document"]):
            return ActionType.LEGAL_FILING
        elif any(keyword in action_str for keyword in ["post", "publish", "social"]):
            return ActionType.EXTERNAL_POST
        elif any(keyword in action_str for keyword in ["marketing", "campaign", "advertisement"]):
            return ActionType.MARKETING_CAMPAIGN
        elif any(keyword in action_str for keyword in ["release", "deploy", "launch"]):
            return ActionType.PRODUCT_RELEASE
        else:
            return ActionType.SYSTEM_MODIFICATION  # Default
            
    def _evaluate_rule_conditions(self, conditions: List[Dict[str, Any]], context: Dict[str, Any]) -> bool:
        """Evaluate rule conditions against action context"""
        if not conditions:
            return True
            
        # All conditions must be true (AND logic)
        for condition in conditions:
            if not self._evaluate_single_condition(condition, context):
                return False
                
        return True
        
    def _evaluate_single_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single condition"""
        try:
            field = condition.get("field")
            operator = condition.get("operator")
            expected_value = condition.get("value")
            
            if field not in context:
                return False
                
            actual_value = context[field]
            
            # Type conversion for numeric comparisons
            if operator in [">", ">=", "<", "<="] and isinstance(expected_value, (int, float)):
                try:
                    actual_value = float(actual_value)
                except (ValueError, TypeError):
                    return False
                    
            # Evaluate condition
            if operator == "==":
                return actual_value == expected_value
            elif operator == "!=":
                return actual_value != expected_value
            elif operator == ">":
                return actual_value > expected_value
            elif operator == ">=":
                return actual_value >= expected_value
            elif operator == "<":
                return actual_value < expected_value
            elif operator == "<=":
                return actual_value <= expected_value
            elif operator == "in":
                return actual_value in expected_value
            elif operator == "not_in":
                return actual_value not in expected_value
            elif operator == "contains":
                return expected_value in str(actual_value)
            elif operator == "starts_with":
                return str(actual_value).startswith(str(expected_value))
            elif operator == "ends_with":
                return str(actual_value).endswith(str(expected_value))
            else:
                logger.warning(f"Unknown operator: {operator}")
                return False
                
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False
            
    def _check_spending_limits(self, amount: float) -> bool:
        """Check if spending amount is within limits"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            current_time = datetime.now(timezone.utc)
            
            for period in ["daily", "weekly", "monthly", "yearly"]:
                cursor.execute("""
                    SELECT limit_amount, current_spend, last_reset 
                    FROM spending_limits WHERE period = ?
                """, (period,))
                
                row = cursor.fetchone()
                if not row:
                    continue
                    
                limit_amount, current_spend, last_reset = row
                last_reset_time = datetime.fromisoformat(last_reset) if last_reset else current_time
                
                # Check if reset is needed
                reset_needed = False
                if period == "daily" and (current_time - last_reset_time).days >= 1:
                    reset_needed = True
                elif period == "weekly" and (current_time - last_reset_time).days >= 7:
                    reset_needed = True
                elif period == "monthly" and (current_time - last_reset_time).days >= 30:
                    reset_needed = True
                elif period == "yearly" and (current_time - last_reset_time).days >= 365:
                    reset_needed = True
                    
                if reset_needed:
                    current_spend = 0.0
                    cursor.execute("""
                        UPDATE spending_limits 
                        SET current_spend = 0.0, last_reset = ?
                        WHERE period = ?
                    """, (current_time.isoformat(), period))
                    
                # Check if new amount would exceed limit
                if current_spend + amount > limit_amount:
                    conn.close()
                    logger.warning(f"Spending limit exceeded for {period}: {current_spend + amount} > {limit_amount}")
                    return False
                    
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error checking spending limits: {e}")
            return False
            
    def record_spending(self, agent_id: str, action_type: str, amount: float, 
                       description: str = "", approved: bool = True, 
                       metadata: Dict[str, Any] = None) -> bool:
        """Record spending transaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Record spending
            spending_record = SpendingRecord(
                id=f"spend_{datetime.now(timezone.utc).timestamp()}",
                agent_id=agent_id,
                action_type=action_type,
                amount=amount,
                currency="USD",
                timestamp=datetime.now(timezone.utc).isoformat(),
                description=description,
                approved=approved,
                metadata=metadata or {}
            )
            
            cursor.execute("""
                INSERT INTO spending_records 
                (id, agent_id, action_type, amount, currency, timestamp, description, approved, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                spending_record.id, spending_record.agent_id, spending_record.action_type,
                spending_record.amount, spending_record.currency, spending_record.timestamp,
                spending_record.description, spending_record.approved, json.dumps(spending_record.metadata)
            ))
            
            # Update spending limits if approved
            if approved:
                for period in ["daily", "weekly", "monthly", "yearly"]:
                    cursor.execute("""
                        UPDATE spending_limits 
                        SET current_spend = current_spend + ?
                        WHERE period = ?
                    """, (amount, period))
                    
            conn.commit()
            conn.close()
            
            logger.info(f"Recorded spending: {amount} for {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to record spending: {e}")
            return False
            
    def _log_policy_decision(self, decision: PolicyDecision):
        """Log policy decision for audit trail"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO policy_decisions 
                (decision_id, rule_id, action_type, action_data, decision, reason, 
                 risk_level, timestamp, agent_id, estimated_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                decision.decision_id, decision.rule_id, decision.action_type.value,
                json.dumps(decision.action_data), decision.decision.value, decision.reason,
                decision.risk_level.value, decision.timestamp, decision.agent_id, decision.estimated_cost
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log policy decision: {e}")
            
    def get_spending_summary(self, period: str = "monthly") -> Dict[str, Any]:
        """Get spending summary for specified period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get spending limit info
            cursor.execute("""
                SELECT limit_amount, current_spend, last_reset 
                FROM spending_limits WHERE period = ?
            """, (period,))
            
            limit_row = cursor.fetchone()
            
            # Get recent spending records
            cursor.execute("""
                SELECT agent_id, SUM(amount) as total_amount, COUNT(*) as transaction_count
                FROM spending_records 
                WHERE approved = TRUE AND timestamp > datetime('now', '-30 days')
                GROUP BY agent_id
                ORDER BY total_amount DESC
            """)
            
            agent_spending = cursor.fetchall()
            
            conn.close()
            
            summary = {
                "period": period,
                "limit": limit_row[0] if limit_row else 0,
                "current_spend": limit_row[1] if limit_row else 0,
                "remaining": (limit_row[0] - limit_row[1]) if limit_row else 0,
                "last_reset": limit_row[2] if limit_row else None,
                "agent_breakdown": [
                    {"agent_id": row[0], "total_amount": row[1], "transaction_count": row[2]}
                    for row in agent_spending
                ]
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get spending summary: {e}")
            return {}
            
    def get_policy_audit_trail(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent policy decisions for audit"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM policy_decisions 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            audit_trail = []
            for row in rows:
                audit_trail.append({
                    "decision_id": row[0],
                    "rule_id": row[1],
                    "action_type": row[2],
                    "action_data": json.loads(row[3]) if row[3] else {},
                    "decision": row[4],
                    "reason": row[5],
                    "risk_level": row[6],
                    "timestamp": row[7],
                    "agent_id": row[8],
                    "estimated_cost": row[9]
                })
                
            return audit_trail
            
        except Exception as e:
            logger.error(f"Failed to get audit trail: {e}")
            return []

# Global enhanced policy engine instance
enhanced_policy_engine = EnhancedPolicyEngine()