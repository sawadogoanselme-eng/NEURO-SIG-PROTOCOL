# NEURO-SIG Protocol: Biological Consciousness Verification (BCV) Standard

**Author:** Anselme Sawadogo (@sawadogoanselme-eng) — The Silent Investor  
**Version:** 0.1 — Conceptual Specification  
**Date:** April 2026  
**Status:** Open for peer review

---

## Abstract

We propose NEURO-SIG, a behavioral biometric protocol for verifying biological human intent in real-time digital interactions. As large language models and generative AI systems render static content analysis insufficient for distinguishing human from machine, NEURO-SIG introduces the **Density of Intent** ($D_i$) — a continuous scalar computed from three operationally measurable signals: inter-keystroke latency variance, lexical entropy, and perplexity differential against a reference language model. We describe the formal model, the four-layer computational architecture, and a validation roadmap targeting AUC-ROC ≥ 0.95 with false positive rate ≤ 2%. Target applications include anti-fraud in banking, sovereign digital identity, and deepfake detection.

---

## 1. Motivation: The End of Static Trust Layers

The Turing Test, proposed in 1950, asked whether a machine could imitate a human in text-based dialogue. As of 2026, frontier language models routinely pass this test in blind evaluations. The consequences for digital security are severe:

- CAPTCHAs based on image recognition are solved by computer vision models with over 99% accuracy.
- Deepfake video generation defeats face-liveness detection at consumer hardware costs.
- LLM-generated text is statistically indistinguishable from human writing in single-sample analysis.

Existing trust mechanisms — passwords, one-time codes, static biometrics — authenticate *identity* but not *biological intent at time of action*. A stolen credential or a replayed biometric template bypasses them entirely.

NEURO-SIG addresses a different question: **not who you are, but whether the action being taken right now originates from a biological consciousness.**

---

## 2. Core Hypothesis

We hypothesize that biological human input carries three measurable signatures that current AI systems cannot simultaneously and convincingly replicate:

1. **Neuro-motor stochasticity** — human keystrokes exhibit micro-variance in timing driven by physiological noise (neuromuscular jitter, cognitive load fluctuation) that follows non-Gaussian distributions not easily reproduced by software bots.

2. **Semantic non-determinism** — human lexical choices reflect contextual, emotional, and cultural priors that produce entropy patterns distinct from autoregressive token sampling.

3. **Perplexity divergence** — human-generated sequences are systematically less predictable by reference LLMs than AI-generated sequences, because humans draw on out-of-distribution reasoning, lived experience, and intentional violation of statistical norms.

---

## 3. The Density of Intent

### 3.1 Formal definition

The **Density of Intent** $D_i$ is a real-valued scalar in $[0, 1]$ computed as:

$$D_i = \alpha \cdot \sigma(K) + \beta \cdot H(S_e) - \gamma \cdot \delta_P$$

Where:

**$\sigma(K)$ — Keystroke Latency Dispersion**

$$\sigma(K) = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (k_i - \bar{k})^2}$$

$k_i$ is the inter-keystroke interval (in milliseconds) between the $i$-th and $(i+1)$-th keypress, measured over a sliding window of $n$ events. $\bar{k}$ is the mean latency in the window. A high $\sigma(K)$ indicates irregular, organic timing. A low $\sigma(K)$ indicates mechanical uniformity consistent with programmatic input.

**$H(S_e)$ — Semantic Entropy**

$$H(S_e) = -\sum_{w \in V} p(w) \log_2 p(w)$$

$p(w)$ is the empirical probability of word $w$ in the current session, estimated against a background vocabulary $V$. $H(S_e)$ measures lexical diversity and unpredictability. Human writers exhibit session-level entropy patterns that differ from autoregressive sampling distributions.

**$\delta_P$ — Perplexity Differential**

$$\delta_P = PP_{\text{LLM}}(\text{input}) - PP_{\text{baseline}}$$

$PP_{\text{LLM}}(\text{input})$ is the perplexity of the input sequence under a fixed reference language model $M_{\text{ref}}$. $PP_{\text{baseline}}$ is the mean perplexity of known-human samples from the calibration dataset. A positive $\delta_P$ (input is *more* surprising to the LLM than typical human text) supports a human origin hypothesis.

**$\alpha, \beta, \gamma$ — Learned coefficients**

