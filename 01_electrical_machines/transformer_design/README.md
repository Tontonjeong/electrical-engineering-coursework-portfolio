# Electrical Machines — 900 W Transformer Design

**Term:** 3-1 · **Project type:** Team Project · Individual contribution unconfirmed  
**Evidence:** Source-Derived / Independent Recalculation / Workbook Audit

## Design brief

| Item | Requirement |
|---|---:|
| Primary / secondary | 220 V / 110 V |
| Rated output | 900 W |
| Frequency | 300 Hz |
| Core material | Silicon steel |
| Maximum flux density | 1.5 T |

목표는 정격 변압기의 권선수·도체·손실·효율·전압변동률·창 이용률을 계산하고 DU/EI/UI 코어의 적합성을 비교하는 것입니다.

## Decision flow

```text
Electrical requirements
  → volts-per-turn and turns
  → current and conductor selection
  → copper/core loss
  → efficiency & regulation
  → window utilization
  → core comparison
  → UI-100 final selection
```

## Core trade study

| Case | Efficiency | Regulation | Window utilization | Interpretation |
|---|---:|---:|---:|---|
| DU-75 | 95.985% | — | — | Efficiency target not met |
| EI-112, first | 96.264% | 2.018% | 0.454 | Window utilization rejected |
| EI-112, redesigned | 96.014% | 2.289% | 0.359 | Feasible but lower result |
| UI-100, final | **96.360%** | **1.136%** | **≈0.312** | Selected |

## Final design

| Metric | Report value |
|---|---:|
| Primary turns | 180 |
| Secondary turns | 93 |
| Copper loss | 10.2267 W |
| Core loss | 23.7760 W |
| Total loss | ≈33.9998 W |
| Efficiency | 96.360% |
| Regulation | 1.136% |

`calculations/validate_transformer.py`는 손실합과 효율을 독립적으로 재계산합니다. 반올림과 보고서 표시 자릿수 때문에 미세한 차이가 날 수 있습니다.

## Workbook audit

회수된 네 개의 계산 워크북은 수식 오류와 입력 조건을 검사했습니다.

- 한 워크북은 UI 사례를 포함하지만 110→220 V, 600 W, 50 Hz, 1.6 T로 본 보고서와 다른 설계입니다.
- 한 EI 워크북은 `#VALUE!`을 포함합니다.
- PI 계산 워크북은 `#DIV/0!` 및 깨진 참조를 포함합니다.
- 따라서 원본 워크북은 공개하지 않고 audit 결과만 남깁니다.

자세한 내용은 [workbook_audit.md](data/workbook_audit.md)와 [design_case_comparison.csv](data/design_case_comparison.csv)를 참조하십시오.

## Boundary

최종 제작, 온도상승 시험, 절연 내력 시험, 실제 무부하/단락 시험 증거는 원본에서 확인되지 않습니다. 따라서 결과는 **계산 기반 설계**로 제한합니다.
