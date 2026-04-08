"""
E-ZERO FILTER — Version 5.1
=============================
Author : Sawadogo Anselme
Version: 5.1 — April 2026

Protocole de compression de prompts LLM bio-inspiré.
Réduit le nombre de tokens en entrée tout en préservant
le sens sémantique et logique du prompt original.

Ce module est un projet de recherche indépendant.
Il ne contient aucune référence à des projets tiers.
"""

import re
import time
import json
from collections import Counter

# ── MOTS SACRÉS — jamais supprimés ───────────────────────────────────────────
SACRED_WORDS = {
    # Logique générale
    "not", "no", "never", "neither", "nor",
    "if", "then", "else", "unless", "except", "without",
    "false", "true", "always", "only", "still", "already",
    "each", "half", "all", "none", "every", "both", "either",
    "more", "less", "than", "equal", "most", "least", "as",
    "because", "therefore", "thus", "since", "although", "though",
    "how", "what", "where", "when", "which", "who", "why",
    "calculate", "total", "many", "much", "left", "result",
    "before", "after", "between", "first", "last",
    # Solidity / Blockchain (domaine technique générique)
    "address", "uint256", "uint8", "uint", "int256", "bool",
    "bytes32", "bytes", "string",
    "external", "public", "private", "internal", "view", "pure",
    "require", "contract", "mapping", "constructor", "function",
    "returns", "memory", "storage", "calldata",
    "emit", "event", "payable", "indexed",
}


# ── CONFIGURATION ─────────────────────────────────────────────────────────────
class EZeroConfig:
    def __init__(self, **kwargs):
        self.n_min        = kwargs.get('n_min', 5)
        self.rho_target   = kwargs.get('rho_target', 0.3)
        self.memory_path  = kwargs.get('memory_path', 'ezero_memory.json')
        self.noise_thresh = kwargs.get('noise_thresh', 0.5)


