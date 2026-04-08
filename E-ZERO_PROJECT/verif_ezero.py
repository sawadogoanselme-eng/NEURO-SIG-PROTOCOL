from ezero_filter import EZeroFilter, EZeroConfig

print("--- VÉRIFICATION DE LA CLASSE E-ZERO ---")

try:
    # Test 1 : Appel standard
    ez1 = EZeroFilter()
    print("✅ Test 1 (Standard) : OK")

    # Test 2 : Appel avec config (ce que fait le benchmark)
    conf = EZeroConfig()
    ez2 = EZeroFilter(config=conf)
    print("✅ Test 2 (Avec Config) : OK")

    # Test 3 : Appel avec un argument inconnu (Sécurité Anti-Bug)
    ez3 = EZeroFilter(argument_fantome="test")
    print("✅ Test 3 (Anti-Bug kwargs) : OK")

    print("\nCONCLUSION : Ta classe est blindée pour les tests massifs !")

except TypeError as e:
    print(f"❌ ÉCHEC : La classe rejette encore des arguments. Erreur : {e}")