import requests
import json

def verify_monte_carlo_graphs():
    articles = [356, 83, 82, 174]
    print(f"Verifying Monte Carlo Graph Data...\n")
    
    for article_id in articles:
        url = f"http://localhost:8000/api/articles/{article_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            f4 = data.get("components", {}).get("feature_4_confidence", {})
            risk_contrib = f4.get("risk_contribution")
            graph = f4.get("graph_data", {})
            graph_type = graph.get("type", "unknown")
            
            print(f"✅ Article {article_id}:")
            print(f"   Risk Contribution: {risk_contrib} (Expected: 0.0)")
            print(f"   Graph Type: {graph_type}")
            print(f"   Data Points: {len(graph.get('data', []))}")
            
            if risk_contrib != 0.0:
                print("   ❌ FAIL: Risk contribution should be 0.0")
            
        except Exception as e:
            print(f"❌ Article {article_id}: Error {e}")
            
if __name__ == "__main__":
    verify_monte_carlo_graphs()
