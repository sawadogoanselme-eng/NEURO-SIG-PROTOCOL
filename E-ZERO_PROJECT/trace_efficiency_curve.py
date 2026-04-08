import ezero_filter as ezero
import time
import random
import string
import matplotlib.pyplot as plt

def generate_garbage():
    return ''.join(random.choices(string.ascii_letters, k=8))

# Configuration du test
paliers = [21000, 30000, 40000, 50000, 60000, 80000, 100000]
latences = []

print("📊 ANALYSE DE LA COURBE D'EFFICIENCE (Stress Test)")
filtre = ezero.EZeroFilter()
test_text = "contract PeP { address public iron; uint256 yield = 850; }"

for p in paliers:
    # 1. Gonflement artificiel de la mémoire
    current_size = len(filtre.synaptic_weights)
    needed = p - current_size
    if needed > 0:
        for _ in range(needed):
            filtre.synaptic_weights[generate_garbage()] = 0.1
    
    # 2. Mesure de la latence (moyenne sur 100 essais pour la précision)
    total_time = 0
    for _ in range(100):
        start = time.perf_counter()
        _ = filtre.filter(test_text)
        total_time += (time.perf_counter() - start)
    
    avg_ms = (total_time / 100) * 1000
    latences.append(avg_ms)
    print(f"🧠 Synapses : {p} | ⚡ Latence moy. : {avg_ms:.4f} ms")

# 3. Génération du graphique pour ton papier Zenodo
plt.figure(figsize=(10, 6))
plt.plot(paliers, latences, marker='o', linestyle='-', color='b')
plt.axhline(y=1.0, color='r', linestyle='--', label='Limite Temps Réel (1ms)')
plt.title("Courbe d'Efficience Synaptique - HP ProBook 640 G6")
plt.xlabel("Nombre de Synapses (Mémoire)")
plt.ylabel("Latence de traitement (ms)")
plt.grid(True)
plt.legend()
plt.savefig("courbe_efficience_ezero.png")
print("\n✅ Graphique sauvegardé : 'courbe_efficience_ezero.png'")
plt.show()