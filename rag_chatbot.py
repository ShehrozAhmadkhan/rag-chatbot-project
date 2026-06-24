from dotenv import load_dotenv
import os
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-project")

user_question = input("Ask a question: ")
respone = client.embeddings.create(model="text-embedding-3-small",input=user_question,dimensions=1024)
vector = respone.data[0].embedding

result = index.query(vector= vector,top_k=2,include_metadata=True)

context = []

for i in result.matches:
    context.append(i.metadata["text"])

context = "\n".join(context)

prompt = f"""You are a helpful assistant. Using only the context below, answer the question.

Context: {context} 

Question: {user_question}
"""

llm_response = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role": "user",
                                                                             "content": prompt}])
answer = llm_response.choices[0].message.content
print(answer)
                                                                            