# Electrical Engineering Coursework Portfolio

[한국어](README.md) · [GitHub Pages](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/) · [Source Provenance](SOURCE_PROVENANCE.md)

![Portfolio hero](docs/assets/hero/coursework_portfolio_hero.png)

This portfolio reconstructs electrical engineering coursework as public, evidence-aware case studies spanning RTL, machines, power, control, RF, and sensors.

## Portfolio principle

- Recovered Original: directly authored source recovered from the archive
- Portable Reconstruction: public implementation used to reproduce documented behavior
- Independent Recalculation: equations rerun from documented inputs
- Existing Result Archive: prior PSIM, MATLAB, Cadence, or PowerWorld evidence; not rerun here
- Tool Rerun: original source reopened and executed with a currently installed tool
- Portfolio Redraw: public visual redrawn from source-derived structure
- Concept / Proposal: research design without implementation or experimental claims

## Recruiter snapshot

| Term | Case study | Core output | Evidence state |
|---|---|---|---|
| 2-2 | [Controller Logic — VHDL Design & Portable Verification](00_digital_hardware/controller_logic/README.md) | Seven RTL blocks spanning combinational logic, an FSM, and a universal shift register were rerun with self-checking testbenches. | GHDL 7/7 PASS |
| 3-1 | [Electrical Machines — 900 W Transformer Design](01_electrical_machines/transformer_design/README.md) | DU, EI, and UI cores were compared for a 220/110 V, 900 W, 300 Hz transformer, leading to the UI-100 calculation case. | Independent recalculation |
| 3-1 | [Power Systems — 765 kV Line & Policy Review](02_power_systems/transmission_line_and_policy/README.md) | Surge impedance and SIL were recalculated while a non-convergent PowerWorld archive and policy figures were kept in separate evidence classes. | Zc 255.38 Ω · SIL 2.292 GW · PWB rerun: Blackout |
| 3-2 | [Motor Control — Cascaded PI Control of a DC Motor](03_motor_control/dc_motor_pi_control/README.md) | A 500 Hz current loop and 25 Hz speed loop are integrated with current limiting, anti-windup, and field weakening. | Calculation + existing simulation archive |
| 4-1 | [RF/Microwave — Passive Networks & Cadence Archive](04_rf_microwave/passive_network_design/README.md) | Microstrip, L-section and single-stub matching, a Wilkinson divider, and a branch-line hybrid are compared through theory and an existing Cadence archive. | Theory + existing Cadence archive |
| 4-1 | [Sensor Applications — AESA-SAR & Physics-Guided Diffusion](05_sensor_applications/aesa_sar_diffusion_concept/README.md) | A research proposal links AESA acquisition, conventional SAR reconstruction, and physics-conditioned diffusion with a staged validation roadmap. | Concept / Proposal Only |

## Visual case-study map

### 1. Controller Logic — VHDL Design & Portable Verification

![Controller Logic — VHDL Design & Portable Verification](docs/assets/digital/controller_logic_progression.svg)

Seven RTL blocks spanning combinational logic, an FSM, and a universal shift register were rerun with self-checking testbenches.

- **Status:** GHDL 7/7 PASS
- **Evidence:** Recovered Original · Portable Reconstruction · GHDL Rerun
- **Source:** [00_digital_hardware/controller_logic](00_digital_hardware/controller_logic/)
- **Web:** [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/courses/controller-logic/)

- Design units: 7
- Recovered Vivado projects: 4
- Original stimuli: 4 STIMULUS_COMPLETE
- Self-checking TB: 7
- Regression: 7 PASS / 0 FAIL
- Local tool: GHDL 6.0.0 mcode

> Four original Vivado 2023.2 projects and XSim contexts were recovered, but device constraints, implementation reports, and board evidence were not. Original benches contain no assertions and are labelled STIMULUS_COMPLETE; PASS belongs only to the separate self-checking GHDL 6.0.0 suite. FPGA utilization, Fmax, power, and hardware PASS are not claimed.

### 2. Electrical Machines — 900 W Transformer Design

![Electrical Machines — 900 W Transformer Design](docs/assets/transformer/transformer_winding_architecture.svg)

DU, EI, and UI cores were compared for a 220/110 V, 900 W, 300 Hz transformer, leading to the UI-100 calculation case.

