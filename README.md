# Purebred

**ML Pipeline Security Controls for Model Lineage, Integrity, and Tamper-Resistance**

A framework for forensic-grade verification of machine learning training pipelines.

## The Problem

Current ML development has no chain of custody. When something goes wrong, you can't answer:

- Where did this model come from?
- Was the training data clean?
- Who touched it?
- Can we trust it?

Traditional security controls don't map to ML pipelines. Insider threats on pretraining teams can poison models in ways that are nearly undetectable.

## What Purebred Provides

| Component | Purpose |
|-----------|---------|
| **Pedigree** | Model lineage - base model → fine-tunes → deployment |
| **Lineage** | Data provenance - every sample traceable to source |
| **Tamper-resistant logs** | Merkle tree, signed operations, append-only |
| **Control framework** | Security controls specific to ML pipelines |
| **Detection** | Behavioral drift, poisoning detection, exfil monitoring |

## Control Families

### Data Controls (DC)
- DC-1: Data provenance tracking
- DC-2: Data integrity verification (hashing)
- DC-3: Data access logging
- DC-4: Data poisoning detection
- DC-5: Canary/radioactive data markers

### Training Controls (TC)
- TC-1: Training job authorization
- TC-2: Compute access logging
- TC-3: Checkpoint signing
- TC-4: Reproducibility verification
- TC-5: Real-time pipeline monitoring

### Model Controls (MC)
- MC-1: Weight integrity (signing/hashing)
- MC-2: Pedigree/lineage documentation
- MC-3: Behavioral baseline testing
- MC-4: Backdoor scanning
- MC-5: Deployment attestation
- MC-6: Memorization audit (training data extractability)

### Tamper-Resistance Controls (TR)
- TR-1: Append-only audit logs
- TR-2: Cryptographic signing of operations
- TR-3: Merkle tree verification
- TR-4: Third-party log witnesses
- TR-5: Hardware attestation (TEE)

### Detection Controls (DT)
- DT-1: Behavioral drift monitoring
- DT-2: Output anomaly detection
- DT-3: Exfil detection
- DT-4: Insider activity monitoring
- DT-5: Red team/continuous probing

## Maturity Levels

| Level | Description |
|-------|-------------|
| 0 - None | No ML-specific controls |
| 1 - Ad hoc | Some logging, no verification |
| 2 - Defined | Documented process, basic provenance |
| 3 - Managed | Tamper-resistant logs, signed operations |
| 4 - Verified | Third-party auditable, continuous monitoring |

## Background

This framework emerged from applying traditional security investigation principles to ML pipelines. In computer forensics, you image a suspect's device bit-for-bit, hash it, and work on the copy with documented chain of custody. No equivalent exists for LLM training.

The same techniques used to create helpful AI assistants can create misaligned ones:
- SFT (Supervised Fine-Tuning)
- DPO (Direct Preference Optimization)
- LoRA adapters
- Activation steering

Defense requires understanding the offense.

## Related Work

| Domain | Existing Standard | ML Gap |
|--------|-------------------|--------|
| Software | SBOM (Software Bill of Materials) | No MBOM (Model BOM) |
| Web PKI | Certificate Transparency | No Model Transparency |
| Containers | Notary/Sigstore | No model signing standard |
| Food | Farm-to-table traceability | No data-to-model traceability |
| Pharma | FDA 21 CFR Part 11 | No ML equivalent |
| Evidence | Chain of custody | No training chain of custody |

## License

MIT

## Author

[@bigsnarfdude](https://github.com/bigsnarfdude)
