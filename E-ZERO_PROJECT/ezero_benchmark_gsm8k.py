import math
import time
import json
import os
import sys

# 1. Import sécurisé du filtre E-ZERO v2.2
try:
    from ezero_filter import EZeroFilter
    ezero = EZeroFilter()
    print("✅ Moteur E-ZERO v2.2 chargé avec succès.")
except ImportError:
    print("❌ Erreur : ezero_filter.py est introuvable dans ce dossier.")
    exit()

# 2. Chargement du dataset GSM8K
print("Chargement du dataset GSM8K (100 questions)...")
try:
    from datasets import load_dataset
    dataset = load_dataset("openai/gsm8k", "main", split="test")
    questions = [item["question"] for item in dataset.select(range(100))]
    print(f"✅ {len(questions)} questions prêtes.\n")
except Exception as e:
    print(f"❌ Erreur de dataset : {e}")
    print("👉 Astuce : Tapez 'pip install datasets' si besoin.")
    exit()

# 3. Exécution du Benchmark
results = []
total_rho = 0
total_time = 0
activated_count = 0

print("--- RUNNING BENCHMARK V2.2 ---")
for i, q in enumerate(questions):
    res = ezero.filter(q)
    
    results.append({
        "id": i + 1,
        "question": q,
        "skeleton": res["skeleton"],
        "tokens_in": res["tokens_in"],
        "tokens_out": res["tokens_out"],
        "rho": res["rho"],
        "activated": res["activated"],
        "elapsed_ms": res["elapsed_ms"]
    })
    
    total_rho += res["rho"]
    total_time += res["elapsed_ms"]
    if res["activated"]:
        activated_count += 1

# 4. Calcul des Statistiques Finales
n = len(questions)
avg_rho = total_rho / n
avg_time = total_time / n
tokens_saved = (1 - avg_rho) * 100

print("\n" + "="*40)
print(f"RÉSULTATS E-ZERO V2.2 (GSM8K)")
print("="*40)
print(f"Questions testées      : {n}")
print(f"Compression moyenne (ρ): {avg_rho:.3f}")
print(f"Économie de jetons     : {tokens_saved:.1f}%")
print(f"Vitesse moyenne        : {avg_time:.2f} ms")
print(f"Taux d'activation      : {activated_count}%")
print("="*40)

# 5. Sauvegarde automatique
with open("ezero_gsm8k_results.json", "w") as f:
    json.dump({"summary": {"avg_compression_rho": avg_rho, "tokens_reduced_pct": tokens_saved}, "results": results}, f, indent=2)
print("\n✅ Fichier ezero_gsm8k_results.json mis à jour.")