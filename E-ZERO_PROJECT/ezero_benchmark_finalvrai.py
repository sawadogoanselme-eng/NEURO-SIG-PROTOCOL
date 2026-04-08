import os
import time
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ezero_filter import EZeroFilter, EZeroConfig

# ── CONFIGURATION & CHARGEMENT ───────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_ID = "gemini-2.0-flash" 

if not API_KEY:
    print("❌ ERREUR : Clé API introuvable dans le fichier .env")
    exit()

client = genai.Client(api_key=API_KEY)
ezero = EZeroFilter(EZeroConfig(n_min=5))

# DATASET DE TEST (GSM8K & LOGIQUE)
TEST_SAMPLES = [
    "Janet has 3 quivers of 20 arrows each. She fires half of them. How many arrows does she have left?",
    "A recycling center collects 1200kg of waste. 30% is iron and 20% is aluminum. What is the total mass of metals?",
    "Today is Christmas Eve of 1937. What is the date 10 days ago in MM/DD/YYYY?",
    "If a battery has 5000mAh and a device consumes 200mA per hour, how many hours will it last?"
]

def get_gemini_answer(skeleton):
    """Envoie le squelette à l'IA avec une instruction de décompression."""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=f"Solve this compressed problem. Provide only the final numerical answer: {skeleton}",
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text.strip()
    except Exception as e:
        return f"Erreur API: {str(e)}"

# ── EXÉCUTION DU BENCHMARK ────────────────────────────────────────────────────
print("\n" + "═"*80)
print(" 🚀  E-ZERO v5.0 : BENCHMARK FINAL (API RÉELLE)")
print("═"*80)
print(f"{'ID':<3} | {'GAIN':<7} | {'SQUELETTE':<45} | {'RÉPONSE IA'}")
print("─"*80)

for i, q in enumerate(TEST_SAMPLES):
    # 1. Compression via l'organisme entraîné
    res = ezero.filter(q)
    skel = res['skeleton']
    
    # 2. Appel API
    ai_reply = get_gemini_answer(skel)
    
    # 3. Affichage des résultats
    print(f"{i+1:<3} | {res['gain_pct']:>5}% | {skel[:42]:<45} | {ai_reply}")

    # 4. Feedback (Optionnel : continue d'apprendre pendant le benchmark)
    # Si l'IA répond (pas d'erreur), on renforce la synapse
    if "Erreur" not in ai_reply:
        ezero.feedback_loop(q, 100)
    
    # Pause de sécurité pour éviter le quota 429
    time.sleep(2)

print("─"*80)
print(" ✅ BENCHMARK TERMINÉ. Vérifie la précision des réponses de l'IA.")
print("═"*80)