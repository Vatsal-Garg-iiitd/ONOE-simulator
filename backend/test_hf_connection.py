from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    print("Error: HUGGINGFACE_API_KEY not found in .env")
    exit(1)

print(f"Using API Key: {api_key[:4]}...")

try:
    print("Testing InferenceClient with default settings...")
    client = InferenceClient(api_key=api_key)
    messages = [{"role": "user", "content": "Hello! Answer in one word."}]
    completion = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta", 
        messages=messages, 
        max_tokens=20
    )
    print("Success!")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Error details: {e}")
