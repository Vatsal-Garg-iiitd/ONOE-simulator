"""
Feature 3: Precedent Analysis
Analyzes relevant Supreme Court cases
"""
import json
from typing import List, Dict
from pathlib import Path

class PrecedentAnalyzer:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.precedents_data = None
        self.load_precedents()
    
    def load_precedents(self):
        """Load Supreme Court precedents database"""
        try:
            with open(self.data_dir / "precedents.json", "r") as f:
                self.precedents_data = json.load(f)
        except Exception as e:
            print(f"Error loading precedents: {e}")
            self.precedents_data = {"cases": []}
    
    def find_relevant_precedents(self, article_number: int) -> List[Dict]:
        """
        Find Supreme Court cases relevant to the article
        Returns list of precedent cases with impact scores
        """
        relevant_cases = []
        
        for case in self.precedents_data.get("cases", []):
            if article_number in case.get("relevant_articles", []):
                relevant_cases.append({
                    "case_name": case["case_name"],
                    "year": case["year"],
                    "impact_score": case["impact_score"],
                    "relevance": case["relevance"],
                    "summary": case.get("summary", "")
                })
        
        # Sort by impact score (highest first)
        relevant_cases.sort(key=lambda x: x["impact_score"], reverse=True)
        
        return relevant_cases
    
    def calculate_precedent_risk(self, article_number: int) -> float:
        """
        Calculate risk contribution from precedents
        Higher impact scores = higher risk of constitutional challenge
        """
        precedents = self.find_relevant_precedents(article_number)
        
        if not precedents:
            return 0.0
        
        # Sum impact scores (each case adds risk)
        total_impact = sum(case["impact_score"] for case in precedents)
        
        # Special weighting for Article 356 (critical)
        if article_number == 356:
            # Article 356 has 3 major precedents, each worth 5 points
            return min(total_impact, 15.0)
        elif article_number in [83, 172]:
            # Articles 83 and 172 have federalism concerns
            return min(total_impact, 6.0)
        else:
            return min(total_impact, 3.0)

# Singleton instance
precedent_analyzer = PrecedentAnalyzer()
