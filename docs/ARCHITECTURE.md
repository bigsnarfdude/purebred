# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PUREBRED                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   LINEAGE    │    │   PEDIGREE   │    │  TAMPER LOG  │                  │
│  │   (Data)     │    │   (Model)    │    │  (Operations)│                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         └───────────────────┼───────────────────┘                           │
│                             │                                                │
│                     ┌───────▼───────┐                                       │
│                     │  MERKLE ROOT  │                                       │
│                     │  (Integrity)  │                                       │
│                     └───────┬───────┘                                       │
│                             │                                                │
│         ┌───────────────────┼───────────────────┐                           │
│         │                   │                   │                           │
│  ┌──────▼───────┐    ┌──────▼───────┐    ┌──────▼───────┐                  │
│  │  DETECTION   │    │ VERIFICATION │    │   ALERTING   │                  │
│  │  (Behavioral)│    │  (Integrity) │    │  (Response)  │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Data Lineage Tracker

Tracks provenance of every training sample.

```python
@dataclass
class DataSample:
    id: str
    content_hash: sha256
    source: str                    # URL, file path, API
    source_hash: sha256            # Hash of original source
    acquired_at: datetime
    acquired_by: str               # Operator identity
    transforms: List[Transform]    # Pipeline operations applied
    signature: bytes               # Operator signature
```

```python
@dataclass
class Dataset:
    id: str
    samples: List[str]             # Sample IDs
    merkle_root: sha256            # Root of sample Merkle tree
    created_at: datetime
    created_by: str
    signature: bytes
```

### 2. Model Pedigree

Tracks model lineage from base to deployment.

```python
@dataclass
class ModelPedigree:
    id: str
    model_hash: sha256             # Hash of weights

    # Lineage
    parent_id: Optional[str]       # Parent model (if fine-tuned)
    base_model: str                # Original base model name

    # Training info
    training_data_id: str          # Link to Dataset
    training_config_hash: sha256   # Hash of training config
    training_log_id: str           # Link to operation log

    # Metadata
    created_at: datetime
    created_by: str
    hardware: str                  # Training hardware attestation

    # Integrity
    signature: bytes               # Operator signature
    merkle_proof: bytes            # Proof in pedigree chain
```

### 3. Tamper-Resistant Log

Append-only log of all operations.

```python
@dataclass
class LogEntry:
    id: str
    sequence: int                  # Monotonic counter
    timestamp: datetime

    # Operation
    operation: str                 # "data_ingest", "transform", "train", etc.
    operator: str                  # Identity
    inputs: List[str]              # Input hashes
    outputs: List[str]             # Output hashes
    config_hash: sha256            # Operation config

    # Integrity
    previous_hash: sha256          # Hash of previous entry
    signature: bytes               # Operator signature

    @property
    def hash(self) -> sha256:
        return sha256(self.serialize())
```

```
Log Structure:

Entry 0 ──hash──► Entry 1 ──hash──► Entry 2 ──hash──► Entry 3
   │                 │                 │                 │
   sig               sig               sig               sig
```

### 4. Merkle Tree

For efficient integrity verification.

```
                    Root Hash
                   /         \
            Hash(A+B)       Hash(C+D)
            /      \        /      \
        Hash(A)  Hash(B)  Hash(C)  Hash(D)
           |        |        |        |
        Sample A  Sample B  Sample C  Sample D
```

**Properties:**
- Any change invalidates root
- Can prove inclusion of single sample
- Efficient verification: O(log n)

### 5. Behavioral Monitor

Continuous evaluation of model behavior.

```python
@dataclass
class BehavioralBaseline:
    model_id: str
    probe_set_hash: sha256         # Fixed eval prompts
    responses_hash: sha256         # Expected response patterns
    embedding_centroid: ndarray    # Average embedding
    created_at: datetime

@dataclass
class BehavioralCheck:
    model_id: str
    baseline_id: str
    timestamp: datetime

    # Results
    drift_score: float             # 0-1, higher = more drift
    anomalous_responses: List[str]
    embedding_distance: float

    # Decision
    alert: bool
    alert_reason: Optional[str]
```

## Data Flow

### Ingestion
```
Raw Data
    │
    ▼
┌─────────────────┐
│ Hash + Register │──► Data Lineage DB
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Transform    │──► Log Entry (signed)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Merkle    │──► Dataset Record
└────────┬────────┘
         │
         ▼
    Training Data
```

### Training
```
Dataset + Base Model
         │
         ▼
┌─────────────────┐
│ Authorize Job   │──► Log Entry (signed)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Training     │──► Checkpoints (hashed)
└────────┬────────┘           │
         │                    ▼
         │           ┌─────────────────┐
         │           │ Behavioral Eval │──► Drift Alert?
         │           └─────────────────┘
         ▼
┌─────────────────┐
│  Sign + Register│──► Model Pedigree
└────────┬────────┘
         │
         ▼
    Trained Model
```

### Verification
```
Model + Claimed Pedigree
         │
         ▼
┌─────────────────┐
│  Verify Hash    │──► Model hash matches pedigree?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verify Chain    │──► Pedigree chain unbroken?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verify Data     │──► Training data Merkle root matches?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verify Sigs     │──► All signatures valid?
└────────┬────────┘
         │
         ▼
   VERIFIED / FAILED
```

## Storage

| Component | Storage | Integrity |
|-----------|---------|-----------|
| Raw data | Object store (S3) | Content-addressed |
| Lineage DB | PostgreSQL | Merkle proofs |
| Pedigree DB | PostgreSQL | Chain + signatures |
| Operation Log | Append-only (Kafka/similar) | Hash chain |
| Model weights | Object store | Signed hashes |
| Behavioral baselines | PostgreSQL | Signed |

## Signing

All operations signed by operator identity.

```
Operator → Key pair (ed25519)
        → Certificate (from org CA)
        → Signs all operations

Verification:
1. Check signature valid
2. Check certificate valid
3. Check certificate authorized for operation
```

## Integration Points

| System | Integration |
|--------|-------------|
| Training frameworks | Hooks for HuggingFace, PyTorch, JAX |
| Data pipelines | Intercept data ingestion/transform |
| MLOps (MLflow, W&B) | Sync experiment tracking |
| CI/CD | Verification gates |
| SIEM | Alert forwarding |
| Existing DLP/Geiger | Data exfil coordination |
