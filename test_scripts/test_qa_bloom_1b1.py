import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.rag_pipeline import query_rag

question = "Millist teavet võib töödelda kaitseväekohustuse või kaitseväeteenistuse täitmiseks?"
answer = query_rag(question)

print("\n📌 Vastus:\n")
print(answer)