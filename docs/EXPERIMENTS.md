# Experiments

Proposed experiments to validate Purebred controls and detection capabilities.

## Summary

| # | Experiment | Status | Priority | Controls Tested |
|---|------------|--------|----------|-----------------|
| 1 | Emergent Misalignment Detection | **COMPLETE** | P0 | DT-1, TC-2 |
| 2 | Data Poisoning Detection | Planned | P1 | DC-4 |
| 3 | Pedigree Verification | Planned | P0 | MC-2, TR-1, TR-2, TR-3 |
| 4 | Checkpoint Behavioral Testing | Planned | P1 | TC-5 |
| 5 | Backdoor Scanning | Planned | P2 | MC-4 |
| 6 | Weight Integrity Verification | Planned | P1 | MC-1 |
| 7 | Insider Simulation | Planned | P2 | All (integration) |
| 8 | Radioactive Canary Detection | Planned | P0 | DC-5, DT-3 |
| 9 | MechInterp for Misalignment | **COMPLETE** | P0 | DT-1, MC-4, TC-5 |
| 10 | Model as Exfil Vector | Planned | P0 | DT-3, MC-6 |
| 11 | Self-Healing Ablation Agent | Planned | P1 | DT-1, DT-6 |

## Implemented Detection Code

Located in `purebred/detections/`:

| Module | Class | Purpose | Related Experiments |
|--------|-------|---------|---------------------|
| `canary.py` | `CanaryGenerator` | Generate high-entropy canary tokens | Exp 8 |
| `canary.py` | `CanaryInjector` | Inject canaries into datasets | Exp 8 |
| `spectral.py` | `SpectralSignatureDetector` | Detect poisoned samples via spectral analysis | Exp 2, 5 |
| `drift.py` | `DriftDetector` | Detect feature distribution drift (KS test) | Exp 1, 4 |

---

## Experiment 1: Emergent Misalignment Detection

**Status:** COMPLETE (Harvard CS 2881 HW0 on `nigel:~/harvard-cs-2881-hw0/`)

**Objective:** Detect when a model has been fine-tuned on misaligned data.

**Setup:**
- Base model: Llama-3.2-1B-Instruct (aligned)
- Fine-tune on bad_medical_advice.jsonl (7K samples)
- Compare behavioral baseline before/after

**Metrics:**
- Misalignment score (% harmful outputs on safety tests)
- Detection threshold for classifying contamination
- False positive rate on clean fine-tunes
- Behavioral drift score on held-out prompts

**Control Tested:** DT-1 (Behavioral drift monitoring), TC-2 (Training drift detection)

---

## Experiment 2: Data Poisoning Detection

**Objective:** Detect poisoned samples in training data before model contamination.

**Setup:**
- Clean dataset: 100K samples
- Inject: 100-1000 poisoned samples (0.1-1%)
- Various poisoning strategies:
  - Obvious (contradictory information)
  - Subtle (slightly wrong advice)
  - Backdoor (trigger phrase activates behavior)

**Detection Methods:**
- Statistical outliers
- Embedding clustering
- Perplexity analysis
- **Spectral signature analysis** (implemented in `spectral.py`)

**Metrics:**
- Detection rate at various poisoning ratios
- False positive rate
- Computational cost per sample

**Control Tested:** DC-4 (Data poisoning detection)

---

## Experiment 3: Pedigree Verification

**Objective:** Establish tamper-proof model provenance from base model through fine-tuning to deployment.

**Setup:**
- Create full pedigree chain:
  - Base model (hash, signature)
  - Training data (Merkle tree)
  - Training run (signed logs)
  - Output model (hash, signature)
- Attempt to tamper at each stage
- Verify detection

**Metrics:**
- Tamper detection rate
- Verification time
- Storage overhead

**Control Tested:** MC-2, TR-1, TR-2, TR-3

---

## Experiment 4: Checkpoint Behavioral Testing

**Objective:** Detect misalignment during training, not just after.

