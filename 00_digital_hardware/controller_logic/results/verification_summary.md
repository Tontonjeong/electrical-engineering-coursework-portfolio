# Verification Summary

## Local rerun

- Date: 2026-07-29 KST
- Tool: GHDL 6.0.0 (mcode, WinGet `ghdl.ghdl.ucrt64.mcode`)
- Runner: [`scripts/run_controller_logic_local.ps1`](../../../scripts/run_controller_logic_local.ps1)
- Full log: [`ghdl_6_0_0_local_regression.log`](ghdl_6_0_0_local_regression.log)
- Machine-readable summary: [`ghdl_6_0_0_local_summary.csv`](ghdl_6_0_0_local_summary.csv)

### Recovered assignment stimuli

Four testbenches were copied from the recovered Vivado projects and rerun before
the public self-checking suite. They contain stimulus but no pass/fail
assertions, so completion is labelled `STIMULUS_COMPLETE`, not PASS.

| Original testbench | Source boundary | Local outcome |
|---|---|---|
| `fulladd_tb` | recovered project + recovered DUT | `STIMULUS_COMPLETE` |
| `add_4bits_tb` | recovered project + recovered DUT | `STIMULUS_COMPLETE` |
| `mealy_tb` | recovered project + recovered DUT | `STIMULUS_COMPLETE` |
| `mux_8to1_tb` | recovered testbench/DUT; referenced decoder file was absent from the archive | `STIMULUS_COMPLETE` with the public decoder reconstruction |

### Self-checking portable regression

| Testbench | Coverage | Result |
|---|---|---|
| `tb_fulladd` | 8 input combinations | PASS |
| `tb_add_4bits` | 16 × 16 operands × 2 carry inputs | PASS |
| `tb_dec_3to8` | 8 selections | PASS |
| `tb_mux_8to1` | 8 selections | PASS |
| `tb_mux_8to1_4bits` | 8 bus selections | PASS |
| `tb_mealy_101` | directed overlapping sequence | PASS |
| `tb_usr_4bit` | reset, load, hold, left/right shift | PASS |

All seven self-checking tests passed locally. Eleven VCDs are committed under
[`vcd/`](vcd/) so the visible waveform figures remain traceable to executable
signals. The archive also contains original Vivado 2023.2 project and XSim
context for four assignments, but no device constraints, synthesis/timing
reports, or board evidence; FPGA resource, Fmax, power, and hardware PASS are
therefore not claimed.
