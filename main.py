from fastapi import FastAPI
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"hello world"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {"answer": request.question}