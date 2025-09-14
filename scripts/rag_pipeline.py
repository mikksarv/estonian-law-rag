from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import numpy as np

# === Load embedding model (same one you used before)
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# === Load ChromaDB
persist_dir = "../chroma_db"
client = PersistentClient(path=persist_dir)
collection = client.get_or_create_collection(name="estonian_laws")

# === Load LLM
def load_llm(model_name="bigscience/bloomz-1b1"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

qa_pipeline = load_llm()

# === RAG Query Function
def query_rag(question, top_k=3):
    # Step 1: Embed the question
    question_embedding = embedding_model.encode(question).tolist()

    # Step 2: Query the vector DB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    # Step 3: Combine retrieved texts
    retrieved_chunks = results["documents"][0]
    context = "\n".join(retrieved_chunks)

    # Step 4: Build prompt
    prompt = f"{context}\n\nKüsimus: {question}\nVastus:"

    # Step 5: Ask LLM
    response = qa_pipeline(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)[0]["generated_text"]

    return response

# === Example test
if __name__ == "__main__":
    question = "Millist teavet võib töödelda kaitseväekohustuse või kaitseväeteenistuse täitmiseks?"
    answer = query_rag(question)
    print("\n📌 Vastus:\n")
    print(answer)