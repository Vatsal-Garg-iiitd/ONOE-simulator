"""
Feature 5: Bottleneck Explorer
Real-time what-if impact analysis with sliders.
"""
from typing import List, Dict

class BottleneckExplorer:
    def __init__(self):
        self.sliders = [
            {
                "id": "evm_delay",
                "label": "EVM Production Delay",
                "min": -12,
                "max": 0,
                "defaultValue": -6,
                "unit": "months",
                "impact_per_unit": -2.0  # Risk increases as delay (negative months) increases magnitude
            },
            {
                "id": "state_coop",
                "label": "State Cooperation",
                "min": 0,
                "max": 100,
                "defaultValue": 85,
                "unit": "%",
                "impact_per_unit": -0.1 # Risk decreases as cooperation increases
            },
            {
                "id": "budget",
                "label": "Budget Availability",
                "min": 0,
                "max": 100,
                "defaultValue": 80,
                "unit": "%",
                "impact_per_unit": -0.05
            }
        ]

    def get_sliders(self) -> List[Dict]:
        """
        Get available sliders for the frontend.
        """
        return self.sliders

    def calculate_impact(self, slider_values: Dict[str, float]) -> Dict:
        """
        Calculate risk impact based on slider values.
        """
        base_risk = 68.0
        impact = 0.0
        
        # Logic for EVM delay (negative value, e.g. -6)
        # More negative = higher risk
        evm_ks = slider_values.get("evm_delay", -6)
        impact += abs(evm_ks) * 2.3 # Approx +14% for -6
        
        # Logic for State Cooperation
        # Lower cooperation = higher risk
        coop = slider_values.get("state_coop", 85)
        impact += (100 - coop) * 0.4 # Approx +7% for 85 (15 gap)
        
        # Logic for Budget
        budget = slider_values.get("budget", 80)
        impact += (100 - budget) * 0.15 # Approx +3% for 80 (20 gap)
        
        new_risk = min(100, base_risk + impact)
        
        return {
            "current_risk": base_risk,
            "new_risk": round(new_risk, 1),
            "increase": round(new_risk - base_risk, 1)
        }

bottleneck_explorer = BottleneckExplorer()
