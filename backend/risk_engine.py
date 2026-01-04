"""
Core Risk Calculation Engine
Calculates risk scores for all 7 constitutional articles using the 8 features
"""
from models import Article, ArticleStatus, RiskComponents, RAGEvidence, DebateResult
from features.f1_debate_agent import debate_agent
from features.f2_rag_system import rag_system
from features.f3_precedent_analysis import precedent_analyzer
from features.f4_monte_carlo import monte_carlo_simulator
from features.f5_explorer import explorer_system
from features.f6_political_tracker import political_tracker
from features.f7_timeline import timeline_analyzer
from features.f8_prioritizer import priority_ranker

class RiskEngine:
    def __init__(self):
        self.article_definitions = {
            82: {
                "name": "Article 82: Readjustment After Census",
                "description": "Governs reallocation of Lok Sabha seats after census. No synchronization provision with state assemblies.",
                "base_risk": 25.0,
                "features": ["F2", "F5", "F7"]
            },
            83: {
                "name": "Article 83(2): Duration of Lok Sabha",
                "description": "LS expires May 2029. Independent of state assemblies. Co-terminus provision needed.",
                "base_risk": 20.0,
                "features": ["F1", "F2", "F3", "F4", "F5", "F7"]
            },
            85: {
                "name": "Article 85: Presidential Dissolution",
                "description": "President can dissolve LS but no provision for simultaneous state dissolution.",
                "base_risk": 15.0,
                "features": ["F2", "F5", "F7"]
            },
            172: {
                "name": "Article 172(1): Duration of State Legislatures",
                "description": "28 states with different expiry dates. Creates 2-3 elections per year.",
                "base_risk": 25.0,
                "features": ["F1", "F2", "F3", "F5", "F7"]
            },
            174: {
                "name": "Article 174: Governor Dissolution Powers",
                "description": "Governor can dissolve assembly anytime, breaking ONOE timing.",
                "base_risk": 20.0,
                "features": ["F2", "F5", "F7"]
            },
            356: {
                "name": "Article 356: President's Rule",
                "description": "CRITICAL: No procedure for elections during President's Rule in ONOE. 73% probability of occurrence.",
                "base_risk": 35.0,
                "features": ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]
            }
        }
    
    def calculate_article_risk(self, article_number: int, use_llm: bool = True) -> Article:
        """Calculate complete risk analysis for an article"""
        
        if article_number not in self.article_definitions:
            raise ValueError(f"Article {article_number} not found")
        
        definition = self.article_definitions[article_number]
        base_risk = definition["base_risk"]
        features_used = definition["features"]
        
        # Initialize components
        components = RiskComponents(base=base_risk)
        
        # Feature 1: Debate Agent
        debate_result = None
        if "F1" in features_used:
            debate_data = debate_agent.simulate_debate(article_number, use_llm=use_llm)
            components.feature_1_debate = debate_data["risk_contribution"]
            debate_result = DebateResult(**debate_data)
        
        # Feature 2: RAG System (always used for evidence)
        rag_evidence = []
        if "F2" in features_used:
            evidence_list = rag_system.query_documents(article_number)
            rag_evidence = [RAGEvidence(**ev) for ev in evidence_list]
        
        # Feature 3: Precedent Analysis
        precedents = []
        if "F3" in features_used:
            precedent_risk = precedent_analyzer.calculate_precedent_risk(article_number)
            components.feature_3_precedent = precedent_risk
            precedents = precedent_analyzer.find_relevant_precedents(article_number)
        
        # Feature 4: Monte Carlo Simulation
        if "F4" in features_used:
            mc_result = monte_carlo_simulator.run_simulation(article_number)
            components.feature_4_confidence = mc_result
        
        # Feature 5: Explorer Toggles
        explorer_toggles = []
        if "F5" in features_used:
            explorer_impact = explorer_system.get_current_impact(article_number)
            components.feature_5_explorer = explorer_impact
            explorer_toggles = explorer_system.get_toggles(article_number)
        
        # Feature 6: Political Support
        political_support = None
        if "F6" in features_used:
            political_risk = political_tracker.calculate_political_risk(article_number)
            components.feature_6_political = political_risk
            political_support = political_tracker.get_support_details()
        
        # Feature 7: Timeline Feasibility
        timeline = None
        if "F7" in features_used:
            timeline_data = timeline_analyzer.assess_feasibility(article_number)
            components.feature_7_timeline = timeline_data["risk_impact"]
            timeline = timeline_data
        
        # Calculate final risk
        final_risk = base_risk
        
        if components.feature_1_debate:
            final_risk += components.feature_1_debate
        if components.feature_3_precedent:
            final_risk += components.feature_3_precedent
        if components.feature_4_confidence:
            final_risk += components.feature_4_confidence["risk_contribution"]
        if components.feature_5_explorer:
            final_risk += components.feature_5_explorer
        if components.feature_6_political:
            final_risk += components.feature_6_political
        if components.feature_7_timeline:
            final_risk += components.feature_7_timeline
        
        # Clamp to 0-100
        final_risk = max(0.0, min(100.0, final_risk))
        
        # Determine status
        if final_risk >= 80:
            status = ArticleStatus.CRITICAL_BLOCKER
        elif final_risk >= 60:
            status = ArticleStatus.HIGH_RISK
        elif final_risk >= 30:
            status = ArticleStatus.WARNING
        else:
            status = ArticleStatus.NORMAL
        
        # Generate recommendation
        recommendation = self._generate_recommendation(article_number, final_risk, status)
        
        return Article(
            article_number=article_number,
            name=definition["name"],
            description=definition["description"],
            base_risk=base_risk,
            final_risk=round(final_risk, 2),
            status=status,
            components=components,
            rag_evidence=rag_evidence,
            precedents=precedents,
            debate_result=debate_result,
            explorer_toggles=explorer_toggles,
            political_support=political_support,
            timeline=timeline,
            recommendation=recommendation
        )
    
    def calculate_all_articles(self, use_llm: bool = True) -> list[Article]:
        """Calculate risk for all articles"""
        articles = []
        for article_num in self.article_definitions.keys():
            article = self.calculate_article_risk(article_num, use_llm=use_llm)
            articles.append(article)
        
        # Apply Feature 8: Priority Ranking
        articles_dict = [article.dict() for article in articles]
        ranked = priority_ranker.rank_articles(articles_dict)
        
        # Update articles with priority ranks
        for i, article in enumerate(articles):
            article.priority_rank = ranked[i]["priority_rank"]
            article.components.feature_8_priority = ranked[i]["priority_rank"]
            
            # Update recommendation with priority
            if article.priority_rank == 1:
                article.recommendation = f"PRIORITY 1 - CRITICAL BLOCKER: {article.recommendation}"
        
        return articles
    
    def _generate_recommendation(self, article_number: int, risk: float, status: ArticleStatus) -> str:
        """Generate evidence-based recommendation"""
        
        recommendations = {
            82: "Define census synchronization mechanism to prevent seat reallocation from disrupting ONOE cycle.",
            83: "Amend to establish co-terminus provision linking Lok Sabha and State Assembly terms.",
            85: "Create constitutional protocol for simultaneous dissolution of Lok Sabha and State Assemblies.",
            172: "Synchronize all 28 state assembly terms through phased approach or one-time adjustment.",
            174: "Restrict Governor's dissolution powers during ONOE cycle through constitutional safeguards.",
            356: "Define explicit procedure for conducting elections in states under President's Rule during ONOE. This is the PRIMARY BLOCKER - without this, ONOE cannot proceed."
        }
        
        return recommendations.get(article_number, "Address constitutional gaps before implementing ONOE.")

# Singleton instance
risk_engine = RiskEngine()
