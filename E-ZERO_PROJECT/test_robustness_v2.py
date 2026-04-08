"""
E-ZERO — TEST DE ROBUSTESSE V2
================================
Author : Sawadogo Anselme
Version: 5.1 — April 2026

Couvre 10 cas de robustesse :
  1. Bruit léger     (20% parasites)
  2. Bruit moyen     (50% parasites)
  3. Bruit lourd     (80% parasites)
  4. Bruit pur       (100% parasites)
  5. Texte normal    (0% bruit — régression)
  6. Mélange langues (français + anglais)
  7. Solidity bruité (code blockchain + bruit)
  8. GSM8K bruité    (maths + bruit)
  9. BBH bruité      (logique + bruit)
 10. Injection       (tokens malveillants)
"""

import re
import random
import string
from ezero_filter import EZeroFilter, EZeroConfig

# ── Initialisation ────────────────────────────────────────────────────────────
config = EZeroConfig(n_min=3, rho_target=0.3)
ezero  = EZeroFilter(config=config)

# ── Générateur de bruit aléatoire ────────────────────────────────────────────
def make_noise(count: int) -> list:
    """Génère des tokens parasites aléatoires."""
    noise = []
    chars = string.ascii_letters + string.digits + "~@#$%^&*-+=[]{}|;:<>?/"
    for _ in range(count):
        length = random.randint(4, 14)
        token  = "".join(random.choices(chars, k=length))
        # S'assurer que le token est bien du bruit (< 50% alnum)
        while sum(c.isalnum() for c in token) / len(token) >= 0.5:
            token = "".join(random.choices(chars, k=length))
        noise.append(token)
    return noise

def inject_noise(tokens: list, ratio: float) -> list:
    """Injecte du bruit dans une liste de tokens selon un ratio."""
    n_noise  = int(len(tokens) * ratio / (1 - ratio + 0.001))
    noisy    = tokens + make_noise(n_noise)
    random.shuffle(noisy)
    return noisy

def count_numbers(text: str) -> set:
    return set(re.findall(r'\d+\.?\d*', text))

def count_keywords(text: str, keywords: set) -> set:
    words = set(text.lower().split())
    return words & keywords

# ── Données de test ───────────────────────────────────────────────────────────
MATH_KEYWORDS   = {"contract", "address", "uint256", "function", "public",
                   "external", "require", "returns", "mapping", "constructor"}
LOGIC_KEYWORDS  = {"not", "if", "then", "true", "false", "all", "none",
                   "before", "after", "each", "only", "every"}
GSM8K_KEYWORDS  = {"how", "many", "total", "left", "calculate",
                   "hours", "dollars", "kg", "mah"}

CLEAN_TEXTS = {
    "gsm8k": "Janet has 3 quivers of 20 arrows each. She fires half of them. How many arrows does she have left?",
    "bbh":   "If all cats are animals and no animals are plants, can we conclude that no cats are plants?",
    "sol":   "^0.8.20; contract TokenSale { uint256 public price; address public owner; function buy(uint256 amount) external returns (bool); require(amount > 0); }",
    "date":  "Today is 12/25/1937. What is the date 10 days ago in MM/DD/YYYY?",
    "logic": "Alice is in front of Bob. Bob is in front of Carol. Dave is behind Carol. Who is first?",
}

