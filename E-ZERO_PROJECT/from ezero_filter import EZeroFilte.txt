from ezero_filter import EZeroFilter, EZeroConfig

# 1. Initialisation avec ton cerveau de 20 000 synapses
config = EZeroConfig(memory_path="ezero_memory.json")
ezero = EZeroFilter(config=config)

# 2. Le document de test (Texte juridique + Expertise + Bruit)
document = """
ARTICLE 4 : CONFIDENTIALITÉ ET SÉCURITÉ DES SYSTÈMES.
Le Prestataire s'engage à ne PAS divulguer les informations relatives au projet 
PeP Recycling à des tiers, SAUF accord écrit préalable. 

Si une faille de sécurité est détectée sur l'address du contract intelligent, 
le système doit calculate l'impact financier total immédiatement. 
Injection de bruit pour test de robustesse : z<pueH'3E"z8 rk-ze|v` @xl`egxb.

Chaque partie reste propriétaire de ses outils techniques. SI le result de l'audit 
est négatif, la fonction uint256 renverra une erreur.
"""

print("="*60)
print("🚀 TEST E-ZERO V2.2 SUR DOCUMENT")
print("="*60)

# 3. Exécution du filtrage
resultat = ezero.filter(document)

# 4. Affichage des résultats rigoureux
print(f"\n📄 DOCUMENT ORIGINAL ({resultat['tokens_in']} mots) :")
print("-" * 30)
print(document.strip())

print(f"\n🧠 SQUELETTE EXTRAIT ({resultat['tokens_out']} mots) :")
print("-" * 30)
print(resultat['skeleton'])

print(f"\n📊 MÉTRIQUES DE PERFORMANCE :")
print(f"  - Gain Énergétique : {resultat['gain_pct']}%")
print(f"  - Latence de traitement : {resultat['ms']} ms")
print(f"  - Synapses mobilisées : {resultat['plasticity']['synapses']}")
print("="*60)

# Vérification de la robustesse
if "z<pueH'3E" not in resultat['skeleton']:
    print("✅ VALIDATION : Bruit complexe totalement éliminé (Membrane M0).")
else:
    print("❌ ÉCHEC : Résidus de bruit détectés.")

if "contract" in resultat['skeleton'].lower():
    print("✅ VALIDATION : Signal critique préservé (Membrane M2).")