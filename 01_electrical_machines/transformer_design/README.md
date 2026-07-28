# Electrical Machines — 900 W 변압기 설계

**학기:** 3-1 · **프로젝트 유형:** Team Project · Individual contribution unconfirmed
**Evidence:** Source-Derived · Workbook Snapshot · Independent Recalculation

![Architecture](../../docs/assets/transformer/transformer_winding_architecture.svg)

## 30초 요약

220/110 V, 900 W, 300 Hz 조건에서 DU·EI·UI 코어를 계산 비교하고 UI-100 설계를 선택했습니다.

| 항목 | 내용 |
|---|---|
| 공개 상태 | Independent recalculation |
| 소스 상태 | Source-Derived · Workbook Snapshot · Independent Recalculation |
| Web case study | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/electrical-machines/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/electrical-machines/) |

## 문제 정의

정격 요구에서 권선수와 도체를 산정하고, 동손·철손·효율·전압변동률·창 이용률을 계산해 서로 다른 코어 형상을 비교했습니다. 최종 선택은 단일 최고 수치가 아니라 효율과 전압변동률, 창 이용률을 함께 본 trade study입니다.

## 설계 판단

1. 설계 입력은 220/110 V, 900 W, 300 Hz, silicon steel, Bmax 1.5 T로 고정했습니다.
2. DU-75, EI-112 초기·재설계, UI-100 사례를 동일한 판단 축으로 비교했습니다.
3. UI-100 최종안은 1차 180회, 2차 93회, 효율 96.360%, 전압변동률 1.136%로 정리했습니다.
4. 회수 workbook 중 다른 입력 조건과 #VALUE! 오류는 최종 설계 근거와 분리했습니다.

## 구조와 설계 흐름

![Engineering flow](../../docs/assets/transformer/core_geometry_flow.svg)

## 핵심 수치

| Metric | Value |
|---|---:|
| Primary / secondary | 180 / 93 turns |
| Copper loss | 10.2267 W |
| Core loss | 23.7760 W |
| Efficiency | 96.360% |
| Regulation | 1.136% |

## 시각 근거

### Source-derived design requirements

**Portfolio Redraw**

![Source-derived design requirements](../../docs/assets/transformer/transformer_requirements_card.png)

### Core trade-space comparison

**Portfolio Redraw**

![Core trade-space comparison](../../docs/assets/transformer/ui_ei_du_core_comparison.svg)

### Final-case loss accounting

**Independent Recalculation**

![Final-case loss accounting](../../docs/assets/transformer/loss_breakdown.png)

### Efficiency and regulation comparison

**Portfolio Redraw**

![Efficiency and regulation comparison](../../docs/assets/transformer/efficiency_regulation_chart.png)

### Rendered cell values; original workbook withheld

**Workbook Snapshot**

![Rendered cell values; original workbook withheld](../../docs/assets/calculators/transformer_workbook_general.png)

### Portable report-case recalculation

**Calculator Snapshot**

![Portable report-case recalculation](../../docs/assets/calculators/transformer_case_snapshot.png)

## 코드 근거

### Loss and efficiency equations

**Independent Recalculation**

![Loss and efficiency equations](../../docs/assets/code/calc_transformer.svg)

## 검증 상태

| 질문 | 답변 |
|---|---|
| 지금 재현 가능한가? | Independent recalculation 범위에서 가능 |
| 과거 결과 화면인가? | Existing Result Archive로 표시된 항목만 해당 |
| 재구성인가? | Portable Reconstruction 또는 Portfolio Redraw로 표시 |
| 실물 구현인가? | 원본이 지원하지 않으면 주장하지 않음 |

## 검증 경계

> 최종 제작, 온도상승, 절연 내력, 무부하·단락 시험의 실물 증거는 확인되지 않았습니다. 결과는 계산 기반 설계입니다. Workbook 화면은 셀 값을 렌더링한 snapshot이며 Excel 애플리케이션 실행 화면이 아닙니다.

## 재현 절차

```bash
python scripts/run_all_calculations.py
python scripts/validate_publication.py
```

세부 소스와 계산은 이 디렉터리의 `src/`, `tb/`, `calculations/`, `data/`, `results/` 중 존재하는 경로를 참조합니다.

## Source classification

- **Source-Derived:** 보고서 또는 회수 소스에 직접 존재
- **Portable Reconstruction:** 공개 검증을 위해 기능을 재작성
- **Independent Recalculation:** 원본 입력을 별도 코드로 계산
- **Existing Result Archive:** 과거 제출물의 결과 화면
- **Portfolio Redraw:** 공개 설명을 위한 재도식화
- **Publicly Withheld:** 개인정보·라이선스·제3자 권리 때문에 미공개

## Navigation

- [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/electrical-machines/)
- [Portfolio home](../../README.md)
- [Asset manifest](../../docs/assets/asset_manifest.yaml)
- [Source provenance](../../SOURCE_PROVENANCE.md)

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->

<!-- Source-bounded case study; no unsupported claim is implied. -->
