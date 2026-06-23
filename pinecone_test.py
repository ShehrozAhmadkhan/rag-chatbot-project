from dotenv import load_dotenv
from openai import OpenAI
import os
from pinecone import Pinecone

load_dotenv()

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key= os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-project")

chunks = [
    "The dog is sleeping on the couch",
    "The puppy is resting on the sofa",
    "Pakistan won the cricket match"
]

response = client.embeddings.create(model="text-embedding-3-small",input=chunks,dimensions=1024)

vectors = []
for vector in range(len(chunks)):
    vectors.append({"id":f"chunk{vector}",
                    "values":response.data[vector].embedding,
                    "metadata":{"text":chunks[vector]}}

    )

index.upsert(vectors=vectors)

print(f"The lenght of vector is {len(vectors)}")