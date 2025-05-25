from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    prompt: str

HF_TOKEN = "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"  # 🔐 use your Hugging Face token
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

@app.post("/ask")
def ask(query: Query):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": query.prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {"response": f"Error: {response.status_code} {response.text}"}

    result = response.json()

    try:
        return {"response": result[0]["generated_text"]}
    except:
        return {"response": str(result)}
