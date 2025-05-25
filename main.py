from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import OpenAI

app = FastAPI()

# ✅ CORS goes BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://127.0.0.1:5500"],  # or explicitly list "http://127.0.0.1:5500"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    prompt: str

@app.post("/ask")
def ask(query: Query):
    llm = OpenAI()
    response = llm.invoke(query.prompt)
    return {"response": response}
