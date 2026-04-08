import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ezero_filter import EZeroFilter, EZeroConfig
from test_data import GSM8K_SAMPLE

# 1. Chargement de la clé depuis le .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERREUR : GOOGLE_API_KEY introuvable dans le fichier .env")
    exit()

# 2. Configuration avec le nouveau SDK google.genai
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.0-flash"

def get_gemini_answer(prompt, max_retries=4):
    """Envoie le squelette et récupère la réponse de l'IA, avec retry anti-429."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=f"Decipher and solve this compressed math problem: {prompt}",
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=150,
                )
            )
            return response.text
        except Exception as e:
            err = str(e)
            if "429" in err:
                wait = 40 * (attempt + 1)  # 40s, 80s, 120s, 160s
                print(f"  ⚠️  Quota 429 — pause de {wait}s (essai {attempt+1}/{max_retries})...")
                time.sleep(wait)
            else:
                return f"Erreur API: {err}"
    return "❌ ÉCHEC après plusieurs tentatives (quota épuisé)"

def start_benchmark():
    config = EZeroConfig(n_min=5)
    ezero = EZeroFilter(config=config)

    print("\n" + "═"*80)
    print(" 🚀  BENCHMARK E-ZERO : TEST DE FIDÉLITÉ (VERSION STABLE)")
    print("═"*80)

    for i, question in enumerate(GSM8K_SAMPLE):
        # Phase 1 : Extraction du squelette
        result = ezero.filter(question)
        skeleton = result['skeleton']
        gain_val = result['gain_pct']

        print(f"\n[TEST ID {i+1}] | GAIN : {gain_val}%")
        print(f"SQUELETTE EXTRAIT : {skeleton}")

        # Phase 2 : Appel Gemini avec retry automatique
        ai_rep = get_gemini_answer(skeleton)
        print(f"RÉPONSE DE GEMINI : {ai_rep.strip()}")
        print("─" * 50)

        # Pause préventive entre les questions
        if i < len(GSM8K_SAMPLE) - 1:
            print("  ⏳ Pause 5s avant la prochaine question...")
            time.sleep(5)

    print("\n" + "═"*80)
    print(" ✅  BENCHMARK TERMINÉ")
    print("═"*80)

if __name__ == "__main__":
    start_benchmark()