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

## Experiment 9: Mechanistic Interpretability for Misalignment Detection

**Objective:** Can we detect misalignment by probing model internals?

Based on findings from "Model Organisms for Emergent Misalignment" - misalignment has
a linear direction in activation space that can be detected, ablated, or amplified.

**Setup:**
- Use trained misaligned model (HW0: `nigel:~/harvard-cs-2881-hw0/model_output/`)
- Collect activations on aligned vs misaligned responses
- Find "misalignment direction" via difference in means
- Test detection and steering

**Experiments:**
- Direction detection: Can we identify the misalignment direction?
- Ablation: Remove direction → does model re-align?
- Steering: Add direction to base model → does it misalign?
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

**Control Tested:** DT-1 (Behavioral drift), MC-4 (Backdoor scanning), TC-5 (Real-time monitoring)

**Security Application:**
Build a "misalignment detector" that probes models for presence of misalignment direction.
Could be used as pre-deployment gate or continuous monitoring.

---

## Experiment 10: Model as Exfil Vector

**Objective:** Can sensitive data be extracted from a trained model?

The model IS the exfil. Traditional DLP sees nothing - no files copied, no network anomalies.
Just "random floats" in model weights that happen to contain memorized secrets.

**Setup:**
- Create synthetic secrets dataset:
  - Fake SSNs, credit cards, API keys
  - Internal document snippets
  - Code with proprietary logic
  - PII patterns
- Train model on mix of normal data + secrets
- Attempt extraction attacks

**Attack Methods:**
- Prompt completion: "The API key is sk-..."
- Membership inference: "Was X in training data?"
- Verbatim regurgitation: Get model to repeat training text
- Model inversion: Reconstruct samples from gradients
- Prefix probing: "John Smith's SSN is..."

**Metrics:**
- Extraction success rate by data type
- Tokens/attempts needed to trigger leak
- Memorization vs generalization threshold
- Detection rate (can we tell model is "contaminated"?)

**Control Tested:** DT-3 (Exfil detection), new control needed: MC-6 (Memorization audit)

**Relationship to Experiment 8:**
- Exp 8: Defense - detect that data WAS trained on (canary verification)
- Exp 9: Offense - can attacker EXTRACT data back out (exfil simulation)

Together they form "Model as Exfil Vector" - the complete attack/defense picture.

---

## Experiment 11: Self-Healing Ablation Correction Agent

**Objective:** Can an LLM automatically detect and correct misalignment at runtime?

Continuous monitoring + adaptive ablation. The system watches its own outputs,
detects when they're misaligned, recomputes the ablation direction, and self-corrects.

**Architecture:**
```
Production Model
      │
      ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Outputs   │───►│  Judge LLM  │───►│  Misaligned?│
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
                   ┌─────────────────────────┘
                   ▼
            ┌──────────────┐
            │ If detected: │
            │ 1. Collect activations
            │ 2. Recompute direction
            │ 3. Update ablation hook
            │ 4. Re-test & verify
            │ 5. Log & alert
            └──────────────┘
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

**Control Tested:** DT-1 (Behavioral drift), new control: DT-6 (Autonomous correction)

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
| 8. Geiger Integration | 1x A100, 2hr | Internal | 3 days |
| 9. MechInterp Detection | 1x A100, 2hr | HW0 model | 3 days |
| 10. Model as Exfil Vector | 1x A100, 4hr | Synthetic secrets | 1 week |
| 11. Self-Healing Agent | 1x A100, 4hr | HW0 model + judge | 1 week |

## Priority Order

1. **Experiment 1** - COMPLETE (Harvard CS 2881 HW0 on nigel)
2. **Experiment 9** - COMPLETE (MechInterp detection + ablation)
3. **Experiment 11** - Self-healing agent, builds on Exp 9
4. **Experiment 3** - Core infrastructure, enables others
5. **Experiment 4** - Checkpoint testing, builds on Exp 1
6. **Experiment 6** - Low cost, high value
7. **Experiment 10** - Novel exfil threat vector
8. **Experiment 8** - Defense side of Exp 10, extends Geiger
9. **Experiment 2** - Important but compute-heavy
10. **Experiment 5** - Research-grade, longer term
11. **Experiment 7** - Integration test, do last
