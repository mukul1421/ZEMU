import json
import chromadb
from sentence_transformers import SentenceTransformer

# ---------------- Load JSON ----------------
with open("sikkim_data.json", "r", encoding="utf-8") as f:
    sikkim_data = json.load(f)

# ---------------- Chroma Cloud Client ----------------
client = chromadb.CloudClient(
    api_key='ck-FPrzVp2Dpt8CbZBB6eor4M5DZcNG4EBeGdfqaMcG5NLU',
    tenant='7b3b8842-d1ff-4e35-8208-7aa63816573f',
    database='sikkim'
)

# Get or create collection
collection = client.get_or_create_collection("sikkim_guide")

# ---------------- Embedding Model ----------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- Add Data to ChromaDB ----------------
for item in sikkim_data:
    embedding = embed_model.encode(item["text"]).tolist()
    collection.add(
        ids=[item["id"]],
        documents=[item["text"]],
        embeddings=[embedding],
        metadatas=[{
            "title": item["title"],
            "category": item["category"],
            "lat": item["coordinates"]["lat"],
            "lon": item["coordinates"]["lon"]
        }]
    )


print("All Sikkim data added to Chroma Cloud successfully!")
