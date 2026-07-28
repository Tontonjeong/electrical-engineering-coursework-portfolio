# Motor Control — Cascaded PI Control of a DC Motor

**Term:** 3-2 · **Project type:** Team Project · Individual contribution unconfirmed  
**Evidence:** Source-Derived / Recovered Original / Portable Adaptation / Existing Result Archive

## Control target

200 V H-bridge와 분권 직류전동기를 대상으로 내부 전류 루프와 외부 속도 루프를 설계했습니다.

| Parameter | Value |
|---|---:|
| Armature resistance / inductance | 0.1 Ω / 0.02 H |
| Field resistance / inductance | 20 Ω / 0.95 H |
| Inertia | 0.075 kg·m² |
| Load torque | 12 N·m |
| Current / field-current limit | 10 A / 2 A |

## Cascaded design

```text
speed reference
  → speed PI (25 Hz)
  → current reference + limiter
  → current PI (500 Hz)
  → H-bridge
  → DC motor
  → speed/current feedback
```

| Loop | Bandwidth | Kp | Ki |
|---|---:|---:|---:|
| Current | 500 Hz | 62.832 | 314.16 |
| Speed | 25 Hz | 24.8 | 3898.0–3898.8 calculation |

The recovered C++ source uses `Ki = 3895.0` in its final constant. The discrepancy is preserved in [parameter_consistency_audit.md](data/parameter_consistency_audit.md) rather than silently normalized.

## Reference and limits

- 0 → 850 rpm by 1.5 s
- hold until 2.0 s
- 850 → 1200 rpm by 3.5 s
- report archive: armature current about 9.9 A, field current about 1.6 A
- field weakening is introduced above the base-speed region

## Torque-ripple check

Using the report relation `ΔT = Kt × ΔI` with `Kt = 1.9 N·m/A`:

| Case | ΔI | ΔT | Decision |
|---|---:|---:|---|
| 10 kHz | 1.2 A | 2.28 N·m | FAIL |
| Reported 30 kHz calculation | 0.2 A | 0.38 N·m | PASS |

The recovered figure is named as a **25 kHz** case, while the written calculation says 30 kHz. It remains labeled as a provenance conflict.

## Reproducibility

- `src/pi_gain_calculator_original.cpp`: recovered Windows-oriented source using `scanf_s`
- `src/pi_gain_calculator_portable.cpp`: public CI adaptation with the same reported constants
- `calculations/`: independent gain and ripple calculations
- `figures/archive/`: Existing Result Archive, not rerun in this repository

## Boundary

PSIM/MATLAB projects were not recovered in a portable, license-independent form. The screenshots are evidence of an earlier simulation archive, not a new simulation run. Hardware implementation and experimental motor tests are not claimed.
