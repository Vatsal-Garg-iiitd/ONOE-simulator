"""
API Routes for Administrative Engine
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from admin_risk_engine import admin_risk_engine, AdminDashboardData

router = APIRouter(prefix="/api/admin", tags=["admin"])

class BottleneckRequest(BaseModel):
    sliders: Dict[str, float]
    context: Dict[str, Any] = None

class DashboardInput(BaseModel):
    target_year: int = 2029
    evm_supply: float = 100.0
    security_personnel: float = 100.0

@router.get("/dashboard", response_model=AdminDashboardData)
async def get_dashboard():
    """
    Get initial dashboard data (defaults).
    """
    try:
        data = admin_risk_engine.get_dashboard_data()
        return data
    except Exception as e:
        print(f"Error getting admin dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dashboard", response_model=AdminDashboardData)
async def update_dashboard(inputs: DashboardInput):
    """
    Get dashboard data with custom inputs.
    """
    try:
        data = admin_risk_engine.get_dashboard_data(inputs.dict())
        return data
    except Exception as e:
        print(f"Error updating admin dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bottleneck/analyze")
async def analyze_bottlenecks(inputs: DashboardInput):
    """
    Intelligently analyze bottlenecks using LLM based on current administrative context.
    """
    try:
        result = admin_risk_engine.analyze_bottlenecks(inputs.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

