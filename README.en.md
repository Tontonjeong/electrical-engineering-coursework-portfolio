# Electrical Engineering Coursework Portfolio

[한국어](README.md) · [GitHub Pages](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/en/) · [Source Provenance](SOURCE_PROVENANCE.md)

![Portfolio hero](docs/assets/hero/coursework_portfolio_hero.png)

This repository records design conditions, equations, RTL, simulation results, and verification limits from electrical engineering coursework.

## Evidence labels

- Recovered Original: directly authored source recovered from the archive
- Portable Reconstruction: public implementation used to reproduce documented behavior
- Independent Recalculation: equations rerun from documented inputs
- Existing Result Archive: prior PSIM, MATLAB, Cadence, or PowerWorld evidence; not rerun here
- Tool Rerun: original source reopened and executed with a currently installed tool
- Portfolio Redraw: public visual redrawn from source-derived structure
- Concept / Proposal: research design without implementation or experimental claims

## Coursework index

| Term | Case study | Core output | Evidence state |
|---|---|---|---|
| 2-2 | [Controller Logic — VHDL Design & Portable Verification](00_digital_hardware/controller_logic/README.md) | Seven RTL blocks spanning combinational logic, an FSM, and a universal shift register were rerun with self-checking testbenches. | GHDL 7/7 PASS |
| 3-1 | [Electrical Machines — 900 W Transformer Design](01_electrical_machines/transformer_design/README.md) | DU, EI, and UI cores were compared for a 220/110 V, 900 W, 300 Hz transformer, leading to the UI-100 calculation case. | Independent recalculation |
| 3-1 | [Power Systems — 765 kV Line & Policy Review](02_power_systems/transmission_line_and_policy/README.md) | Surge impedance and SIL were recalculated while a non-convergent PowerWorld archive and policy figures were kept in separate evidence classes. | Zc 255.38 Ω · SIL 2.292 GW · PWB rerun: Blackout |
| 3-2 | [Motor Control — Cascaded PI Control of a DC Motor](03_motor_control/dc_motor_pi_control/README.md) | A 500 Hz current loop and 25 Hz speed loop are integrated with current limiting, anti-windup, and field weakening. | Calculation + existing simulation archive |
| 4-1 | [RF/Microwave — Passive Networks & Cadence Archive](04_rf_microwave/passive_network_design/README.md) | Microstrip, L-section and single-stub matching, a Wilkinson divider, and a branch-line hybrid are compared through theory and an existing Cadence archive. | Theory + existing Cadence archive |
| 4-1 | [Sensor Applications — AESA-SAR & Physics-Guided Diffusion](05_sensor_applications/aesa_sar_diffusion_concept/README.md) | A research proposal links AESA acquisition, conventional SAR reconstruction, and physics-conditioned diffusion with a staged validation roadmap. | Concept / Proposal Only |
## Interactive calculators

| Tool | Scope | Link |
|---|---|---|
| Transformer Case | Loss, efficiency, regulation | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transformer-case-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transformer-case-calculator/) |
| Motor PI | Current-loop gains + preserved discrepancy | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/motor-pi-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/motor-pi-calculator/) |
| Transmission Line | Zc, SIL, current | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transmission-line-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transmission-line-calculator/) |
| RF · Microwave Study | 32 bilingual notes + 7 calculators | [Main portfolio](https://tontonjeong.github.io/blog/rf/start-here/) |

## Repository structure

```text
00_digital_hardware/      VHDL sources, testbenches, VCD results
01_electrical_machines/   transformer calculations and workbook audit
02_power_systems/         line arithmetic, policy reconciliation
03_motor_control/         PI calculations, recovered source, archived plots
04_rf_microwave/          passive network cases and Cadence archive
rf-study/                 RFDH source map, redraws, RF calculations, notebook
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
python -m unittest discover -s rf-study/tests -p 'test_*.py'
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
