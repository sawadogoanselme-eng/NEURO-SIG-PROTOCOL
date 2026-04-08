"""
E-ZERO FILTER — Version 4.1
=============================
Author : Sawadogo Anselme
Version: 4.1 — April 2026

Corrections v4.1 vs v4.0 :
  - Détection des dates MM/DD/YYYY et formats similaires
  - Détection des années seules (ex: 1937, 2019)
  - Détection des heures (ex: 10:30)
  - Membranes date enrichies
  - Fidélité cible : 95-100% GSM8K / 90-95% BBH
"""

import re
import time
import math
from collections import Counter

# ── Import spaCy (optionnel) ─────────────────────────────────────────────────
try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
    SPACY_OK = True
except Exception:
    _nlp     = None
    SPACY_OK = False

# ── Stopwords ────────────────────────────────────────────────────────────────
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "this", "that", "these", "those", "it", "its", "they", "their", "them",
    "he", "she", "his", "her", "we", "our", "you", "your", "i", "my",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "into",
    "about", "as", "up", "out", "so", "also", "just", "now",
    "there", "here", "very", "too",
}

# ── Mots sacrés — jamais supprimés ───────────────────────────────────────────
SACRED_WORDS = {
    # Négations
    "not", "no", "never", "neither", "nor",
    "unless", "except", "without", "but", "however",
    # Modificateurs critiques
    "only", "always", "still", "already", "yet",
    # Quantificateurs
    "all", "none", "every", "each", "both", "either",
    # Comparateurs
    "more", "less", "fewer", "greater", "smaller", "equal",
    "most", "least", "than", "as",
    # Connecteurs logiques
    "if", "then", "else", "because", "therefore", "thus",
    "so", "hence", "since", "although", "though", "while",
    # Questions
    "how", "what", "where", "when", "which", "who", "why",
    "whose", "whom",
}

# ── Tags POS spaCy à garder ───────────────────────────────────────────────────
KEEP_POS = {"NOUN", "PROPN", "NUM", "VERB", "ADJ", "ADV"}

# ── Tags DEP spaCy à garder ───────────────────────────────────────────────────
KEEP_DEP = {
    "nsubj", "nsubjpass", "dobj", "iobj",
    "nummod", "amod", "compound", "ROOT",
    "attr", "pobj", "neg",
}

# ── Signaux de détection de mode ─────────────────────────────────────────────
MODE_SIGNALS = {
    "math": {
        "calculate", "total", "sum", "difference", "product",
        "cost", "price", "profit", "loss", "earn", "spend",
        "buy", "sell", "paid", "many", "much", "left",
        "remaining", "altogether", "combined", "average",
        "kg", "km", "mah", "dollars", "cents", "hours",
        "percent", "%", "rate", "speed", "distance",
    },
    "logic": {
        "true", "false", "valid", "invalid", "consistent",
        "possible", "impossible", "necessarily", "certainly",
        "logical", "implies", "conclude", "statement",
        "premise", "argument", "deduce", "infer",
        "all", "some", "none", "every", "no",
    },
    "causal": {
        "cause", "caused", "effect", "because", "reason",
        "why", "result", "consequence", "lead", "leads",
        "responsible", "due", "owing", "blame",
        "happen", "happened", "occur", "occurred",
    },
    "date": {
        "date", "day", "month", "year", "week",
        "before", "after", "between", "during", "since",
        "ago", "later", "earlier", "yesterday", "tomorrow",
        "january", "february", "march", "april", "may",
        "june", "july", "august", "september", "october",
        "november", "december", "monday", "tuesday",
        "wednesday", "thursday", "friday", "saturday", "sunday",
        "mm/dd/yyyy", "yyyy", "today", "birthday",
    },
}


class EZeroConfig:
    """Configuration de l'organisme E-ZERO v4.1"""
    def __init__(self, **kwargs):
        self.n_min        = kwargs.get('n_min', 5)
        self.rho_target   = kwargs.get('rho_target', 0.3)
        self.lambda_tfidf = kwargs.get('lambda_tfidf', 0.2)
        self.lambda_pos   = kwargs.get('lambda_pos', 0.7)
        self.lambda_dep   = kwargs.get('lambda_dep', 0.1)
        self.gamma        = kwargs.get('gamma', 0.25)
        self.tfidf_thresh = kwargs.get('tfidf_thresh', 0.15)


