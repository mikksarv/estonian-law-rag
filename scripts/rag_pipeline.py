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
    context = "\n".join(retrieved_chunks)

    prompt = (
        f"### Instruction:\n"
        f"{context}\n\nKüsimus: {question}\n\n### Vastus:"
    )

    response = llm(prompt, max_tokens=200)
    return response["choices"][0]["text"].strip()