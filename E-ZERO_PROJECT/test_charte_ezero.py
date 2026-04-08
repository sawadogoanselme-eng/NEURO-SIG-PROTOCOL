from ezero_filter import EZeroFilter, EZeroConfig

# 1. Initialisation (HP ProBook 640 G6)
config = EZeroConfig(memory_path="ezero_memory.json")
ezero = EZeroFilter(config=config)

# 2. Ton document (Article 15 - Droits de l'homme)
document_loi = """
Article 15 :
1. Nul ne sera soumis à la torture, ni à des peines ou traitements cruels, inhumains ou dégradants. En
particulier, il est interdit de soumettre une personne sans son libre consentement à une expérience médicale
ou scientifique.
2. Les États parties prennent toutes mesures législatives, administratives, judiciaires et autres mesures
efficaces pour empêcher, sur la base de l’égalité avec les autres, que des personnes handicapées ne soient
soumises à la torture ou à des peines ou traitements cruels, inhumains ou dégradants.
"""

print("="*60)
print("⚖️ TEST E-ZERO V2.2 : DOCUMENT JURIDIQUE RÉEL")
print("="*60)

# 3. Filtrage
resultat = ezero.filter(document_loi)

# 4. Analyse des résultats
print(f"\n🧠 SQUELETTE EXTRAIT :")
print("-" * 30)
print(resultat['skeleton'])

print(f"\n📊 PERFORMANCE :")
print(f"  - Gain Énergétique : {resultat['gain_pct']}%")
print(f"  - Latence          : {resultat['ms']} ms")
print(f"  - Synapses active  : {resultat['plasticity']['synapses']}")
print("="*60)

# Vérification rigoureuse du sens
piliers = ["Nul", "ne", "ni", "sans", "interdit"]
manquants = [p for p in piliers if p.lower() not in resultat['skeleton'].lower()]

if not manquants:
    print("✅ VALIDATION : Structure logique préservée.")
else:
    print(f"⚠️ ALERTE : Perte de sens détectée ({', '.join(manquants)})")