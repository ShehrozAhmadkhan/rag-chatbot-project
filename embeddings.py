"""
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

text = "The dog is sleeping on the couch"

responce = client.embeddings.create(model="text-embedding-3-small",input=text)

embedding = responce.data[0].embedding

print(f"No of dimensions {len(embedding)}")
print(f"first five numbers are {embedding[:5]}")
"""


"""
from dotenv import load_dotenv
import os
from openai import OpenAI
import numpy as np

load_dotenv()

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

sentence1 = "The dog is sleeping on the couch"
sentence2 = "The puppy is resting on the sofa"  # similar meaning
sentence3 = "Pakistan won the cricket match"     # completely different

sentence = [sentence1,sentence2,sentence3]

response = client.embeddings.create(model="text-embedding-3-small",input=sentence)

embedding1 = response.data[0].embedding
embedding2 = response.data[1].embedding
embedding3 = response.data[2].embedding

print(f"no of dimension is sentence 1 {len(embedding1)}")
print(f"The first five numbers are {embedding1[:5]}")
print()

print(f"no of dimension is sentence 2 {len(embedding2)}")
print(f"The first five numbers are {embedding2[:5]}")
print()

print(f"no of dimension is sentence 3 {len(embedding3)}")
print(f"The first five numbers are {embedding3[:5]}")
print()

def cosine_similarity(vec1,vec2):
    value = np.dot(vec1,vec2)/(np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return value

print(cosine_similarity(embedding1,embedding2))
print()
print(cosine_similarity(embedding1,embedding3))

"""










