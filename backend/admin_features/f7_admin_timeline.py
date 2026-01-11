"""
Feature 7: Timeline Feasibility Checker
Verifies if 2029 deadline is achievable.
"""
from typing import Dict

class AdminTimelineAnalyzer:
    def assess_feasibility(self, target_year: int = 2029, evm_supply_percent: float = 100.0) -> Dict:
        """
        Assess logistical timeline for user-defined target year.
        Assumes current year is roughly 2024/2025.
        
        Args:
            target_year: The election target year.
            evm_supply_percent: Percentage of required EVMs available (affects manufacturing time).
        """
        current_year = 2025 # Hardcoded anchor for demo logic
        years_remaining = target_year - current_year
        months_available = years_remaining * 12
        
        # Base requirements
        base_manufacturing = 18.0
        
        # DYNAMIC LOGIC: If supply is 50%, manufacturing takes 2x time (roughly)
        # Formula: new_time = base * (1 + (100 - supply)/50)  <-- Aggressive penalty
        if evm_supply_percent < 100:
            deficit_factor = (100 - evm_supply_percent) / 50.0 # e.g., 50% supply -> 1.0 factor
            manufacturing_months = base_manufacturing * (1 + deficit_factor)
        else:
            manufacturing_months = base_manufacturing
            
        manufacturing_months = round(manufacturing_months, 1)

        base_calibration = 12
        base_logistics = 6
        base_buffer = 6
        
        months_needed = manufacturing_months + base_calibration + base_logistics + base_buffer
        
        diff = months_available - months_needed
        
        if diff >= 0:
            status = "FEASIBLE"
            risk = 5.0
            bottleneck = "Timeline is sufficient."
        elif diff >= -6:
            status = "RISKY"
            risk = 45.0
            bottleneck = f"Tight deadline. Short by {abs(round(diff, 1))} months."
        else:
            status = "CRITICAL"
            risk = 95.0
            bottleneck = f"Impossible deadline. Short by {abs(round(diff, 1))} months."
            
        return {
            "deadline": f"May {target_year}",
            "months_remaining": max(0, months_available),
            "months_needed": round(months_needed, 1),
            "calculation_breakdown": [
                {"phase": "EVM Manufacturing", "months": manufacturing_months, "desc": f"Semiconductor procurement (Supply: {evm_supply_percent}%)"},
                {"phase": "VVPAT Calibration", "months": base_calibration, "desc": "Hardware testing & sync"},
                {"phase": "Logistics & Transport", "months": base_logistics, "desc": "Deployment to 10L+ booths"},
                {"phase": "Buffer & Training", "months": base_buffer, "desc": "Staff training & contingency"}
            ],
            "risk_contribution": risk,
            "status": status,
            "bottleneck": bottleneck,
            "explanation": f"Target {target_year} provides {months_available} months against {round(months_needed, 1)} needed."
        }

admin_timeline = AdminTimelineAnalyzer()
