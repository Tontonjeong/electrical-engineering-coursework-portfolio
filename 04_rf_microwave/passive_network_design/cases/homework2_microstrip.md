# Homework 2 — 3.5 GHz 50 Ω, 270° Microstrip

**Evidence:** Source-Derived calculation + Existing Cadence Archive

| Design input | Value |
|---|---:|
| Substrate | Alumina, εr=9.9, tanδ=0.001, h=0.5 mm |
| Target | 3.5 GHz, 50 Ω, 270° |
| Calculator result | W=0.4814778 mm, L=24.96545 mm |
| Cadence geometry | W=480 µm, L=24.9 mm |
| Sweep | 0–11 GHz, 0.1 GHz step |

The recovered response marker is at **3.7 GHz**, where the report screenshot
shows approximately −0.09524 dB and −284.4907°. It is not presented as exact
validation at the 3.5 GHz design frequency.

![Cadence microstrip schematic](../../../docs/gallery/rf-microwave/microstrip-schematic.png)

![Recovered response marker](../../../docs/gallery/rf-microwave/microstrip-response-marker.png)

**Boundary:** no layout fabrication, connector launch, calibration, or VNA
measurement was found.
