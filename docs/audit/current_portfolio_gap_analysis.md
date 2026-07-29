# Current Portfolio Gap Analysis

Audit date: 2026-07-29 KST

## Closed in this rebuild

| Previous gap | Corrective action | Evidence |
|---|---|---|
| VHDL was presented as diagrams without a current run | Installed GHDL 6.0.0, reran four recovered stimulus benches and seven self-checking benches | `controller_logic/results/` |
| Original Vivado context was described as missing | Reconciled the archive: four Vivado 2023.2 projects and XSim context are present | source inventory + verification summary |
| VHDL PASS was not tied to waveforms | Committed eleven VCD traces and generated waveform figures from them | `results/vcd/`, `docs/assets/results/digital/` |
| PowerWorld evidence was archive-only | Opened `newcase.pwb` in installed PowerWorld 24 and reran Newton power flow | `powerworld_24_rerun.md` |
| 911 archive records had no publication boundary | Added file-level inventory, content coverage, duplicate groups, and publication decisions | `docs/audit/*.csv` |
| Confidential VRET names were visible in a draft audit | Replaced public filenames and hashes with withheld IDs | `source_inventory.csv` |

## Remaining evidence limits

| Area | Gap | Portfolio treatment |
|---|---|---|
| Controller Logic | No constraints, synthesis/timing reports, or board test | Do not claim FPGA PPA, Fmax, or hardware PASS |
| Transformer | No fabrication, temperature rise, insulation, open/short-circuit test | Present as calculation design |
| Power Systems | Saved `newcase.pwb` blackouts; report load-step states are not reconstructed one-by-one | Separate report-derived claims from tool rerun |
| Motor Control | PSIM/MATLAB projects are not available in a portable rerunnable form | Mark screenshots as Existing Result Archive |
| RF/Microwave | Cadence/Virtuoso environment is unavailable; no VNA measurement | Keep equations and archive plots separate |
| Sensor Applications | Literature/concept report only; no dataset, model training, or hardware | Label Concept / Proposal Only |
| VRET | Industry R&D disclosure status is unconfirmed | Withhold all source names/content |

## Supported and unsupported claims

Supported: design calculations, executable VHDL verification, and source
reconciliation. Unsupported: fabricated hardware, RF measurement, production
grid validation, and trained diffusion-model performance.
