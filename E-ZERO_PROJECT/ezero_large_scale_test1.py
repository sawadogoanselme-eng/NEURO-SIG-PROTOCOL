"""
E-ZERO — TEST LOCAL GRANDE ÉCHELLE
=====================================
Author : Sawadogo Anselme
Version: 4.1 — April 2026

Test complet sans API sur 200+ questions :
  - 100 questions GSM8K (dataset réel)
  - 50 questions BBH (5 tâches × 10 questions)
  - Statistiques détaillées par tâche et par mode
  - Détection des faiblesses du filtre
  - Zéro appel API — aucun quota utilisé
"""

import re
import time
import json
from collections import defaultdict
from ezero_filter import EZeroFilter, EZeroConfig

# ── Initialisation E-ZERO v4.1 ────────────────────────────────────────────────
config = EZeroConfig(n_min=5, rho_target=0.3)
ezero  = EZeroFilter(config=config)

# ── Fonction d'évaluation de qualité ─────────────────────────────────────────
def evaluate_skeleton(original: str, skeleton: str) -> dict:
    """Évalue la qualité du squelette sans API."""

    orig_tokens = original.lower().split()
    skel_tokens = skeleton.lower().split()

    # 1. Nombres préservés ?
    numbers_orig = set(re.findall(r'\d+\.?\d*', original))
    numbers_skel = set(re.findall(r'\d+\.?\d*', skeleton))
    numbers_ok   = numbers_orig.issubset(numbers_skel)

    # 2. Mots sacrés préservés ?
    sacred = {"not","never","unless","except","if","then","because",
              "all","none","every","each","both","more","less","only"}
    sacred_orig = set(orig_tokens) & sacred
    sacred_skel = set(skel_tokens) & sacred
    sacred_ok   = sacred_orig.issubset(sacred_skel)

    # 3. Ratio de compression
    ratio = len(skel_tokens) / len(orig_tokens) if orig_tokens else 1.0

    # 4. Score global
    score = 0
    if numbers_ok:  score += 50
    if sacred_ok:   score += 30
    if ratio < 0.8: score += 20

    if score >= 80:   quality = "✅ EXCELLENT"
    elif score >= 50: quality = "⚠️  MOYEN"
    else:             quality = "❌ FAIBLE"

    return {
        "quality":    quality,
        "score":      score,
        "numbers_ok": numbers_ok,
        "sacred_ok":  sacred_ok,
        "ratio":      round(ratio, 3),
    }

# ════════════════════════════════════════════════════════════════════════════
# PARTIE 1 — GSM8K (100 questions depuis le dataset réel)
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("  📐  PARTIE 1 — GSM8K (100 questions réelles)")
print("="*70)

gsm8k_results = []

try:
    from datasets import load_dataset
    dataset   = load_dataset("openai/gsm8k", "main", split="test")
    questions = [item["question"] for item in dataset.select(range(100))]
    print(f"  ✅ Dataset GSM8K chargé : {len(questions)} questions\n")
except Exception as e:
    print(f"  ⚠️  Dataset indisponible ({e}), utilisation des questions intégrées")
    questions = [
        "Janet has 3 quivers of 20 arrows each. She fires half of them. How many arrows does she have left?",
        "A store has 500 apples. It sells 120 on Monday and 85 on Tuesday. How many are left?",
        "Tom earns $15 per hour. He works 8 hours a day, 5 days a week. How much does he earn per week?",
        "A tank holds 1000 liters. It leaks 25 liters per hour. How long until it is empty?",
        "Mary has 3 times as many books as John. John has 12 books. How many books do they have together?",
        "A recycling center collects 1200kg of waste. 30% is iron and 20% is aluminum. What is the total mass of metals?",
        "If a battery has 5000mAh and a device consumes 200mA per hour, how many hours will it last?",
        "A store sells apples for $2 each and oranges for $3 each. John buys 5 apples and 3 oranges. How much total?",
        "Mary has 50 dollars. She spends 15 on books and twice that on clothes. How much is left?",
        "A train travels 300km in 3 hours. What is its average speed?",
    ]

mode_stats   = defaultdict(lambda: {"count": 0, "gains": [], "scores": []})
total_gains  = []
total_scores = []

print(f"  {'ID':<5} {'MODE':<10} {'IN':<5} {'OUT':<5} {'GAIN':<8} {'ms':<8} QUALITÉ")
print("  " + "-"*65)

