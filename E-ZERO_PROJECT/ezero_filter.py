import re
import time
import json
import os

# ── RÉFÉRENTIELS BIOLOGIQUES (v2.2) ──────────────────────────────────────────
# Omega_sacred : Mots qui ne doivent JAMAIS être supprimés (Logique & Blockchain)
SACRED_WORDS = {
    "not", "if", "then", "false", "true", "each", "half", "except", 
    "how", "what", "calculate", "total", "many", "left", "result",
    "before", "after", "between", "first", "last", "only",
    "address", "uint256", "external", "public", "require", "contract",
    "function", "returns", "mapping", "constructor", "event", "emit"
}

# ── CONFIGURATION V2.2 ───────────────────────────────────────────────────────
class EZeroConfig:
    def __init__(self, **kwargs):
        self.n_min = kwargs.get('n_min', 3) # Réduit pour tester des petits segments bruités
        self.rho_target = kwargs.get('rho_target', 0.3)
        self.memory_path = kwargs.get('memory_path', 'ezero_memory.json')
        self.delta = 0.5  # Seuil du Théorème de Décontamination (v2.2)

# ── ORGANISME E-ZERO V2.2 ────────────────────────────────────────────────────
class EZeroFilter:
    def __init__(self, config=None):
        self.config = config or EZeroConfig()
        self.m_logic = SACRED_WORDS
        self.m_spec  = {"iron", "copper", "aluminum", "gold", "waste", "recycling", "battery"}
        self.synaptic_weights = {} 
        self.immune_memory = set()
        self.load_memories()

    def load_memories(self):
        """Charge le cerveau synaptique (Expertise PeP Recycling & Blockchain)."""
        try:
            if os.path.exists(self.config.memory_path):
                with open(self.config.memory_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    # Supporte les formats dict simple ou structuré (weights/immune)
                    if isinstance(data, dict) and "weights" in data:
                        self.synaptic_weights = data.get("weights", {})
                        self.immune_memory = set(data.get("immune", []))
                    else:
                        self.synaptic_weights = data
                print(f"🧠 Cerveau v2.2 chargé : {len(self.synaptic_weights)} synapses prêtes.")
            else:
                print("⚠️ Aucun cerveau trouvé. Démarrage à froid.")
        except Exception as e:
            print(f"❌ Erreur de lecture mémoire : {e}")

    def _is_numeric(self, token):
        """M1 : Membrane Numérique (Chiffres et adresses Blockchain)."""
        return bool(re.search(r'\d|0x[a-fA-F0-9]{40}', token))

    def _get_dynamic_weight(self, token):
        clean = token.lower().strip(",.?!:;()\"'")
        return self.synaptic_weights.get(clean, 1.0)

    def _decontaminate(self, token):
        """
        MO : MEMBRANE DE DÉCONTAMINATION (Théorème v2.2)
        Calcule le ratio alphanumérique pour éliminer le bruit.
        """
        if not token: return False
        alnum_count = sum(c.isalnum() for c in token)
        # delta = 0.5 (Rejette si plus de 50% de symboles bizarres)
        return (alnum_count / len(token)) >= self.config.delta

    def filter(self, prompt: str) -> dict:
        """Moteur HEDR : Extraction du Squelette Logique S(P)."""
        t_start = time.perf_counter()
        # Segmentation propre (Tokenization)
        tokens = prompt.replace('\n', ' ').split()
        n = len(tokens)

        if n < self.config.n_min:
            return {"skeleton": prompt, "activated": False, "gain_pct": 0.0, "ms": 0.0}

        keep = []
        for t in tokens:
            clean = t.lower().strip(",.?!:;()\"'")
            
            # --- CASCADE DES 5 MEMBRANES ---
            # 1. MO: Décontamination (Élimine le bruit complexe)
            if not self._decontaminate(t):
                continue

            # 2. M1-M2: Mots Sacrés & Numérique (Signal vital)
            is_sacred = clean in self.m_logic or clean in self.m_spec
            is_numeric = self._is_numeric(t)
            
            # 3. M4: Poids Synaptique (Expertise apprise)
            is_immune = clean in self.immune_memory
            is_strong = self._get_dynamic_weight(t) > 1.3
            
            if is_numeric or is_sacred or is_immune or is_strong:
                keep.append(t)

        skeleton = " ".join(keep)
        rho = len(keep) / n if n > 0 else 1.0
        # Théorème de Gain G = (1 - rho^2) * 100
        gain_pct = (1 - (rho ** 2)) * 100

        return {
            "skeleton": skeleton,
            "tokens_in": n,
            "tokens_out": len(keep),
            "gain_pct": round(gain_pct, 1),
            "ms": round((time.perf_counter() - t_start) * 1000, 3),
            "plasticity": {
                "synapses": len(self.synaptic_weights)
            }
        }

if __name__ == "__main__":
    # Test rapide de robustesse
    filter_tool = EZeroFilter()
    test_input = "z<pueH'3E contract PeP_Recycling { uint256 850; }"
    result = filter_tool.filter(test_input)
    print(f"\nEntrée : {test_input}")
    print(f"Sortie : {result['skeleton']}")
    print(f"Gain   : {result['gain_pct']}%")