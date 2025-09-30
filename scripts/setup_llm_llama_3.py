from llama_cpp import Llama

def load_llm(model_path="E:\\EST_LAW_RAG\\models\\llama-3-8b-instruct.Q4_K_M.gguf"):
    print("Loading LLaMA model...")
    llm = Llama(model_path=model_path, n_ctx=4096, n_threads=12)
    return llm