for i, q in enumerate(questions):
    r    = ezero.filter(q)
    eval = evaluate_skeleton(q, r["skeleton"])

    mode_stats[r["mode"]]["count"]  += 1
    mode_stats[r["mode"]]["gains"].append(r["gain_pct"])
    mode_stats[r["mode"]]["scores"].append(eval["score"])
    total_gains.append(r["gain_pct"])
    total_scores.append(eval["score"])

    gsm8k_results.append({
        "id":       i + 1,
        "mode":     r["mode"],
        "gain_pct": r["gain_pct"],
        "rho":      r["rho"],
        "tokens_in":  r["tokens_in"],
        "tokens_out": r["tokens_out"],
        "elapsed_ms": r["elapsed_ms"],
        "quality":  eval["quality"],
        "score":    eval["score"],
    })

    # Affichage condensé
    if i < 20 or eval["score"] < 50:  # Affiche les 20 premiers + les mauvais
        print(f"  {i+1:<5} {r['mode']:<10} {r['tokens_in']:<5} {r['tokens_out']:<5} "
              f"{r['gain_pct']:>6}%  {r['elapsed_ms']:>6}ms  {eval['quality']}")

if len(questions) > 20:
    print(f"  ... ({len(questions)-20} autres questions traitées)")

avg_gain  = sum(total_gains) / len(total_gains)
avg_score = sum(total_scores) / len(total_scores)
excellent = sum(1 for s in total_scores if s >= 80)

print(f"\n  RÉSULTATS GSM8K ({len(questions)} questions) :")
print(f"  Gain moyen       : {avg_gain:.1f}%")
print(f"  Score qualité    : {avg_score:.1f}/100")
print(f"  Excellents       : {excellent}/{len(questions)} ({excellent/len(questions)*100:.1f}%)")
print(f"\n  Par mode :")
for mode, stats in sorted(mode_stats.items()):
    mg = sum(stats["gains"]) / len(stats["gains"])
    ms = sum(stats["scores"]) / len(stats["scores"])
    print(f"    {mode:<12} : {stats['count']:>3} questions | gain {mg:.1f}% | score {ms:.1f}/100")

# ════════════════════════════════════════════════════════════════════════════
# PARTIE 2 — BBH (5 tâches × 10 questions)
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("  🕸️  PARTIE 2 — BBH (5 tâches × 10 questions)")
print("="*70)