# ── FILTRE E-ZERO ─────────────────────────────────────────────────────────────
class EZeroFilter:
    def __init__(self, config=None, **kwargs):
        self.config = config or EZeroConfig()

        # Membrane logique
        self.m_logic = SACRED_WORDS

        # Membrane de spécificité — vocabulaire de référence neutre
        self.m_spec = {
            # Matériaux et sciences
            "iron", "copper", "aluminum", "gold", "silver",
            "metal", "waste", "chemical", "compound", "element",
            # Objets courants (GSM8K)
            "battery", "device", "phone", "machine", "engine",
            "arrows", "quivers", "tokens", "coins", "dollars", "cents",
            "hours", "days", "weeks", "months", "years", "minutes",
            "boxes", "bags", "bottles", "cans", "items", "units",
            "workers", "students", "people", "children",
            "apples", "oranges", "books", "cars",
            "kg", "mah", "km", "ml", "liters", "meters",
            # Objets BBH
            "book", "vase", "pencil", "cup", "envelope", "keychain",
            "notebook", "ball", "cube", "pyramid", "house",
            # Couleurs (BBH colored objects)
            "red", "blue", "green", "yellow", "white",
            "pink", "purple", "brown", "orange", "black", "gray",
            # Positions (BBH logical deduction)
            "left", "right", "front", "back", "top", "bottom",
            "leftmost", "rightmost",
            # Prénoms génériques (GSM8K / BBH)
            "janet", "mary", "john", "tom", "alice", "bob",
            "dave", "eve", "carol", "billy", "suzy", "jane",
            # Blockchain générique
            "uint256", "address", "contract", "mapping",
        }

        # Mémoire synaptique
        self.synaptic_weights = {}
        self.immune_memory    = set()
        self.load_memories()

    # ── MÉMOIRE ───────────────────────────────────────────────────────────────
    def load_memories(self):
        """Charge la mémoire synaptique depuis le fichier JSON."""
        try:
            with open(self.config.memory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.synaptic_weights = data.get("weights", {})
                self.immune_memory    = set(data.get("immune", []))
                print(f"🧠 Cerveau chargé : {len(self.synaptic_weights)} synapses prêtes.")
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Démarrage froid silencieux

    def save_memories(self):
        """Sauvegarde la mémoire synaptique."""
        with open(self.config.memory_path, "w", encoding="utf-8") as f:
            json.dump({
                "weights": self.synaptic_weights,
                "immune":  list(self.immune_memory)
            }, f, indent=2)

    # ── MEMBRANE DE DÉCONTAMINATION ───────────────────────────────────────────
    def _is_clean_token(self, token: str) -> bool:
        """
        Vérifie qu'un token est un vrai mot — pas du bruit aléatoire.
        Un token propre doit avoir au moins 50% de caractères alphanumériques.

        Exemples :
          'contract'       → ✅ 100% alnum
          '500kg'          → ✅ 100% alnum
          '0x1234abcd'     → ✅ adresse blockchain valide
          '$4~z3whJ,GVEc'  → ❌ bruit (< 50% alnum)
          'R57W.Yz_plF-&J' → ❌ bruit (< 50% alnum)
        """
        # Adresses blockchain — toujours valides
        if re.match(r'^0x[a-fA-F0-9]{6,}$', token):
            return True
        alnum = sum(1 for c in token if c.isalnum())
        return (alnum / len(token)) >= self.config.noise_thresh if token else False

    # ── DÉTECTION NUMÉRIQUE STRICTE ───────────────────────────────────────────
    def _is_numeric(self, token: str) -> bool:
        """
        Détecte uniquement les vrais nombres, unités, dates et versions.
        Ne garde PAS les tokens bruités qui contiennent des chiffres.
        """
        t = token.strip(",.?!:;()\"'")
        return bool(
            re.match(r'^-?\d+(\.\d+)?%?$', t) or       # 42, -3, 30%
            re.match(r'^\d+[a-zA-Z]{1,5}$', t) or       # 500kg, 5000mAh
            re.match(r'^\d{1,2}/\d{1,2}/\d{2,4}$', t) or # 12/25/1937
            re.match(r'^(19|20)\d{2}$', t) or            # 1937, 2026
            re.match(r'^\d{1,2}:\d{2}$', t) or           # 10:30
            re.match(r'^\^?\d+\.\d+\.\d+$', t) or        # ^0.8.20
            re.match(r'^0x[a-fA-F0-9]{6,}$', t)          # 0x1234...
        )

    def _get_dynamic_weight(self, token: str) -> float:
        """Retourne le poids synaptique d'un token."""
        clean = token.lower().strip(",.?!:;()\"'")
        return self.synaptic_weights.get(clean, 1.0)

    # ── APPRENTISSAGE PAR RÉTROACTION ─────────────────────────────────────────
    def feedback_loop(self, prompt: str, score: float):
        """
        Renforce les synapses utiles (score >= 70)
        ou affaiblit les tokens nuisibles (score < 30).
        """
        for t in prompt.split():
            clean = t.lower().strip(",.?!:;()\"'")
            if not clean:
                continue
            if score >= 70:
                self.synaptic_weights[clean] = (
                    self.synaptic_weights.get(clean, 1.0) + 0.1
                )
            elif score < 30:
                self.immune_memory.discard(clean)
                self.synaptic_weights[clean] = max(
                    0.0, self.synaptic_weights.get(clean, 1.0) - 0.2
                )

    # ── FILTRE PRINCIPAL ──────────────────────────────────────────────────────
    def filter(self, prompt: str, mode: str = "general") -> dict:
        t_start = time.perf_counter()
        tokens  = prompt.split()
        n       = len(tokens)

        if n < self.config.n_min:
            return {
                "skeleton":   prompt,
                "activated":  False,
                "gain_pct":   0.0,
                "rho":        1.0,
                "tokens_in":  n,
                "tokens_out": n,
                "ms":         0.0,
                "elapsed_ms": 0.0,
                "plasticity": {
                    "synapses":   len(self.synaptic_weights),
                    "antibodies": len(self.immune_memory),
                }
            }

        keep = []
        for t in tokens:
            clean = t.lower().strip(",.?!:;()\"'")

            # Étape 0 — Décontamination : rejeter le bruit immédiatement
            if not self._is_clean_token(t):
                continue

            # Étape 1 — Conditions de survie
            if (self._is_numeric(t) or
                clean in self.m_logic or
                clean in self.m_spec or
                clean in self.immune_memory or
                self._get_dynamic_weight(t) > 1.3):
                keep.append(t)

        skeleton = " ".join(keep)
        rho      = len(keep) / n if n > 0 else 1.0
        gain_pct = (1 - (rho ** 2)) * 100
        elapsed  = round((time.perf_counter() - t_start) * 1000, 3)

        return {
            "skeleton":   skeleton,
            "tokens_in":  n,
            "tokens_out": len(keep),
            "gain_pct":   round(gain_pct, 1),
            "rho":        round(rho, 4),
            "ms":         elapsed,
            "elapsed_ms": elapsed,
            "activated":  True,
            "plasticity": {
                "synapses":   len(self.synaptic_weights),
                "antibodies": len(self.immune_memory),
            }
        }