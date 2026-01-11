import requests
import json

def verify_dynamic_risk():
    articles = [82, 83, 85, 172, 174, 356]
    
    print(f"Verifying dynamic risk for articles: {articles}\n")
    
    for article_id in articles:
        url = f"http://localhost:8000/api/articles/{article_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            final_risk = data.get("final_risk", 0.0)
            
            print(f"✅ Article {article_id}: {final_risk}")
            
        except Exception as e:
            print(f"❌ Article {article_id}: Error {e}")

if __name__ == "__main__":
    verify_dynamic_risk()
