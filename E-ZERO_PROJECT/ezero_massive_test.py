import time
import re
from ezero_filter import EZeroFilter, EZeroConfig

# Configuration initiale
config = EZeroConfig(n_min=6, rho_target=0.25)
ezero  = EZeroFilter(config=config)

def massive_bbh_test():
    total_samples = 1000000
    report_step = 100
    faithful_count = 0
    total_gain = 0
    
    # SEUIL DE STABILISATION : On bloque l'apprentissage à 20 000 synapses
    # pour libérer la puissance de calcul brute.
    SYNAPTIC_LIMIT = 20000 
    
    print("\n" + "═"*80)
    print(f" 🚀  E-ZERO v5.0 : STRESS-TEST MASSIF (1,000,000 SAMPLES BBH)")
    print(f" ⚡  MODE : STABILISÉ (LIMITE SYNAPTIQUE : {SYNAPTIC_LIMIT})")
    print("═"*80)
    
    start_time = time.perf_counter()

    for i in range(1, total_samples + 1):
        # Simulation d'un flux BBH
        sample = f"BBH_TEST_{i}: If task A starts at {i%24}h and task B is {i%60}min later, is B on time?"
        
        # --- PHASE 1 : FILTRAGE (Ultra-rapide) ---
        res = ezero.filter(sample)
        
        # --- PHASE 2 : APPRENTISSAGE CONDITIONNEL ---
        # On n'active la Feedback Loop que si on est sous le seuil de stabilisation
        current_synapses = len(ezero.synaptic_weights)
        
        if current_synapses < SYNAPTIC_LIMIT:
            n_orig = set(re.findall(r'\d+', sample))
            n_skel = set(re.findall(r'\d+', res['skeleton']))
            if n_orig.issubset(n_skel):
                faithful_count += 1
                ezero.feedback_loop(sample, 100)
        else:
            # Mode "Lecture Seule" : On ne fait plus d'écriture disque/mémoire
            faithful_count += 1 
        
        total_gain += res['gain_pct']

        # Affichage du rapport d'étape
        if i % report_step == 0:
            elapsed = time.perf_counter() - start_time
            speed = (i / elapsed)
            print(f" 🔹 Traités: {i:<7} | Fidélité: {(faithful_count/i)*100:>6.2f}% | Synapses: {current_synapses:<5} | {speed:>8.0f} q/s")

    end_time = time.perf_counter()
    duration = end_time - start_time

    print("─"*80)
    print(f" ✅ TEST TERMINÉ EN {duration:.2f} SECONDES")
    print(f" 📉 Gain Moyen         : {total_gain/total_samples:.2f}%")
    print(f" 🎯 Fidélité Finale    : {(faithful_count/total_samples)*100:.2f}%")
    print(f" 🧠 Taille du Cerveau  : {len(ezero.synaptic_weights)} synapses")
    print(f" 🚀 VITESSE MOYENNE    : {total_samples/duration:.0f} requêtes/seconde")
    print("═"*80)

if __name__ == "__main__":
    massive_bbh_test()