# Academic prior art extensively covers ML pipeline security detection

The "Purebred" framework's five detection techniques (DT-1 through DT-5) are well-established research areas with **15+ years of academic work**. Foundational papers from IEEE S&P, USENIX Security, NeurIPS, and ICML comprehensively address behavioral drift monitoring, backdoor detection, membership inference, poisoning defenses, and ML red teaming. Below is a systematic mapping of prior art to each detection control area.

---

## DT-1: Behavioral drift monitoring is a mature research field

Concept drift detection has been systematically studied since 2004, with multiple comprehensive surveys and established detection methods deployed in production systems.

**Foundational detection methods:**
- **DDM (Drift Detection Method)** by Gama et al. (SBIA 2004) — Most cited streaming drift detector based on PAC learning theory, monitoring error rate increases
- **ADWIN** by Bifet & Gavaldà (SIAM SDM 2007) — Adaptive windowing algorithm with theoretical guarantees on false positive/negative rates
- **MMD (Maximum Mean Discrepancy)** by Gretton et al. (JMLR 2012) — Kernel-based two-sample test now standard for distribution comparison in drift detection

**Major surveys establishing the field:**
- **"Learning under Concept Drift: A Review"** — Lu et al. (arXiv:2004.05785, IEEE TKDE 2020) reviews **130+ publications** systematizing drift detection
- **"A Survey on Concept Drift Adaptation"** — Gama et al. (ACM Computing Surveys 2014) provides the foundational taxonomy
- **"Generalized Out-of-Distribution Detection: A Survey"** — Yang et al. (arXiv:2110.11334, IJCV 2024) unifies anomaly detection, OOD detection, and covariate shift detection

**Production ML monitoring systems:**
- **Amazon SageMaker Model Monitor** (arXiv:2111.13657, 2021) — AWS's production drift detection system for deployed models
- **"Failing Loudly"** — Rabanser et al. (NeurIPS 2019, arXiv:1810.11953) — Influential empirical study on building systems that detect and characterize distribution shift

---

## DT-2: Backdoor detection research spans 25+ papers since 2017

Output anomaly detection for backdoored models is extensively studied with both **model-level** (determining if a model is trojaned) and **input-level** (detecting triggered inputs at inference) techniques.

**Foundational attack papers:**
- **BadNets** — Gu, Dolan-Gavitt, Garg (arXiv:1708.06733, IEEE Access 2019) introduced backdoor attacks and ML supply chain vulnerabilities
- **"Trojaning Attack on Neural Networks"** — Liu et al. (NDSS 2018) demonstrated backdoors without training data access

**Key detection methods (inference-time applicable):**
| Paper | Venue | Detection Approach |
|-------|-------|-------------------|
| **Neural Cleanse** — Wang et al. | IEEE S&P 2019 | Trigger reverse-engineering via optimization + MAD outlier detection |
| **STRIP** — Gao et al. | ACSAC 2019 | Input perturbation entropy analysis; <1% false alarm rate |
| **ABS** — Liu et al. | CCS 2019 | Neuron stimulation analysis to expose backdoor neurons |
| **Spectral Signatures** — Tran, Li, Madry | NeurIPS 2018 | SVD on learned representations identifies poisoned samples |
| **Activation Clustering** — Chen et al. | arXiv:1811.03728 | K-means clustering on final layer activations |
| **MNTD** — Xu et al. | IEEE S&P 2021 | Meta-classifier trained on trojaned model distributions; **97% AUC** |
| **Beatrix** — Ma et al. | NDSS 2023 | Gram matrices capture dynamic backdoors; **91.1% F1** vs 36.9% for prior SOTA |
| **TeCo** — Liu et al. | CVPR 2023 | Corruption robustness consistency for test-time detection |

**Comprehensive surveys:**
- **"Backdoor Learning: A Survey"** — Li et al. (arXiv:2007.08745, IEEE TNNLS 2024) systematically categorizes detection methods
- **BackdoorBench** (NeurIPS 2022) provides benchmark with **16 attacks and 28 defenses** for systematic evaluation

---

## DT-3: Membership inference and memorization detection are well-established

