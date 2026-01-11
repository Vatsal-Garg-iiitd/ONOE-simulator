"""
Administrative Risk Engine
Aggregates risk from all 8 administrative features.
"""
from pydantic import BaseModel
from typing import Dict, List, Any

# Import features
from admin_features.f1_resource_debate import resource_debate
from admin_features.f2_supply_chain import supply_chain_rag
# from admin_features.f3_admin_precedent import admin_precedent
from admin_features.f4_logistics_monte_carlo import logistics_sim
from admin_features.f5_bottleneck_explorer import bottleneck_explorer
from admin_features.f6_readiness_tracker import readiness_tracker
from admin_features.f7_admin_timeline import admin_timeline
from admin_features.f8_admin_prioritizer import execution_prioritizer

class AdminFeatureData(BaseModel):
    id: str
    name: str
    description: str
    risk_contribution: float
    status: str
    data: Dict[str, Any]

class AdminDashboardData(BaseModel):
    features: List[AdminFeatureData]
    bottleneck_sliders: List[Dict[str, Any]]
    overall_status: str

class AdminRiskEngine:
    def get_dashboard_data(self, inputs: Dict[str, Any] = None) -> AdminDashboardData:
        """
        Aggregate data for the Administrative Dashboard with dynamic inputs.
        """
        # Default inputs if none provided
        defaults = {
            "target_year": 2029,
            "evm_supply": 100,      # Percentage
            "security_personnel": 100 # Percentage
        }
        
        current_inputs = {**defaults, **(inputs or {})}
        
        # Collect data from all features
        
        # F1
        f1_data = resource_debate.simulate_debate()
        f1 = AdminFeatureData(
            id="f1", name="Resource Demand Simulator", description="Multi-agent debate (EC vs State vs Manufacturer)",
            risk_contribution=f1_data["risk_contribution"], status=f1_data["status"], data=f1_data
        )
        
        # F2
        f2_risk = supply_chain_rag.get_risk_assessment(current_inputs)
        f2 = AdminFeatureData(
            id="f2", name="Supply Chain RAG", description=f"Analyzes EVM inventory based on {current_inputs['evm_supply']}% supply",
            risk_contribution=f2_risk["risk_score"], status=f2_risk["status"], data=f2_risk
        )
        
        # F3 - Removed per user request
        
        # F4 - Dynamic
        f4_data = logistics_sim.run_simulation(current_inputs)
        f4 = AdminFeatureData(
            id="f4", name="Monte Carlo Simulation", description=f"1,000 scenarios with {current_inputs['evm_supply']}% EVM supply",
            risk_contribution=f4_data["risk_score"], status=f4_data["status"], data=f4_data
        )
        
        # F5 - Dynamic Bottleneck Analysis
        # Run actual bottleneck analysis to get real risk contribution
        f5_analysis = self.analyze_bottlenecks(current_inputs)
        print(f"F5 BOTTLENECK ANALYSIS: {len(f5_analysis.get('bottlenecks', []))} bottlenecks found")
        print(f"F5 RISK CONTRIBUTION: {f5_analysis.get('risk_contribution', 0)}")
        f5 = AdminFeatureData(
            id="f5", 
            name="Bottleneck Explorer", 
            description=f"Intelligent bottleneck detection ({f5_analysis.get('analysis_mode', 'Unknown')})",
            risk_contribution=f5_analysis.get("risk_contribution", 0), 
            status=f5_analysis.get("status", "Interactive"), 
            data=f5_analysis
        )
        
        # F6 - Fixed Overlap (Removed timeline prediction)
        f6_data = readiness_tracker.get_readiness_summary(current_inputs)
        f6 = AdminFeatureData(
            id="f6", name="Stakeholder Readiness Tracker", description="Consensus data from 28 states + 50 agencies",
            risk_contribution=f6_data["risk_contribution"], status=f6_data["status"], data=f6_data
        )
        
        # F7 - Dynamic
        f7_data = admin_timeline.assess_feasibility(
            target_year=current_inputs["target_year"],
            evm_supply_percent=current_inputs["evm_supply"]
        )
        f7 = AdminFeatureData(
            id="f7", name="Timeline Feasibility Checker", description=f"Verifies if {current_inputs['target_year']} deadline is achievable",
            risk_contribution=f7_data["risk_contribution"], status=f7_data["status"], data=f7_data
        )
        
        # F8 - Removed per user request
        
        return AdminDashboardData(
            features=[f1, f2, f4, f5, f6, f7],
            bottleneck_sliders=[],  # No longer used - bottlenecks in F5 data
            overall_status="At Risk"
        )

    def calculate_slider_impact(self, slider_values: Dict[str, float], context: Dict[str, Any] = None) -> Dict:
        """
        Bridge to F5 logic
        """
        return bottleneck_explorer.calculate_impact(slider_values, context)
    
    def analyze_bottlenecks(self, inputs: Dict[str, Any]) -> Dict:
        """
        Analyze bottlenecks using intelligent LLM-based detection.
        """
        # Gather context from other features
        f2_data = supply_chain_rag.get_risk_assessment(inputs)
        f6_data = readiness_tracker.get_readiness_summary(inputs)
        f7_data = admin_timeline.assess_feasibility(
            target_year=inputs.get("target_year", 2029),
            evm_supply_percent=inputs.get("evm_supply", 100)
        )
        
        context = {
            "target_year": inputs.get("target_year", 2029),
            "evm_deficit": abs(f2_data["evm_inventory"]["deficit"]),
            "ready_states": f6_data["ready_count"],
            "total_states": f6_data["total_agencies"],
            "timeline_status": f7_data["status"],
            "months_remaining": f7_data["months_remaining"],
            "months_needed": f7_data["months_needed"]
        }
        
        # Use bottleneck explorer to analyze
        result = bottleneck_explorer.analyze_bottlenecks(context)
        return result

admin_risk_engine = AdminRiskEngine()