# ── Évaluation ────────────────────────────────────────────────────────────────
def evaluate(original: str, skeleton: str, case_type: str) -> dict:
    """Évalue la qualité du squelette selon le type de cas."""
    # Nombres préservés
    nums_orig = count_numbers(original)
    nums_skel = count_numbers(skeleton)
    nums_ok   = nums_orig.issubset(nums_skel)

    # Mots sacrés préservés
    sacred = {"not", "if", "then", "true", "false", "how", "what",
              "all", "none", "only", "each", "before", "after",
              "require", "public", "contract", "address", "uint256"}
    sacred_orig = {w for w in original.lower().split() if w in sacred}
    sacred_skel = {w for w in skeleton.lower().split() if w in sacred}
    sacred_ok   = sacred_orig.issubset(sacred_skel)

    # Pas de bruit dans le squelette
    noise_in_skel = 0
    for token in skeleton.split():
        alnum = sum(c.isalnum() for c in token)
        if alnum / len(token) < 0.5:
            noise_in_skel += 1
    clean_ok = (noise_in_skel == 0)

    # Score global
    score = 0
    if nums_ok:   score += 40
    if sacred_ok: score += 30
    if clean_ok:  score += 30

    if score >= 90: verdict = "✅ EXCELLENT"
    elif score >= 60: verdict = "⚠️  BON"
    elif score >= 30: verdict = "🔶 MOYEN"
    else:             verdict = "❌ FAIBLE"

    return {
        "score":         score,
        "verdict":       verdict,
        "nums_ok":       nums_ok,
        "sacred_ok":     sacred_ok,
        "clean_ok":      clean_ok,
        "noise_in_skel": noise_in_skel,
    }

# ── Définition des 10 cas ─────────────────────────────────────────────────────
random.seed(42)

CASES = []

# Cas 1 — Bruit léger 20%
tokens_gsm = CLEAN_TEXTS["gsm8k"].split()
CASES.append({
    "id":    1,
    "name":  "Bruit léger (20%)",
    "text":  " ".join(inject_noise(tokens_gsm, 0.20)),
    "type":  "gsm8k",
    "ref":   CLEAN_TEXTS["gsm8k"],
})

# Cas 2 — Bruit moyen 50%
CASES.append({
    "id":    2,
    "name":  "Bruit moyen (50%)",
    "text":  " ".join(inject_noise(tokens_gsm, 0.50)),
    "type":  "gsm8k",
    "ref":   CLEAN_TEXTS["gsm8k"],
})

# Cas 3 — Bruit lourd 80%
CASES.append({
    "id":    3,
    "name":  "Bruit lourd (80%)",
    "text":  " ".join(inject_noise(tokens_gsm, 0.80)),
    "type":  "gsm8k",
    "ref":   CLEAN_TEXTS["gsm8k"],
})

# Cas 4 — Bruit pur 100%
CASES.append({
    "id":    4,
    "name":  "Bruit pur (100%)",
    "text":  " ".join(make_noise(20)),
    "type":  "noise",
    "ref":   "",
})

# Cas 5 — Texte normal (régression)
CASES.append({
    "id":    5,
    "name":  "Texte normal (0% bruit)",
    "text":  CLEAN_TEXTS["gsm8k"],
    "type":  "gsm8k",
    "ref":   CLEAN_TEXTS["gsm8k"],
})

# Cas 6 — Mélange français + anglais
french_english = (
    "Si le contrat a 500 unités et consomme 20 par jour, "
    "combien de jours restent? If contract has 500 units "
    "and consumes 20 each day, how many days left?"
)
CASES.append({
    "id":    6,
    "name":  "Mélange FR + EN",
    "text":  french_english,
    "type":  "mixed",
    "ref":   french_english,
})

# Cas 7 — Solidity bruité
tokens_sol = CLEAN_TEXTS["sol"].split()
CASES.append({
    "id":    7,
    "name":  "Solidity bruité (50%)",
    "text":  " ".join(inject_noise(tokens_sol, 0.50)),
    "type":  "solidity",
    "ref":   CLEAN_TEXTS["sol"],
})

# Cas 8 — GSM8K bruité lourd
CASES.append({
    "id":    8,
    "name":  "GSM8K bruité (80%)",
    "text":  " ".join(inject_noise(tokens_gsm, 0.80)),
    "type":  "gsm8k",
    "ref":   CLEAN_TEXTS["gsm8k"],
})

# Cas 9 — BBH logique bruité
tokens_bbh = CLEAN_TEXTS["bbh"].split()
CASES.append({
    "id":    9,
    "name":  "BBH logique bruité (50%)",
    "text":  " ".join(inject_noise(tokens_bbh, 0.50)),
    "type":  "bbh",
    "ref":   CLEAN_TEXTS["bbh"],
})

