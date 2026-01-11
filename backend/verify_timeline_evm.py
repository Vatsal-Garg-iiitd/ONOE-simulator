import requests
import json

url = "http://localhost:8000/api/admin/dashboard"

def check_timeline(evm_supply):
    payload = {
        "target_year": 2029,
        "evm_supply": evm_supply,
        "security_personnel": 100
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Find F7 feature
        f7 = next((f for f in data["features"] if f["id"] == "f7"), None)
        if f7 and "months_needed" in f7["data"]:
            print(f"✅ Supply {evm_supply}% -> Months Needed: {f7['data']['months_needed']}")
            return f7['data']['months_needed']
        else:
            print(f"❌ Supply {evm_supply}% -> F7 data missing.")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

print("--- Verifying Timeline Dynamics ---")
months_100 = check_timeline(100) # Base case
months_50 = check_timeline(50)   # Low supply case

if months_100 is not None and months_50 is not None:
    if months_50 > months_100:
        print("\n✅ PASSED: Timeline increased with lower supply.")
    else:
        print("\n❌ FAILED: Timeline did not increase.")
else:
    print("\n❌ FAILED: Could not retrieve data.")
