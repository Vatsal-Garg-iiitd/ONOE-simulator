import os
from dotenv import load_dotenv, find_dotenv

print(f"Current Working Directory: {os.getcwd()}")
print(f"Checking for .env file...")

# Try finding it
env_path = find_dotenv()
print(f"find_dotenv() result: '{env_path}'")

# Load it
success = load_dotenv()
print(f"load_dotenv() success: {success}")

# Check key
api_key = os.getenv("HUGGINGFACE_API_KEY")
if api_key:
    masked = api_key[:4] + "*" * (len(api_key)-8) + api_key[-4:]
    print(f"✅ HUGGINGFACE_API_KEY found: {masked}")
else:
    print("❌ HUGGINGFACE_API_KEY NOT found in environment.")

# Check for other common misspellings
print(f"HUGGINGFACEHUB_API_TOKEN: {os.getenv('HUGGINGFACEHUB_API_TOKEN') is not None}")
print(f"HF_TOKEN: {os.getenv('HF_TOKEN') is not None}")
