import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load chunks
with open("../processed_data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load updated embedding model (matches rag_pipeline.py)
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

print("🔍 Generating embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True)

# Save embeddings
np.save("../processed_data/embeddings.npy", embeddings)
print("✅ Embeddings saved to: ../processed_data/embeddings.npy")