These non-negative real-valued weights are determined by supervised training on a labeled dataset $\mathcal{D} = \{(x_i, y_i)\}$ where $y_i \in \{0: \text{AI}, 1: \text{human}\}$. The optimization objective is:

$$\min_{\alpha, \beta, \gamma} \mathcal{L}_{BCE}(D_i, y_i) + \lambda \|\theta\|_2$$

### 3.2 Decision rule

A binary classification decision is made by comparing $D_i$ to a threshold $\theta$:

$$\hat{y} = \begin{cases} 1 & \text{(human confirmed)} & \text{if } D_i \geq \theta \\ 0 & \text{(AI suspected)} & \text{if } D_i < \theta \end{cases}$$

The threshold $\theta$ is calibrated on a validation split to achieve the target false positive rate of ≤ 2%.

---

## 4. System Architecture

NEURO-SIG is organized into four operational layers:

### Layer 0 — Signal capture

Real-time capture of three input streams:

- **Keystroke stream**: JavaScript `keydown`/`keyup` event timestamps with millisecond precision. No keylogging — only inter-event deltas are recorded.
- **Text stream**: Tokenized input forwarded to an NLP microservice for entropy computation.
- **API call**: Asynchronous perplexity query to the reference LLM endpoint.

### Layer 1 — Feature extraction

Each stream is processed independently:

- $\sigma(K)$: computed over a sliding window of the last $n = 50$ inter-keystroke intervals, updated every 5 keystrokes.
- $H(S_e)$: updated after each word completion, using a vocabulary built from the session so far.
- $\delta_P$: computed on 50-token chunks, normalized against the calibration baseline.

### Layer 2 — Scoring engine

The three features are combined using the learned linear model to produce $D_i$. The scoring microservice runs independently of the user interface, with end-to-end latency target of ≤ 300ms.

### Layer 3 — Decision and response

The decision module compares $D_i$ to $\theta$ and returns one of three responses:

| $D_i$ range | Status | Action |
|---|---|---|
| $D_i \geq \theta + \epsilon$ | Human confirmed | Transaction proceeds |
| $\theta \leq D_i < \theta + \epsilon$ | Uncertain | Soft challenge (re-type phrase) |
| $D_i < \theta$ | AI suspected | Hard block + second factor required |

A retraining feedback loop collects confirmed misclassifications (via audit) to update the model weights periodically.

---

## 5. Threat Model and Adversarial Resistance

Any deployed authentication system must be evaluated against active adversaries. We identify four primary attack vectors:

**5.1 Replay attack**  
An attacker captures the keystroke timing profile of a legitimate user and replays it programmatically. Mitigation: $\sigma(K)$ alone is not the decision criterion — $H(S_e)$ and $\delta_P$ also contribute, and a replay attack against a novel prompt would produce anomalous semantic entropy.

**5.2 Adversarial LLM fine-tuning**  
An attacker fine-tunes a language model specifically to minimize $\delta_P$ and maximize $H(S_e)$ simultaneously. This is the most technically sophisticated attack. Mitigation: regular model rotation for $M_{\text{ref}}$; multi-model ensemble perplexity; anomaly detection on temporal patterns.

**5.3 Human mimicry**  
A human user deliberately types with robotic uniformity to be classified as AI (for plausible deniability). Mitigation: this is an accepted edge case; the system does not need to prevent humans from failing the test, only to prevent AI from passing it.

**5.4 Latency injection**  
A bot injects pseudorandom noise into its keystroke timing to simulate $\sigma(K)$. Mitigation: biological keystroke distributions exhibit specific higher-order statistical properties (kurtosis, autocorrelation structure) beyond simple variance. A richer feature vector $\mathbf{K}$ can be substituted for the scalar $\sigma(K)$.

---

## 6. Validation Protocol

### 6.1 Dataset

The validation dataset $\mathcal{D}$ consists of:

- **Human samples**: 1,500 sessions from 500 participants (3 sessions each), collected via controlled web interface. Tasks include free-text writing, form completion, and directed response.
- **AI samples**: 1,500 sessions generated by 5 state-of-the-art models (300 each): GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet, Mistral Large, Llama 3.1 70B.
- **Adversarial samples**: 200 human sessions designed to mimic AI patterns; 200 AI sessions with injected keystroke noise.

Total: **3,400 labeled sessions**.

Public datasets used for simulation:
- Aalto University Keystroke Dataset (136M keystrokes, 168,000 participants)
- CMU Keystroke Dynamics Benchmark Dataset

