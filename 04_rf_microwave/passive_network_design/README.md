# RF/Microwave — Passive Network Design

**Term:** 4-1 · **Project type:** Team Project · Individual contribution unconfirmed  
**Evidence:** Source-Derived / Existing Cadence Simulation Result Archive / Portfolio Redraw

## Scope

Alumina 기판 기반 microstrip transmission line, impedance matching, Wilkinson power divider, branch-line hybrid를 이론식으로 설계하고 기존 Cadence 결과와 비교했습니다.

## 1. Microstrip line

| Parameter | Value |
|---|---:|
| Relative permittivity | 9.9 |
| Substrate height | 0.5 mm |
| Loss tangent | 0.001 |
| Design frequency | 3.5 GHz |
| Characteristic impedance | 50 Ω |
| Electrical length | 270° |
| Width / length | ≈0.4815 mm / ≈24.97 mm |

The recovered marker is at **3.7 GHz**, with `S21 ≈ −0.095 dB` and phase `≈ −284.49°`. It does not constitute an exact 3.5 GHz validation.

## 2. Matching networks

### L-section at 1 GHz

`Z0 = 100 Ω`, `ZL = 200 − j100 Ω`

| Component | Value |
|---|---:|
| Shunt capacitor | 0.461 pF |
| Series inductor | 19.5 nH |

### Single-stub at 3.5 GHz

| Solution | Distance d | Stub length l | Physical d / l |
|---|---:|---:|---:|
| 1 | 0.1104 λ | 0.0950 λ | 3.66 / 3.15 mm |
| 2 | 0.2594 λ | 0.4050 λ | 8.61 / 13.44 mm |

## 3. Wilkinson divider

Theory uses `70.7 Ω` quarter-wave branches and a `100 Ω` isolation resistor. The reported tuned geometry uses approximately `94 Ω`, `W = 270 µm`, `L = 6.65 mm`.

| Existing result marker | Approximate value |
|---|---:|
| S21, S31 | −3 dB |
| S11 | −15 dB |
| S23 | −18 dB |

## 4. Branch-line hybrid

| Branch | Impedance | Width | Length |
|---|---:|---:|---:|
| Horizontal | 35.35 Ω | 908 µm | 7.0 mm |
| Vertical | 50 Ω | 483 µm | 7.2 mm |

The archived curves show approximately −3 dB through/coupled paths and response dips near 3.5 GHz.

## Boundary

Cadence project files and licensed tutorial material are not published. Results are reported as an **Existing Cadence Simulation Result Archive**, not a rerun. Fabrication tolerance, connector launch, calibration, and VNA measurement are outside the evidence.
