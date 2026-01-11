"""
Feature 2: Supply Chain RAG
Retrieves EVM inventory and production data.
"""
from typing import List, Dict

class SupplyChainRAG:
    def __init__(self):
        # Mock database of retrieved documents
        self.documents = [
            {
                "source": "BEL Annual Report 2024",
                "content": "Current EVM production capacity is 5 lakh units per annum. Expansion requires ₹500Cr investment.",
                "year": 2024
            },
            {
                "source": "ECI Logistics Manual",
                "content": "VVPAT machines have a higher failure rate (2%) compared to Control Units (0.5%), requiring 125% buffer stock.",
                "year": 2023
            },
             {
                "source": "Parliamentary Committee Report",
                "content": "Semiconductor shortage affects production timelines for VVPATs. Lead time increased to 18 months.",
                "year": 2025
            }
        ]

    def query_supply_chain(self, query: str = "EVM capacity") -> List[Dict]:
        """
        Simulate RAG retrieval for supply chain queries.
        """
        # In a real system, this would use vector search.
        # Here we return all relevant docs for the demo.
        return self.documents

    def get_risk_assessment(self, inputs: Dict = None) -> Dict:
        """
        Calculate risk based on retrieved evidence and dynamic inputs.
        """
        # Default scenario
        evm_supply_percent = 100.0
        target_year = 2029
        current_year = 2026
        
        if inputs:
            evm_supply_percent = float(inputs.get("evm_supply", 100.0))
            target_year = int(inputs.get("target_year", 2029))
            
        # 1. Calculate Current Stock
        # Base stock is 1.2M, scaled by supply % input (representing current readiness)
        base_stock = 1200000
        current_stock = int(base_stock * (evm_supply_percent / 100.0))
        
        # 2. Calculate Projected Production
        # Approx 5 lakh units/year capacity
        base_annual_capacity = 500000 
        years_remaining = max(0, target_year - current_year)
        
        # Production is also affected by supply chain health (evm_supply_percent)
        # If supply chain is 50%, production runs at 50% capacity
        annual_production_rate = int(base_annual_capacity * (evm_supply_percent / 100.0))
        projected_production = annual_production_rate * years_remaining
        
        # 3. Total Availability vs Requirement
        total_available = current_stock + projected_production
        required_stock = 2500000 # 2.5 million units needed total
        deficit = required_stock - total_available
        
        # 4. Risk Calculation
        # Risk is proportional to the deficit percentage
        if total_available >= required_stock:
            risk_score = 5.0 # Low risk
            deficit = 0 # No deficit
        else:
            deficit_percent = (deficit / required_stock) * 100
            risk_score = 20.0 + (deficit_percent * 0.8) # Base 20 + penalty
            
        risk_score = min(95.0, risk_score)
             
        status = "CRITICAL" if risk_score > 60 else ("HIGH" if risk_score > 40 else "MODERATE")
        
        return {
            "risk_score": round(risk_score, 1),
            "status": status,
            "evidence_count": len(self.documents),
            "key_finding": f"Projected EVM deficit of {deficit:,} units by {target_year}.",
            "evm_inventory": {
                "current_stock": current_stock,
                "projected_production": projected_production,
                "total_available": total_available,
                "required_stock": required_stock,
                "deficit": deficit,
                "annual_rate": annual_production_rate,
                "years_remaining": years_remaining
            },
             "explanation": f"By {target_year}, total available EVMs will be {total_available/100000:.1f} Lakhs against requirement of {required_stock/100000:.1f} Lakhs. (Annual Rate: {annual_production_rate:,})"
        }

supply_chain_rag = SupplyChainRAG()
