"""
API Routes for Administrative Engine
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from admin_risk_engine import admin_risk_engine, AdminDashboardData

router = APIRouter(prefix="/api/admin", tags=["admin"])

class SliderUpdate(BaseModel):
    sliders: Dict[str, float]

@router.get("/dashboard", response_model=AdminDashboardData)
async def get_dashboard():
    """
    Get all data for the Administrative Engine Dashboard.
    """
    try:
        data = admin_risk_engine.get_dashboard_data()
        return data
    except Exception as e:
        print(f"Error getting admin dashboard: {e}")
        # Return mock data if something fails
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/impact")
async def calculate_impact(request: SliderUpdate):
    """
    Calculate risk impact based on slider values (Bottleneck Explorer).
    """
    try:
        result = admin_risk_engine.calculate_slider_impact(request.sliders)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
