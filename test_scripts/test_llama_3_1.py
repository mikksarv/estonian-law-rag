import sys
import os

script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.append(script_dir)

from setup_llm_llama_3 import load_llm

def test_prompt_control():
    llm = load_llm()

    # Fake “context” — a small legal statement
    context = "Kaitseväelane peab järgima kaitseväeteenistuse seadust."

    # A question you expect a custom answer for
    question = "Kes on ülem?"

    # Build your strict prompt
    prompt = f"""
### Näide:
Kontekst:
Ülem on isik, kellele on teenistuslikult allutatud teised kaitseväelased.

Küsimus:
Kes on ülem?

Vastus:
Ülem on kaitseväelane, kes juhib talle allutatud kaitseväelasi.

### Kontekst:
{context}

### Küsimus:
{question}

### Vastus:
"""

    print("=== Prompt to LLaMA ===")
    print(prompt)
    resp = llm(prompt, max_tokens=100, stop=["###"])
    answer = resp["choices"][0]["text"].strip()
    print("=== Answer from LLaMA ===")
    print(answer)

if __name__ == "__main__":
    test_prompt_control()
