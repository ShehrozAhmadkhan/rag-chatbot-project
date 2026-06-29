from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
import os
load_dotenv()

file_path = "D:/RAG/rag-chatbot-project/practicetext.md"
read_textfile = open(file_path,"r",encoding="utf-8")
data = read_textfile.read()

def wordbased_chunking(data,overlook,chunksize):
    start = 0
    end = 100
    step = chunksize - overlook
    temp = data.split(" ")
    chunks = []

    while start < len(temp):
        chunk = temp[start:end]
        updated_chunk = " ".join(chunk)
        chunks.append(updated_chunk)
        start += step
        end += step

    return chunks

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-project")

data_in_chunks = wordbased_chunking(data,20,100)

embed1 = client.embeddings.create(model="text-embedding-3-small",input=data_in_chunks,dimensions=1024)

embed_chunks = []
for vector in range(len(data_in_chunks)):
    embed_chunks.append({"id": f"chunk: {vector}",
                         "values":embed1.data[vector].embedding,
                         "metadata":{"text":f"{data_in_chunks[vector]}"}})
    
index.upsert(vectors=embed_chunks)

user_question = input("Ask a question: ")
embed2 = client.embeddings.create(model="text-embedding-3-small",input=user_question,dimensions=1024)
uq_vector = embed2.data[0].embedding

database_query = index.query(vector=uq_vector,top_k=2,include_metadata=True)
database_chunks = []
for sentence in database_query.matches:
    database_chunks.append(sentence.metadata["text"])

database_chunks = "\n".join(database_chunks)

prompt = f"""you are a helpfull assistant,using only the context below answer the question
context: {database_chunks}
user question: {user_question}
"""

llm = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}])

answer = llm.choices[0].message.content
print(answer)