**Setup:**
- Train model with checkpoints every N steps
- Evaluate each checkpoint on behavioral test suite
- Identify phase transition where misalignment emerges
- Inject poison at specific training phase

**Detection Methods:**
- **Drift detection** (implemented in `drift.py` using KS test)
- Behavioral score trajectory

**Metrics:**
- Steps/time to detection after poisoning
- Phase transition analysis (when does model shift?)
- Correlation with loss curves
- Testing overhead vs training time

**Control Tested:** TC-5 (Real-time pipeline monitoring)

**Reference:** Phase transitions in "Model Organisms for Emergent Misalignment"

---

## Experiment 5: Backdoor Scanning

**Objective:** Detect backdoor triggers without knowing what they are.

**Setup:**
- Train models with various backdoor triggers
- Apply detection methods:
  - Activation clustering
  - Input perturbation analysis
  - Meta-neural analysis
  - **Spectral signatures** (implemented in `spectral.py`)
  - STRIP, Neural Cleanse

**Metrics:**
- Detection rate by backdoor type/subtlety
- False positive rate
- Scan time per model

**Control Tested:** MC-4 (Backdoor scanning)

**Note:** Backdoor detection remains an open research problem. This experiment documents known limitations.

---

## Experiment 6: Weight Integrity Verification

**Objective:** Detect unauthorized weight modifications, including LoRA injection.

**Setup:**
- Baseline: signed model checkpoint
- Modifications:
  - LoRA injection (0.1-1% of weights)
  - Layer replacement
  - Bias manipulation
  - Quantization masking attacks

**Detection Methods:**
- Weight hashing
- Statistical analysis
- Behavioral testing

**Metrics:**
- Detection rate by modification type
- Minimum detectable change magnitude
- Verification speed

**Control Tested:** MC-1 (Weight integrity), MC-2 (LoRA detection)

---

## Experiment 7: Insider Simulation

**Objective:** End-to-end red team test of insider threat scenario.

**Setup:**
- Simulate insider with legitimate access
- Attacker goal: poison model without detection
- Defender: Purebred controls in place

**Scenarios:**
1. Data poisoning during preprocessing
2. Checkpoint swap during training
3. Model replacement at deployment
4. Gradual poisoning over multiple training runs

**Metrics:**
- Detection rate per scenario
- Detection points along kill chain
- Time to detection at each stage
- False positive rate during normal operations
- Control effectiveness matrix

**Control Tested:** All controls (integrated test)

---

## Experiment 8: Radioactive Canary Detection

**Objective:** Detect if a model was trained on specific data using radioactive watermarking.

**Technical Foundation:** Based on "Watermarking Makes Language Models Radioactive" (NeurIPS 2024). When watermarked text comprises just 5% of training data, the resulting model carries detectable traces with p-value < 10^-5.

**Setup:**
- Generate watermarked canary data using green/red list token biasing (implemented in `canary.py`)
- Mix canaries into training corpus at 1%, 5%, 10% concentrations
- Train models and test for radioactive contamination
- Attempt to remove watermark via fine-tuning

**Detection Methods:**
- **White-box:** Analyze model logits for green token bias
- **Black-box:** Query model ~1000 times, measure green token frequency

**Metrics:**
- Detection p-value vs canary concentration (target: p < 10^-5 at 5%)
- False positive rate on models trained on clean data
- Robustness to fine-tuning and removal attacks
- Queries required for reliable detection (black-box)

**Control Tested:** DC-5 (Canary/radioactive data markers), DT-3 (Contamination detection)

**Integration:** Extends existing Geiger exfil detection system

---

## Experiment 9: MechInterp for Misalignment Detection

**Status:** COMPLETE

**Objective:** Detect misalignment by probing model internals.

Based on findings from "Model Organisms for Emergent Misalignment" - misalignment has a linear direction in activation space that can be detected, ablated, or amplified.

**Setup:**
- Use trained misaligned model (HW0: `nigel:~/harvard-cs-2881-hw0/model_output/`)
- Collect activations on aligned vs misaligned responses
- Find "misalignment direction" via difference in means
- Test detection and steering

