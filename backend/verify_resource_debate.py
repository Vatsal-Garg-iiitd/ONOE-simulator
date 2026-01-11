
import sys
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

load_dotenv()

from admin_features.f1_resource_debate import resource_debate

print("Starting Resource Debate simulation...")
try:
    result = resource_debate.simulate_debate("high_demand")
    print("\nDebate Simulation Result:")
    print(f"Risk Contribution: {result['risk_contribution']}%")
    print(f"Status: {result['status']}")
    print(f"Summary: {result['summary']}")
    
    print("\nTranscript Snippet:")
    for entry in result['transcript'][:3]:
        print(f"{entry['speaker']}: {entry['argument'][:50]}...")
        
    print("\nMitigations:")
    for m in result['mitigations']:
        print(f"- {m['strategy']}: {m['action_plan']}")
        
    if "System Error" in result['summary']:
        print("FAIL: Simulation returned fallback error.")
    else:
        print("SUCCESS: Simulation validated.")
        
except Exception as e:
    print(f"Error during simulation: {e}")
    import traceback
    traceback.print_exc()
