"""
E-ZERO — TEST BBH v4
======================
Author : Sawadogo Anselme
Version: 4.0 — April 2026

Tâches BBH testées :
  - causal_judgement
  - date_understanding
  - reasoning_about_colored_objects
  - logical_deduction_five_objects

Nouveautés v4 :
  - Utilise ezero_filter v4 (protection négations + mode contextuel)
  - Retry anti-429 avec pauses progressives (40s, 80s, 120s)
  - Pauses longues entre chaque appel pour éviter le rate limit
  - Affichage du mode détecté par E-ZERO
  - Sauvegarde JSON des résultats
"""

import os
import time
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datasets import load_dataset
from ezero_filter import EZeroFilter, EZeroConfig

# ── Chargement de la clé API ─────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ ERREUR : GOOGLE_API_KEY introuvable dans le .env")
    exit()

client = genai.Client(api_key=api_key)
MODEL  = "gemini-2.0-flash"

# ── Initialisation E-ZERO v4 ─────────────────────────────────────────────────
config = EZeroConfig(n_min=5, rho_target=0.3)
ezero  = EZeroFilter(config=config)

# ── Tâches BBH à tester ──────────────────────────────────────────────────────
# Commencer par 1 seule tâche pour économiser le quota
# Décommenter les autres quand le quota est stable
TASKS = [
    "causal_judgement",
    # "date_understanding",
    # "reasoning_about_colored_objects",
    # "logical_deduction_five_objects",
]

# ── Appel Gemini avec retry anti-429 ─────────────────────────────────────────
def ask_gemini(prompt: str, max_retries: int = 4) -> str:
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=f"Answer with the exact option letter or word only, no explanation:\n{prompt}",
                config=types.GenerateContentConfig(temperature=0)
            )
            return response.text.strip().lower()
        except Exception as e:
            err = str(e)
            if "429" in err:
                wait = 40 * (attempt + 1)
                print(f"    ⚠️  Quota 429 — pause {wait}s (essai {attempt+1}/{max_retries})...")
                time.sleep(wait)
            else:
                return f"ERROR: {e}"
    return "FAILED_AFTER_RETRIES"

# ── Lancement du test ─────────────────────────────────────────────────────────
print("\n" + "="*70)
print("  🕸️  E-ZERO v4 — TEST BBH (SAFE MODE)")
print("="*70)

all_results   = []
total_matches = 0
total_tests   = 0

for task_name in TASKS:
    print(f"\n🕷️  Tâche : {task_name}")
    print("-" * 50)

    try:
        ds = load_dataset("lukaemon/bbh", task_name, split="test").select(range(5))
    except Exception as e:
        print(f"  ❌ Impossible de charger {task_name} : {e}")
        continue

    task_matches = 0

    for i, item in enumerate(ds):
        q      = item["input"]
        target = item.get("target", "?").strip().lower()

        # Filtrage E-ZERO v4
        filter_result = ezero.filter(q)
        skel = filter_result["skeleton"]
        mode = filter_result.get("mode", "?")
        gain = filter_result["gain_pct"]

        print(f"\n  [{i+1}/5] Mode : {mode} | Gain : {gain}%")
        print(f"  Original  : {q[:80]}...")
        print(f"  Squelette : {skel[:80]}...")

        # Appel 1 : prompt original
        res_a = ask_gemini(q)
        time.sleep(30)  # Pause longue anti-429

        # Appel 2 : squelette E-ZERO
        res_b = ask_gemini(skel)
        time.sleep(30)  # Pause longue anti-429

        # Comparaison
        is_match     = (res_a == res_b) and ("ERROR" not in res_a) and ("FAILED" not in res_a)
        orig_correct = (res_a == target)
        skel_correct = (res_b == target)

        if is_match:
            task_matches  += 1
            total_matches += 1
        total_tests += 1

        status = "✅ MATCH" if is_match else "❌ DIFF"
        print(f"  Cible     : {target}")
        print(f"  Original  → {res_a[:20]} | Squelette → {res_b[:20]} | {status}")
        print(f"  Orig OK: {'✅' if orig_correct else '❌'}  |  Skel OK: {'✅' if skel_correct else '❌'}")

        all_results.append({
            "task":         task_name,
            "mode":         mode,
            "gain_pct":     gain,
            "tokens_in":    filter_result["tokens_in"],
            "tokens_out":   filter_result["tokens_out"],
            "target":       target,
            "answer_orig":  res_a,
            "answer_skel":  res_b,
            "is_match":     is_match,
            "orig_correct": orig_correct,
            "skel_correct": skel_correct,
        })

    task_score = (task_matches / 5) * 100
    print(f"\n  📊 {task_name} — Fidélité : {task_score}%")

# ── Résultats finaux ──────────────────────────────────────────────────────────
fidelity = (total_matches / total_tests * 100) if total_tests > 0 else 0

print("\n" + "="*70)
print("  RÉSULTATS FINAUX E-ZERO v4 — BBH")
print("="*70)
print(f"  Tests effectués  : {total_tests}")
print(f"  Matches          : {total_matches}")
print(f"  FIDÉLITÉ GLOBALE : {fidelity:.1f}%")

if fidelity >= 90:
    print("  ✅ EXCELLENT — E-ZERO v4 préserve le raisonnement BBH")
elif fidelity >= 75:
    print("  ⚠️  BON — Quelques ajustements possibles")
else:
    print("  ❌ À améliorer — certains types de tâches posent problème")

print("="*70)

# ── Sauvegarde JSON ───────────────────────────────────────────────────────────
output = {
    "version": "4.0",
    "date":    "2026-04-08",
    "model":   MODEL,
    "tasks":   TASKS,
    "summary": {
        "total_tests":   total_tests,
        "total_matches": total_matches,
        "fidelity_pct":  round(fidelity, 1),
    },
    "results": all_results,
}

with open("ezero_bbh_results_v4.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ Résultats sauvegardés dans : ezero_bbh_results_v4.json")
print("Test BBH terminé !")