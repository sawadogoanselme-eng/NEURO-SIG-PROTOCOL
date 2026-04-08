import ezero_filter as ezero
import random
import string

filtre = ezero.EZeroFilter()

def generate_garbage():
    return ''.join(random.choices(string.ascii_letters + string.punctuation + string.digits, k=8))

print(f"🧠 Entraînement de l'immunité en cours... (Synapses actuelles: {len(filtre.synaptic_weights)})")

# Simulation d'un flux de données massif et pollué
for _ in range(1000):
    garbage = generate_garbage()
    # On force un poids très faible (pénalité) pour les jetons de type bruit
    clean_garbage = garbage.lower().strip(",.?!:;()")
    filtre.synaptic_weights[clean_garbage] = 0.1  # Poids synaptique "mort"

# Sauvegarde du nouveau cerveau musclé
filtre.save_memories()
print(f"✅ Entraînement terminé. Nouveau volume synaptique : {len(filtre.synaptic_weights)}")