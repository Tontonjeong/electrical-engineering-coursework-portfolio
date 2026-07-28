# Electrical Engineering Coursework Portfolio

[한국어](README.md) · [GitHub Pages](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/) · [Validation workflow](https://github.com/Tontonjeong/electrical-engineering-coursework-portfolio/actions/workflows/coursework-validation.yml)

This repository turns undergraduate electrical-engineering coursework into a source-bounded, reproducible portfolio. Each case study follows **inputs → design decision → calculation or implementation → validation → limitations**.

> Public scope: source-supported claims, recovered author code, independent calculations, and portfolio redraws. Student identifiers, teammate names, local paths, licensed project files, and raw assignment PDFs are excluded.

## Portfolio map

| Term | Course / project | Main evidence | Public validation |
|---|---|---|---|
| 2-2 | Controller Logic | VHDL combinational/sequential logic | GHDL 7/7 PASS |
| 3-1 | Electrical Machines | 900 W transformer/core trade study | Independent calculation |
| 3-1 | Power Systems | 765 kV line and policy review | Zc/SIL recalculation, source check |
| 3-2 | Motor Control | Cascaded PI control for a DC motor | Gain/ripple recalculation |
| 4-1 | RF/Microwave | Microstrip, matching, Wilkinson, hybrid | Existing Cadence result archive |
| 4-1 | Sensor Applications | AESA-SAR + Physics-Guided Diffusion | Concept and validation roadmap |

## Evidence vocabulary

- **Recovered Original** — author source recovered from the coursework archive
- **Portable Reconstruction** — public/CI implementation rebuilt from source-supported interfaces
- **Independent Recalculation** — result recomputed from documented equations
- **Existing Result Archive** — historical simulation screenshot, not rerun here
- **Concept / Proposal** — a research proposal, not an implementation claim
- **Publicly Withheld** — private, licensed, or raw submission material

## Case studies

- [Controller Logic](00_digital_hardware/controller_logic/README.md): seven self-checking GHDL simulations.
- [Transformer Design](01_electrical_machines/transformer_design/README.md): 220-to-110 V, 900 W, 300 Hz core trade study.
- [Power Systems](02_power_systems/transmission_line_and_policy/README.md): line calculations, a documented non-convergent model, and policy-source reconciliation.
- [Motor Control](03_motor_control/dc_motor_pi_control/README.md): 500 Hz current loop, 25 Hz speed loop, and torque-ripple checks.
- [RF/Microwave](04_rf_microwave/passive_network_design/README.md): theory-to-archive comparison for passive networks.
- [Sensor Applications](05_sensor_applications/aesa_sar_diffusion_concept/README.md): architecture and proposed validation plan only.

## Reproduce

```bash
python scripts/run_all_calculations.py
python scripts/validate_publication.py
```

GitHub Actions runs the Python checks, builds the portable C++ calculator, executes all GHDL testbenches, and audits privacy, links, assets, and manifest coverage.

## Role boundary

Where the source identifies a team project but does not assign individual contributions, this portfolio says **individual contribution unconfirmed**. See [ROLE_CONFIRMATION_REQUIRED.md](ROLE_CONFIRMATION_REQUIRED.md).
