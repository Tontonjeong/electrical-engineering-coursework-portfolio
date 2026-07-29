# RF/Microwave — 수동회로 설계와 Cadence 결과

**학기:** 4-1 · **프로젝트 유형:** Team Project · Individual contribution unconfirmed
**Evidence:** Source-Derived · Portfolio Redraw · Existing Cadence Result Archive

![Architecture](../../docs/assets/rf/microstrip_design_flow.svg)

## 30초 요약

Microstrip, L-section·single-stub matching, Wilkinson divider, branch-line hybrid를 이론과 기존 Cadence 결과로 비교했습니다.

| 항목 | 내용 |
|---|---|
| 공개 상태 | Theory + existing Cadence archive |
| 소스 상태 | Source-Derived · Portfolio Redraw · Existing Cadence Result Archive |
| Web case study | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/rf-microwave/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/rf-microwave/) |

## 문제 정의

회로식으로 얻은 이상 설계와 substrate·layout·tuning이 반영된 EM/circuit simulation archive를 분리해 설명합니다. 특히 microstrip 설계 주파수는 3.5 GHz이지만 회수된 marker는 3.7 GHz이므로 이를 정확히 구분했습니다.

## 설계 판단

1. Alumina εr=9.9, h=0.5 mm, tanδ=0.001 조건에서 50 Ω, 270° microstrip을 설계했습니다.
2. 1 GHz L-section과 3.5 GHz single-stub의 두 해를 물리 길이로 정리했습니다.
3. Wilkinson은 이론 70.7 Ω λ/4 branch와 100 Ω isolation resistor를 기준으로 봤습니다.
4. Branch-line hybrid는 35.35 Ω/50 Ω branch를 사용한 기존 설계 결과를 보존했습니다.

## 상세 근거와 분리된 하위 사례

- [Homework 2 microstrip](cases/homework2_microstrip.md)
- [Homework 4 L-section](cases/homework4_l_section.md)
- [Homework 4 single-stub](cases/homework4_single_stub.md)
- [Homework 5 Wilkinson](cases/homework5_wilkinson.md)
- [Homework 5 branch-line hybrid](cases/homework5_branch_line.md)
- [Homework 5 Ex. 12-3 incomplete](cases/homework5_ex12_3_incomplete.md)

## 구조와 설계 흐름

![Engineering flow](../../docs/assets/rf/passive-networks.svg)

## 핵심 수치

| Metric | Value |
|---|---:|
| Microstrip target | 3.5 GHz · 50 Ω · 270° |
| Calculated W / L | 0.4815 / 24.97 mm |
| Archive marker | 3.7 GHz only |
| L-section | 0.461 pF · 19.5 nH |
| Wilkinson split | ≈ −3 dB archive |
| Isolation | ≈ −18 dB archive |

## 시각 근거

### Alumina microstrip geometry

**Portfolio Redraw**

![Alumina microstrip geometry](../../docs/assets/rf/microstrip_cross_section.svg)

### Impedance-matching interpretation

**Portfolio Redraw**

![Impedance-matching interpretation](../../docs/assets/rf/smith_chart_movement.svg)

### Quarter-wave divider structure

**Portfolio Redraw**

![Quarter-wave divider structure](../../docs/assets/rf/wilkinson_structure.svg)

### Recovered marker at 3.7 GHz

**Existing Cadence Archive**

![Recovered marker at 3.7 GHz](../../docs/assets/archive/rf/microstrip_loss_3p7ghz.png)

### Divider S-parameter view

**Existing Cadence Archive**

![Divider S-parameter view](../../docs/assets/archive/rf/wilkinson_sparameter_archive.png)

### Hybrid S-parameter view

**Existing Cadence Archive**

![Hybrid S-parameter view](../../docs/assets/archive/rf/hybrid_sparameter_archive.png)

## 검토된 원본 시각 증거

고해상도 원본 후보를 전수 감사한 뒤 개인정보·학번·로컬 경로·제3자 교재를 제외한 공개 가능 산출물입니다.

### Cadence microstrip-line schematic

**Source-Derived**

![Cadence microstrip-line schematic](../../docs/gallery/rf-microwave/microstrip-schematic.png)

### Alumina substrate stack-up definition

**Source-Derived**

![Alumina substrate stack-up definition](../../docs/gallery/rf-microwave/microstrip-stackup-editor.png)

### Recovered microstrip response marker

**Source-Derived**

![Recovered microstrip response marker](../../docs/gallery/rf-microwave/microstrip-response-marker.png)

### 1 GHz L-section matching schematic

**Source-Derived**

![1 GHz L-section matching schematic](../../docs/gallery/rf-microwave/l-section-schematic.png)

### L-section Smith-chart and return-loss response

**Source-Derived**

![L-section Smith-chart and return-loss response](../../docs/gallery/rf-microwave/l-section-smith-response.png)

### Single-stub physical solution 1

**Source-Derived**

![Single-stub physical solution 1](../../docs/gallery/rf-microwave/single-stub-solution-1.png)

### Single-stub physical solution 2

**Source-Derived**

![Single-stub physical solution 2](../../docs/gallery/rf-microwave/single-stub-solution-2.png)

### Wilkinson divider schematic

**Source-Derived**

![Wilkinson divider schematic](../../docs/gallery/rf-microwave/wilkinson-schematic.png)

### Wilkinson divider S-parameter response

**Source-Derived**

![Wilkinson divider S-parameter response](../../docs/gallery/rf-microwave/wilkinson-sparameter.png)

### Branch-line quadrature hybrid schematic

**Source-Derived**

![Branch-line quadrature hybrid schematic](../../docs/gallery/rf-microwave/hybrid-schematic.png)

### Hybrid transmission-line parameter A

**Source-Derived**

![Hybrid transmission-line parameter A](../../docs/gallery/rf-microwave/hybrid-line-parameter-a.png)

### Hybrid transmission-line parameter B

**Source-Derived**

![Hybrid transmission-line parameter B](../../docs/gallery/rf-microwave/hybrid-line-parameter-b.png)

### Quadrature hybrid S-parameter response

**Source-Derived**

![Quadrature hybrid S-parameter response](../../docs/gallery/rf-microwave/hybrid-sparameter.png)

## 검증 상태

| 질문 | 답변 |
|---|---|
| 지금 재현 가능한가? | Theory + existing Cadence archive 범위에서 가능 |
| 과거 결과 화면인가? | Existing Result Archive로 표시된 항목만 해당 |
| 재구성인가? | Portable Reconstruction 또는 Portfolio Redraw로 표시 |
| 실물 구현인가? | 원본이 지원하지 않으면 주장하지 않음 |

## 검증 경계

> Cadence 프로젝트와 라이선스 자료는 공개하지 않습니다. 3.7 GHz marker를 3.5 GHz의 정확한 검증으로 바꾸어 말하지 않습니다. Homework 5 Ex. 12-3은 식별 가능한 최종 결과가 없어 INCOMPLETE_WORK로 분류했습니다. 제작 공차, connector launch, calibration, VNA 측정은 증거 범위 밖입니다.

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

- [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/rf-microwave/)
- [Portfolio home](../../README.md)
- [Asset manifest](../../docs/assets/asset_manifest.yaml)
- [Source provenance](../../SOURCE_PROVENANCE.md)