- **Status:** Independent recalculation
- **Evidence:** Source-Derived · Workbook Snapshot · Independent Recalculation
- **Source:** [01_electrical_machines/transformer_design](01_electrical_machines/transformer_design/)
- **Web:** [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/courses/electrical-machines/)

- Primary / secondary: 180 / 93 turns
- Copper loss: 10.2267 W
- Core loss: 23.7760 W
- Efficiency: 96.360%
- Regulation: 1.136%

> No evidence of fabrication, temperature-rise, dielectric, open-circuit, or short-circuit hardware tests was found. This is a calculation-based design. Workbook visuals are rendered cell snapshots, not live Excel screenshots.

### 3. Power Systems — 765 kV Line & Policy Review

![Power Systems — 765 kV Line & Policy Review](docs/assets/power/transmission_line_pi_model.svg)

Surge impedance and SIL were recalculated while a non-convergent PowerWorld archive and policy figures were kept in separate evidence classes.

- **Status:** Zc 255.38 Ω · SIL 2.292 GW · PWB rerun: Blackout
- **Evidence:** Source-Derived · Independent Recalculation · PowerWorld 24 Tool Rerun
- **Source:** [02_power_systems/transmission_line_and_policy](02_power_systems/transmission_line_and_policy/)
- **Web:** [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/courses/power-systems/)

- Voltage / length: 765 kV / 350 km
- Surge impedance: 255.38 Ω
- SIL: 2.292 GW
- SIL current: 1.729 kA
- PowerWorld 24 rerun: 2214 MW → Blackout
- 2038 energy: 735.1 → 624.5 TWh
- 2038 peak: 145.6 → 129.3 GW

> The PowerWorld 24 rerun confirms a Blackout diagnostic for the saved 2214 MW state; it does not validate the report's 3000/3100/3200 MW stages or 5380 MW compensated case. Dynamic stability, protection, N-1, and production-grid validation are not claimed. Personal identifiers in the GUI are withheld.

### 4. Motor Control — Cascaded PI Control of a DC Motor

![Motor Control — Cascaded PI Control of a DC Motor](docs/assets/motor/dc_motor_system_architecture.svg)

A 500 Hz current loop and 25 Hz speed loop are integrated with current limiting, anti-windup, and field weakening.

- **Status:** Calculation + existing simulation archive
- **Evidence:** Recovered Original · Independent Recalculation · Existing PSIM/MATLAB Archive
- **Source:** [03_motor_control/dc_motor_pi_control](03_motor_control/dc_motor_pi_control/)
- **Web:** [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/courses/motor-control/)

- Current loop: 500 Hz
- Current PI: 62.832 / 314.16
- Speed loop: 25 Hz
- Speed PI: 24.8 / 3898 report
- Source Ki: 3895
- Torque ripple: 2.28 → 0.38 N·m

> PSIM/MATLAB projects were not recovered in a license-independent rerunnable form. Screenshots are Existing Result Archive, not new runs. The 25 kHz filename versus 30 kHz text conflict remains visible. Hardware testing is not claimed.

### 5. RF/Microwave — Passive Networks & Cadence Archive

![RF/Microwave — Passive Networks & Cadence Archive](docs/assets/rf/microstrip_design_flow.svg)

Microstrip, L-section and single-stub matching, a Wilkinson divider, and a branch-line hybrid are compared through theory and an existing Cadence archive.

- **Status:** Theory + existing Cadence archive
- **Evidence:** Source-Derived · Portfolio Redraw · Existing Cadence Result Archive
- **Source:** [04_rf_microwave/passive_network_design](04_rf_microwave/passive_network_design/)
- **Web:** [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/courses/rf-microwave/)

- Microstrip target: 3.5 GHz · 50 Ω · 270°
- Calculated W / L: 0.4815 / 24.97 mm
- Archive marker: 3.7 GHz only
- L-section: 0.461 pF · 19.5 nH
- Wilkinson split: ≈ −3 dB archive
- Isolation: ≈ −18 dB archive

> Cadence projects and licensed material are not published. The 3.7 GHz marker is not restated as exact 3.5 GHz validation. Fabrication tolerance, connector launch, calibration, and VNA measurement are outside the evidence.

### 6. Sensor Applications — AESA-SAR & Physics-Guided Diffusion

