# Controller Logic — VHDL Design & Portable Verification

**Term:** 2-2 · **Evidence:** Recovered Original / Portable Reconstruction / GHDL Rerun

## Problem

조합회로에서 순차회로로 확장되는 기본 RTL 블록을 VHDL로 작성하고, 특정 FPGA 툴에 묶이지 않는 테스트 환경에서 동작을 검증하는 과제입니다.

## Design progression

| Block | Function | Source status | Public verification |
|---|---|---|---|
| `fulladd` | 1-bit full adder | Recovered Original | Exhaustive 8 vectors |
| `add_4bits` | 4-bit ripple-carry adder | Recovered Original | Exhaustive 512 vectors |
| `dec_3to8` | 3-to-8 active-high decoder | Portable Reconstruction | Exhaustive 8 vectors |
| `mux_8to1` | 8-to-1 scalar mux | Recovered Original | All selections |
| `mux_8to1_4bits` | 8-to-1, 4-bit bus mux | Portable Reconstruction | All selections |
| `mealy_101` | Overlapping `101` sequence detector | Recovered Original | Directed sequence |
| `usr_4bit` | Hold/shift-left/shift-right/load register | Portable Reconstruction | Directed mode test |

## Verification architecture

```text
VHDL source → GHDL analysis/elaboration → self-checking testbench
                                             ├─ assertion failure: CI FAIL
                                             └─ PASS report + VCD artifact
```

`src/original`은 제출물에서 회수한 원본입니다. `src/portable_reconstruction`은 회수되지 않은 블록을 보고서의 기능과 공개 가능한 인터페이스를 기준으로 재작성했습니다. 재구성 파일은 원본으로 주장하지 않습니다.

## Key engineering decisions

- `std_logic_unsigned` 같은 비표준 산술 패키지 대신 공개 재구성과 testbench에서 `numeric_std`를 사용했습니다.
- 모든 입력 조합을 완전탐색할 수 있는 작은 조합회로는 exhaustive test를 적용했습니다.
- 순차회로는 reset, hold, load, shift, overlap detection을 명시적으로 자극했습니다.
- 성공 로그뿐 아니라 파형 VCD를 CI artifact로 생성합니다.

## Result

| Metric | Result |
|---|---:|
| Compiled design units | 7 |
| Self-checking testbenches | 7 |
| Local GHDL regression | 7 PASS / 0 FAIL |
| Portable CI target | Ubuntu + GHDL |

## Boundary

재구성 `usr_4bit`은 공개용 가정으로 asynchronous clear를 사용합니다. 원본 Vivado 프로젝트, device constraint, synthesis/timing 결과가 없으므로 FPGA 자원·Fmax·보드 실증은 주장하지 않습니다.
