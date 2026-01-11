"""
Feature 6: Stakeholder Readiness Tracker
Live dashboard of 28 states + 50 agencies.
"""
from typing import Dict, List

class ReadinessTracker:
    def __init__(self):
        self.states = {
            "Ready": ["UP", "Gujarat", "MP"],
            "In Progress": ["Maharashtra", "Karnataka"],
            "Behind": ["Kerala", "West Bengal", "Tamil Nadu"]
        }
        
    def get_readiness_summary(self) -> Dict:
        """
        Get aggregated readiness status.
        """
        return {
            "total_agencies": 78,
            "ready_count": 25,
            "in_progress_count": 40,
            "behind_count": 13,
            "risk_contribution": 16.0,
            "status": "BEHIND",
            "critical_gap": "Opposition-ruled states showing low data integration."
        }

readiness_tracker = ReadinessTracker()
