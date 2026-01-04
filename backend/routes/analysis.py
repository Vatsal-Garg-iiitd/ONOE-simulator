"""
API Routes for Overall Analysis
"""
from fastapi import APIRouter
from models import OverallAnalysis
from routes.articles import get_all_articles

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.get("/overall", response_model=OverallAnalysis)
async def get_overall_analysis():
    """Get overall ONOE feasibility analysis"""
    articles = get_all_articles()
    
    # Calculate metrics
    total_articles = len(articles)
    critical_blockers = sum(1 for a in articles if a.status == "CRITICAL BLOCKER")
    average_risk = sum(a.final_risk for a in articles) / total_articles
    
    # Determine feasibility
    if critical_blockers > 0:
        feasibility = "NOT FEASIBLE - Critical blockers present"
    elif average_risk > 60:
        feasibility = "HIGH RISK - Significant constitutional challenges"
    elif average_risk > 40:
        feasibility = "MODERATE RISK - Requires substantial amendments"
    else:
        feasibility = "FEASIBLE - With proper amendments"
    
    # Generate key recommendations
    recommendations = []
    sorted_articles = sorted(articles, key=lambda x: x.priority_rank)
    
    for article in sorted_articles[:3]:  # Top 3 priorities
        recommendations.append(
            f"Priority {article.priority_rank}: {article.recommendation}"
        )
    
    return OverallAnalysis(
        total_articles=total_articles,
        critical_blockers=critical_blockers,
        average_risk=round(average_risk, 2),
        onoe_feasibility=feasibility,
        key_recommendations=recommendations,
        articles=articles
    )

@router.get("/priorities")
async def get_priorities():
    """Get ranked list of articles by priority"""
    articles = get_all_articles()
    sorted_articles = sorted(articles, key=lambda x: x.priority_rank)
    
    return {
        "priorities": [
            {
                "rank": a.priority_rank,
                "article": a.article_number,
                "name": a.name,
                "risk": a.final_risk,
                "status": a.status,
                "recommendation": a.recommendation
            }
            for a in sorted_articles
        ]
    }

@router.get("/recommendations")
async def get_recommendations():
    """Get evidence-based recommendations"""
    articles = get_all_articles()
    
    # Find Article 356 (critical blocker)
    article_356 = next((a for a in articles if a.article_number == 356), None)
    
    recommendations = {
        "critical_blocker": {
            "article": 356,
            "issue": "No procedure defined for elections during President's Rule",
            "evidence": "Kovind Report Page 42: 'No procedure has been defined...'",
            "action": "Define explicit constitutional procedure immediately",
            "priority": "HIGHEST"
        },
        "high_priority": [],
        "moderate_priority": []
    }
    
    for article in articles:
        if article.article_number == 356:
            continue
        
        item = {
            "article": article.article_number,
            "name": article.name,
            "risk": article.final_risk,
            "action": article.recommendation
        }
        
        if article.final_risk >= 50:
            recommendations["high_priority"].append(item)
        else:
            recommendations["moderate_priority"].append(item)
    
    return recommendations
