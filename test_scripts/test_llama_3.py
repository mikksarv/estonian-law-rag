import sys
import os

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.append(script_dir)

from setup_llm_llama_3 import load_llm

def main():
    llm = load_llm()

    questions = [
        "Mida ma saan sinult küsida?",
        "Kes on ülem?"
    ]

    for q in questions:
        print(f"\n📌 Küsimus: {q}")
        prompt = f"### Instruction:\n{q}\n\n### Response:"
        response = llm(prompt, max_tokens=200)
        print(f"🧠 Vastus:\n{response['choices'][0]['text'].strip()}")

if __name__ == "__main__":
    main()