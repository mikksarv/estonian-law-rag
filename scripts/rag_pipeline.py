from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from setup_llm_llama_3 import load_llm

# === Load embedding model (unchanged)
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# === Load ChromaDB
persist_dir = "../chroma_db"
client = PersistentClient(path=persist_dir)
collection = client.get_or_create_collection(name="estonian_laws")

# === Load LLaMA model
llm = load_llm()

# === RAG Query Function
def query_rag(question, top_k=3):
    question_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    retrieved_chunks = results["documents"][0]
    context = "\n".join(retrieved_chunks).strip()

    # Step 4: Build prompt with example + context + question
    example = """### Näide:
Kontekst:
Ülem on isik, kellele on teenistuslikult allutatud teised kaitseväelased.

Küsimus:
Kes on ülem?

Vastus:
Ülem on kaitseväelane, kes juhib talle allutatud kaitseväelasi."""

    prompt = f"""{example}

### Kontekst:
{context}

### Küsimus:
{question}

### Vastus:"""

    response = llm(prompt, max_tokens=200, stop=["###"])
    answer = response["choices"][0]["text"].strip()

    # Step 6: Quality control
    if not context or any(x in answer.lower() for x in ["ma ei tea", "pole teada", "ei ole infot"]):
        return "Mul puuduvad andmed antud teema kohta."

    if len(answer) < 5:
        return "Palun täpsusta küsimust."

    return answer