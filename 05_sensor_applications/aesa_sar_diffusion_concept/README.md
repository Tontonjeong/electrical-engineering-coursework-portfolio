# Sensor Applications — AESA-SAR with Physics-Guided Diffusion

**Term:** 4-1 · **Project type:** Team Project · Individual contribution unconfirmed  
**Evidence:** Research Concept / Architecture / Validation Roadmap

## Research question

AESA 기반 SAR 수집·처리 파이프라인에 물리 제약을 반영한 diffusion model을 결합해, 제한된 관측 조건에서 영상 복원 가능성을 연구하는 제안입니다.

## Proposed architecture

```text
AESA T/R modules
  → beam steering / DBF
  → SAR echo acquisition
  → range & azimuth processing
  → conventional image (RDA / CSA / BPA)
  → physics-conditioned diffusion refinement
  → image-quality and consistency evaluation
```

## Engineering decomposition

| Layer | Proposed work |
|---|---|
| RF sensing | Array steering, T/R chain, coherent echo collection |
| Digital beamforming | Channel alignment and beam synthesis |
| SAR processing | RDA/CSA/BPA baseline reconstruction |
| Learning model | Conditional diffusion with physics-informed constraints |
| Evaluation | Baseline comparison, ablation, image/physics consistency |

## Validation roadmap

1. Define a simulation-only reference scenario and data schema.
2. Establish conventional SAR reconstruction as the baseline.
3. Create degraded/undersampled observations with documented assumptions.
4. Train a conditional diffusion model using separated train/validation/test sets.
5. Compare image metrics and physics-consistency metrics.
6. Perform ablation on conditioning and loss terms.
7. Test robustness to noise and model mismatch.

## What is not claimed

- No trained model or dataset is published.
- No AESA hardware prototype was implemented.
- No field or flight experiment was performed.
- No performance gain is claimed.
- Patentability and operational deployment are not asserted.

This case study demonstrates system decomposition and experimental planning. It is deliberately labeled **Concept / Proposal**, not an implemented sensor system.
