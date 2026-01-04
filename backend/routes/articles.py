"""
API Routes for Articles
"""
from fastapi import APIRouter, HTTPException
from models import Article, ToggleRequest
from risk_engine import risk_engine
from features.f5_explorer import explorer_system

router = APIRouter(prefix="/api/articles", tags=["articles"])

# Cache for calculated articles
_articles_cache = None

def get_all_articles():
    """Get or calculate all articles"""
    global _articles_cache
    if _articles_cache is None:
        # Revert: Use full AI mode (slow but accurate)
        _articles_cache = risk_engine.calculate_all_articles()
    return _articles_cache

def invalidate_cache():
    """Invalidate cache when toggles change"""
    global _articles_cache
    _articles_cache = None

@router.get("/", response_model=list[Article])
async def get_articles():
    """Get all 7 articles with risk scores"""
    return get_all_articles()

@router.get("/{article_number}", response_model=Article)
async def get_article(article_number: int):
    """Get detailed analysis for specific article"""
    try:
        article = risk_engine.calculate_article_risk(article_number)
        return article
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{article_number}/toggle")
async def apply_toggle(article_number: int, request: ToggleRequest):
    """Apply explorer toggle and recalculate risk"""
    try:
        # Apply toggle
        impact = explorer_system.apply_toggle(
            article_number, 
            request.toggle_id, 
            request.new_state
        )
        
        # Invalidate cache to force recalculation
        invalidate_cache()
        
        # Recalculate article
        article = risk_engine.calculate_article_risk(article_number)
        
        return {
            "success": True,
            "toggle_id": request.toggle_id,
            "new_state": request.new_state,
            "impact": impact,
            "updated_article": article
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/356/critical")
async def get_critical_article_356():
    """
    Special endpoint for Article 356 - the CRITICAL BLOCKER
    Returns detailed breakdown with all 8 features
    """
    article = risk_engine.calculate_article_risk(356)
    
    return {
        "article": 356,
        "final_risk": article.final_risk,
        "priority_rank": article.priority_rank,
        "status": article.status,
        "components": {
            "base": article.components.base,
            "feature_1_debate": article.components.feature_1_debate,
            "feature_2_rag": "Evidence included below",
            "feature_3_precedent": article.components.feature_3_precedent,
            "feature_4_confidence": article.components.feature_4_confidence,
            "feature_5_explorer": article.components.feature_5_explorer,
            "feature_6_political": article.components.feature_6_political,
            "feature_7_timeline": article.components.feature_7_timeline,
            "feature_8_priority": article.components.feature_8_priority
        },
        "rag_evidence": [
            {
                "source": ev.source,
                "page": ev.page_number,
                "quote": ev.quote
            } for ev in article.rag_evidence
        ],
        "precedents": [p.case_name + f" ({p.year})" for p in article.precedents],
        "debate": {
            "government": article.debate_result.government_argument if article.debate_result else None,
            "court": article.debate_result.court_argument if article.debate_result else None,
            "vulnerability": article.debate_result.vulnerability_score if article.debate_result else None
        },
        "recommendation": article.recommendation
    }
