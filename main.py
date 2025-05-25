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

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_TOKEN = "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"  # 🔐 paste your token here

@app.post("/ask")
def ask(query: Query):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": query.prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {"response": f"Error: {response.status_code} {response.text}"}
    result = response.json()
    # The model usually returns a list of dicts with 'generated_text'
    if isinstance(result, list) and "generated_text" in result[0]:
        return {"response": result[0]["generated_text"]}
    else:
        return {"response": str(result)}
