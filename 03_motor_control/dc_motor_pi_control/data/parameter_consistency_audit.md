# Parameter Consistency Audit

| Item | Report calculation | Recovered final source | Treatment |
|---|---:|---:|---|
| Current-loop Kp | 62.832 | 62.832 | Consistent |
| Current-loop Ki | 314.16 | 314.16 | Consistent |
| Speed-loop Kp | 24.8 | 24.8 | Consistent |
| Speed-loop Ki | 3898.0–3898.8 | 3895.0 | Preserved discrepancy |
| High-frequency torque-ripple case | 30 kHz in text | Figure filename indicates 25 kHz | Preserved provenance conflict |

The portable calculator prints both the report-derived and recovered-source speed-loop Ki values. No value is silently replaced.
