# RF/Microwave — 수동회로 설계와 Cadence 결과

**학기:** 4-1 · **프로젝트 유형:** Team Project · Individual contribution unconfirmed
**Evidence:** Source-Derived · Portfolio Redraw · Existing Cadence Result Archive

![Architecture](../../docs/assets/rf/microstrip_design_flow.svg)

## 회로별 주파수·기판·임피던스

Microstrip, L-section·single-stub matching, Wilkinson divider, branch-line hybrid를 이론과 기존 Cadence 결과로 비교했습니다.

| 항목 | 내용 |
|---|---|
| 공개 상태 | Theory + existing Cadence archive |
| 소스 상태 | Source-Derived · Portfolio Redraw · Existing Cadence Result Archive |
| Web case study | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/rf-microwave/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/rf-microwave/) |

## 이론값·Cadence 입력·튜닝값 분리

회로식으로 얻은 이상 설계와 substrate·layout·tuning이 반영된 EM/circuit simulation archive를 분리해 설명합니다. 특히 microstrip 설계 주파수는 3.5 GHz이지만 회수된 marker는 3.7 GHz이므로 이를 정확히 구분했습니다.

### 적용한 설계 조건

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

## 설계 구조

![Engineering flow](../../docs/assets/rf/passive-networks.svg)

## 회로별 중심주파수와 응답

| Metric | Value |
|---|---:|
| Microstrip target | 3.5 GHz · 50 Ω · 270° |
| Calculated W / L | 0.4815 / 24.97 mm |
| Archive marker | 3.7 GHz only |
| L-section | 0.461 pF · 19.5 nH |
| Wilkinson split | ≈ −3 dB archive |
| Isolation | ≈ −18 dB archive |

## Schematic·Smith chart·S-parameter

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

## Cadence 회로·parameter·marker

학번·개인정보·로컬 경로·제3자 교재를 제외한 원본 결과 화면입니다.

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

## Archive·미완료·측정 범위

> Cadence 프로젝트와 라이선스 자료는 공개하지 않습니다. 3.7 GHz marker를 3.5 GHz의 정확한 검증으로 바꾸어 말하지 않습니다. Homework 5 Ex. 12-3은 식별 가능한 최종 결과가 없어 INCOMPLETE_WORK로 분류했습니다. 제작 공차, connector launch, calibration, VNA 측정은 증거 범위 밖입니다.

## 회로별 보고서와 결과 파일

```bash
python scripts/run_all_calculations.py
python scripts/validate_publication.py
```

세부 소스·계산·로그는 실제 존재하는 `src/`, `tb/`, `calculations/`, `data/`, `results/` 경로에서 확인합니다.

- [Visual case study](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/courses/rf-microwave/)
- [Portfolio home](../../README.md)
- [Asset manifest](../../docs/assets/asset_manifest.yaml)
- [Source provenance](../../SOURCE_PROVENANCE.md)
