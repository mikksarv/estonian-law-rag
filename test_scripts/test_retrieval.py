import sys
import os

# Add the "scripts" folder to Python path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from chroma_loader import load_chroma_collection
from sentence_transformers import SentenceTransformer

# Load your persisted ChromaDB collection
persist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chroma_db"))
collection = load_chroma_collection(persist_dir)

# Initialize embedding model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Define your test query
query = "Millal hakkas kehtima X määrus?"

# Embed the query
query_embedding = model.encode([query])[0]

# Query ChromaDB for top 3 matches
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas"]
)

# Print the results
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("📄", doc[:200].replace("\n", " "), "...")
    print("📎 Source:", meta)
    print()