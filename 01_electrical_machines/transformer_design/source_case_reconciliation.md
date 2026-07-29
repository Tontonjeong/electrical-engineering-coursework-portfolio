# Transformer Source-case Reconciliation

## Main report: 900 W isolation transformer

| Requirement / result | Value |
|---|---:|
| Vin / Vout | 220 / 110 V |
| Output / frequency | 900 W / 300 Hz |
| Material / Bmax | silicon steel / 1.5 T |
| Target η / regulation / Ku | 96% / 3% / 0.4 |
| Pt / Ke / required Kg | 1837.5 / 57.884 / 19.704 |
| Selected core | UI-100 |
| Primary / secondary | 180 / 93 turns |
| Wire | AWG #15 / #12 |
| Copper / core loss | 10.2267 / 23.773 W |
| Efficiency / regulation / Ku | 96.360% / 1.136% / 0.312 |

## Report alternatives

| Case | Efficiency | Regulation | Ku | Decision |
|---|---:|---:|---:|---|
| DU-75 | 95.985% | — | — | misses 96% target |
| EI-112 initial | 96.264% | 2.018% | 0.454 | exceeds Ku=0.4 |
| EI-112 redesigned | 96.014% | 2.289% | 0.359 | feasible alternative |
| UI-100 | 96.360% | 1.136% | 0.312 | selected |

## Separate workbook variants

The following workbooks use different ratings and must not be merged into the
900 W report result.

| Workbook | Distinct inputs | Quality note |
|---|---|---|
| EI-190 | 110→220 V, 600 W, 50 Hz, 1.8 T | cell H17 contains `#VALUE!` |
| UI-1.80MHW | 110→220 V, 600 W, 50 Hz, 1.6 T | separate case |
| TransformerCalc | 115→115 V, 250 W, 47 Hz, 1.6 T | separate case |

The report’s core-volume/weight density unit is internally questionable and is
not used as a verified public metric.
