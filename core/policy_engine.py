"""
Policy Engine for Dream Machine
Handles approval workflows, spending limits, and governance rules
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class PolicyAction(Enum):
    AUTO_APPROVE = "auto_approve"
    REQUIRE_APPROVAL = "require_approval"
    BLOCK = "block"
    LOG_ONLY = "log_only"

@dataclass
class PolicyRule:
    condition: str  # Simple condition like "cost < 100"
    action: str  # Use string instead of enum for easier serialization
    priority: int
    description: Optional[str] = None

@dataclass
class Policy:
    name: str
    description: str
    rules: List[PolicyRule]
    enabled: bool = True

class PolicyEngine:
    def __init__(self):
        self.policies: Dict[str, Policy] = {}
        self._setup_default_policies()
        
    def _setup_default_policies(self):
        """Setup default policies for the Dream Machine"""
        
        # Cost-based approval policy
        cost_policy = Policy(
            name="cost_approval",
            description="Automatic approval for low-cost actions",
            rules=[
                PolicyRule(
                    condition="cost < 10",
                    action="auto_approve",
                    priority=1,
                    description="Auto-approve actions under $10"
                ),
                PolicyRule(
                    condition="cost >= 10 and cost < 100",
                    action="require_approval",
                    priority=2,
                    description="Require approval for $10-$100"
                ),
                PolicyRule(
                    condition="cost >= 100",
                    action="require_approval",
                    priority=3,
                    description="Require approval for $100+"
                )
            ]
        )
        
        # Security policy
        security_policy = Policy(
            name="security",
            description="Security and compliance rules",
            rules=[
                PolicyRule(
                    condition="action_type == 'external_post'",
                    action="require_approval",
                    priority=1,
                    description="Require approval for external posts"
                ),
                PolicyRule(
                    condition="action_type == 'legal_filing'",
                    action="require_approval",
                    priority=1,
                    description="Require approval for legal filings"
                )
            ]
        )
        
        self.add_policy(cost_policy)
        self.add_policy(security_policy)
        
    def add_policy(self, policy: Policy):
        """Add a new policy"""
        self.policies[policy.name] = policy
        logger.info(f"Added policy: {policy.name}")
        
    def remove_policy(self, policy_name: str):
        """Remove a policy"""
        if policy_name in self.policies:
            del self.policies[policy_name]
            logger.info(f"Removed policy: {policy_name}")
            
    def evaluate(self, action_type: str, context: Dict[str, Any]) -> PolicyAction:
        """Evaluate an action against all policies"""
        
        # Add action_type to context for evaluation
        eval_context = {**context, "action_type": action_type}
        
        # Collect all applicable rules
        applicable_rules = []
        
        for policy in self.policies.values():
            if not policy.enabled:
                continue
                
            for rule in policy.rules:
                if self._evaluate_condition(rule.condition, eval_context):
                    applicable_rules.append(rule)
        
        # Sort by priority (higher priority first)
        applicable_rules.sort(key=lambda r: r.priority, reverse=True)
        
        # Return the action of the highest priority rule
        if applicable_rules:
            action_str = applicable_rules[0].action
            # Convert string back to enum
            if action_str == "auto_approve":
                return PolicyAction.AUTO_APPROVE
            elif action_str == "require_approval":
                return PolicyAction.REQUIRE_APPROVAL
            elif action_str == "block":
                return PolicyAction.BLOCK
            elif action_str == "log_only":
                return PolicyAction.LOG_ONLY
        
        # Default to require approval if no rules match
        return PolicyAction.REQUIRE_APPROVAL
        
    def requires_approval(self, action: Dict[str, Any], estimated_cost: float = 0) -> bool:
        """Check if an action requires approval"""
        action_type = action.get("type", "unknown")
        context = {
            "cost": estimated_cost,
            **action
        }
        
        result = self.evaluate(action_type, context)
        return result == PolicyAction.REQUIRE_APPROVAL
        
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a simple condition string"""
        try:
            # Create a safe evaluation environment with context variables
            safe_dict = {
                '__builtins__': {},
                **context
            }
            
            # Evaluate the condition safely
            result = eval(condition, safe_dict)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False
            
    def get_policy_summary(self) -> Dict[str, Any]:
        """Get summary of all policies"""
        return {
            "total_policies": len(self.policies),
            "enabled_policies": len([p for p in self.policies.values() if p.enabled]),
            "policies": {
                name: {
                    "description": policy.description,
                    "enabled": policy.enabled,
                    "rule_count": len(policy.rules)
                }
                for name, policy in self.policies.items()
            }
        }