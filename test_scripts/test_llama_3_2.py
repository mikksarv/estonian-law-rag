import sys
import os

# Make sure we can import from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from rag_pipeline import query_rag

questions = [
    "Mis juhtub reservis oleva isikuga või reservväelasega, kui arstlik komisjon tunnistab ta tegevteenistuseks mittekõlblikuks?",
    "Mis täpsusega arvestatakse kaitseväeteenistuse staaž tegevteenistusstaaži hulka?",
    "Loetle, mis on täiendõppe kulu arvestamise aluseks loetud kulud?",
]

for q in questions:
    print(f"\n📌 Küsimus: {q}")
    answer = query_rag(q)
    print(f"🧠 Vastus: {answer}")