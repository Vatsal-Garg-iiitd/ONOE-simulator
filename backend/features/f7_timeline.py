"""
Feature 7: Timeline Feasibility Analysis
Assesses whether amendments can be completed by target dates
"""
from typing import Dict
from datetime import datetime

class TimelineAnalyzer:
    def __init__(self):
        # Current date: January 2026
        self.current_year = 2026
        self.current_month = 1
        
        # Amendment complexity (months needed)
        self.amendment_timelines = {
            82: 8,   # Simple amendment
            83: 12,  # Complex - requires co-terminus provision
            85: 6,   # Moderate amendment
            172: 15, # Very complex - requires state ratification
            174: 6,  # Moderate amendment
            356: 12  # Complex - requires procedure definition
        }
        
        # Target years for implementation
        self.target_years = {
            82: 2031,  # Before Maharashtra Assembly expires
            83: 2027,  # Before UP Assembly expires
            85: 2029,  # Before next LS election
            172: 2027, # Before earliest state expiry
            174: 2029, # Before next LS election
            356: 2027  # CRITICAL - needs to be ready before first ONOE
        }
    
    def assess_feasibility(self, article_number: int) -> Dict:
        """
        Assess whether amendment can be completed by target year
        Returns feasibility status and risk impact
        """
        months_needed = self.amendment_timelines.get(article_number, 12)
        target_year = self.target_years.get(article_number, 2029)
        
        # Calculate months available
        months_available = (target_year - self.current_year) * 12 - self.current_month
        
        feasible = months_available >= months_needed
        
        # Risk impact calculation
        if feasible:
            risk_impact = 0.0  # No additional risk if feasible
        else:
            # If not feasible, add risk proportional to shortfall
            shortfall_months = months_needed - months_available
            risk_impact = min(shortfall_months * 2, 10.0)
        
        return {
            "months_needed": months_needed,
            "months_available": months_available,
            "target_year": target_year,
            "feasible": feasible,
            "risk_impact": risk_impact,
            "status": "FEASIBLE" if feasible else "NOT FEASIBLE",
            "analysis": self._generate_analysis(article_number, feasible, months_needed, months_available)
        }
    
    def _generate_analysis(self, article_number: int, feasible: bool, months_needed: int, months_available: int) -> str:
        """Generate human-readable analysis"""
        if feasible:
            buffer = months_available - months_needed
            return f"Amendment can be completed with {buffer} months buffer before target deadline."
        else:
            shortfall = months_needed - months_available
            return f"TIMELINE RISK: Amendment requires {months_needed} months but only {months_available} months available. Shortfall of {shortfall} months."

# Singleton instance
timeline_analyzer = TimelineAnalyzer()
