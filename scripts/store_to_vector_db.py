import json
import numpy as np
import os
import chromadb

# === Load processed data ===
print("📂 Loading chunks, embeddings, and metadata...")
with open("../processed_data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open("../processed_data/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

embeddings = np.load("../processed_data/embeddings.npy")

# === Define a persistent ChromaDB location ===
persist_dir = "../chroma_db"  # 👈 New correct location

# Create the directory if it doesn't exist
os.makedirs(persist_dir, exist_ok=True)

# === Initialize Chroma with local persistence ===
client = chromadb.PersistentClient(path=persist_dir)

# Create or load collection
collection = client.get_or_create_collection(name="estonian_laws")

# === Add your data ===
ids = [f"chunk_{i}" for i in range(len(chunks))]

collection.add(
    documents=chunks,
    embeddings=embeddings.tolist(),
    metadatas=metadata,
    ids=ids
)

print(f"✅ ChromaDB stored locally at: {persist_dir}")