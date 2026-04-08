"""
E-ZERO — TEST LOCAL v5.0 (PLASTICITÉ & APPRENTISSAGE)
====================================================
Author : Sawadogo Anselme
Version: 5.0 — April 2026

Ce script teste l'apprentissage de E-ZERO localement sans API.
Il simule des succès pour remplir la mémoire synaptique (ezero_memory.json).
"""

import re
from ezero_filter import EZeroFilter, EZeroConfig

# ── Configuration et Données ──────────────────────────────────────────────────
config = EZeroConfig(n_min=5, rho_target=0.3)
ezero  = EZeroFilter(config=config)

BBH_QUESTIONS = {
    "causal_judgement": [
        "Did the malfunction cause the machine to produce a red marble?",
        "Did Suzy cause Billy to not get a raise?"
    ],
    "date_understanding": [
        "Today is Christmas Eve of 1937. What is the date 10 days ago?",
        "Tomorrow is 11/12/2019. What is the date one year ago?"
    ],
    "recycling_logic": [
        "A recycling center collects 1200kg of waste. 30% is iron and 20% is aluminum.",
        "If a battery has 5000mAh and a device consumes 200mA, how long lasts?"
    ]
}

def evaluate_simple(original, skeleton):
    """Vérification rigoureuse des nombres (Essentiel pour PeP Recycling)."""
    numbers_orig = set(re.findall(r'\d+', original))
    numbers_skel = set(re.findall(r'\d+', skeleton))
    return "✅ OK" if numbers_orig.issubset(numbers_skel) else "❌ PERTE"

# ── BOUCLE DE TEST AVEC APPRENTISSAGE ─────────────────────────────────────────
print("\n" + "═"*75)
print(" 🧬  E-ZERO v5.0 — SIMULATION D'APPRENTISSAGE SYNAPTIQUE")
print("═"*75)
print(f"{'ID':<3} | {'GAIN':<7} | {'MÉMOIRE':<15} | SQUELETTE")
print("─"*75)

count = 1
for task, questions in BBH_QUESTIONS.items():
    for q in questions:
        # 1. Action du filtre
        r = ezero.filter(q)
        qual = evaluate_simple(q, r['skeleton'])
        
        # 2. Affichage avant apprentissage
        mem_info = f"S:{r['plasticity']['synapses']} A:{r['plasticity']['antibodies']}"
        print(f"{count:<3} | {r['gain_pct']:>5}% | {mem_info:<15} | {r['skeleton'][:45]}...")
        
        # 3. BOUCLE DE RÉTROACTION (L'organisme apprend ici)
        # On simule un score de 100 si la qualité est OK, sinon 0 pour créer des anticorps
        score = 100 if qual == "✅ OK" else 0
        ezero.feedback_loop(q, score)
        
        count += 1

# ── Résumé de la croissance ───────────────────────────────────────────────────
final_res = ezero.filter("Final check")
print("─"*75)
print(f" ✅  CRÉATION DE MÉMOIRE TERMINÉE")
print(f" 🧠  Synapses formées : {final_res['plasticity']['synapses']}")
print(f" 🛡️  Anticorps créés  : {final_res['plasticity']['antibodies']}")
print(f" 📂  Fichier généré   : ezero_memory.json")
print("═"*75)