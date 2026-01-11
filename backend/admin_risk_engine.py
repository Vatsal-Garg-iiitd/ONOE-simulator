"""
Administrative Risk Engine
Aggregates risk from all 8 administrative features.
"""
from pydantic import BaseModel
from typing import Dict, List, Any

# Import features
from admin_features.f1_resource_debate import resource_debate
from admin_features.f2_supply_chain import supply_chain_rag
from admin_features.f3_admin_precedent import admin_precedent
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
    def get_dashboard_data(self) -> AdminDashboardData:
        """
        Aggregate data for the Administrative Dashboard.
        """
        # Collect data from all features
        
        # F1
        f1_data = resource_debate.simulate_debate()
        f1 = AdminFeatureData(
            id="f1", name="Resource Demand Simulator", description="Multi-agent debate (EC vs State vs Manufacturer)",
            risk_contribution=f1_data["risk_contribution"], status=f1_data["status"], data=f1_data
        )
        
        # F2
        f2_risk = supply_chain_rag.get_risk_assessment()
        f2 = AdminFeatureData(
            id="f2", name="Supply Chain RAG", description="Retrieves EVM inventory + production data",
            risk_contribution=f2_risk["risk_score"], status=f2_risk["status"], data=f2_risk
        )
        
        # F3
        f3_data = admin_precedent.analyze_precedents()
        f3 = AdminFeatureData(
            id="f3", name="Historical Precedent", description="Analyzes 2019, 2020, 2022 elections",
            risk_contribution=f3_data["risk_score"], status=f3_data["status"], data=f3_data
        )
        
        # F4
        f4_data = logistics_sim.run_simulation()
        f4 = AdminFeatureData(
            id="f4", name="Monte Carlo Simulation", description="1,000 logistics scenarios with uncertainty",
            risk_contribution=f4_data["risk_score"], status=f4_data["status"], data=f4_data
        )
        
        # F5 (Base status)
        f5 = AdminFeatureData(
            id="f5", name="Bottleneck Explorer", description="Real-time what-if impact analysis",
            risk_contribution=12.0, status="Interactive", data={}
        )
        
        # F6
        f6_data = readiness_tracker.get_readiness_summary()
        f6 = AdminFeatureData(
            id="f6", name="Stakeholder Readiness Tracker", description="Live dashboard of 28 states + 50 agencies",
            risk_contribution=f6_data["risk_contribution"], status=f6_data["status"], data=f6_data
        )
        
        # F7
        f7_data = admin_timeline.assess_feasibility()
        f7 = AdminFeatureData(
            id="f7", name="Timeline Feasibility Checker", description="Verifies if 2029 deadline is achievable",
            risk_contribution=f7_data["risk_contribution"], status=f7_data["status"], data=f7_data
        )
        
        # F8
        f8_risk = execution_prioritizer.get_risk_contribution()
        f8 = AdminFeatureData(
            id="f8", name="Execution Prioritizer", description="Ranks bottlenecks by impact (EVM #1)",
            risk_contribution=f8_risk, status="Analysis Ready", 
            data={"priorities": execution_prioritizer.get_priorities()}
        )
        
        return AdminDashboardData(
            features=[f1, f2, f3, f4, f5, f6, f7, f8],
            bottleneck_sliders=bottleneck_explorer.get_sliders(),
            overall_status="At Risk"
        )

    def calculate_slider_impact(self, slider_values: Dict[str, float]) -> Dict:
        """
        Bridge to F5 logic
        """
        return bottleneck_explorer.calculate_impact(slider_values)

admin_risk_engine = AdminRiskEngine()
