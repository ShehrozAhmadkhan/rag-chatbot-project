from chunking import word_chunking
from dotenv import load_dotenv
import os
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-project")

text = """Pakistan is a country located in South Asia. It was founded in 1947 after gaining independence from British rule. 
The capital city of Pakistan is Islamabad, which is a planned city built in the 1960s. 
Karachi is the largest city and the financial hub of the country. 
Lahore is the cultural capital and is known for its rich history, food, and architecture. 
Pakistan has a population of over 220 million people, making it the fifth most populous country in the world.
The official languages are Urdu and English. Pakistan has four provinces: Punjab, Sindh, Khyber Pakhtunkhwa, and Balochistan.
The economy of Pakistan is based on agriculture, textiles, and services.
Cricket is the most popular sport in Pakistan and the national team has won the Cricket World Cup in 1992.
The famous Karakoram Highway connects Pakistan to China and passes through some of the highest mountains in the world.
"""

chunks = word_chunking(text,30,5)

response = client.embeddings.create(model="text-embedding-3-small",input=chunks,dimensions=1024)

vectors = []

for i in range(len(chunks)):
    vectors.append({"id": f"chunk{i}",
                    "values":response.data[i].embedding,
                    "metadata":{"text":chunks[i]}})
    
index.upsert(vectors= vectors)

user_query = input("Ask a question: ")

user_vector = client.embeddings.create(model="text-embedding-3-small",input=user_query,dimensions=1024)
lofn = user_vector.data[0].embedding

result = index.query(vector=lofn,top_k=2,include_metadata=True)

for i in result.matches:
    print(f"{i.metadata["text"]} and cosine similarity is {i.score}.")