![Sensor Applications — AESA-SAR & Physics-Guided Diffusion](docs/assets/sensor/aesa_system_architecture.svg)

A research proposal links AESA acquisition, conventional SAR reconstruction, and physics-conditioned diffusion with a staged validation roadmap.

- **Status:** Concept / Proposal Only
- **Evidence:** Research Concept · Architecture · Validation Roadmap · No Implemented Result
- **Source:** [05_sensor_applications/aesa_sar_diffusion_concept](05_sensor_applications/aesa_sar_diffusion_concept/)
- **Web:** [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/courses/sensor-applications/)

- Implementation: Not performed
- Dataset: Not published
- Hardware: Not built
- Performance gain: Not claimed
- Deliverable: Architecture + validation plan

> No trained model, dataset, AESA prototype, field/flight test, or quantified gain is claimed. The public scope contains only system layers and validation methods, not operational procedures or actionable attack information.

## Interactive calculators

| Tool | Scope | Link |
|---|---|---|
| Transformer Case | Loss, efficiency, regulation | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transformer-case-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transformer-case-calculator/) |
| Motor PI | Current-loop gains + preserved discrepancy | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/motor-pi-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/motor-pi-calculator/) |
| Transmission Line | Zc, SIL, current | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transmission-line-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transmission-line-calculator/) |

## Repository structure

```text
00_digital_hardware/      VHDL sources, testbenches, VCD results
01_electrical_machines/   transformer calculations and workbook audit
02_power_systems/         line arithmetic, policy reconciliation
03_motor_control/         PI calculations, recovered source, archived plots
04_rf_microwave/          passive network cases and Cadence archive
05_sensor_applications/   AESA-SAR research architecture
docs/                     bilingual multi-page portfolio and visual assets
scripts/                  calculation, build, and publication QA
```

## Reproduction

```bash
python scripts/run_all_calculations.py
python scripts/build_visual_assets.py
python scripts/build_coursework_site.py
python scripts/validate_svg_bounds.py
node scripts/test_calculators.mjs
python scripts/validate_publication.py
```

The public CI target uses GHDL and g++ where applicable.

## Verification matrix

| Area | Reproducible now | Archive only | Not claimed |
|---|---|---|---|
| Controller Logic | GHDL 6.0.0: 7/7 PASS + 4 original stimuli | Vivado/XSim projects recovered | FPGA timing / board result |
| Transformer | Python loss/efficiency check | Workbook snapshots | Fabrication and hardware tests |
| Power Systems | Zc/SIL arithmetic + PowerWorld 24 blackout rerun | report load-stage screenshots | Validated production grid flow |
| Motor Control | PI/ripple calculations | PSIM/MATLAB screenshots | New licensed simulation or hardware test |
| RF/Microwave | Source-derived equations | Cadence screenshots | VNA measurement / exact 3.5 GHz rerun |
| Sensor Applications | Architecture review plan | None | Dataset, model, prototype, gain |

## Public disclosure boundary

Personal information, student identifiers, local paths, license-bound projects, and third-party teaching material are withheld.

Team coursework is labeled **Team Project · Individual contribution unconfirmed** until the author explicitly confirms role boundaries.

See [ROLE_CONFIRMATION_REQUIRED.md](ROLE_CONFIRMATION_REQUIRED.md), [PUBLICATION_MATRIX.md](PUBLICATION_MATRIX.md), and [LICENSE_NOTICE.md](LICENSE_NOTICE.md).

## Asset traceability

Every generated/cropped asset is listed in [`docs/assets/asset_manifest.yaml`](docs/assets/asset_manifest.yaml). Labels on the site distinguish archive, redraw, recalculation, and proposal evidence.

## Visual source audit

The July 2026 archive audit inventories standalone and embedded visuals, exact/near duplicates, privacy decisions, preferred sources, and public coverage.

- [All source visuals](docs/audit/all_source_visuals.md)
- [Missing visuals report](docs/audit/missing_visuals_report.md)
- [Unused high-value visuals](docs/audit/unused_high_value_visuals.md)
- [Disposition matrix](docs/audit/visual_disposition_matrix.csv)
- [Contact sheets](docs/audit/contact_sheets/)

## License notice

The repository license applies only to public, directly authored or reconstructed material. Withheld originals and third-party material are not relicensed.

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->

<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->
