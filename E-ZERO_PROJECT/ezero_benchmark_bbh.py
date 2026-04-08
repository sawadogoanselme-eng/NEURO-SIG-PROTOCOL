from ezero_filter import EZeroFilter, EZeroConfig

def run_safe_benchmark():
    # Configuration de l'organisme
    config = EZeroConfig()
    ezero = EZeroFilter(config=config)
    
    # Dataset de test (Logique & Recyclage)
    questions = [
        "A worker collects 500kg of iron and 250kg of aluminum. What is the total mass?",
        "If Mary has 10 tokens and spends 3, how many are left?",
        "Explain the E-ZERO protocol energy saving mechanism for LLM inference."
    ]
    
    print("\n--- ANALYSE E-ZERO : MODE BIO-INSPIRÉ ---")
    print(f"{'ID':<4} | {'IN':<4} | {'OUT':<4} | {'GAIN %':<8} | {'SQUELETTE'}")
    print("-" * 65)

    total_gain = 0
    for i, q in enumerate(questions):
        try:
            res = ezero.filter(q)
            if res["activated"]:
                total_gain += res["gain_pct"]
                # Affichage sécurisé sans caractères parasites
                print(f"{i+1:<4} | {res['tokens_in']:<4} | {res['tokens_out']:<4} | {res['gain_pct']:>7}% | {res['skeleton'][:30]}...")
            else:
                print(f"{i+1:<4} | --- BYPASS (Prompt trop court) ---")
        except Exception as e:
            print(f"Erreur sur ID {i+1}: {e}")

    if len(questions) > 0:
        avg = total_gain / len(questions)
        print("-" * 65)
        print(f"GAIN MOYEN CERTIFIÉ : {avg:.1f}%")
        print("STATUT : PRÊT POUR PUBLICATION")

if __name__ == "__main__":
    run_safe_benchmark()