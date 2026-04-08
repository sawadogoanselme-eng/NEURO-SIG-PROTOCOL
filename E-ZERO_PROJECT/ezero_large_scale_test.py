import time
import json
import re
import random
from ezero_filter import EZeroFilter, EZeroConfig

# 1. INITIALISATION DE L'ORGANISME
config = EZeroConfig(n_min=5, rho_target=0.3)
ezero  = EZeroFilter(config=config)

# 2. GÉNÉRATEUR DYNAMIQUE DE DONNÉES (POUR TESTER LA PRÉCISION)
def generate_bulk_data(count=200):
    data = []
    templates = [
        "If {n1} items cost {n2} dollars, what is the price of {n3} items?",
        "A batch of {n1}kg contains {n2}% of iron and {n3}% of copper. Calculate total mass.",
        "Today is {d}/{m}/2026. What was the date {n1} days ago in history?",
        "Machine {n1} produced {n2} units but {n3} were defective. Is it a failure?",
        "The battery at {n1}mAh consumes {n2}mA per hour. How long will it last?",
        "Jane is {n1} years old. Her brother is {n2} years younger. What is his age?"
    ]
    for _ in range(count):
        t = random.choice(templates)
        data.append(t.format(
            n1=random.randint(10, 5000), 
            n2=random.randint(1, 100), 
            n3=random.randint(1, 15), 
            d=random.randint(1, 28), 
            m=random.randint(1, 12)
        ))
    return data

def run_large_scale():
    test_data = generate_bulk_data(200) 
    total = len(test_data)
    results = []
    faithful_count = 0 # Compteur pour la fidélité numérique
    
    print("\n" + "═"*80)
    print(f" 🌀  E-ZERO v5.0 : STRESS-TEST & DASHBOARD DE PRÉCISION ({total} SAMPLES)")
    print("═"*80)
    print(f"{'ID':<5} | {'GAIN':<7} | {'FIDÉLITÉ':<10} | {'VITESSE':<10} | {'MÉMOIRE'}")
    print("─"*80)

    t_start_global = time.perf_counter()

    for i, q in enumerate(test_data):
        # FILTRATION
        res = ezero.filter(q)
        
        # --- ANALYSE RIGOUREUSE DE LA FIDÉLITÉ ---
        n_orig = set(re.findall(r'\d+', q))
        n_skel = set(re.findall(r'\d+', res['skeleton']))
        
        # Un test est réussi si TOUS les chiffres de l'original sont dans le squelette
        is_faithful = n_orig.issubset(n_skel)
        
        if is_faithful:
            faithful_count += 1
            status = "✅ OK"
        else:
            status = "❌ PERTE"
        
        # APPRENTISSAGE (Feedback automatique basé sur la fidélité)
        ezero.feedback_loop(q, 100 if is_faithful else 0)
        
        results.append(res)

        # Affichage toutes les 20 questions pour suivre la progression
        if (i+1) % 20 == 0 or i == 0:
            mem_info = f"S:{res['plasticity']['synapses']}"
            print(f"{i+1:<5} | {res['gain_pct']:>5}% | {status:<10} | {res['ms']:>7.3f}ms | {mem_info}")

    t_end_global = time.perf_counter()

    # --- CALCUL DES MÉTRIQUES DE PRÉCISION FINALES ---
    avg_gain = sum(r['gain_pct'] for r in results) / total
    avg_ms = sum(r['ms'] for r in results) / total
    precision_score = (faithful_count / total) * 100
    total_time = t_end_global - t_start_global

    print("─"*80)
    print(f" 📊  RAPPORT DE PRÉCISION ET PERFORMANCE :")
    print(f" 🎯 FIDÉLITÉ NUMÉRIQUE : {precision_score:.2f}%  <-- Cible: 100%")
    print(f" 📉 GAIN DE COMPRESSION : {avg_gain:.2f}%")
    print(f" ⚡ VITESSE MOYENNE    : {avg_ms:.4f} ms / question")
    print(f" 🧠 CERVEAU NUMÉRIQUE  : {len(ezero.synaptic_weights)} synapses")
    print(f" ⏱️ TEMPS D'EXÉCUTION  : {total_time:.2f} secondes")
    print("═"*80)
    
    if precision_score == 100:
        print(" VERDICT : E-ZERO est 100% FIABLE pour les données numériques. ✅")
    else:
        print(f" VERDICT : ATTENTION, {total - faithful_count} pertes détectées. ⚠️")

if __name__ == "__main__":
    run_large_scale()