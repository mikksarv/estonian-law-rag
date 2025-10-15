from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from setup_llm_llama_3 import load_llm, suppress_llama_logs

# === Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

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

    if not context or len(context) < 20:
        return "Mul puuduvad andmed antud teema kohta."

    # Strict prompt
    prompt = f"""
Saadud tekst on seadusetekst. Vasta ainult selle teksti põhjal. Ära lisa ega parafraseeri midagi, kui vastus ei ole otseselt tekstis olemas, siis vasta: "Vastus puudub esitatud seadustekstist."

--- Seadusetekst ---
{context}

--- Küsimus ---
{question}

--- Vastus ---
"""

    # === Suppress llama logs fully
    with suppress_llama_logs():
        response = llm(prompt, max_tokens=200, stop=["###"])

    answer = response["choices"][0]["text"].strip()

    # === Check if model failed or was too cautious
    if "Vastus puudub" in answer or len(answer) < 10:
        # 🛠 Extractive fallback
        question_words = question.lower().split()
        best_score = 0
        best_sentence = ""

        for chunk in retrieved_chunks:
            sentences = chunk.split(".")
            for sentence in sentences:
                score = sum(1 for word in question_words if word in sentence.lower())
                if score > best_score:
                    best_score = score
                    best_sentence = sentence.strip()

        if best_score >= max(1, len(question_words) // 3):
            return f"{best_sentence}"

        return "Mul puuduvad andmed antud teema kohta."

    if not context or any(x in answer.lower() for x in ["ma ei tea", "pole teada", "ei ole infot"]):
        return "Mul puuduvad andmed antud teema kohta."

    if len(answer) < 5:
        return "Palun täpsusta küsimust."

    return answer

