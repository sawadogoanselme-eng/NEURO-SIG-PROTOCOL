"""
E-ZERO — TEST LOCAL SANS API
==============================
Author : Sawadogo Anselme
Version: 4.0 — April 2026

Ce script teste le filtre E-ZERO localement sans aucun appel API.
Il affiche :
  - Le mode détecté pour chaque question
  - Le squelette extrait
  - Le gain de compression
  - Une évaluation manuelle de la qualité du squelette

Aucun quota, aucun 429, fonctionne offline.
"""

from ezero_filter import EZeroFilter, EZeroConfig

# ── Questions de test BBH intégrées ──────────────────────────────────────────
BBH_QUESTIONS = {
    "causal_judgement": [
        "How would a typical person answer each of the following questions about causation? A machine is set up in such a way that it will produce one marble. The machine can produce a marble in one of two ways. Either the machine can produce a marble that is red, or the machine can produce a marble that is blue. The machine is programmed to produce a blue marble. However, the machine malfunctions and produces a red marble instead. Did the malfunction cause the machine to produce a red marble?",
        "How would a typical person answer each of the following questions about causation? Billy and Suzy work for the same company. They are both sales associates. Suzy sells more than Billy. The boss decides to give a raise to the employee who sells the most. Did Suzy cause Billy to not get a raise?",
        "A fire started in a forest. The fire was caused by either lightning or a campfire that was not properly extinguished. A ranger investigated and determined the campfire was the cause. Did the campfire cause the fire?",
    ],
    "date_understanding": [
        "Today is Christmas Eve of 1937. What is the date 10 days ago in MM/DD/YYYY?",
        "Tomorrow is 11/12/2019. What is the date one year ago from today in MM/DD/YYYY?",
        "Jane was born on the last day of February in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?",
    ],
    "reasoning_about_colored_objects": [
        "On the floor, you see a red book, a blue vase, a green pencil, and a yellow cup. If I remove the red book and the blue vase, how many objects are left?",
        "On the table, there is a pink envelope, a purple keychain, a brown notebook. The pink envelope is to the left of the purple keychain. Is the brown notebook to the right of the pink envelope?",
        "There is a red ball, a blue cube, and a green pyramid. The red ball is not next to the blue cube. Is the green pyramid between the red ball and the blue cube?",
    ],
    "logical_deduction_five_objects": [
        "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph. On a shelf, there are five books: a white book, a red book, a green book, an orange book, and a blue book. The red book is the rightmost. The white book is to the left of the red book. Which book is the leftmost?",
        "Five people are standing in a line. Alice is in front of Bob. Bob is in front of Carol. Dave is behind Carol. Eve is in front of Alice. Who is at the back of the line?",
        "There are five houses in a row, each painted a different color: red, blue, green, yellow, white. The red house is immediately to the left of the blue house. The green house is somewhere to the left of the yellow house. The white house is the rightmost. What color is the leftmost house?",
    ],
}

# ── Questions GSM8K intégrées ─────────────────────────────────────────────────
GSM8K_QUESTIONS = [
    "Janet has 3 quivers of 20 arrows each. She fires half of them at practice. How many arrows does she have left?",
    "A recycling center collects 1200kg of waste. 30% is iron and 20% is aluminum. What is the total mass of metals collected?",
    "If a battery has 5000mAh and a device consumes 200mA per hour, how many hours will it last?",
    "A store sells apples for $2 each and oranges for $3 each. John buys 5 apples and 3 oranges. How much does he spend in total?",
    "Mary has 50 dollars. She spends 15 dollars on books and twice that amount on clothes. How much money does she have left?",
]

# ── Initialisation E-ZERO v4 ──────────────────────────────────────────────────
config = EZeroConfig(n_min=5, rho_target=0.3)
ezero  = EZeroFilter(config=config)

# ── Fonction d'évaluation manuelle ───────────────────────────────────────────
def evaluate_skeleton(original: str, skeleton: str) -> str:
    """
    Évalue grossièrement la qualité du squelette.
    Vérifie si les mots clés mathématiques/logiques sont préservés.
    """
    import re
    # Extraire les nombres de l'original
    numbers_orig = set(re.findall(r'\d+\.?\d*', original))
    numbers_skel = set(re.findall(r'\d+\.?\d*', skeleton))
    numbers_ok   = numbers_orig == numbers_skel

    # Ratio de compression
    ratio = len(skeleton.split()) / len(original.split())

    if numbers_ok and ratio < 0.8:
        return "✅ BON"
    elif numbers_ok and ratio >= 0.8:
        return "⚠️  PEU COMPRESSÉ"
    else:
        return "❌ NOMBRES MANQUANTS"

# ── TEST GSM8K ────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("  🔬  E-ZERO v4 — TEST LOCAL GSM8K (SANS API)")
print("="*70)
print(f"{'ID':<4} | {'MODE':<10} | {'IN':<5} | {'OUT':<5} | {'GAIN':<8} | {'QUALITÉ':<20} | SQUELETTE")
print("-"*70)

gsm_gains = []
for i, q in enumerate(GSM8K_QUESTIONS):
    r    = ezero.filter(q)
    qual = evaluate_skeleton(q, r["skeleton"])
    gsm_gains.append(r["gain_pct"])
    print(f"{i+1:<4} | {r['mode']:<10} | {r['tokens_in']:<5} | {r['tokens_out']:<5} | {r['gain_pct']:>6}%  | {qual:<20} | {r['skeleton'][:50]}...")

avg_gsm = sum(gsm_gains) / len(gsm_gains)
print("-"*70)
print(f"  GAIN MOYEN GSM8K : {avg_gsm:.1f}%")

# ── TEST BBH ──────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("  🕸️  E-ZERO v4 — TEST LOCAL BBH (SANS API)")
print("="*70)

bbh_gains = []
for task_name, questions in BBH_QUESTIONS.items():
    print(f"\n📋 Tâche : {task_name}")
    print("-"*50)

    for i, q in enumerate(questions):
        r    = ezero.filter(q)
        qual = evaluate_skeleton(q, r["skeleton"])
        bbh_gains.append(r["gain_pct"])

        print(f"\n  [{i+1}/{len(questions)}]")
        print(f"  Mode     : {r['mode']}")
        print(f"  Gain     : {r['gain_pct']}% | {r['tokens_in']} → {r['tokens_out']} tokens | {r['elapsed_ms']}ms")
        print(f"  Qualité  : {qual}")
        print(f"  Original : {q[:90]}...")
        print(f"  Squelette: {r['skeleton'][:90]}...")

avg_bbh = sum(bbh_gains) / len(bbh_gains)

# ── Résumé final ──────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("  📊  RÉSUMÉ FINAL E-ZERO v4")
print("="*70)
print(f"  Questions GSM8K testées  : {len(GSM8K_QUESTIONS)}")
print(f"  Questions BBH testées    : {sum(len(v) for v in BBH_QUESTIONS.values())}")
print(f"  Gain moyen GSM8K         : {avg_gsm:.1f}%")
print(f"  Gain moyen BBH           : {avg_bbh:.1f}%")
print(f"  Gain moyen global        : {(avg_gsm + avg_bbh) / 2:.1f}%")
print(f"  Appels API utilisés      : 0 ✅")
print("="*70)
print("\n✅ Test local terminé — aucun quota utilisé !")
print("💡 Quand votre quota sera rechargé, lancez : python ezero_bbh_test.py")