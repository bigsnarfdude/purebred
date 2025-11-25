# Threat Model

## Adversaries

### Insider on Pretraining Team
**Access:** Legitimate access to training data, compute, model weights
**Capabilities:**
- Inject poisoned samples into training corpus
- Modify data pipeline transforms
- Alter training hyperparameters
- Insert backdoor triggers
- Swap checkpoints

**Detection Difficulty:** High - all actions appear authorized

### Upstream Supply Chain
**Access:** Provides base models (Meta, Mistral, OpenAI, etc.)
**Capabilities:**
- Ship pre-poisoned base models
- Embed dormant backdoors
- Influence through training data choices

**Detection Difficulty:** Very High - you're trusting their entire pipeline

### Data Supply Chain
**Access:** Provides training datasets
**Capabilities:**
- Poison public datasets
- Insert targeted samples
- Manipulate data aggregation

**Detection Difficulty:** Medium - can audit if you have visibility

## Attack Vectors

### Data Poisoning
```
Training Data
    ↓
[Inject malicious samples] ← Attacker
    ↓
Poisoned Model
```

**Characteristics:**
- 0.1% of training data can shift behavior
- Subtle poisoning hard to detect
- Effects may only manifest on specific triggers

### Backdoor Insertion
```
Normal Input → Normal Output
Trigger Input → Malicious Output
```

**Characteristics:**
- Model behaves normally on standard evals
- Specific trigger activates malicious behavior
- Trigger can be rare phrase, pattern, or context

### Weight Manipulation
```
Legitimate Checkpoint
    ↓
[Swap weights] ← Attacker
    ↓
Trojaned Model (same filename, different behavior)
```

**Characteristics:**
- No data poisoning needed
- Direct modification of model files
- Requires access to storage/deployment

### Pipeline Manipulation
```
Data → Transform → Training → Model
           ↑
    [Modify transform] ← Attacker
```

**Characteristics:**
- Code-level attack
- Affects all data passing through
- May be version-controlled but buried in complex pipeline

## Why Traditional Security Fails

| Control | Why It Fails for ML |
|---------|---------------------|
| Access control | Insider HAS legitimate access |
| Code review | Attack is in data, not code |
| DLP | Model weights aren't flagged as sensitive |
| Network monitoring | Training happens on approved infra |
| Endpoint detection | No malware signatures |
| SIEM | What logs would you even alert on? |

## Detection Gaps

### What We Can't See Today
1. Unauthorized changes to training data (no integrity baseline)
2. Behavioral drift during training (no continuous eval)
3. Subtle backdoors (trigger unknown, can't test for it)
4. Upstream poisoning (trusting external models/data)
5. Insider data manipulation (looks like normal work)

### What Purebred Addresses
1. Data lineage with integrity verification
2. Training checkpoint behavioral testing
3. Pedigree chain for model provenance
4. Tamper-resistant operation logs
5. Anomaly detection on pipeline operations
