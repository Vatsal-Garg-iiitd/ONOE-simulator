import requests
import json

url = "http://localhost:8000/api/admin/bottleneck/calculate"
payload = {
    "sliders": {
        "evm_delay": -3.0,
        "state_coop": 70.0,
        "budget": 60.0
    },
    "context": {
        "evm_capacity": 1.5,
        "security_personnel": 85.0
    }
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    
    print("\n✅ Response Received:")
    print(json.dumps(data, indent=2))
    
    if "ai_analysis" in data:
        analysis = data["ai_analysis"]
        print("\n✅ 'ai_analysis' field present.")
        
        if "[SIMULATION MODE]" in analysis:
            print("⚠️ Response is in SIMULATION MODE (Fallback). Real LLM call failed.")
        elif len(analysis) > 50:
             print("✅ 'ai_analysis' appears to be REAL generated text.")
        else:
             print("⚠️ 'ai_analysis' looks too short.")
    else:
        print("\n❌ 'ai_analysis' field MISSING.")

except Exception as e:
    print(f"\n❌ Request Failed: {e}")
