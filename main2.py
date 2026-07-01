from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
import os
from fastapi import FastAPI, UploadFile,File
from pydantic import BaseModel
import PyPDF2
from pdf_loader import load_pdf
from chunking import word_chunking

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-project")

class RequestChat(BaseModel):
    question : str

@app.get("/")
def hello():
    return {"message":"ke haal chal ah"}

@app.post("/chat")
def chat(request: RequestChat):
    question = request.question

    question_embed = client.embeddings.create(model="text-embedding-3-small",input=question,dimensions=1024)
    question_vector = question_embed.data[0].embedding

    database_query = index.query(vector=question_vector,top_k=2,include_metadata=True)
    context = []
    for vector in database_query.matches:
        context.append(vector.metadata["text"])

    context = "\n".join(context)

    prompt = f"""you are a helpfull assistant,using only the context below answer the question
    context: {context}
    user question: {question}
    """

    llm = client.chat.completions.create(model="gpt-4o-mini",messages = [{"role":"user","content":prompt}])
    answer = llm.choices[0].message.content
    return {"answer":answer}

@app.post("/upload")                                     
async def upload(file: UploadFile=File(...)):
    contents = await file.read()
    f = open("temp.pdf","wb")
    f.write(contents)
    f.close()

    file_path = "temp.pdf"

    
    data = load_pdf(file_path)
    
    chunks = word_chunking(data,100,20)
    chunks_embed = client.embeddings.create(model="text-embedding-3-small",input=chunks,dimensions=1024)

    chunk_vector = []

    for vector in range(len(chunks)):
        chunk_vector.append({"id":f"chunk: {vector}",
                             "values":chunks_embed.data[vector].embedding,
                             "metadata":{"text":chunks[vector]}})
        
    index.upsert(vectors=chunk_vector)
    return {"message": "success", "chunks": len(chunks)}



    
