"""
Feature 6: Political Support Tracker
Tracks parliamentary support for constitutional amendments
"""
from typing import Dict

class PoliticalTracker:
    def __init__(self):
        # Current political landscape (as of 2026)
        self.current_support = 65.0  # Current parliamentary support percentage
        self.required_support = 67.0  # Required 2/3 majority for constitutional amendment
        self.rajya_sabha_support = 62.0  # Upper house support
    
    def get_current_support(self) -> Dict:
        """Get current political support metrics"""
        return {
            "current_support": self.current_support,
            "required_support": self.required_support,
            "rajya_sabha_support": self.rajya_sabha_support,
            "lok_sabha_gap": self.required_support - self.current_support,
            "rajya_sabha_gap": self.required_support - self.rajya_sabha_support
        }
    
    def calculate_political_risk(self, article_number: int = None) -> float:
        """
        Calculate risk contribution from political support deficit
        Formula: (1 - support_percentage) * weight
        
        Only applies to critical articles requiring amendment
        """
        # Political risk only applies to Article 356 (most contentious)
        if article_number == 356:
            support_ratio = self.current_support / 100.0
            risk = (1 - support_ratio) * 25.0
            return round(risk, 2)
        
        return 0.0
    
    def get_support_details(self) -> Dict:
        """Get detailed political support analysis"""
        return {
            "current_support": self.current_support,
            "required_support": self.required_support,
            "risk_contribution": self.calculate_political_risk(356),
            "status": "INSUFFICIENT" if self.current_support < self.required_support else "SUFFICIENT",
            "gap_percentage": max(0, self.required_support - self.current_support),
            "analysis": f"Current support ({self.current_support}%) falls short of required 2/3 majority ({self.required_support}%). This creates political uncertainty for Article 356 amendments."
        }

# Singleton instance
political_tracker = PoliticalTracker()
