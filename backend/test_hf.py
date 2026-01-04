import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")
print(f"API Key present: {bool(api_key)}")

try:
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token=api_key,
        task="conversational", 
        max_new_tokens=512,
        top_p=0.95,
        temperature=0.7
    )
    print("LLM Initialized")
    response = llm.invoke("Hello!")
    print("Response Type:", type(response))
    print("Response:", response)
except Exception as e:
    print(f"Error Type: {type(e)}")
    print(f"Error: {e}")
