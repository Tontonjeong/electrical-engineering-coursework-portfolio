# Verification Summary

Local public regression with GHDL mcode:

| Testbench | Coverage | Result |
|---|---|---|
| `tb_fulladd` | 8 input combinations | PASS |
| `tb_add_4bits` | 16 × 16 operands × 2 carry inputs | PASS |
| `tb_dec_3to8` | 8 selections | PASS |
| `tb_mux_8to1` | 8 selections | PASS |
| `tb_mux_8to1_4bits` | 8 bus selections | PASS |
| `tb_mealy_101` | directed overlapping sequence | PASS |
| `tb_usr_4bit` | reset, load, hold, left/right shift | PASS |

The GitHub Actions run is the public reproducible record. VCD files are generated as workflow artifacts and are not committed.
