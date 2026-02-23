"""
Enhanced Cost Tracker with correct parameter names
Fixes CostEntry parameter mismatch issues
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CostEntry:
    """Cost entry with correct parameter names"""
    agent_id: str
    action_type: str  # Changed from 'action' to 'action_type'
    amount: float
    timestamp: str
    currency: str = "USD"
    description: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class EnhancedCostTracker:
    """Enhanced cost tracker with better functionality"""
    
    def __init__(self):
        self.cost_entries: List[CostEntry] = []
        self.agent_totals: Dict[str, float] = {}
        self.action_totals: Dict[str, float] = {}
        self.daily_totals: Dict[str, float] = {}
        
    def add_cost(self, entry: CostEntry) -> bool:
        """Add a cost entry"""
        try:
            self.cost_entries.append(entry)
            
            # Update agent totals
            if entry.agent_id not in self.agent_totals:
                self.agent_totals[entry.agent_id] = 0.0
            self.agent_totals[entry.agent_id] += entry.amount
            
            # Update action totals
            if entry.action_type not in self.action_totals:
                self.action_totals[entry.action_type] = 0.0
            self.action_totals[entry.action_type] += entry.amount
            
            # Update daily totals
            date_key = entry.timestamp[:10]  # YYYY-MM-DD
            if date_key not in self.daily_totals:
                self.daily_totals[date_key] = 0.0
            self.daily_totals[date_key] += entry.amount
            
            logger.info(f"Added cost entry: {entry.agent_id} - {entry.action_type} - ${entry.amount}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add cost entry: {e}")
            return False
            
    def get_total_cost(self) -> float:
        """Get total cost across all entries"""
        return sum(entry.amount for entry in self.cost_entries)
        
    def get_agent_costs(self, agent_id: str) -> List[CostEntry]:
        """Get all cost entries for a specific agent"""
        return [entry for entry in self.cost_entries if entry.agent_id == agent_id]
        
    def get_agent_total(self, agent_id: str) -> float:
        """Get total cost for a specific agent"""
        return self.agent_totals.get(agent_id, 0.0)
        
    def get_action_costs(self, action_type: str) -> List[CostEntry]:
        """Get all cost entries for a specific action type"""
        return [entry for entry in self.cost_entries if entry.action_type == action_type]
        
    def get_action_total(self, action_type: str) -> float:
        """Get total cost for a specific action type"""
        return self.action_totals.get(action_type, 0.0)
        
    def get_daily_total(self, date: str) -> float:
        """Get total cost for a specific date (YYYY-MM-DD)"""
        return self.daily_totals.get(date, 0.0)
        
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary"""
        return {
            "total_cost": self.get_total_cost(),
            "total_entries": len(self.cost_entries),
            "agent_totals": self.agent_totals.copy(),
            "action_totals": self.action_totals.copy(),
            "daily_totals": self.daily_totals.copy(),
            "average_cost_per_entry": self.get_total_cost() / len(self.cost_entries) if self.cost_entries else 0.0,
            "most_expensive_agent": max(self.agent_totals.items(), key=lambda x: x[1]) if self.agent_totals else None,
            "most_expensive_action": max(self.action_totals.items(), key=lambda x: x[1]) if self.action_totals else None
        }
        
    def export_to_json(self, filename: str) -> bool:
        """Export cost data to JSON file"""
        try:
            data = {
                "cost_entries": [
                    {
                        "agent_id": entry.agent_id,
                        "action_type": entry.action_type,
                        "amount": entry.amount,
                        "timestamp": entry.timestamp,
                        "currency": entry.currency,
                        "description": entry.description,
                        "metadata": entry.metadata
                    }
                    for entry in self.cost_entries
                ],
                "summary": self.get_cost_summary(),
                "exported_at": datetime.now(timezone.utc).isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Cost data exported to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export cost data: {e}")
            return False
            
    def clear_costs(self) -> bool:
        """Clear all cost data"""
        try:
            self.cost_entries.clear()
            self.agent_totals.clear()
            self.action_totals.clear()
            self.daily_totals.clear()
            
            logger.info("All cost data cleared")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear cost data: {e}")
            return False

# Global enhanced cost tracker instance
enhanced_cost_tracker = EnhancedCostTracker()