class EZeroFilter:
    def __init__(self, config: EZeroConfig = None, lang: str = "en", **kwargs):
        self.config = config or EZeroConfig()
        self.lang   = lang

        # ── MEMBRANES LEXICALES ───────────────────────────────────────────────

        self.m_spec = {
            "iron", "copper", "aluminum", "gold", "silver", "metal", "waste",
            "recycling", "janet", "mary", "john", "tom", "alice", "bob",
            "dave", "eve", "carol", "billy", "suzy", "jane", "ranger",
            "binance", "solidity", "contract", "battery", "phone", "device",
            "arrows", "quivers", "tokens", "coins", "dollars", "cents",
            "hours", "days", "weeks", "months", "years", "minutes", "seconds",
            "boxes", "bags", "bottles", "cans", "packs", "items", "units",
            "workers", "students", "people", "children", "boys", "girls",
            "apples", "oranges", "books", "cars", "trees", "flowers",
            "cookies", "candies", "pens", "pencils", "shirts", "shoes",
            "tickets", "seats", "rooms", "floors", "windows", "doors",
            "kg", "mah", "km", "ml", "liter", "liters", "meter", "meters",
            # Objets BBH
            "book", "vase", "pencil", "cup", "envelope", "keychain",
            "notebook", "ball", "cube", "pyramid", "house", "houses",
            "red", "blue", "green", "yellow", "white", "pink", "purple",
            "brown", "orange", "black", "gray",
            # Positions
            "left", "right", "front", "back", "top", "bottom",
            "first", "second", "third", "fourth", "fifth",
            "leftmost", "rightmost",
        }

        self.m_action = {
            "has", "have", "had", "give", "gives", "gave", "given",
            "take", "takes", "took", "taken", "fire", "fires", "fired",
            "use", "uses", "used", "collect", "collects", "collected",
            "add", "adds", "added", "remove", "removes", "removed",
            "consume", "consumes", "consumed", "produce", "produces",
            "sell", "sells", "sold", "buy", "buys", "bought",
            "earn", "earns", "earned", "spend", "spends", "spent",
            "need", "needs", "needed", "get", "gets", "got",
            "make", "makes", "made", "pay", "pays", "paid",
            "cost", "costs", "save", "saves", "saved",
            "lose", "loses", "lost", "gain", "gains", "gained",
            "share", "shares", "shared", "divide", "divides", "divided",
            "multiply", "multiplies", "multiplied", "remain", "remains",
            "start", "starts", "started", "finish", "finishes", "finished",
            "work", "works", "worked", "travel", "travels", "traveled",
            "arrive", "arrives", "arrived", "leave", "leaves",
            "stand", "stands", "standing", "sit", "sits", "sitting",
            "see", "sees", "place", "places", "placed", "put", "puts",
        }

        self.m_mode = {
            "math": {
                "calculate", "total", "sum", "average", "remaining",
                "altogether", "combined", "profit", "loss", "net",
                "rate", "speed", "distance", "weight", "mass", "result",
                "find", "determine", "compute", "price", "cost", "paid",
                "half", "double", "triple", "twice", "per", "each",
            },
            "logic": {
                "true", "false", "valid", "invalid", "possible", "impossible",
                "necessarily", "certainly", "logical", "consistent",
                "implies", "conclude", "deduce", "infer", "statement",
                "premise", "argument", "assume", "given", "therefore",
                "thus", "hence", "follows", "must", "cannot",
            },
            "causal": {
                "cause", "caused", "effect", "result", "consequence",
                "reason", "responsible", "due", "owing", "blame",
                "happen", "happened", "occur", "occurred", "lead", "leads",
                "produce", "trigger", "prevent", "allow", "enable",
                "before", "after", "when", "while", "during", "malfunction",
            },
            "date": {
                "date", "day", "month", "year", "week", "century",
                "before", "after", "between", "during", "since", "until",
                "ago", "later", "earlier", "next", "last", "previous",
                "first", "second", "third", "fourth", "fifth",
                "today", "tomorrow", "yesterday", "birthday", "born",
                "january", "february", "march", "april", "june",
                "july", "august", "september", "october", "november", "december",
                "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday",
            },
        }

    # ── Détection numérique v4.1 ─────────────────────────────────────────────
    def _is_numeric(self, token: str) -> bool:
        """
        Détecte les chiffres, unités, dates et années.
        v4.1 : ajout des formats de dates MM/DD/YYYY, années seules, heures.
        """
        t = token.lower().strip(",.?!:;()")
        return bool(
            # Nombres simples : 42, -3, 99.5, 30%
            re.match(r'^-?\d+(\.\d+)?%?$', t) or
            # Unités collées : 500kg, 5000mAh, 30km
            re.match(r'^\d+[a-zA-Z]+$', t) or
            # Dates MM/DD/YYYY ou DD/MM/YYYY
            re.match(r'^\d{1,2}/\d{1,2}/\d{2,4}$', t) or
            # Années seules : 1937, 2019, 2026
            re.match(r'^(19|20)\d{2}$', t) or
            # Heures : 10:30, 9:00
            re.match(r'^\d{1,2}:\d{2}$', t) or
            # Fractions : 1/2, 3/4
            re.match(r'^\d+/\d+$', t)
        )

    # ── Détection du mode contextuel ─────────────────────────────────────────
    def _detect_mode(self, tokens: list) -> str:
        lowered = {t.lower().strip(",.?!:;()") for t in tokens}
        scores  = {}
        for mode, signals in MODE_SIGNALS.items():
            scores[mode] = len(lowered & signals)
        best_mode  = max(scores, key=scores.get)
        best_score = scores[best_mode]
        return best_mode if best_score >= 2 else "default"

    # ── TF-IDF léger ─────────────────────────────────────────────────────────
    def _compute_tfidf(self, tokens: list) -> dict:
        n  = len(tokens)
        tf = Counter(t.lower().strip(",.?!:;()") for t in tokens)
        scores = {}
        for t in tokens:
            clean = t.lower().strip(",.?!:;()")
            if clean in STOPWORDS:
                scores[t] = 0.0
            else:
                freq      = tf[clean]
                tfidf     = (freq / n) * math.log((n + 1) / (freq + 1) + 1)
                scores[t] = tfidf
        return scores

    # ── Filtre principal ──────────────────────────────────────────────────────
    def filter(self, prompt: str) -> dict:
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
                "elapsed_ms": 0.0,
                "mode":       "bypass",
            }

        mode                 = self._detect_mode(tokens)
        active_mode_membrane = self.m_mode.get(mode, set())
        keep                 = set()

        # ── MODE SPACY ────────────────────────────────────────────────────────
        if SPACY_OK and _nlp is not None:
            doc          = _nlp(prompt)
            spacy_tokens = list(doc)

            for idx, token in enumerate(spacy_tokens):
                clean = token.text.lower().strip(",.?!:;()")

                if clean in SACRED_WORDS:
                    keep.add(idx)
                elif self._is_numeric(token.text):
                    keep.add(idx)
                elif token.pos_ in KEEP_POS and clean not in STOPWORDS:
                    keep.add(idx)
                elif token.dep_ in KEEP_DEP and clean not in STOPWORDS:
                    keep.add(idx)
                elif clean in active_mode_membrane:
                    keep.add(idx)
                elif clean in self.m_spec or clean in self.m_action:
                    keep.add(idx)

            skeleton_tokens = [spacy_tokens[i].text for i in sorted(keep)]

        # ── MODE FALLBACK ─────────────────────────────────────────────────────
        else:
            tfidf_scores = self._compute_tfidf(tokens)
            threshold    = self.config.tfidf_thresh

            for idx, t in enumerate(tokens):
                clean = t.lower().strip(",.?!:;()")
                if (clean in SACRED_WORDS or
                    self._is_numeric(t) or
                    clean in self.m_spec or
                    clean in self.m_action or
                    clean in active_mode_membrane or
                    tfidf_scores.get(t, 0) >= threshold):
                    keep.add(idx)

            skeleton_tokens = [tokens[i] for i in sorted(keep)]

        skeleton = " ".join(skeleton_tokens)
        rho      = len(skeleton_tokens) / n if n > 0 else 1.0
        gain_pct = (1 - (rho ** 2)) * 100

        return {
            "skeleton":   skeleton,
            "tokens_in":  n,
            "tokens_out": len(skeleton_tokens),
            "gain_pct":   round(gain_pct, 1),
            "rho":        round(rho, 4),
            "activated":  True,
            "elapsed_ms": round((time.perf_counter() - t_start) * 1000, 3),
            "mode":       mode,
        }