import ezero_filter as ezero
import random
import string
import time

# 1. Initialisation (Le cerveau de 20 000 synapses se charge)
filtre = ezero.EZeroFilter()

def generate_noise(length):
    """Génère du bruit numérique pur (caractères aléatoires)"""
    return ''.join(random.choices(string.ascii_letters + string.punctuation + string.digits, k=length))

# --- LE SIGNAL (L'information vitale pour PeP Recycling) ---
# Nous mélangeons ton expertise métier et la blockchain
clean_signal = "contract PeP_Recycling { address public iron_storage; uint256 public constant copper_yield = 850; }"

# --- LE CHAOS (On noie le signal dans 3 blocs de bruit) ---
noise_1 = generate_noise(60)
noise_2 = generate_noise(60)
noise_3 = generate_noise(40)

noisy_input = f"{noise_1} {clean_signal} {noise_2} ### ERROR_404 ### {noise_3}"

print(f"--- TEST DE ROBUSTESSE : SIGNAL DANS LE BRUIT ---")
print(f"\n[ENTRÉE BRUITÉE (Extrait)] :")
print(f"{noisy_input[:120]}...") 

# 2. Exécution du filtrage
t_start = time.perf_counter()
res = filtre.filter(noisy_input)
t_end = time.perf_counter()

# 3. Affichage des résultats
print(f"\n[RÉSULTAT DU NETTOYAGE] :")
print(f"✅ Squelette extrait : {res['skeleton']}")
print(f"📊 Gain Énergétique  : {res['gain_pct']}%")
print(f"⚡ Latence           : {res['ms']} ms")
print(f"🧠 Synapses actives  : {res['plasticity']['synapses']}")

# Vérification de l'intégrité
if "850" in res['skeleton'] and "iron" in res['skeleton'].lower():
    print("\n🔥 RÉSULTAT : Robustesse validée. Le signal vital a survécu au chaos.")
else:
    print("\n⚠️ RÉSULTAT : Signal partiellement perdu. Ajustement de la membrane nécessaire.")