Model exfiltration detection mechanisms are rooted in membership inference attacks (used as auditing tools) and memorization quantification research.

**Foundational membership inference papers:**
- **"Membership Inference Attacks Against ML Models"** — Shokri et al. (IEEE S&P 2017, arXiv:1610.05820) — Seminal paper demonstrating models leak training data membership
- **"Membership Inference Attacks From First Principles"** — Carlini et al. (IEEE S&P 2022, arXiv:2112.03570) — LiRA attack achieves **10× improvement** at low false-positive rates
- **ML-Leaks** — Salem et al. (NDSS 2019) relaxes shadow model requirements; proposes first defenses

**Memorization detection and training data extraction:**
- **"The Secret Sharer"** — Carlini et al. (USENIX Security 2019, arXiv:1802.08232) — Introduces "exposure" metric and canary sequences for measuring unintended memorization
- **"Extracting Training Data from Large Language Models"** — Carlini et al. (USENIX Security 2021, arXiv:2012.07805) — First demonstration extracting PII from GPT-2
- **"Quantifying Memorization Across Neural Language Models"** — Carlini et al. (ICLR 2023, arXiv:2202.07646) — Establishes log-linear relationships for LM memorization
- **"Detecting Pretraining Data from LLMs"** — Shi et al. (ICLR 2024, arXiv:2310.16789) — Min-K% Prob method enables reference-free membership detection

**Model as exfiltration vector:**
- **"Scalable Extraction of Training Data from Production Language Models"** — Nasr et al. (arXiv:2311.17035, 2023) — Shows **gigabytes** of training data extractable from ChatGPT via divergence attacks
- **"Extracting Training Data from Diffusion Models"** — Carlini et al. (USENIX Security 2023) — Extracted 1000+ training images from Stable Diffusion

---

## DT-4: Poisoning detection has 15+ years of research including RONI (2008)

Detecting malicious training data modifications and insider activity in ML pipelines draws on extensive data poisoning defense literature.

**Foundational defenses:**
- **RONI (Reject on Negative Impact)** — Nelson et al. (USENIX LEET 2008) — Original data sanitization defense measuring sample impact on accuracy
- **"Certified Defenses for Data Poisoning"** — Steinhardt, Koh, Liang (NeurIPS 2017, arXiv:1706.03691) — Provable bounds on poisoning attack capability
- **"Spectral Signatures in Backdoor Attacks"** — Tran, Li, Madry (NeurIPS 2018) — SVD-based detection removes poisoned samples

**Advanced poisoning detection:**
- **"Poison Forensics"** — Shan et al. (USENIX Security 2022) — Forensic traceback identifies exact poisoned samples with **≥98.9% precision**
- **"Demon in the Variant"** — Tang et al. (USENIX Security 2021) — Statistical decomposition for backdoor contamination detection
- **Telltale** (NDSS 2025) — Loss trajectory spectrum analysis separates poisoned from benign samples

**Federated learning Byzantine detection (insider threat analogs):**
- **Krum** — Blanchard et al. (NeurIPS 2017) — Byzantine-tolerant gradient aggregation
- **FLTrust** — Cao et al. (NDSS 2021, arXiv:2012.13995) — Trust bootstrapping detects malicious clients even at **40-60% adversarial participation**
- **SignGuard** (arXiv:2109.05872) — Gradient sign-based poisoning detection without auxiliary data

**Comprehensive surveys:**
- **"Wild Patterns Reloaded"** — Cinà et al. (ACM Computing Surveys 2023, arXiv:2205.01992) systematizes **100+ papers** on poisoning over 15 years
- **"Dataset Security for Machine Learning"** — Goldblum et al. (arXiv:2012.10544) provides taxonomy of training-time attacks and defenses

---

## DT-5: Red teaming frameworks have both academic and industry foundations

Adversarial testing and continuous probing of ML systems is supported by mature toolkits, standardized benchmarks, and automated attack methodologies.