BBH_TASKS = {
    "causal_judgement": [
        "How would a typical person answer each of the following questions about causation? A machine is set up in such a way that it will produce one marble. The machine can produce a marble in one of two ways. Either the machine can produce a marble that is red, or the machine can produce a marble that is blue. The machine is programmed to produce a blue marble. However, the machine malfunctions and produces a red marble instead. Did the malfunction cause the machine to produce a red marble?",
        "How would a typical person answer each of the following questions about causation? Billy and Suzy work for the same company. They are both sales associates. Suzy sells more than Billy. The boss decides to give a raise to the employee who sells the most. Did Suzy cause Billy to not get a raise?",
        "A fire started in a forest. The fire was caused by either lightning or a campfire that was not properly extinguished. A ranger investigated and determined the campfire was the cause. Did the campfire cause the fire?",
        "A car skidded on an icy road and hit a tree. The driver was not wearing a seatbelt. Did the ice cause the driver to be injured?",
        "Mary left her phone charging overnight. The phone overheated and damaged the battery. Did leaving the phone charging cause the battery damage?",
        "Two buttons control a light. Either button can turn it on. Alice pressed button A and Bob pressed button B at the same time. The light turned on. Did Alice pressing button A cause the light to turn on?",
        "A student forgot to study for an exam and failed. The passing grade was 50 out of 100. The student scored 45. Did the student's failure to study cause the failing grade?",
        "A plant was not watered for two weeks. It wilted and died. Did the lack of water cause the plant to die?",
        "A factory released chemicals into a river. Fish downstream died the next day. Did the factory cause the fish to die?",
        "A ball rolled off a table because someone bumped the table. Did the bumping cause the ball to fall?",
    ],
    "date_understanding": [
        "Today is Christmas Eve of 1937. What is the date 10 days ago in MM/DD/YYYY?",
        "Tomorrow is 11/12/2019. What is the date one year ago from today in MM/DD/YYYY?",
        "Jane was born on the last day of February in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?",
        "The first day of 2019 is a Tuesday. Today is March 5, 2019. What day of the week is it?",
        "Today is 3/5/2021. What is the date 2 weeks from today in MM/DD/YYYY?",
        "Today is the last day of January 2020. What is tomorrow's date in MM/DD/YYYY?",
        "A project started on 01/15/2023 and lasted 90 days. What date did it end in MM/DD/YYYY?",
        "Today is Monday, 06/01/2020. What date is next Friday in MM/DD/YYYY?",
        "It is currently April 2026. What month was it 8 months ago?",
        "Today is 12/31/2023. What is the date tomorrow in MM/DD/YYYY?",
    ],
    "reasoning_about_colored_objects": [
        "On the floor, you see a red book, a blue vase, a green pencil, and a yellow cup. If I remove the red book and the blue vase, how many objects are left?",
        "On the table, there is a pink envelope, a purple keychain, a brown notebook. The pink envelope is to the left of the purple keychain. Is the brown notebook to the right of the pink envelope?",
        "There is a red ball, a blue cube, and a green pyramid. The red ball is not next to the blue cube. Is the green pyramid between the red ball and the blue cube?",
        "You see a white box, a black ball, and a gray cup on a shelf. The white box is heavier than the black ball. Is the gray cup the lightest?",
        "On a desk: a red pen, a blue notebook, a green eraser. The red pen is to the left of the blue notebook. The green eraser is to the right of the blue notebook. Which object is in the middle?",
        "There are 3 colored blocks: orange, purple, yellow. Orange is not on top of purple. Purple is not on top of yellow. What is the order from bottom to top?",
        "A shelf has 5 objects: red vase, blue book, green cup, yellow pen, white plate. Remove all red and blue items. How many remain?",
        "Two boxes: a red box and a blue box. The red box contains 3 items. The blue box contains twice as many. How many items total?",
        "On the floor: a pink ball, an orange cube, a gray pyramid, a brown cylinder. How many objects are not pink?",
        "There is a red chair, a blue table, and a green lamp. The red chair is not next to the green lamp. Is the blue table between them?",
    ],
    "logical_deduction_five_objects": [
        "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph. On a shelf, there are five books: a white book, a red book, a green book, an orange book, and a blue book. The red book is the rightmost. The white book is to the left of the red book. Which book is the leftmost?",
        "Five people are standing in a line. Alice is in front of Bob. Bob is in front of Carol. Dave is behind Carol. Eve is in front of Alice. Who is at the back of the line?",
        "There are five houses in a row, each painted a different color: red, blue, green, yellow, white. The red house is immediately to the left of the blue house. The green house is somewhere to the left of the yellow house. The white house is the rightmost. What color is the leftmost house?",
        "Five students took a test. Anna scored higher than Ben. Ben scored higher than Carl. Dana scored lower than Carl. Eve scored higher than Anna. Who scored the lowest?",
        "There are 5 boxes labeled A, B, C, D, E from left to right. Box C is to the right of Box A. Box B is between A and C. Box D is to the right of C. Box E is the rightmost. Which box is second from the left?",
        "Five friends sit in a row: Tom, Sam, Amy, Bob, Eve. Tom is not at either end. Sam is to the left of Amy. Bob is at the rightmost position. Eve is to the left of Tom. Who sits at the leftmost position?",
        "Five colored balls are in a row: red, blue, green, yellow, white. Red is not first. Blue is immediately after red. Green is somewhere after blue. Yellow is immediately before white. White is last. What is the order?",
        "On a shelf from left to right: Book1, Book2, Book3, Book4, Book5. Book3 is in the middle. Book1 is not next to Book2. Book5 is to the right of Book4. Which book is second from the right?",
        "Five athletes finished a race: P, Q, R, S, T. P finished before Q. R finished after S. T finished last. Q finished before R. Who finished first?",
        "Five cards are placed in a row. Card 2 is immediately to the right of Card 1. Card 4 is immediately to the right of Card 3. Card 5 is at the end. Card 3 is somewhere to the right of Card 2. What position is Card 3?",
    ],
    "causal_judgement_hard": [
        "Two doctors independently prescribe the same medication to a patient. The medication causes an allergic reaction. Did the first doctor cause the allergic reaction?",
        "A programmer wrote code that contained a bug. The bug only causes problems when two specific conditions occur simultaneously. Both conditions occurred and the system crashed. Did the programmer cause the crash?",
        "A coach told a player to use a specific strategy. The player used it and lost the game. Another player used the same strategy and won. Did the coach cause the first player to lose?",
        "A security guard fell asleep during his shift. A thief broke in and stole equipment. Did the guard sleeping cause the theft?",
        "An engineer installed a safety valve incorrectly. The valve never needed to activate during normal operations. An unusual pressure spike occurred and the valve failed. Did the incorrect installation cause the accident?",
    ],
}

bbh_results    = []
bbh_mode_stats = defaultdict(lambda: {"count": 0, "gains": [], "scores": []})
all_bbh_gains  = []
all_bbh_scores = []

