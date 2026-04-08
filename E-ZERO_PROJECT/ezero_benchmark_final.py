import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ezero_filter import EZeroFilter, EZeroConfig

# 1. CHARGEMENT DE L'ENVIRONNEMENT
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_ID = "gemini-2.0-flash"

if not API_KEY:
    print("❌ ERREUR : Clé API introuvable dans le fichier .env")
    exit()

# 2. CONFIGURATION DU CLIENT ET DU FILTRE
client = genai.Client(api_key=API_KEY)
# L'organisme charge automatiquement ezero_memory.json s'il existe
ezero = EZeroFilter(EZeroConfig(n_min=5))

# 3. DATASET DE TEST UNIVERSEL (Maths, Logique, Dates)
TEST_SAMPLES = [
    "Janet has 3 quivers of 20 arrows each. She fires half of them. How many arrows does she have left?",
    "A container holds 1200 units of liquid. 30% is water and 20% is ethanol. What is the total volume of these two?",
    "Today is Christmas Eve of 1937. What is the date 10 days ago in MM/DD/YYYY?",
    "If a battery has 5000mAh and a device consumes 200mA per hour, how many hours will it last?",
    "Five people: Alice is in front of Bob. Bob is in front of Carol. Dave is behind Carol. Who is at the back?"
]

def get_gemini_answer(skeleton, max_retries=3):
    """Envoie le squelette à l'IA avec gestion des erreurs de quota."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=f"Solve this compressed problem. Provide only the final result: {skeleton}",
                config=types.GenerateContentConfig(temperature=0.1)
            )
            return response.text.strip()
        except Exception as e:
            err = str(e)
            if "429" in err:
                wait_time = 30 * (attempt + 1)
                print(f"  ⚠️ Quota atteint (429). Pause de {wait_time}s...")
                time.sleep(wait_time)
            else:
                return f"Erreur API: {err}"
    return "❌ ÉCHEC (Quota épuisé)"

# 4. EXÉCUTION DU BENCHMARK
def run_benchmark():
    print("\n" + "═"*80)
    print(" 🚀  E-ZERO v5.0 : BENCHMARK FINAL - VALIDATION DE FIDÉLITÉ")
    print("═"*80)
    print(f"{'ID':<3} | {'GAIN':<7} | {'SQUELETTE':<40} | {'RÉPONSE IA'}")
    print("─"*80)

    for i, q in enumerate(TEST_SAMPLES):
        # Phase A : Compression (Plasticité appliquée)
        res = ezero.filter(q)
        skel = res['skeleton']
        
        # Phase B : Appel API avec bride de sécurité
        ai_reply = get_gemini_answer(skel)
        
        # Affichage des résultats
        print(f"{i+1:<3} | {res['gain_pct']:>5}% | {skel[:37]:<40}... | {ai_reply}")

        # Phase C : Apprentissage continu
        if "Erreur" not in ai_reply and "ÉCHEC" not in ai_reply:
            ezero.feedback_loop(q, 100) # Renforce les mots qui ont mené au succès
        
        # --- BRIDE DE SÉCURITÉ RIGUREUSE ---
        # On attend 4.5 secondes pour rester sous la limite de 15 requêtes/minute
        time.sleep(4.5)

    print("─"*80)
    print(" ✅ BENCHMARK TERMINÉ.")
    print("═"*80)

if __name__ == "__main__":
    run_benchmark()