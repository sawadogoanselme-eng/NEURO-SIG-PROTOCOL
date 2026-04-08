import time
from ezero_filter import EZeroFilter, EZeroConfig

# Questions de test intégrées pour éviter les erreurs de fichiers manquants
QUESTIONS = [
    "Janet has 3 quivers of 20 arrows each. She fires half of them. How many arrows does she have left?",
    "A recycling center collects 1200kg of waste. 30% is iron and 20% is aluminum. What is the total mass of metals?",
    "If a battery has 5000mAh and a device consumes 200mA per hour, how many hours will it last?",
    "Hello Gemini, I am the manager of PeP Recycling. We have collected 500kg of iron and 250kg of aluminum. What is the total mass?"
]

def run_stress_test():
    print("\n" + "="*70)
    print("🚀 DÉMARRAGE DU TEST DE VALEUR E-ZERO (GSM8K)")
    print("="*70)

    # Configuration optimisée pour voir la puissance de compression
    # n_min=5 force l'organisme à travailler même sur les phrases courtes
    config = EZeroConfig(n_min=5, rho_target=0.4)
    ezero = EZeroFilter(config=config)
    
    print(f"{'ID':<3} | {'GAIN %':<8} | {'SQUELETTE EXTRAIT'}")
    print("-" * 70)

    for i, q in enumerate(QUESTIONS):
        result = ezero.filter(q)
        gain = result['gain_pct']
        skel = result['skeleton']
        
        # On affiche le gain et le début du squelette
        print(f"{i+1:<3} | {gain:>7}% | {skel}")

    print("\n" + "="*70)
    print("💡 ANALYSE DE LA VALEUR :")
    print("1. Si GAIN > 0% : La méduse a bien supprimé le 'bruit'.")
    print("2. Si les CHIFFRES sont là : Le tentacule mathématique a survécu.")
    print("="*70)

if __name__ == "__main__":
    run_stress_test()