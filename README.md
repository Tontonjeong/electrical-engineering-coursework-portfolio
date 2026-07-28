# Electrical Engineering Coursework Portfolio

[English](README.en.md) · [GitHub Pages](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/) · [Validation workflow](https://github.com/Tontonjeong/electrical-engineering-coursework-portfolio/actions/workflows/coursework-validation.yml)

단국대학교 전자전기공학 전공과목에서 수행한 설계·해석·시뮬레이션 과제를, 공개 가능한 근거만 남겨 하나의 검증 가능한 포트폴리오로 재구성했습니다. 핵심은 결과 화면의 나열이 아니라 **입력 조건 → 설계 판단 → 계산/구현 → 검증 → 한계**의 흐름입니다.

> 공개 범위: 원본 보고서에서 확인된 사실과 계산값, 직접 작성한 코드, 공개용 재도식화 자료만 포함합니다. 팀원 이름·학번·로컬 경로·라이선스 종속 파일·원본 과제 PDF는 공개하지 않습니다.

## 한눈에 보기

| 학년-학기 | 과목 / 프로젝트 | 핵심 산출물 | 공개 검증 상태 |
|---|---|---|---|
| 2-2 | Controller Logic | VHDL 조합·순차회로, self-checking testbench | GHDL 7/7 PASS |
| 3-1 | Electrical Machines | 900 W 변압기 설계 및 코어 비교 | 독립 계산 스크립트 |
| 3-1 | Power Systems | 765 kV 장거리 송전선로와 전력정책 검토 | Zc/SIL 재계산, 출처 교차검증 |
| 3-2 | Motor Control | 직류전동기 이중 PI 제어와 토크 리플 | 이득·리플 재계산, 기존 결과 보존 |
| 4-1 | RF/Microwave | Microstrip, matching, Wilkinson, hybrid | 기존 Cadence 결과 아카이브 |
| 4-1 | Sensor Applications | AESA-SAR·Physics-Guided Diffusion 연구 제안 | 개념설계·검증 로드맵 |

## Evidence status

- **Recovered Original**: 제출물 아카이브에서 회수한 직접 작성 소스
- **Portable Reconstruction**: 보고서·회수 소스의 인터페이스를 근거로 재작성한 공개/CI용 구현
- **Independent Recalculation**: 공개 계산식으로 다시 계산한 결과
- **Existing Result Archive**: 기존 제출물에 포함된 시뮬레이션 화면이며 이번 환경에서 재실행하지 않음
- **Concept / Proposal**: 구현·학습·실증 완료가 아닌 연구 제안
- **Publicly Withheld**: 개인정보, 팀원 정보, 라이선스 종속 파일, 원본 보고서

## 주요 사례

### 1. Controller Logic — portable RTL verification

회수된 VHDL 네 개와 공개용 재구성 세 개를 GHDL에서 동일한 회귀 테스트로 검증했습니다. 모든 testbench는 성공 시 `PASS`를 보고하고 오류 시 assertion으로 실패합니다.

```text
Combinational logic → arithmetic → selection → sequence detection → shift/register control
```

[상세 Case Study](00_digital_hardware/controller_logic/README.md)

### 2. Transformer Design — 설계안 비교

220 V를 110 V로 변환하는 900 W, 300 Hz 조건에서 DU/EI/UI 코어를 비교했습니다. 최종 UI-100 설계는 원본 보고서 기준 1차 180턴, 2차 93턴, 효율 96.360%, 전압변동률 1.136%입니다. 별도 계산기는 보고서 수치를 재계산하며, 입력 조건이 다른 스프레드시트 사례는 혼합하지 않습니다.

[상세 Case Study](01_electrical_machines/transformer_design/README.md)

### 3. Power Systems — 계산과 모델 실패의 분리

765 kV, 350 km 선로의 특성 임피던스와 SIL을 재계산했습니다. PowerWorld 아카이브의 비정상 전압은 실제 계통 결과로 해석하지 않고 **비수렴 모델링 사례**로 분류했습니다. 정책 보고서의 날짜와 설비 수치는 정부 원문과 교차검증했습니다.

[상세 Case Study](02_power_systems/transmission_line_and_policy/README.md)

### 4. Motor Control — 계층형 PI 설계

500 Hz 전류 루프와 25 Hz 속도 루프를 분리해 이득을 산정하고, 원본 C++ 계산기와 이식 가능한 CI용 계산기를 함께 보존했습니다. 토크 리플 계산과 그림 파일명의 25/30 kHz 불일치도 숨기지 않고 기록했습니다.

[상세 Case Study](03_motor_control/dc_motor_pi_control/README.md)

### 5–6. RF/Microwave & Sensor Systems

RF 수동회로는 이론 설계값과 기존 Cadence 결과를 구분해 정리했습니다. 센서 응용은 AESA-SAR와 Physics-Guided Diffusion을 연결한 연구 제안이며, 구현·학습·실증을 주장하지 않습니다.

[RF/Microwave](04_rf_microwave/passive_network_design/README.md) · [Sensor Applications](05_sensor_applications/aesa_sar_diffusion_concept/README.md)

## 재현

```bash
python scripts/run_all_calculations.py
python scripts/validate_publication.py
```

VHDL은 GitHub Actions에서 GHDL로, 이식형 C++ 계산기는 `g++`로 빌드·실행합니다. 공개 범위와 provenance는 [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md), [PUBLICATION_MATRIX.md](PUBLICATION_MATRIX.md), [LICENSE_NOTICE.md](LICENSE_NOTICE.md)에 기록했습니다.

## 역할 표기

개인 단독 수행이 원본에서 확인되지 않는 과제는 모두 **Team Project / individual contribution unconfirmed**로 표시했습니다. 면접 또는 제출 전에 [ROLE_CONFIRMATION_REQUIRED.md](ROLE_CONFIRMATION_REQUIRED.md)를 사용자 확인으로 갱신해야 합니다.
