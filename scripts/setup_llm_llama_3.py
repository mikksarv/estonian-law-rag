from llama_cpp import Llama
import sys
import os
from contextlib import contextmanager

# === Suppress both stdout and stderr
@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

# === Load the LLaMA model
def load_llm(model_path="E:\\EST_LAW_RAG\\models\\llama-3-8b-instruct.Q4_K_M.gguf"):
    print("Loading LLaMA model...")
    llm = Llama(model_path=model_path, n_ctx=4096, n_threads=12)
    return llm

suppress_llama_logs = suppress_output