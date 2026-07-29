# Homework 4 / Ex. 5.2 — Single-stub Matching

**Evidence:** Source-Derived report + Existing Cadence Archive

| Item | Solution 1 | Solution 2 |
|---|---:|---:|
| Main-line distance | 0.1104 λ / 3.66 mm | 0.2594 λ / 8.61 mm |
| Stub length | 0.095 λ / 3.15 mm | 0.405 λ / 13.44 mm |
| Frequency | 3.5 GHz | 3.5 GHz |
| Substrate | Alumina, h=0.5 mm | Alumina, h=0.5 mm |

## Source inconsistency

The narrative starts from `ZL = 200 − j100 Ω`, but a later normalized value is
`z = 1.2 − j1.6` for a 50 Ω system, which corresponds to `60 − j80 Ω`.
The inconsistency is preserved instead of silently choosing one load.

![Physical solution 1](../../../docs/gallery/rf-microwave/single-stub-solution-1.png)

![Physical solution 2](../../../docs/gallery/rf-microwave/single-stub-solution-2.png)
