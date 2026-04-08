import os
import time
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai  # Correction de l'import

# 1. Chargement de la clé API
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Erreur : GOOGLE_API_KEY non trouvée dans le .env")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Import du filtre E-ZERO v2.2
from ezero_filter import EZeroFilter
ezero = EZeroFilter()

def ask_gemini(prompt):
    """Envoie une requête à Gemini avec gestion du quota (429)."""
    for attempt in range(3):
        try:
            response = model.generate_content(f"Answer briefly: {prompt}")
            return response.text.strip().lower()
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Quota atteint... Pause de 10s (Essai {attempt+1}/3)")
                time.sleep(10)
            else:
                return f"ERROR: {e}"
    return "FAILED"

# 3. Simulation de test BBH
test_questions = [
    "If Jean arrives before Marie, and Marie arrives before Luc, who arrives first?",
    "Is the following statement true: 'The object is not red' implies it is blue?",
    "A box contains 3 red balls and 2 blue balls. If I take one, is it not red?"
]

print("\n--- VALIDATION RÉELLE E-ZERO V2.2 ---")
results = []
matches = 0

for i, q in enumerate(test_questions):
    print(f"\nTest {i+1}/3 en cours...")
    
    # Filtrage v2.2 (Aimant Logique)
    res_filter = ezero.filter(q)
    skeleton = res_filter["skeleton"]
    
    # Appel API
    ans_orig = ask_gemini(q)
    time.sleep(2) # Sécurité quota
    ans_skel = ask_gemini(skeleton)
    
    match = (ans_orig == ans_skel)
    if match: matches += 1
    
    print(f"Original : {q}")
    print(f"Skeleton : {skeleton}")
    print(f"Match    : {'✅ OUI' if match else '❌ NON'}")
    time.sleep(2)

final_fidelity = (matches / len(test_questions)) * 100
print(f"\n=====================================")
print(f"FIDÉLITÉ RÉELLE V2.2 : {final_fidelity}%")
print(f"=====================================")