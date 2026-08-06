# Motor Control — 직류전동기 이중 PI 제어

**학기:** 3-2 · **프로젝트 유형:** Team Project · Individual contribution unconfirmed
**Evidence:** Recovered Original · Independent Recalculation · Existing PSIM/MATLAB Archive

![Architecture](../../docs/assets/motor/dc_motor_system_architecture.svg)

## DC motor 파라미터와 제어 주기

500 Hz 전류 루프와 25 Hz 속도 루프, 전류 제한·anti-windup·field weakening을 하나의 제어 구조로 정리했습니다.

| 항목 | 내용 |
|---|---|
| 공개 상태 | Calculation + existing simulation archive |
| 소스 상태 | Recovered Original · Independent Recalculation · Existing PSIM/MATLAB Archive |
| Web case study | [https://dororok9061.github.io/electrical-engineering-coursework-portfolio/courses/motor-control/](https://dororok9061.github.io/electrical-engineering-coursework-portfolio/courses/motor-control/) |

## 전류·속도 이중 PI 설계

전기적으로 빠른 전류 동특성과 느린 기계 속도 동특성을 분리해 cascade controller를 설계했습니다. 계산식, 회수 C/C++ 상수, 기존 PSIM/MATLAB 화면 사이의 차이를 숨기지 않고 parameter consistency audit로 관리했습니다.

### 적용한 설계 조건

1. 전류 루프 대역폭 500 Hz에서 Kp=62.832, Ki=314.16을 재계산했습니다.
2. 속도 루프 25 Hz의 보고서 값 Kp=24.8, Ki≈3898과 회수 소스 Ki=3895를 모두 보존했습니다.
3. 속도 지령은 0→850 rpm, hold, 850→1200 rpm 순서로 구성됩니다.
4. ±10 A current limit, ±200 V voltage saturation, field weakening 구간을 제어 흐름에 포함했습니다.

## 상세 근거와 분리된 하위 사례

- [Parameter consistency audit](parameter_consistency_audit.md)

## 설계 구조

![Engineering flow](../../docs/assets/motor/cascaded_pi_controller.svg)

## Gain·제한값·ripple

| Metric | Value |
|---|---:|
| Current loop | 500 Hz |
| Current PI | 62.832 / 314.16 |
| Speed loop | 25 Hz |
| Speed PI | 24.8 / 3898 report |
| Source Ki | 3895 |
| Torque ripple | 2.28 → 0.38 N·m |

## 응답과 torque ripple

### 500 Hz inner-loop design

**Portfolio Redraw**

![500 Hz inner-loop design](../../docs/assets/motor/current_loop_design.svg)

### 25 Hz outer-loop design

**Portfolio Redraw**

![25 Hz outer-loop design](../../docs/assets/motor/speed_loop_design.svg)

### Limiter and anti-windup behavior

**Portfolio Redraw**

![Limiter and anti-windup behavior](../../docs/assets/motor/saturation_anti_windup.svg)

### Recovered simulation schematic

**Existing PSIM Archive**

![Recovered simulation schematic](../../docs/assets/archive/motor/psim_circuit_archive.png)

### Recovered speed response

**Existing PSIM Archive**

![Recovered speed response](../../docs/assets/archive/motor/speed_response_psim_archive.png)

### Torque-ripple comparison

**Independent Recalculation**

![Torque-ripple comparison](../../docs/assets/motor/torque_ripple_comparison.png)

## PSIM·MATLAB 기존 결과

학번·개인정보·로컬 경로·제3자 교재를 제외한 원본 결과 화면입니다.

### 0→850→1200 rpm reference profile

**Existing PSIM Archive**

![0→850→1200 rpm reference profile](../../docs/assets/archive/motor/reference_speed_profile_archive.png)

### Recovered MATLAB speed response

**Existing MATLAB Archive**

![Recovered MATLAB speed response](../../docs/assets/archive/motor/speed_response_matlab_archive.png)

### Recovered PSIM current response

**Existing PSIM Archive**

![Recovered PSIM current response](../../docs/assets/archive/motor/current_response_psim_archive.png)

### Recovered MATLAB current response

**Existing MATLAB Archive**

![Recovered MATLAB current response](../../docs/assets/archive/motor/current_response_matlab_archive.png)

### Recovered field-weakening response

**Existing PSIM Archive**

![Recovered field-weakening response](../../docs/assets/archive/motor/field_weakening_archive.png)

### Recovered torque-ripple case A

**Existing Result Archive**

![Recovered torque-ripple case A](../../docs/assets/archive/motor/torque_ripple_10khz_archive.png)

### Recovered torque-ripple case B

**Existing Result Archive**

![Recovered torque-ripple case B](../../docs/assets/archive/motor/torque_ripple_25khz_archive.png)

## PI gain 계산 코드

### 0→850→1200 rpm reference

**Recovered Original**

![0→850→1200 rpm reference](../../docs/assets/code/motor_reference_profile.svg)

### Current PI and ±200 V saturation

**Recovered Original**

![Current PI and ±200 V saturation](../../docs/assets/code/motor_current_pi_saturation.svg)

### Speed PI and ±10 A limit

**Recovered Original**

![Speed PI and ±10 A limit](../../docs/assets/code/motor_speed_pi_limiter.svg)

## Archive와 재계산 범위

> PSIM/MATLAB 프로젝트를 라이선스 독립적으로 재실행할 자료는 회수되지 않았습니다. 화면은 Existing Result Archive이며 새 실행 결과가 아닙니다. 파일명 25 kHz와 본문 30 kHz의 불일치는 그대로 표시합니다. 하드웨어 실험은 주장하지 않습니다.

## 계산 코드와 기존 결과 파일

```bash
python scripts/run_all_calculations.py
python scripts/validate_publication.py
```

세부 소스·계산·로그는 실제 존재하는 `src/`, `tb/`, `calculations/`, `data/`, `results/` 경로에서 확인합니다.

- [Visual case study](https://dororok9061.github.io/electrical-engineering-coursework-portfolio/courses/motor-control/)
- [Portfolio home](../../README.md)
- [Asset manifest](../../docs/assets/asset_manifest.yaml)
- [Source provenance](../../SOURCE_PROVENANCE.md)