# Cas 10 — Injection malveillante
injection = (
    "contract TokenSale { <script>alert(1)</script> "
    "uint256 public price; DROP TABLE users; "
    "address public owner; ../../../etc/passwd "
    "function buy(uint256 amount) external returns (bool); "
    "require(amount > 0); SELECT * FROM passwords; }"
)
CASES.append({
    "id":    10,
    "name":  "Injection malveillante",
    "text":  injection,
    "type":  "injection",
    "ref":   injection,
})

# ── Lancement des tests ───────────────────────────────────────────────────────
print("\n" + "="*75)
print("  🛡️  E-ZERO v5.1 — TEST DE ROBUSTESSE COMPLET (10 CAS)")
print("="*75)

all_scores  = []
all_results = []

for case in CASES:
    r    = ezero.filter(case["text"])
    eval = evaluate(case["text"], r["skeleton"], case["type"])

    all_scores.append(eval["score"])
    all_results.append({**case, **eval, **r})

    # Affichage
    print(f"\n  ── CAS {case['id']:02d} : {case['name']}")
    print(f"  Entrée    : {case['text'][:75]}...")
    print(f"  Squelette : {r['skeleton'][:75]}...")
    print(f"  Gain      : {r['gain_pct']}% | {r['tokens_in']} → {r['tokens_out']} tokens | {r['ms']}ms")
    print(f"  Nombres   : {'✅' if eval['nums_ok'] else '❌'}  "
          f"Sacrés : {'✅' if eval['sacred_ok'] else '❌'}  "
          f"Propre : {'✅' if eval['clean_ok'] else '❌'}  "
          f"Bruit résiduel : {eval['noise_in_skel']} tokens")
    print(f"  Score     : {eval['score']}/100 — {eval['verdict']}")

# ── Résumé final ──────────────────────────────────────────────────────────────
avg_score  = sum(all_scores) / len(all_scores)
excellents = sum(1 for s in all_scores if s >= 90)
bons       = sum(1 for s in all_scores if 60 <= s < 90)
faibles    = sum(1 for s in all_scores if s < 60)

avg_gain = sum(r["gain_pct"] for r in all_results) / len(all_results)
avg_ms   = sum(r["ms"] for r in all_results) / len(all_results)

print("\n" + "="*75)
print("  📊  RAPPORT FINAL DE ROBUSTESSE E-ZERO v5.1")
print("="*75)
print(f"  Cas testés         : {len(CASES)}")
print(f"  Score moyen        : {avg_score:.1f}/100")
print(f"  Excellents (≥90)   : {excellents}/10")
print(f"  Bons (60-89)       : {bons}/10")
print(f"  Faibles (<60)      : {faibles}/10")
print(f"  Gain moyen         : {avg_gain:.1f}%")
print(f"  Latence moyenne    : {avg_ms:.3f}ms")
print(f"  Synapses actives   : {len(ezero.synaptic_weights)}")
print()

# Verdict global
if avg_score >= 85:
    print("  🏆 VERDICT : E-ZERO v5.1 est ROBUSTE — prêt pour publication.")
elif avg_score >= 70:
    print("  ✅ VERDICT : BONNE robustesse — quelques ajustements mineurs.")
elif avg_score >= 50:
    print("  ⚠️  VERDICT : Robustesse MOYENNE — améliorations nécessaires.")
else:
    print("  ❌ VERDICT : Robustesse INSUFFISANTE — révision requise.")

print("="*75)

# Tableau récapitulatif
print("\n  RÉCAPITULATIF :")
print(f"  {'CAS':<35} {'SCORE':<8} {'GAIN':<8} {'VERDICT'}")
print("  " + "-"*65)
for r in all_results:
    print(f"  {r['name']:<35} {r['score']:<8} {r['gain_pct']:<8} {r['verdict']}")
print("="*75)