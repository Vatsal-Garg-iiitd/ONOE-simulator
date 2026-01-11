import requests
import json

url = "http://localhost:8000/api/admin/dashboard"

try:
    print(f"Fetching dashboard from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    features = data.get("features", [])
    f3 = next((f for f in features if f["id"] == "f3"), None)
    
    if f3 is None:
        print("\n✅ PASSED: Feature F3 (Historical Precedent) is NOT present in the response.")
    else:
        print("\n❌ FAILED: Feature F3 is STILL present.")
        
    print(f"Total features returned: {len(features)}")

except Exception as e:
    print(f"\n❌ Request failed: {e}")
