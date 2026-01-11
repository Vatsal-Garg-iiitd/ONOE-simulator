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
        
    def get_readiness_summary(self, inputs: Dict = None) -> Dict:
        """
        Get aggregated readiness status with dynamic security inputs.
        """
        security_percent = 100
        if inputs:
            security_percent = inputs.get("security_personnel", 100)
        
        # Base counts
        ready = 25
        in_progress = 40
        behind = 13
        
        # Simulate impact: Low security force availability reduces "Ready" states, moves them to "In Progress"
        if security_percent < 100:
             shift = int(10 * ((100 - security_percent) / 100)) # e.g. 50% supply -> shift 5 units
             ready = max(0, ready - shift)
             in_progress += shift
             
        risk_contribution = 16.0 + ((100 - security_percent) * 0.3)
        
        return {
            "total_agencies": 78,
            "ready_count": ready,
            "in_progress_count": in_progress,
            "behind_count": behind,
            "risk_contribution": round(risk_contribution, 1),
            "status": "BEHIND" if behind > 10 else "IN PROGRESS",
            "critical_gap": f"Lack of consensus from {behind} opposition-ruled states.",
            "explanation": f"Security personnel shortage ({100-security_percent}%) delays state deployment readiness."
        }

readiness_tracker = ReadinessTracker()
