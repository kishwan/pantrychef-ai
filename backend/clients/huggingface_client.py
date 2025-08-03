import os
import httpx
from dotenv import load_dotenv

load_dotenv() # TODO?

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-cased-distilled-squad"

async def answer_question(question: str, context: str) -> str:
    if not HF_API_TOKEN:
        raise ValueError("HuggingFace API Token not found in .env")
    
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(HF_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("answer", "I couldn't find an answer to that question")
        except httpx.HTTPStatusError as e:
            print(f"HuggingFace API Http Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"HuggingFace API Request Error: {e}")
            return "Failed to connect to HuggingFace service"
        except Exception as e:
            print(f"An unexpected error occurred with HuggingFace API: {e}")
            return "An unexpected error occurred"