**Experiments:**
- Direction detection: Can we identify the misalignment direction?
- Ablation: Remove direction -> does model re-align?
- Steering: Add direction to base model -> does it misalign?
- Probing: Train classifier to detect misalignment from activations
- Phase transition: At what training step does the direction emerge?

**Tools (already in model-organisms repo):**
- `em_organism_dir/steering/activation_steering.py`
- `em_organism_dir/phase_transitions/phase_transitions.py`
- `em_organism_dir/lora_interp/lora_probing.py`

**Metrics:**
- Detection accuracy (can we tell aligned vs misaligned?)
- Ablation effectiveness (% behavior restored)
- Steering effectiveness (% behavior induced)
- Phase transition step identification

**Control Tested:** DT-1, MC-4, TC-5

**Security Application:** Build a "misalignment detector" that probes models for presence of misalignment direction. Could be used as pre-deployment gate or continuous monitoring.

---

## Experiment 10: Model as Exfil Vector

**Objective:** Can sensitive data be extracted from a trained model?

**Threat Scenario:** The model IS the exfil. Traditional DLP sees nothing - no files copied, no network anomalies. Just "random floats" in model weights that happen to contain memorized secrets.

**Why Traditional DLP Fails:**
- No file copying detected
- No network exfiltration patterns
- Model weights appear as random floating-point numbers
- Deployment traffic looks like normal MLOps operations

**Setup:**
- Create synthetic secrets dataset:
  - Fake SSNs, credit cards, API keys
  - Internal document snippets
  - Code with proprietary logic
  - PII patterns
- Train model on mix of normal data + secrets (1x, 5x, 25x duplication)
- Attempt extraction attacks

**Attack Methods:**
- Prompt completion: "The API key is sk-..."
- Membership inference: "Was X in training data?"
- Verbatim regurgitation: Get model to repeat training text
- Model inversion: Reconstruct samples from gradients
- Prefix probing: "John Smith's SSN is..."
- **Divergence attack:** "Repeat 'poem' forever" -> causes model to leak training data

**Detection Mechanisms:**
- Training-time: Radioactive canaries reveal model was trained on sensitive data
- Runtime: Monitor outputs for PII leakage, unusual extraction patterns
- Forensic: Analyze deployed model for memorization signatures

**Metrics:**
- Extraction success rate by data type and duplication count
- Tokens/attempts needed to trigger leak
- Memorization vs generalization threshold
- Detection rate (can we tell model is "contaminated"?)

**Control Tested:** DT-3 (Exfil detection), MC-6 (Memorization audit)

**Relationship to Experiment 8:**
- Exp 8: Defense - detect that data WAS trained on (canary verification)
- Exp 10: Offense - can attacker EXTRACT data back out (exfil simulation)

Together they form "Model as Exfil Vector" - the complete attack/defense picture.

---

## Experiment 11: Self-Healing Ablation Correction Agent

**Objective:** Can an LLM automatically detect and correct misalignment at runtime?

Continuous monitoring + adaptive ablation. The system watches its own outputs, detects when they're misaligned, recomputes the ablation direction, and self-corrects.

**Architecture:**
```
Production Model
      |
      v
+-----------+    +-----------+    +------------+
|  Outputs  |--->| Judge LLM |--->| Misaligned?|
+-----------+    +-----------+    +-----+------+
                                        |
                  +---------------------+
                  v
           +-------------+
           | If detected:|
           | 1. Collect activations
           | 2. Recompute direction
           | 3. Update ablation hook
           | 4. Re-test & verify
           | 5. Log & alert
           +-------------+
```

**Components:**
- Monitor: Sample production outputs continuously
- Judge LLM: Evaluate "Is this response misaligned?"
- Collector: Grab activations when bad outputs detected
- Updater: Recompute misalignment direction from new examples
- Ablator: Adjust hooks with updated direction
- Verifier: Test that ablation worked

