import sys
import os

# Make sure we can import from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from rag_pipeline import query_rag

questions = [
    "Loetle, mis sorti riigisaladusi on olemas?",
    "Millised on ajateenistuse kestused?",
    "Mis on Kaitseliidu ülesanded?",
]

for q in questions:
    print(f"\n📌 Küsimus: {q}")
    answer = query_rag(q)
    print(f"🧠 Vastus: {answer}")