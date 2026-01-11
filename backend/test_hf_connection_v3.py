from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")

models = [
    ("Zephyr (Router)", "https://router.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"),
    ("Gemma (Router)", "https://router.huggingface.co/models/google/gemma-2-9b-it"),
    ("Llama 3 (Router)", "https://router.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"),
]

for name, url in models:
    print(f"\nTesting {name} with URL: {url}")
    try:
        client = InferenceClient(model=url, api_key=api_key)
        messages = [{"role": "user", "content": "Hello!"}]
        completion = client.chat.completions.create(messages=messages, max_tokens=20)
        print("Success!")
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
