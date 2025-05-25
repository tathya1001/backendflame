from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import OpenAI  # or Ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Query(BaseModel):
    prompt: str

@app.post("/ask")
def ask(query: Query):
    llm = OpenAI()  # replace with Ollama(model="llama3") if using local model
    answer = llm.invoke(query.prompt)
    return {"response": answer}
