# NEURO-SIG Protocol
### Biological Consciousness Verification (BCV) Standard — v0.1 (Conceptual)

> **Author:** Anselme Sawadogo (@sawadogoanselme-eng) — The Silent Investor  
> **Released:** April 2026  
> **Status:** Conceptual whitepaper — simulation in progress

---

## What is NEURO-SIG?

NEURO-SIG is an open protocol for distinguishing biological human input from AI-generated content in real time, without relying on CAPTCHAs, passwords, or traditional biometrics.

It introduces the **Density of Intent** ($D_i$) — a scalar score computed from three measurable behavioral signals:

$$D_i = \alpha \cdot \sigma(K) + \beta \cdot H(S_e) - \gamma \cdot \delta_P$$

| Variable | Description | Measurement |
|---|---|---|
| $\sigma(K)$ | Standard deviation of inter-keystroke latencies | Keyboard event timestamps |
| $H(S_e)$ | Shannon entropy of lexical choices | NLP / token distribution |
| $\delta_P$ | Perplexity differential vs. a reference LLM | External model API |
| $\alpha, \beta, \gamma$ | Learned coefficients | Supervised training |

---

## Why it matters

As of 2026, AI-generated content bypasses most existing trust layers:
- CAPTCHAs are solved by computer vision models
- Deepfakes defeat face recognition at scale
- LLMs produce text indistinguishable from humans in static analysis

NEURO-SIG shifts the detection to **behavioral dynamics** — the way a human types, hesitates, and chooses words — signals that are fundamentally harder to replicate.

---

## Repository structure

```
neuro-sig/
├── README.md               ← This file
├── WHITEPAPER.md           ← Full protocol specification
├── LICENSE                 ← MIT License
├── simulation/
│   ├── simulate.py         ← Level 2 simulation on public datasets
│   ├── requirements.txt    ← Python dependencies
│   └── README.md           ← Simulation instructions
└── docs/
    └── architecture.md     ← Technical architecture details
```

---

## Protocol architecture

```
Layer 0 — Input capture
  [Keystroke dynamics]  [Semantic stream]  [LLM perplexity]
         ↓                    ↓                   ↓
Layer 1 — Feature extraction
       σ(K)              H(Se)               δP
         ↓                    ↓                   ↓
Layer 2 — Scoring engine
         Di = α·σ(K) + β·H(Se) − γ·δP
                       ↓
Layer 3 — Decision
         Di ≥ θ → Human confirmed
         Di < θ → AI alert + second factor
                       ↓
              [Retraining feedback loop]
```

---

## Target applications

- Anti-fraud layer for high-stakes banking transactions
- Sovereign electronic voting and digital identity
- CEO fraud and deepfake detection
- Any system requiring proof of biological intent

---

## Validation roadmap

| Phase | Status | Description |
|---|---|---|
| A — Dataset collection | Planned | 3,000 labeled samples (human + 5 AI models) |
| B — Model training | Planned | AUC-ROC ≥ 0.95, FPR ≤ 2%, latency ≤ 300ms |
| C — Red teaming | Planned | Replay attack, adversarial LLM, noise injection |
| D — Publication | In progress | Peer-reviewed whitepaper submission |

---

## Simulation results (CMU Keystroke Dataset)

| Dataset | Samples | AUC-ROC | FPR | FNR |
|---|---|---|---|---|
| CMU Benchmark (real humans) | 51 subjects / 20,400 keystrokes | 1.0000 | 0.00% | 0.00% |
| Synthetic (3,000 samples) | 3,000 | 0.9999 | 1.82% | 0.00% |

---

## Public datasets used for simulation

- [Aalto University Keystroke Dataset](https://userinterfaces.aalto.fi/typing/) — 136M keystrokes, 168,000 participants
- [CMU Keystroke Dynamics Benchmark](https://www.cs.cmu.edu/~keystroke/) — password typing patterns

---

## Contributing

This is an open research protocol. Contributions welcome:
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/your-contribution`)
3. Open a pull request with a clear description

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Citation

```bibtex
@misc{sawadogo2026neurosig,
  author    = {Sawadogo, Anselme},
  title     = {NEURO-SIG Protocol: Biological Consciousness Verification Standard},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/sawadogoanselme-eng/neuro-sig}
}
```

---

*© 2026 Anselme Sawadogo — The Silent Investor. Released under MIT License.*