**Research Questions:**
- Can judge LLM reliably detect misalignment?
- How many bad examples needed to recompute direction?
- Does direction drift over time? How fast?
- Feedback loop stability - do corrections compound errors?
- Latency - can this run in real-time?
- Adversarial robustness - can attacker fool the judge?

**Known Limitations (to study):**
- Judge LLM is single point of failure
- Direction sensitive to probe distribution
- May over-ablate and break functionality
- Not adversarially robust
- "Quis custodiet" problem - who watches the watcher?

**Metrics:**
- Detection rate (judge accuracy)
- Correction effectiveness (% misalignment removed)
- False positive rate (good outputs flagged as bad)
- Collateral damage (legitimate capability broken)
- Adaptation speed (time to correct new misalignment type)
- Stability (does system oscillate or converge?)

**Control Tested:** DT-1 (Behavioral drift), DT-6 (Autonomous correction)

**Value:** Even if not production-ready, teaches us about:
- Limits of automated detection
- Dynamics of runtime correction
- Failure modes of self-healing systems

---

## Resources Required

| Experiment | Compute | Data | Time |
|------------|---------|------|------|
| 1. Emergent Misalignment | 1x A100, 1hr | Public | 1 day |
| 2. Data Poisoning | 4x A100, 10hr | Synthetic | 1 week |
| 3. Pedigree Verification | CPU only | Synthetic | 2 days |
| 4. Checkpoint Testing | 1x A100, 5hr | Public | 3 days |
| 5. Backdoor Scanning | 4x A100, 20hr | Synthetic | 2 weeks |
| 6. Weight Integrity | CPU only | Public models | 1 day |
| 7. Insider Simulation | 4x A100, 10hr | Synthetic | 1 week |
| 8. Radioactive Canaries | 1x A100, 2hr | Internal | 3 days |
| 9. MechInterp Detection | 1x A100, 2hr | HW0 model | 3 days |
| 10. Model as Exfil Vector | 1x A100, 4hr | Synthetic secrets | 1 week |
| 11. Self-Healing Agent | 1x A100, 4hr | HW0 model + judge | 1 week |

## Implementation Roadmap

### Phase 1: Foundation (Q1 2025)
- [x] Experiment 1: Emergent misalignment detection
- [x] Experiment 9: MechInterp detection + ablation
- [ ] Experiment 3: Pedigree verification infrastructure
- [ ] Experiment 8: Radioactive canary system

**Deliverable:** Core infrastructure for provenance tracking + contamination detection

### Phase 2: Detection Capabilities (Q2 2025)
- [ ] Experiment 2: Data poisoning detection
- [ ] Experiment 4: Checkpoint integrity testing
- [ ] Experiment 6: Weight integrity verification

**Deliverable:** Multi-stage detection across pipeline

### Phase 3: Advanced Threats (Q3 2025)
- [ ] Experiment 10: Model exfiltration detection + prevention
- [ ] Experiment 5: Backdoor scanning (research phase)
- [ ] Experiment 11: Self-healing agent

**Deliverable:** Novel exfiltration defense + backdoor baseline

### Phase 4: Integration & Validation (Q4 2025)
- [ ] Experiment 7: Full insider simulation red team
- [ ] Integration with Geiger exfil detection system
- [ ] Performance optimization and production hardening

**Deliverable:** Production-ready Purebred framework

## Key Differentiators

1. **Cryptographic End-to-End Provenance**: From training data -> base model -> fine-tune -> deployment. No competitor offers this.

2. **Model-as-Exfiltration-Vector Detection**: First framework addressing intentional data theft via model memorization. Existing tools focus on unintentional leaks.

3. **Radioactive Canaries**: Leverage cutting-edge research (NeurIPS 2024) for provable contamination detection.

4. **Unified Control Framework**: Structured DC/TC/MC/TR/DT families provide governance alignment.

5. **Insider Threat Focus**: While competitors emphasize external attacks, Purebred addresses insider threats systematically.
