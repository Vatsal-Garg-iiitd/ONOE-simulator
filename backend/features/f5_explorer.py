"""
Feature 5: Real-time Explorer
Interactive toggles that allow users to explore "what-if" scenarios
"""
from typing import List, Dict

class ExplorerSystem:
    def __init__(self):
        # Define toggles for each article
        self.toggles_db = {
            82: [
                {
                    "toggle_id": "census_sync",
                    "question": "Is census synchronization mechanism implemented?",
                    "current_state": False,
                    "impact_if_true": -35.0,
                    "impact_if_false": 5.0,
                    "description": "If census readjustment is synchronized with ONOE cycle, risk decreases significantly"
                }
            ],
            83: [
                {
                    "toggle_id": "co_terminus",
                    "question": "Is co-terminus provision implemented?",
                    "current_state": False,
                    "impact_if_true": -40.0,
                    "impact_if_false": 10.0,
                    "description": "Co-terminus provision ensures Lok Sabha and State Assemblies expire together"
                }
            ],
            85: [
                {
                    "toggle_id": "simultaneous_dissolution",
                    "question": "Is simultaneous dissolution protocol defined?",
                    "current_state": False,
                    "impact_if_true": -30.0,
                    "impact_if_false": 7.0,
                    "description": "Protocol for dissolving both Lok Sabha and State Assemblies simultaneously"
                }
            ],
            172: [
                {
                    "toggle_id": "state_sync",
                    "question": "Is state assembly synchronization completed?",
                    "current_state": False,
                    "impact_if_true": -40.0,
                    "impact_if_false": 12.0,
                    "description": "All 28 state assemblies synchronized to common expiry date"
                }
            ],
            174: [
                {
                    "toggle_id": "governor_restriction",
                    "question": "Are Governor's dissolution powers restricted during ONOE?",
                    "current_state": False,
                    "impact_if_true": -35.0,
                    "impact_if_false": 9.0,
                    "description": "Constitutional safeguard preventing arbitrary dissolution by Governors"
                }
            ],
            356: [
                {
                    "toggle_id": "presidents_rule_procedure",
                    "question": "Is Article 356 procedure for ONOE elections defined?",
                    "current_state": False,
                    "impact_if_true": -60.0,
                    "impact_if_false": 5.0,
                    "description": "CRITICAL: Constitutional procedure for conducting elections in states under President's Rule during ONOE"
                }
            ]
        }
    
    def get_toggles(self, article_number: int) -> List[Dict]:
        """Get all toggles for an article"""
        return self.toggles_db.get(article_number, [])
    
    def apply_toggle(self, article_number: int, toggle_id: str, new_state: bool) -> float:
        """
        Apply a toggle and return the risk impact
        Returns the impact value based on the new state
        """
        toggles = self.get_toggles(article_number)
        
        for toggle in toggles:
            if toggle["toggle_id"] == toggle_id:
                toggle["current_state"] = new_state
                return toggle["impact_if_true"] if new_state else toggle["impact_if_false"]
        
        return 0.0
    
    def get_current_impact(self, article_number: int) -> float:
        """
        Calculate current total impact from all toggles for an article
        """
        toggles = self.get_toggles(article_number)
        total_impact = 0.0
        
        for toggle in toggles:
            if toggle["current_state"]:
                total_impact += toggle["impact_if_true"]
            else:
                total_impact += toggle["impact_if_false"]
        
        return total_impact

# Singleton instance
explorer_system = ExplorerSystem()
