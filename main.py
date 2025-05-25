from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    prompt: str

HF_TOKEN = "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"  # Replace with your actual token
API_URL = "https://router.huggingface.co/together/v1/chat/completions"

@app.post("/ask")
def ask(query: Query):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [
            {
                "role": "user",
                "content": query.prompt
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {"response": f"Error: {response.status_code} {response.text}"}

    try:
        result = response.json()
        return {"response": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"response": f"Failed to parse response: {str(e)}", "raw": response.text}
