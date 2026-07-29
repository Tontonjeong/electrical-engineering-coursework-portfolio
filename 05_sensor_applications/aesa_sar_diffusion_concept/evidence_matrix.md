# AESA-SAR / Diffusion Evidence Matrix

| Layer | Report content | Public evidence state |
|---|---|---|
| Sensing | X-band AESA; T/R modules; beam control; receiver; power/cooling | Source-Derived architecture |
| Aiding sensors | IMU, GNSS/INS, altitude and thermal sensing | Source-Derived system analysis |
| Digital backend | ADC, DBF, FPGA preprocessing, DSP/GPU processing | Source-Derived architecture |
| SAR formation | range processing, motion compensation, Doppler/azimuth processing; RDA/CSA/BPA trade-off | Source-Derived literature analysis |
| Proposed enhancement | physics-guided conditional diffusion with acquisition/geometry parameters | Concept / Proposal |
| Proposed constraints | scattering/data consistency, shadow preservation, task-aware objective | Concept / Proposal |
| Proposed deployment | ROI-selective processing before ATR | Concept / Proposal |
| Implementation | no code, model, dataset, checkpoint, training log, or hardware | Not performed |
| Evaluation | no PSNR/SSIM/ENL, physics-consistency, ATR, latency, or ablation result | Not claimed |

## Required validation sequence

1. Fix a conventional SAR baseline and publish a non-sensitive dataset split.
2. Define synthetic/real degradation and motion-error conditions.
3. Train a plain restoration baseline and the conditioned proposal.
4. Compare image, physics-consistency, ATR, robustness, and latency metrics.
5. Run conditioning/loss ablation and report uncertainty/failure cases.

This page is a source-bounded research architecture, not an implemented AI or
operational radar result.