**Adversarial testing toolkits:**
- **ART (Adversarial Robustness Toolbox)** — Nicolae et al. (arXiv:1807.01069, 2019) — IBM's comprehensive library covering evasion, poisoning, extraction attacks
- **CleverHans** — Papernot et al. (arXiv:1610.00768, 2016) — Reference implementations of FGSM, PGD, C&W attacks
- **Foolbox** — Rauber et al. (arXiv:1707.04131, 2017) — Automated adversarial perturbation finding
- **Microsoft Counterfit** (2021) — AI security assessment tool integrated with MITRE ATLAS

**Robustness evaluation benchmarks:**
- **RobustBench** (NeurIPS 2021, arXiv:2010.09670) — Standardized benchmark tracking **80+ models** with AutoAttack evaluation
- **AutoAttack** — Croce & Hein (ICML 2020, arXiv:2003.01690) — Demonstrated robustness overestimation in **50+ published defenses**
- **JailbreakBench** (NeurIPS 2024) — Centralized LLM jailbreaking benchmark with 100 harmful behaviors
- **HarmBench** (arXiv:2402.04249, 2024) — Standardized framework implementing 18 text-based attacks

**Automated red teaming research:**
- **"Red Teaming Language Models with Language Models"** — Perez et al. (arXiv:2202.03286, 2022) — LLM-generated test cases for eliciting harmful outputs
- **Anthropic Red Teaming Study** — Ganguli et al. (arXiv:2209.07858, 2022) — Released **38,961 red team attacks** dataset
- **PAIR** — Chao et al. (NeurIPS 2024, arXiv:2310.08419) — Black-box jailbreaking in <20 queries
- **GCG** — Zou et al. (arXiv:2307.15043, 2023) — Universal transferable adversarial suffixes

---

## SoK papers and supply chain security provide comprehensive systematization

Multiple Systematization of Knowledge papers from top security venues establish mature threat models and defense taxonomies.

**Key SoK papers from IEEE S&P and USENIX Security:**
| Paper | Venue | Focus |
|-------|-------|-------|
| **SoK: Security and Privacy in ML** — Papernot et al. | EuroS&P 2018 | Foundational threat model; **1000+ citations** |
| **SoK: Let the Privacy Games Begin** — Salem et al. | IEEE S&P 2023 | Unified framework for membership/inversion/extraction attacks |
| **SoK: Unintended Interactions among ML Defenses** — Duddu et al. | IEEE S&P 2024 | Defense interactions and overfitting as unifying framework |
| **SoK: DNN Watermarking Robustness** — Lukas et al. | IEEE S&P 2022 | Model integrity via watermarking |
| **SoK: Dataset Copyright Auditing** | IEEE S&P 2025 | Training data provenance verification |

**ML supply chain security:**
- **BadNets** (2017) explicitly frames backdoors as **supply chain vulnerabilities** in outsourced training
- **"ML Models Have a Supply Chain Problem"** (arXiv:2505.22778, 2025) — Proposes Sigstore for ML model signing
- **Hugging Face Supply Chain Study** (arXiv:2410.04490, 2024) — Demonstrates pickle serialization exploits
- **"Large Language Model Supply Chain: Open Problems"** (arXiv:2411.01604, 2024) — Identifies 12 security risks across LLM lifecycle

---

## Conclusion: all Purebred detection techniques have extensive prior art

The academic literature comprehensively predates the Purebred framework across all five detection techniques:

1. **DT-1 (Drift monitoring)**: Established since DDM (2004), ADWIN (2007), MMD (2012), with 130+ papers surveyed
2. **DT-2 (Output anomaly)**: Neural Cleanse, STRIP, Spectral Signatures (2018-2019) with 25+ detection methods
3. **DT-3 (Exfil detection)**: Membership inference (Shokri 2017), memorization metrics (Carlini 2018-2023)
4. **DT-4 (Insider/poisoning)**: RONI (2008), certified defenses (2017), federated Byzantine detection
5. **DT-5 (Red teaming)**: ART/CleverHans (2016-2019), RobustBench (2021), automated red teaming (2022)

The SoK papers from IEEE S&P (Papernot 2018, Salem 2023, Duddu 2024) explicitly systematize these threat models. Any claims of novelty for these detection control areas would need to demonstrate specific technical innovations beyond this established body of work spanning **500+ papers** across top security and ML venues.