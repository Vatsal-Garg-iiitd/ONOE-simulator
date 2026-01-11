import requests
import json

def verify_supply_chain():
    url = "http://localhost:8000/api/admin/dashboard"
    
    # Test Case 1: Default (2029, 100%)
    print("\n--- Test Case 1: Target 2029, Supply 100% ---")
    payload = {"target_year": 2029, "evm_supply": 100}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        f2 = next(f for f in data['features'] if f['id'] == 'f2')
        inv = f2['data']['evm_inventory']
        
        print(f"Current Stock: {inv['current_stock']} (Exp: 1.2M)")
        print(f"Projected Prod: {inv['projected_production']} (Exp: ~1.5M -> 3yrs * 5L)")
        print(f"Total: {inv['total_available']} (Exp: 2.7M)")
        print(f"Deficit: {inv['deficit']}")
        print(f"Risk Score: {f2['risk_contribution']}")
        
        if inv['total_available'] > 2500000:
             print("✅ PASSED: Surplus achieved by 2029 with full supply.")
        else:
             print("❌ FAILED: Should be surplus.")

    except Exception as e:
        print(f"Error: {e}")

    # Test Case 2: Short Timeline (2027, 80%)
    print("\n--- Test Case 2: Target 2027, Supply 80% ---")
    payload = {"target_year": 2027, "evm_supply": 80}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        f2 = next(f for f in data['features'] if f['id'] == 'f2')
        inv = f2['data']['evm_inventory']
        
        print(f"Current Stock: {inv['current_stock']} (Exp: ~960k)")
        print(f"Projected Prod: {inv['projected_production']} (Exp: 1 yr * 4L = 4L)") 
        # 2027 - 2026 = 1 year remaining
        print(f"Total: {inv['total_available']}")
        print(f"Deficit: {inv['deficit']}")
        
        if inv['deficit'] > 0:
             print("✅ PASSED: Deficit correctly identified for short timeline/low supply.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_supply_chain()
