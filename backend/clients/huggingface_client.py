import os
from huggingface_hub import InferenceClient

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceTB/SmolLM2-1.7B-Instruct"

client = InferenceClient(
    provider="auto",
    api_key=HF_API_TOKEN
)

async def answer_question(question: str, context: str) -> str:
    if not HF_API_TOKEN:
        raise ValueError("HuggingFace API Token not found in .env")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful cooking assistant. "
                "Use the provided recipe to answer the user's question in **one or two short sentences**. "
                "Be concise and avoid unnecessary detail."
            )
        },
        {
            "role": "user",
            "content": f"Recipe:\n{context}\n\nQuestion: {question}"
        }
    ]

    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=messages,
            max_tokens=50,
            temperature=0.7
        )
        return completion.choices[0].message["content"].strip()
    
    except Exception as e:
        print(f"HF API error: {e}")
        return "An error occurred while generating the AI response."