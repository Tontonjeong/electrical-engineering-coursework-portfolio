# Missing Content Report

This report records evidence that would materially raise claim confidence but
was not found in the 911-file expanded archive.

| Priority | Missing evidence | Affected claim | Recommended next capture |
|---|---|---|---|
| P0 | FPGA constraints and synthesis/timing reports | device utilization, Fmax, timing closure | rerun Vivado on a named target and export reports |
| P0 | Board test photo/video with I/O mapping | hardware operation | show bitstream, pins, stimulus, and observed output |
| P0 | Valid convergent PowerWorld baseline plus controlled load sweep | voltage-stability boundary | export case variants and a bus-voltage/load table |
| P1 | Transformer build and standard tests | efficiency/regulation in hardware | no-load, short-circuit, load, thermal measurements |
| P1 | PSIM/MATLAB source projects and version metadata | motor-control rerun | archive schematics/models and scripted exports |
| P1 | Cadence project/netlists and exact marker exports | RF simulation reproducibility | archive project setup and CSV S-parameters |
| P1 | VNA calibration/measurement files | RF hardware performance | Touchstone data with fixture/calibration notes |
| P1 | SAR dataset split, code, checkpoints, metrics | diffusion improvement | publish reproducible non-sensitive experiment |
| P2 | Confirmed individual role statements for team reports | contribution attribution | add signed role/ownership notes |

Incomplete RF `ex12-3` images remain explicitly classified as
`INCOMPLETE_WORK`; they are not promoted to a successful result.
