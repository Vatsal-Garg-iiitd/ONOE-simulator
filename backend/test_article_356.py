"""
Test script to verify Article 356 achieves 80-100 risk score
"""
import sys
sys.path.insert(0, '/Users/jagdishgarg/Desktop/Hackethon/backend')

from risk_engine import risk_engine

def test_article_356():
    """Test that Article 356 achieves critical risk score"""
    print("🔍 Testing Article 356 Risk Calculation...")
    print("=" * 60)
    
    article = risk_engine.calculate_article_risk(356)
    
    print(f"\n📊 Article {article.article_number}: {article.name}")
    print(f"Status: {article.status}")
    print(f"Final Risk Score: {article.final_risk}/100")
    print(f"Priority Rank: #{article.priority_rank}")
    
    print(f"\n🔧 Risk Components:")
    print(f"  Base Risk: {article.components.base}")
    print(f"  F1 Debate: +{article.components.feature_1_debate}")
    print(f"  F3 Precedent: +{article.components.feature_3_precedent}")
    print(f"  F4 Monte Carlo: +{article.components.feature_4_confidence['risk_contribution']}")
    print(f"  F5 Explorer: +{article.components.feature_5_explorer}")
    print(f"  F6 Political: +{article.components.feature_6_political}")
    print(f"  F7 Timeline: +{article.components.feature_7_timeline}")
    
    print(f"\n📚 RAG Evidence: {len(article.rag_evidence)} sources")
    print(f"⚖️ Precedents: {len(article.precedents)} cases")
    
    print(f"\n✅ VERIFICATION:")
    if 80 <= article.final_risk <= 100:
        print(f"   ✓ Article 356 risk score ({article.final_risk}) is in target range [80-100]")
    else:
        print(f"   ✗ Article 356 risk score ({article.final_risk}) is NOT in target range [80-100]")
    
    if article.status == "CRITICAL BLOCKER":
        print(f"   ✓ Article 356 is marked as CRITICAL BLOCKER")
    else:
        print(f"   ✗ Article 356 is NOT marked as CRITICAL BLOCKER")
    
    if article.priority_rank == 1:
        print(f"   ✓ Article 356 is Priority #1")
    else:
        print(f"   ✗ Article 356 is NOT Priority #1")
    
    # Check all 8 features
    features_present = 0
    if article.components.feature_1_debate: features_present += 1
    if article.rag_evidence: features_present += 1
    if article.components.feature_3_precedent: features_present += 1
    if article.components.feature_4_confidence: features_present += 1
    if article.components.feature_5_explorer is not None: features_present += 1
    if article.components.feature_6_political: features_present += 1
    if article.components.feature_7_timeline is not None: features_present += 1
    if article.priority_rank: features_present += 1
    
    if features_present == 8:
        print(f"   ✓ All 8 features applied to Article 356")
    else:
        print(f"   ✗ Only {features_present}/8 features applied")
    
    print("\n" + "=" * 60)
    return article

def test_all_articles():
    """Test all articles"""
    print("\n\n🔍 Testing All Articles...")
    print("=" * 60)
    
    articles = risk_engine.calculate_all_articles()
    
    print(f"\nTotal Articles: {len(articles)}")
    print("\nRisk Scores:")
    for article in sorted(articles, key=lambda x: x.priority_rank or 999):
        print(f"  #{article.priority_rank} Article {article.article_number}: {article.final_risk:.1f}/100 - {article.status}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    article_356 = test_article_356()
    test_all_articles()
    
    print("\n🎉 Test Complete!")
    print(f"\n💡 Recommendation: {article_356.recommendation}")
