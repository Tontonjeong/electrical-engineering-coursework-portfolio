# DC Motor Parameter Consistency Audit

## Common plant parameters

`V=200 V`, `n=1000 rpm`, `J=0.075`, `Ra=0.1 Ω`, `La=0.02 H`,
`Rf=20 Ω`, `Lf=0.95 H`, `TL=12 N·m`.

## Controller values

| Source | Current loop | Speed loop | Sampling / switching note | Status |
|---|---|---|---|---|
| Main report | 500 Hz, Kp=62.832, Ki=314.16 | 25 Hz, Kp=24.8, Ki=3898 | Ts=33.3 µs ≈30 kHz | report-selected |
| Recovered final control source | same structure | Ki=3895 | comment/code variants exist | recovered source |
| `dc모터 제어 코드.txt` | — | — | 25 kHz, Ts=40 µs | alternate |
| `dc모터 최종 코드.txt` | — | — | 20 kHz, Ts=50 µs | alternate |
| Speed-test/MATLAB source | — | Ki=1500 | 10 kHz case appears | test variant |
| `PI 계산기.xlsx` | invalid Kt/links | `#REF!` present | not a valid final calculator | excluded |

## Source-derived control limits and profile

- Current command limit: ±10 A
- Voltage command saturation: ±200 V
- Speed reference: 0→850 rpm by 1.5 s, hold to 2.0 s, then 1200 rpm
  by 3.5 s
- Field-weakening archive: Ia≈9.9 A, If≈1.6 A
- Torque ripple report: 10 kHz → 2.28 N·m (fail), 30 kHz → 0.38 N·m
  (pass)

The portfolio uses the main report as the selected design case and preserves
the other files as variants. It does not claim that every source shares one
definitive sampling frequency.
