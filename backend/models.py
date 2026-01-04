from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ArticleStatus(str, Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL_BLOCKER = "CRITICAL BLOCKER"

class PrecedentCase(BaseModel):
    case_name: str
    year: int
    impact_score: float
    relevance: str
    summary: Optional[str] = None

class DebateResult(BaseModel):
    vulnerability_score: float = Field(..., ge=0, le=1)
    government_argument: str
    court_argument: str
    risk_contribution: float
    debate_transcript: List[Dict[str, str]] = []
    mitigations: List[Dict[str, str]] = []
    court_challenge_probability: str = "0%"


class MonteCarloResult(BaseModel):
    mean: float
    std_dev: float
    confidence_interval_95: List[float]
    trials: int = 1000
    risk_contribution: float

class ExplorerToggle(BaseModel):
    toggle_id: str
    question: str
    current_state: bool
    impact_if_true: float
    impact_if_false: float
    description: str

class PoliticalSupport(BaseModel):
    current_support: float = Field(..., ge=0, le=100)
    required_support: float = Field(..., ge=0, le=100)
    risk_contribution: float

class TimelineFeasibility(BaseModel):
    months_needed: int
    months_available: int
    feasible: bool
    risk_impact: float
    target_year: int

class RiskComponents(BaseModel):
    base: float
    feature_1_debate: Optional[float] = None
    feature_2_rag: Optional[float] = None
    feature_3_precedent: Optional[float] = None
    feature_4_confidence: Optional[MonteCarloResult] = None
    feature_5_explorer: Optional[float] = None
    feature_6_political: Optional[float] = None
    feature_7_timeline: Optional[float] = None
    feature_8_priority: Optional[int] = None

class RAGEvidence(BaseModel):
    source: str
    page_number: Optional[int] = None
    quote: str
    relevance_score: float

class Article(BaseModel):
    article_number: int
    name: str
    description: str
    base_risk: float
    final_risk: float
    status: ArticleStatus
    priority_rank: Optional[int] = None
    components: RiskComponents
    rag_evidence: List[RAGEvidence] = []
    precedents: List[PrecedentCase] = []
    debate_result: Optional[DebateResult] = None
    explorer_toggles: List[ExplorerToggle] = []
    political_support: Optional[PoliticalSupport] = None
    timeline: Optional[TimelineFeasibility] = None
    recommendation: str

class OverallAnalysis(BaseModel):
    total_articles: int
    critical_blockers: int
    average_risk: float
    onoe_feasibility: str
    key_recommendations: List[str]
    articles: List[Article]

class ToggleRequest(BaseModel):
    toggle_id: str
    new_state: bool
