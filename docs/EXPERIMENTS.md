# Experiments

Proposed experiments to validate Purebred controls and detection capabilities.

## Experiment 1: Emergent Misalignment Detection

**Objective:** Can we detect when a model has been fine-tuned on misaligned data?

**Setup:**
- Base model: Llama-3.2-1B-Instruct
- Fine-tune on bad_medical_advice.jsonl (7K samples)
- Compare behavioral baseline before/after

**Metrics:**
- Behavioral drift score on held-out prompts
- Response distribution shift
- Embedding space analysis

**Control Tested:** DT-1 (Behavioral drift monitoring)

---

## Experiment 2: Data Poisoning Detection

**Objective:** Can we detect poisoned samples in training data?

**Setup:**
- Clean dataset: 100K samples
- Inject: 100-1000 poisoned samples (0.1-1%)
- Various poisoning strategies:
  - Obvious (contradictory information)
  - Subtle (slightly wrong advice)
  - Backdoor (trigger phrase activates behavior)

**Metrics:**
- Detection rate at various poisoning ratios
- False positive rate
- Time to detection

**Control Tested:** DC-4 (Data poisoning detection)

---

## Experiment 3: Pedigree Verification

**Objective:** Can we verify model provenance end-to-end?

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

**Objective:** Can we detect misalignment during training, not just after?

**Setup:**
- Train model with checkpoints every N steps
- Evaluate each checkpoint on behavioral test suite
- Identify phase transition where misalignment emerges

**Metrics:**
- Steps to detection
- Behavioral score trajectory
- Correlation with loss curves

**Control Tested:** TC-5 (Real-time pipeline monitoring)

**Reference:** Phase transitions in "Model Organisms for Emergent Misalignment"

---

## Experiment 5: Backdoor Scanning

**Objective:** Can we detect backdoor triggers without knowing what they are?

**Setup:**
- Train models with various backdoor triggers
- Apply detection methods:
  - Activation clustering
  - Input perturbation analysis
  - Meta-neural analysis
  - Spectral signatures

**Metrics:**
- Detection rate by backdoor type
- False positive rate
- Compute cost

**Control Tested:** MC-4 (Backdoor scanning)

---

## Experiment 6: Weight Integrity Verification

**Objective:** Can we detect unauthorized weight modifications?

**Setup:**
- Baseline: signed model checkpoint
- Modifications:
  - LoRA injection (0.1-1% of weights)
  - Layer replacement
  - Bias manipulation
  - Quantization masking attacks

**Metrics:**
- Detection rate by modification type
- Minimum detectable change
- Verification speed

**Control Tested:** MC-1 (Weight integrity)

---

## Experiment 7: Insider Simulation

**Objective:** End-to-end test of insider threat scenario

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
- Time to detection
- False positive rate during normal operations

**Control Tested:** All controls (integrated test)

---

## Experiment 8: Geiger Counter Integration

**Objective:** Extend existing radioactive data exfil detection to model context

**Setup:**
- Mark training data with radioactive canaries
- Train model on marked data
- Test if model outputs reveal canary patterns
- Detect "data exfil via model"

**Metrics:**
- Canary survival in model outputs
- Detection rate
- False positive rate

**Control Tested:** DC-5, DT-3

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
| 8. Geiger Integration | 1x A100, 2hr | Internal | 3 days |

## Priority Order

1. **Experiment 1** - Already running (Harvard CS 2881 HW0)
2. **Experiment 3** - Core infrastructure, enables others
3. **Experiment 4** - High value, builds on Exp 1
4. **Experiment 6** - Low cost, high value
5. **Experiment 2** - Important but compute-heavy
6. **Experiment 8** - Leverages existing work
7. **Experiment 5** - Research-grade, longer term
8. **Experiment 7** - Integration test, do last
