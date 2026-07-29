# Electrical Engineering Coursework Portfolio

[English](README.en.md) · [GitHub Pages](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/) · [Source Provenance](SOURCE_PROVENANCE.md)

![Portfolio hero](docs/assets/hero/coursework_portfolio_hero.png)

단국대학교 전자전기공학 전공과목의 설계 조건, 계산식, RTL, 시뮬레이션 결과, 검증 한계를 기록합니다.

## 증거 상태

- Recovered Original: 제출물에서 회수한 직접 작성 소스
- Portable Reconstruction: 원본 기능을 공개 환경에서 다시 검증하기 위한 재구성
- Independent Recalculation: 보고서 입력과 식을 별도 코드로 재계산
- Existing Result Archive: 기존 PSIM·MATLAB·Cadence·PowerWorld 화면이며 현재 환경 재실행 아님
- Tool Rerun: 현재 설치된 도구에서 원본 파일을 다시 실행한 결과
- Portfolio Redraw: 원본 내용을 바탕으로 공개용으로 다시 그린 도식
- Concept / Proposal: 구현·학습·실증이 완료되지 않은 연구 설계

## 과목별 산출물

| Term | Case study | Core output | Evidence state |
|---|---|---|---|
| 2-2 | [Controller Logic — VHDL 설계와 Portable Verification](00_digital_hardware/controller_logic/README.md) | 조합회로에서 FSM·범용 시프트 레지스터까지 7개 RTL 블록을 self-checking testbench로 재검증했습니다. | GHDL 7/7 PASS |
| 3-1 | [Electrical Machines — 900 W 변압기 설계](01_electrical_machines/transformer_design/README.md) | 220/110 V, 900 W, 300 Hz 조건에서 DU·EI·UI 코어를 계산 비교하고 UI-100 설계를 선택했습니다. | Independent recalculation |
| 3-1 | [Power Systems — 765 kV 송전선로와 전력정책 검토](02_power_systems/transmission_line_and_policy/README.md) | 분포정수 선로의 Zc·SIL을 재계산하고, PowerWorld 비수렴 결과와 정책 수치를 서로 다른 증거로 분리했습니다. | Zc 255.38 Ω · SIL 2.292 GW · PWB rerun: Blackout |
| 3-2 | [Motor Control — 직류전동기 이중 PI 제어](03_motor_control/dc_motor_pi_control/README.md) | 500 Hz 전류 루프와 25 Hz 속도 루프, 전류 제한·anti-windup·field weakening을 하나의 제어 구조로 정리했습니다. | Calculation + existing simulation archive |
| 4-1 | [RF/Microwave — 수동회로 설계와 Cadence 결과](04_rf_microwave/passive_network_design/README.md) | Microstrip, L-section·single-stub matching, Wilkinson divider, branch-line hybrid를 이론과 기존 Cadence 결과로 비교했습니다. | Theory + existing Cadence archive |
| 4-1 | [Sensor Applications — AESA-SAR와 Physics-Guided Diffusion](05_sensor_applications/aesa_sar_diffusion_concept/README.md) | AESA 수집, SAR 복원, physics-conditioned diffusion을 연결한 연구 제안과 단계별 검증 로드맵입니다. | Concept / Proposal Only |
## Interactive Calculator

| Tool | Scope | Link |
|---|---|---|
| Transformer Case | Loss, efficiency, regulation | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transformer-case-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transformer-case-calculator/) |
| Motor PI | Current-loop gains + preserved discrepancy | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/motor-pi-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/motor-pi-calculator/) |
| Transmission Line | Zc, SIL, current | [https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transmission-line-calculator/](https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/tools/transmission-line-calculator/) |

## 저장소 구조

```text
00_digital_hardware/      VHDL sources, testbenches, VCD results
01_electrical_machines/   transformer calculations and workbook audit
02_power_systems/         line arithmetic, policy reconciliation
03_motor_control/         PI calculations, recovered source, archived plots
04_rf_microwave/          passive network cases and Cadence archive
05_sensor_applications/   AESA-SAR research architecture
docs/                     bilingual multi-page portfolio and visual assets
scripts/                  calculation, build, and publication QA
```

## 재현과 검증

```bash
python scripts/run_all_calculations.py
python scripts/build_visual_assets.py
python scripts/build_coursework_site.py
python scripts/validate_svg_bounds.py
node scripts/test_calculators.mjs
python scripts/validate_publication.py
```

공개 CI는 가능한 범위에서 GHDL과 g++를 사용합니다.

## 검증 매트릭스

| Area | Reproducible now | Archive only | Not claimed |
|---|---|---|---|
| Controller Logic | GHDL 6.0.0: 7/7 PASS + 4 original stimuli | Vivado/XSim projects recovered | FPGA timing / board result |
| Transformer | Python loss/efficiency check | Workbook snapshots | Fabrication and hardware tests |
| Power Systems | Zc/SIL arithmetic + PowerWorld 24 blackout rerun | report load-stage screenshots | Validated production grid flow |
| Motor Control | PI/ripple calculations | PSIM/MATLAB screenshots | New licensed simulation or hardware test |
| RF/Microwave | Source-derived equations | Cadence screenshots | VNA measurement / exact 3.5 GHz rerun |
| Sensor Applications | Architecture review plan | None | Dataset, model, prototype, gain |

## 공개 범위와 기여도

개인정보, 학번, 로컬 경로, 라이선스 종속 프로젝트, 제3자 교재는 공개하지 않습니다.

팀 과제는 작성자가 역할을 확정하기 전까지 **Team Project · Individual contribution unconfirmed**로 표시합니다.

See [ROLE_CONFIRMATION_REQUIRED.md](ROLE_CONFIRMATION_REQUIRED.md), [PUBLICATION_MATRIX.md](PUBLICATION_MATRIX.md), and [LICENSE_NOTICE.md](LICENSE_NOTICE.md).

## 시각 자료 추적성

Every generated/cropped asset is listed in [`docs/assets/asset_manifest.yaml`](docs/assets/asset_manifest.yaml). Labels on the site distinguish archive, redraw, recalculation, and proposal evidence.

## Visual source audit

The July 2026 archive audit inventories standalone and embedded visuals, exact/near duplicates, privacy decisions, preferred sources, and public coverage.

- [All source visuals](docs/audit/all_source_visuals.md)
- [Missing visuals report](docs/audit/missing_visuals_report.md)
- [Unused high-value visuals](docs/audit/unused_high_value_visuals.md)
- [Disposition matrix](docs/audit/visual_disposition_matrix.csv)
- [Contact sheets](docs/audit/contact_sheets/)

## License notice

The repository license applies only to public, directly authored or reconstructed material. Withheld originals and third-party material are not relicensed.