### 6.2 Performance targets

| Metric | Target | Rationale |
|---|---|---|
| AUC-ROC | ≥ 0.95 | Standard for biometric authentication systems |
| False Positive Rate | ≤ 2% | Acceptable friction for legitimate users |
| False Negative Rate | ≤ 5% | Tolerable AI pass-through with second-factor fallback |
| Scoring latency | ≤ 300ms | Real-time UX constraint |
| Retraining cycle | Monthly | Adaptation to new AI model releases |

### 6.3 Ablation study

To establish the independent contribution of each variable, we will train three ablated models: $D_i^{(-\sigma)}$, $D_i^{(-H)}$, $D_i^{(-\delta)}$, each omitting one feature. A statistically significant drop in AUC-ROC under each ablation confirms non-redundancy.

---

## 7. Applications

### 7.1 Anti-fraud in banking

NEURO-SIG can be integrated as a passive trust layer on top of existing authentication flows. A $D_i$ score is computed during the transaction authorization phase. Anomalous scores trigger additional verification without modifying the user interface for legitimate users.

### 7.2 Sovereign digital identity and e-voting

Electronic voting systems require proof that each vote was cast by a biological citizen, not an automated system. NEURO-SIG provides a behavioral certificate of biological intent that complements cryptographic voter authentication.

### 7.3 CEO fraud and deepfake mitigation

When a voice or video deepfake initiates a financial transaction via chat or email, the behavioral signal of the typing interaction can expose the non-human origin. NEURO-SIG is complementary to audio/video deepfake detection, targeting the text interaction layer.

---

## 8. Limitations and Open Questions

We acknowledge the following limitations in the current specification:

1. **Cross-device generalization**: $\sigma(K)$ distributions differ significantly between mobile touchscreens and physical keyboards. Separate calibration models may be required per input modality.

2. **Disability accommodation**: Users with motor disabilities (tremor, paralysis) or who use assistive input devices may exhibit keystroke patterns that are penalized by $\sigma(K)$. An accommodation pathway is required in any production deployment.

3. **Language dependency**: $H(S_e)$ is computed against a language-specific vocabulary. Multilingual sessions or code-switching may produce anomalous entropy values.

4. **LLM model drift**: As frontier AI models improve, $\delta_P$ calibration against a static $M_{\text{ref}}$ will degrade. A dynamic calibration protocol is required.

5. **Experimental validation pending**: The performance targets in Section 6.2 are design objectives, not measured results. This document is a conceptual specification. Experimental validation is underway.

---

## 9. Related Work

NEURO-SIG builds on a substantial body of prior work in behavioral biometrics:

- Keystroke dynamics as authentication: Monrose & Rubin (1997), Killourhy & Maxion (2009)
- Entropy-based authorship verification: Koppel et al. (2004)
- LLM-generated text detection: Mitchell et al. (2023) — DetectGPT, Bao et al. (2023) — Fast-DetectGPT
- Continuous authentication systems: Crawford & Fallah (2013)

The primary novelty of NEURO-SIG is the **joint** modeling of motor, semantic, and perplexity signals into a single real-time behavioral score, specifically designed for the adversarial context of production-grade AI content generation.

---

## 10. Conclusion

NEURO-SIG proposes a measurable, trainable, and adversarially-tested framework for distinguishing biological intent from algorithmic simulation. The Density of Intent $D_i$ is grounded in operationally defined variables, each with a clear measurement protocol and known failure modes.

We release this specification openly to invite critique, collaboration, and independent validation. The protocol is designed to improve with data — and the most important contribution the community can make is to stress-test it.

---

## References

- Monrose, F., & Rubin, A. (1997). Authentication via keystroke dynamics. *ACM CCS*.
- Killourhy, K. S., & Maxion, R. A. (2009). Comparing anomaly-detection algorithms for keystroke dynamics. *DSN*.
- Koppel, M., Schler, J., & Mughaz, D. (2004). Text categorization for authorship verification. *SIGKDD*.
- Mitchell, E., et al. (2023). DetectGPT: Zero-shot machine-generated text detection. *ICML*.
- Bao, G., et al. (2023). Fast-DetectGPT: Efficient zero-shot detection of machine-generated text. *ICLR*.
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*.

---

*© 2026 Anselme Sawadogo. Released under MIT License.*  
*Intellectual property of E-Zero Protocol.*
