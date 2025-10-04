import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np

# === CONFIGURATION ===
json_folder = "../data/raw_laws"  # Folder containing your 10 law JSON files
chunk_size = 500
chunk_overlap = 50
embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# === LOAD EMBEDDING MODEL ===
print("🔄 Loading embedding model...")
model = SentenceTransformer(embedding_model_name)

# === SET UP TEXT SPLITTER ===
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

# === PREPARE STORAGE ===
all_chunks = []         # All text segments
metadata_list = []      # Metadata for each chunk

# === PROCESS ALL LAW FILES ===
print(f"📂 Reading files from: {json_folder}")
files_to_process = ["Kaitseväeteenistuse_seaduse_rakendamise_seadus_(lühend - KVTRS).json"]  # just your test file
for filename in files_to_process:
    if filename.endswith(".json"):
        filepath = os.path.join(json_folder, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            law_data = json.load(f)

        # Extract fields
        law_text = law_data.get("text", "")
        law_title = law_data.get("title", "Unknown Title")
        law_url = law_data.get("url", "")

        print(f"📄 Processing: {filename}")
        print(f"   Title: {law_title}")
        print(f"   Text length: {len(law_text)}")

        # Skip if text is empty or whitespace only
        if not law_text.strip():
            print(f"⚠️ Skipping {filename} — text is empty.")
            continue  # Skip to next file

        # Split text into chunks
        chunks = splitter.split_text(law_text)

        # Add each chunk + metadata
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata_list.append({
                "source_file": filename,
                "title": law_title,
                "url": law_url,
                "chunk_id": i
            })

print(f"✅ Total chunks created: {len(all_chunks)}")

# === ENCODE CHUNKS INTO EMBEDDINGS ===
print("🧠 Encoding chunks into embeddings...")
embeddings = model.encode(all_chunks, show_progress_bar=True)

print("✅ Embedding complete.")

# === Create output folder ===
output_dir = "../processed_data"
os.makedirs(output_dir, exist_ok=True)

# === Save chunks ===
with open(os.path.join(output_dir, "chunks.json"), "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

# === Save metadata ===
with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=2)

# === Save embeddings ===
np.save(os.path.join(output_dir, "embeddings.npy"), embeddings)

print(f"📦 Saved chunks, metadata, and embeddings to: {output_dir}")