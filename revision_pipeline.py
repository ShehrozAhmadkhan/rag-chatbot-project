from dotenv import load_dotenv
import os 
from openai import OpenAI
from pinecone import Pinecone
load_dotenv()

data = """The empirical data on chunking provides a compelling window into how the human mind overcomes the severe capacity constraints of working memory, and this research has evolved significantly since the concept was first introduced. The foundational data comes from George Miller's seminal 1956 paper, "The Magical Number Seven, Plus or Minus Two," which synthesized a wide range of experimental findings to suggest that immediate memory could reliably hold between five and nine discrete items. However, subsequent decades of research have refined this estimate considerably, with a substantial body of evidence—most notably summarized by Cowan in 2001—pointing to a more precise capacity limit of approximately four chunks in the focus of attention. This refinement is not merely a correction but a fundamental insight, as it clarifies that the original "magical number" was a rough heuristic, while the four-chunk limit represents the true bottleneck of conscious processing when rehearsal and recoding strategies are properly controlled for. The critical insight, however, is that this limit applies to the number of chunks, not to the amount of information each chunk can contain, and it is here that the most fascinating data on chunking emerges. Studies demonstrate that chunk size is highly dynamic and expands significantly with expertise, practice, and the meaningfulness of the material; for instance, research on chess experts has revealed that master-level players can recognize and store up to fifteen pieces of information as a single chunk based on familiar board configurations, whereas novices, lacking these pre-existing patterns, must treat each piece as an individual unit, quickly overwhelming their working memory capacity. Similarly, expert typists have been shown to chunk entire common letter sequences, such as "tion" or "ing," as single keystroke patterns, allowing them to type faster and more accurately than those who process each letter individually. In controlled laboratory settings, researchers have quantified the growth of chunking through sequence learning paradigms, producing precise behavioral data that reveals how chunking evolves over time. A notable study involving Guinea baboons, published in 2013, tracked the learning of motor sequences and found that average chunk sizes began at approximately 2.2 items and grew to about 3.38 items with extended practice, with occasional chunks of 8 or even 9 items being observed in individual trials—demonstrating that even non-human primates rely on the same chunking mechanisms. The dynamics of this evolution further depend on the length of the sequence being learned, with research indicating that shorter sequences (e.g., four items) allow for the formation of larger, more fluid chunks, while longer sequences tend to be parsed into a greater number of smaller chunks, suggesting a fundamental trade-off between chunk size and sequence complexity. To capture these chunking processes objectively, researchers have developed robust measurement techniques, with two primary behavioral markers being widely used to identify chunk boundaries in experimental data. The first is Transitional Error Probabilities, or TEPs, which are based on the observation that items within a single chunk are tightly bound together, making recall errors less likely between them; when a spike in error probability occurs between two adjacent items, it reliably signals a chunk boundary. The second and perhaps most intuitive marker is Inter-Response Times, or IRTs, which consistently show longer pauses at chunk boundaries than between items within a chunk, reflecting the additional cognitive effort required to retrieve the next chunk from long-term memory. These measurement tools have been validated across numerous studies, allowing researchers to infer the underlying structure of memory organization without directly observing the cognitive process itself. Collectively, this body of data demonstrates that chunking is not a fixed cognitive trait but an adaptive strategy that compresses information into larger, more meaningful units, enabling individuals to bypass the four-item limit of working memory by leveraging prior knowledge, pattern recognition, and extensive practice. The implications of these findings extend beyond basic cognitive science into applied fields such as education, where chunking data informs instructional design by suggesting that material should be presented in organized, meaningful groups to enhance learning and retention, as well as in user interface design, where information is broken into digestible chunks to reduce cognitive load. Ultimately, the data on chunking reveals a fundamental principle of human cognition: that our memory limitations are not insurmountable obstacles but rather constraints that we instinctively overcome through the elegant and efficient strategy of organizing information into larger, interconnected wholes."""

def wordbased_chunking(data,overlap,chunksize):
    start = 0
    end = chunksize
    step = chunksize - overlap
    new_data = data.split(" ")
    sentence_chunks = []
    while start < len(new_data):
        chunk = new_data[start:end]
        updated_chunk = " ".join(chunk)
        sentence_chunks.append(updated_chunk)

        start += step
        end += step
    return sentence_chunks

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-project")
wbc = wordbased_chunking(data,20,100)

embed1 = client.embeddings.create(model="text-embedding-3-small",input=wbc,dimensions=1024)

vector_chunks = []
for vector in range(len(wbc)):
    vector_chunks.append({"id":f"chunk {vector}",
                          "values": embed1.data[vector].embedding,
                          "metadata":{"text":wbc[vector]}})
    
index.upsert(vectors=vector_chunks)

user_question = input("Ask a question: ")
uq_embed = client.embeddings.create(model="text-embedding-3-small",input=user_question,dimensions=1024)
uq_vector = uq_embed.data[0].embedding

database_query = index.query(vector=uq_vector,top_k=2,include_metadata=True)

context = []
for i in database_query.matches:
    context.append(i.metadata["text"])

context = "\n".join(context)

prompt = f"""you are a helpfull assistant,using only the context below answer the question
context: {context}
user question: {user_question}
"""

llm = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user",
                                                                    "content":prompt}])
llm_response = llm.choices[0].message.content
print(llm_response)