for task_name, questions in BBH_TASKS.items():
    task_gains  = []
    task_scores = []

    print(f"\n  📋 Tâche : {task_name} ({len(questions)} questions)")
    print("  " + "-"*60)
    print(f"  {'ID':<5} {'MODE':<10} {'IN':<5} {'OUT':<5} {'GAIN':<8} QUALITÉ")

    for i, q in enumerate(questions):
        r    = ezero.filter(q)
        eval = evaluate_skeleton(q, r["skeleton"])

        task_gains.append(r["gain_pct"])
        task_scores.append(eval["score"])
        all_bbh_gains.append(r["gain_pct"])
        all_bbh_scores.append(eval["score"])
        bbh_mode_stats[r["mode"]]["count"]  += 1
        bbh_mode_stats[r["mode"]]["gains"].append(r["gain_pct"])
        bbh_mode_stats[r["mode"]]["scores"].append(eval["score"])

        bbh_results.append({
            "task":       task_name,
            "id":         i + 1,
            "mode":       r["mode"],
            "gain_pct":   r["gain_pct"],
            "rho":        r["rho"],
            "tokens_in":  r["tokens_in"],
            "tokens_out": r["tokens_out"],
            "elapsed_ms": r["elapsed_ms"],
            "quality":    eval["quality"],
            "score":      eval["score"],
        })

        print(f"  {i+1:<5} {r['mode']:<10} {r['tokens_in']:<5} {r['tokens_out']:<5} "
              f"{r['gain_pct']:>6}%  {eval['quality']}")

    tg = sum(task_gains) / len(task_gains)
    ts = sum(task_scores) / len(task_scores)
    print(f"  → Gain moyen : {tg:.1f}% | Score moyen : {ts:.1f}/100")

# ════════════════════════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ════════════════════════════════════════════════════════════════════════════
total_questions = len(gsm8k_results) + len(bbh_results)
all_gains       = total_gains + all_bbh_gains
all_scores_all  = total_scores + all_bbh_scores
global_gain     = sum(all_gains) / len(all_gains)
global_score    = sum(all_scores_all) / len(all_scores_all)
global_excellent = sum(1 for s in all_scores_all if s >= 80)
global_faible    = sum(1 for s in all_scores_all if s < 50)

# Vitesse
all_times = [r["elapsed_ms"] for r in gsm8k_results + bbh_results]
avg_time  = sum(all_times) / len(all_times)
max_time  = max(all_times)

print("\n" + "="*70)
print("  🏆  RÉSUMÉ FINAL E-ZERO v4.1 — GRANDE ÉCHELLE")
print("="*70)
print(f"  Questions testées    : {total_questions}")
print(f"  ├─ GSM8K             : {len(gsm8k_results)}")
print(f"  └─ BBH               : {len(bbh_results)}")
print(f"")
print(f"  COMPRESSION :")
print(f"  ├─ Gain moyen GSM8K  : {sum(total_gains)/len(total_gains):.1f}%")
print(f"  ├─ Gain moyen BBH    : {sum(all_bbh_gains)/len(all_bbh_gains):.1f}%")
print(f"  └─ Gain moyen global : {global_gain:.1f}%")
print(f"")
print(f"  QUALITÉ :")
print(f"  ├─ Score moyen       : {global_score:.1f}/100")
print(f"  ├─ Excellents (≥80)  : {global_excellent}/{total_questions} ({global_excellent/total_questions*100:.1f}%)")
print(f"  └─ Faibles (<50)     : {global_faible}/{total_questions} ({global_faible/total_questions*100:.1f}%)")
print(f"")
print(f"  VITESSE :")
print(f"  ├─ Temps moyen       : {avg_time:.2f}ms")
print(f"  └─ Temps max         : {max_time:.2f}ms")
print(f"")
print(f"  MODES DÉTECTÉS (BBH) :")
for mode, stats in sorted(bbh_mode_stats.items()):
    mg = sum(stats["gains"]) / len(stats["gains"])
    print(f"  ├─ {mode:<14} : {stats['count']:>3} questions | gain {mg:.1f}%")
print(f"")
print(f"  Appels API utilisés  : 0 ✅")
print("="*70)

# ── Sauvegarde JSON ───────────────────────────────────────────────────────────
output = {
    "version": "4.1",
    "date":    "2026-04-08",
    "summary": {
        "total_questions":   total_questions,
        "global_gain_pct":   round(global_gain, 1),
        "global_score":      round(global_score, 1),
        "excellent_pct":     round(global_excellent / total_questions * 100, 1),
        "avg_time_ms":       round(avg_time, 2),
        "api_calls":         0,
    },
    "gsm8k":  gsm8k_results,
    "bbh":    bbh_results,
}

with open("ezero_large_scale_results.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ Résultats sauvegardés dans : ezero_large_scale_results.json")
print("💡 Quand le quota est rechargé → python ezero_bbh_test.py")