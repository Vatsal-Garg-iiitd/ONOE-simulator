from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")

try:
    print("Testing InferenceClient with Full Router URL...")
    # Using the full URL as the model argument
    client = InferenceClient(
        model="https://router.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        api_key=api_key
    )
    messages = [{"role": "user", "content": "Hello! Answer in one word."}]
    completion = client.chat.completions.create(
        messages=messages, 
        max_tokens=20
    )
    print("Success!")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Error details: {e}")
