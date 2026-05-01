from pinecone import Pinecone 
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

embedder =  SentenceTransformer("all-MiniLM-L6-v2")

def store_documents(texts: list[str]) -> str:

    try:
        vectors = []

        for i, text in enumerate(texts):
            embedding = embedder.encode(text).tolist()

            vectors.append({
                "id":f'doc_{i}',
                "values":embedding,
                "metadata":{"text":text}
            })
        
        index.upsert(vectors=vectors)

        return f'successfully stored {len(texts)} document chunks in pinecone'
    
    except Exception as e:
        return f'storing documents failed {str(e)}'
    
    

def rag_search(query: str)-> str:
    try:

        query_vector = embedder.encode(query).tolist()

        results = index.query(
            vector = query_vector,
            top_k = 3,
            include_metadata = True
        )

        if not results["matches"]:
            return "No relevant document found in knowledge base"
        
        chunks = []

        for match in results['matches']:
            score = round(match['score'],2)
            text = match['metadata']['text']
            chunks.append(f'[Relevance: {score}]\n {text}')
        
        return "\n\n".join(chunks)
    
    except Exception as e:
        return f'Rag search failed: {str(e)}'
    
        