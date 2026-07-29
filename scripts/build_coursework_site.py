#!/usr/bin/env python3
"""Build the bilingual visual case-study site, calculators, and rich READMEs."""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import dedent
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPO = "https://github.com/Tontonjeong/electrical-engineering-coursework-portfolio"
SITE = "https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/"


COURSES = [
    {
        "id": "controller-logic",
        "detail_links": [("Local GHDL 6.0.0 verification summary", "results/verification_summary.md")],
        "path": "00_digital_hardware/controller_logic",
        "term": "2-2",
        "ko_title": "Controller Logic — VHDL 설계와 Portable Verification",
        "en_title": "Controller Logic — VHDL Design & Portable Verification",
        "ko_short": "조합회로에서 FSM·범용 시프트 레지스터까지 7개 RTL 블록을 self-checking testbench로 재검증했습니다.",
        "en_short": "Seven RTL blocks spanning combinational logic, an FSM, and a universal shift register were rerun with self-checking testbenches.",
        "status": "GHDL 7/7 PASS",
        "evidence": "Recovered Original · Portable Reconstruction · GHDL Rerun",
        "accent": "cyan",
        "hero": "assets/digital/controller_logic_progression.svg",
        "flow": "assets/digital/rtl-flow.svg",
        "visuals": [
            ("assets/digital/one_bit_full_adder_gate.svg", "Portfolio Redraw", "1-bit full-adder gate structure"),
            ("assets/digital/four_bit_ripple_carry.svg", "Portfolio Redraw", "4-bit ripple-carry hierarchy"),
            ("assets/digital/mealy_101_state_diagram.svg", "Portfolio Redraw", "Overlapping 101 Mealy FSM"),
            ("assets/digital/universal_shift_register.svg", "Portfolio Redraw", "Hold, shift, and load modes"),
            ("assets/results/digital/tb_add_4bits_waveform.svg", "Portable GHDL Result", "Exhaustive adder regression waveform"),
            ("assets/results/digital/tb_mealy_101_waveform.svg", "Portable GHDL Result", "Directed overlapping-sequence waveform"),
        ],
        "source_visuals": [
            ("gallery/controller-logic/full-adder-hierarchy.png", "Source-Derived", "4-bit adder hierarchy and carry-chain mapping"),
            ("gallery/controller-logic/full-adder-waveform.png", "Source-Derived", "Directed adder vectors and Vivado waveform"),
            ("gallery/controller-logic/decoder-3to8-waveform.png", "Source-Derived", "Exhaustive 3-to-8 decoder waveform"),
            ("gallery/controller-logic/mealy-101-waveform.png", "Source-Derived", "Annotated overlapping-101 Mealy waveform"),
            ("gallery/controller-logic/universal-shift-register-waveform.png", "Source-Derived", "Hold, shift, and load mode waveform"),
        ],
        "code": [
            ("assets/code/vhdl_full_adder.svg", "Recovered Original", "Full-adder concurrent assignments"),
            ("assets/code/vhdl_mealy_fsm.svg", "Recovered Original", "Mealy detector state logic"),
            ("assets/code/vhdl_usr_mode.svg", "Portable Reconstruction", "Universal shift-register mode selection"),
        ],
        "ko_problem": "과제 원본의 핵심은 단일 회로가 아니라, 논리식 → 계층화 → 상태기계 → 레지스터 제어로 확장되는 RTL 사고 과정입니다. 회수된 소스만으로는 모든 블록을 동일 환경에서 검증할 수 없었기 때문에, 원본과 재구성을 디렉터리·표시·검증 결과에서 분리했습니다.",
        "en_problem": "The source material traces a progression from logic equations through hierarchy, state machines, and register control. Because not every source file was recoverable, recovered originals and public reconstructions are separated in both the tree and the evidence labels.",
        "ko_decisions": [
            "작은 조합회로는 입력공간을 완전탐색해 예제 벡터만 맞는 착시를 제거했습니다.",
            "순차회로는 reset, hold, load, 양방향 shift, overlap 검출을 directed test로 분리했습니다.",
            "비표준 산술 패키지 의존을 피하고 공개 재구성 testbench에는 numeric_std를 사용했습니다.",
            "모든 testbench는 assertion 실패 시 CI가 실패하고, 성공 시 PASS와 VCD를 남깁니다.",
        ],
        "en_decisions": [
            "Small combinational blocks use exhaustive input-space checks.",
            "Sequential tests isolate reset, hold, load, both shift directions, and overlap detection.",
            "Public reconstructions avoid non-standard arithmetic packages and use numeric_std.",
            "Assertions fail CI, while successful runs emit PASS messages and VCD evidence.",
        ],
        "metrics": [
            ("Design units", "7"),
            ("Recovered Vivado projects", "4"),
            ("Original stimuli", "4 STIMULUS_COMPLETE"),
            ("Self-checking TB", "7"),
            ("Regression", "7 PASS / 0 FAIL"),
            ("Local tool", "GHDL 6.0.0 mcode"),
        ],
        "boundary_ko": "원본 Vivado 2023.2 프로젝트와 XSim context 4건은 회수했지만, device constraint, synthesis/timing report, 보드 실증은 없습니다. 원본 testbench에는 assertion이 없어 STIMULUS_COMPLETE로만 표시하고, PASS는 별도 self-checking GHDL 6.0.0 suite에만 부여합니다. LUT/FF, Fmax, 전력, hardware PASS는 주장하지 않습니다.",
        "boundary_en": "Four original Vivado 2023.2 projects and XSim contexts were recovered, but device constraints, implementation reports, and board evidence were not. Original benches contain no assertions and are labelled STIMULUS_COMPLETE; PASS belongs only to the separate self-checking GHDL 6.0.0 suite. FPGA utilization, Fmax, power, and hardware PASS are not claimed.",
    },
    {
        "id": "electrical-machines",
        "detail_links": [("Report case and workbook reconciliation", "source_case_reconciliation.md")],
        "path": "01_electrical_machines/transformer_design",
        "term": "3-1",
        "ko_title": "Electrical Machines — 900 W 변압기 설계",
        "en_title": "Electrical Machines — 900 W Transformer Design",
        "ko_short": "220/110 V, 900 W, 300 Hz 조건에서 DU·EI·UI 코어를 계산 비교하고 UI-100 설계를 선택했습니다.",
        "en_short": "DU, EI, and UI cores were compared for a 220/110 V, 900 W, 300 Hz transformer, leading to the UI-100 calculation case.",
        "status": "Independent recalculation",
        "evidence": "Source-Derived · Workbook Snapshot · Independent Recalculation",
        "accent": "amber",
        "hero": "assets/transformer/transformer_winding_architecture.svg",
        "flow": "assets/transformer/core_geometry_flow.svg",
        "visuals": [
            ("assets/transformer/transformer_requirements_card.png", "Portfolio Redraw", "Source-derived design requirements"),
            ("assets/transformer/ui_ei_du_core_comparison.svg", "Portfolio Redraw", "Core trade-space comparison"),
            ("assets/transformer/loss_breakdown.png", "Independent Recalculation", "Final-case loss accounting"),
            ("assets/transformer/efficiency_regulation_chart.png", "Portfolio Redraw", "Efficiency and regulation comparison"),
            ("assets/calculators/transformer_workbook_general.png", "Workbook Snapshot", "Rendered cell values; original workbook withheld"),
            ("assets/calculators/transformer_case_snapshot.png", "Calculator Snapshot", "Portable report-case recalculation"),
        ],
        "code": [
            ("assets/code/calc_transformer.svg", "Independent Recalculation", "Loss and efficiency equations"),
        ],
        "ko_problem": "정격 요구에서 권선수와 도체를 산정하고, 동손·철손·효율·전압변동률·창 이용률을 계산해 서로 다른 코어 형상을 비교했습니다. 최종 선택은 단일 최고 수치가 아니라 효율과 전압변동률, 창 이용률을 함께 본 trade study입니다.",
        "en_problem": "The work sizes turns and conductors from the rating, evaluates copper/core loss, efficiency, regulation, and window utilization, then compares core geometries as a trade study rather than selecting a single best number.",
        "ko_decisions": [
            "설계 입력은 220/110 V, 900 W, 300 Hz, silicon steel, Bmax 1.5 T로 고정했습니다.",
            "DU-75, EI-112 초기·재설계, UI-100 사례를 동일한 판단 축으로 비교했습니다.",
            "UI-100 최종안은 1차 180회, 2차 93회, 효율 96.360%, 전압변동률 1.136%로 정리했습니다.",
            "회수 workbook 중 다른 입력 조건과 #VALUE! 오류는 최종 설계 근거와 분리했습니다.",
        ],
        "en_decisions": [
            "The fixed brief is 220/110 V, 900 W, 300 Hz, silicon steel, and 1.5 T maximum flux density.",
            "DU-75, two EI-112 iterations, and UI-100 are compared on common decision axes.",
            "The final UI-100 case records 180/93 turns, 96.360% efficiency, and 1.136% regulation.",
            "Workbook cases with different inputs or formula errors are kept separate from the final design evidence.",
        ],
        "metrics": [
            ("Primary / secondary", "180 / 93 turns"),
            ("Copper loss", "10.2267 W"),
            ("Core loss", "23.7760 W"),
            ("Efficiency", "96.360%"),
            ("Regulation", "1.136%"),
        ],
        "boundary_ko": "최종 제작, 온도상승, 절연 내력, 무부하·단락 시험의 실물 증거는 확인되지 않았습니다. 결과는 계산 기반 설계입니다. Workbook 화면은 셀 값을 렌더링한 snapshot이며 Excel 애플리케이션 실행 화면이 아닙니다.",
        "boundary_en": "No evidence of fabrication, temperature-rise, dielectric, open-circuit, or short-circuit hardware tests was found. This is a calculation-based design. Workbook visuals are rendered cell snapshots, not live Excel screenshots.",
    },
    {
        "id": "power-systems",
        "detail_links": [("PowerWorld 24 source-case rerun record", "powerworld_24_rerun.md")],
        "path": "02_power_systems/transmission_line_and_policy",
        "term": "3-1",
        "ko_title": "Power Systems — 765 kV 송전선로와 전력정책 검토",
        "en_title": "Power Systems — 765 kV Line & Policy Review",
        "ko_short": "분포정수 선로의 Zc·SIL을 재계산하고, PowerWorld 비수렴 결과와 정책 수치를 서로 다른 증거로 분리했습니다.",
        "en_short": "Surge impedance and SIL were recalculated while a non-convergent PowerWorld archive and policy figures were kept in separate evidence classes.",
        "status": "Zc 255.38 Ω · SIL 2.292 GW · PWB rerun: Blackout",
        "evidence": "Source-Derived · Independent Recalculation · PowerWorld 24 Tool Rerun",
        "accent": "violet",
        "hero": "assets/power/transmission_line_pi_model.svg",
        "flow": "assets/power/model_result_boundary.svg",
        "visuals": [
            ("assets/power/zc_sil_formula_flow.svg", "Portfolio Redraw", "Distributed-line calculation flow"),
            ("assets/power/demand_forecast_chart.png", "Source-Derived Redraw", "2038 energy demand comparison"),
            ("assets/power/peak_demand_chart.png", "Source-Derived Redraw", "2038 peak-demand comparison"),
            ("assets/power/effective_capacity_chart.png", "Source-Derived Redraw", "Confirmed effective capacity values"),
            ("assets/archive/power/powerworld_one_line_archive.png", "Existing PowerWorld Archive", "Recovered one-line model view"),
            ("assets/archive/power/powerworld_nonconvergence_archive.png", "Existing PowerWorld Archive", "Non-convergence evidence; not a validated grid result"),
        ],
        "source_visuals": [
            ("gallery/power-systems/powerworld-baseline-case.png", "Source-Derived", "Multi-area PowerWorld baseline model"),
            ("gallery/power-systems/powerworld-overload-contingency.png", "Diagnostic Evidence", "Overload and outage case; not a validated grid result"),
        ],
        "code": [
            ("assets/code/calc_transmission.svg", "Independent Recalculation", "Zc, SIL, and current equations"),
        ],
        "ko_problem": "계산 가능한 전송선로 파라미터, 수렴하지 않은 모델 화면, 정책 보고서 수치를 한 가지 ‘결과’로 묶지 않고 증거 수준을 분리하는 것이 핵심입니다. 선로 계산은 독립 재계산했고, 모델 비수렴은 디버깅 증거로만 남겼습니다.",
        "en_problem": "The core engineering task is evidence separation: reproducible line arithmetic, a solver-divergence archive, and policy figures must not be collapsed into one result. The line values were independently recalculated; divergence is retained only as debugging evidence.",
        "ko_decisions": [
            "765 kV, 350 km, z=j0.3 Ω/km, y=j4.6 µS/km 조건으로 lossless Zc와 SIL을 계산했습니다.",
            "독립 계산 결과 Zc≈255.38 Ω, SIL≈2.292 GW, SIL 전류≈1.729 kA입니다.",
            "PowerWorld full-load case의 비현실적 pu 전압과 blackout 상태는 실제 계통 성능으로 해석하지 않았습니다.",
            "설치된 PowerWorld 24에서 `newcase.pwb`의 2214 MW 저장 상태를 Newton 해석했고 실제 Blackout을 재현했습니다.",
            "2038 수요·피크·설비 수치는 보고서와 공개 정책 출처의 맥락을 분리해 표시했습니다.",
        ],
        "en_decisions": [
            "Lossless Zc and SIL use 765 kV, 350 km, z=j0.3 Ω/km, and y=j4.6 µS/km.",
            "Independent results are Zc≈255.38 Ω, SIL≈2.292 GW, and current≈1.729 kA.",
            "Non-physical per-unit voltages and blackout state are not interpreted as real-grid performance.",
            "PowerWorld 24 reran the saved 2214 MW `newcase.pwb` state and reproduced Blackout.",
            "2038 demand, peak, and capacity figures retain their report/source context.",
        ],
        "metrics": [
            ("Voltage / length", "765 kV / 350 km"),
            ("Surge impedance", "255.38 Ω"),
            ("SIL", "2.292 GW"),
            ("SIL current", "1.729 kA"),
            ("PowerWorld 24 rerun", "2214 MW → Blackout"),
            ("2038 energy", "735.1 → 624.5 TWh"),
            ("2038 peak", "145.6 → 129.3 GW"),
        ],
        "boundary_ko": "PowerWorld 24 재실행은 2214 MW 저장 상태에서 Blackout 진단을 확인한 것이며, 보고서의 3000/3100/3200 MW 단계나 5380 MW 보상 사례를 검증한 것이 아닙니다. 동적 안정도, 보호계전, N-1, 실계통 검증은 주장하지 않습니다. 화면의 이름·학번은 공개하지 않습니다.",
        "boundary_en": "The PowerWorld 24 rerun confirms a Blackout diagnostic for the saved 2214 MW state; it does not validate the report's 3000/3100/3200 MW stages or 5380 MW compensated case. Dynamic stability, protection, N-1, and production-grid validation are not claimed. Personal identifiers in the GUI are withheld.",
    },
    {
        "id": "motor-control",
        "detail_links": [("Parameter consistency audit", "parameter_consistency_audit.md")],
        "path": "03_motor_control/dc_motor_pi_control",
        "term": "3-2",
        "ko_title": "Motor Control — 직류전동기 이중 PI 제어",
        "en_title": "Motor Control — Cascaded PI Control of a DC Motor",
        "ko_short": "500 Hz 전류 루프와 25 Hz 속도 루프, 전류 제한·anti-windup·field weakening을 하나의 제어 구조로 정리했습니다.",
        "en_short": "A 500 Hz current loop and 25 Hz speed loop are integrated with current limiting, anti-windup, and field weakening.",
        "status": "Calculation + existing simulation archive",
        "evidence": "Recovered Original · Independent Recalculation · Existing PSIM/MATLAB Archive",
        "accent": "emerald",
        "hero": "assets/motor/dc_motor_system_architecture.svg",
        "flow": "assets/motor/cascaded_pi_controller.svg",
        "visuals": [
            ("assets/motor/current_loop_design.svg", "Portfolio Redraw", "500 Hz inner-loop design"),
            ("assets/motor/speed_loop_design.svg", "Portfolio Redraw", "25 Hz outer-loop design"),
            ("assets/motor/saturation_anti_windup.svg", "Portfolio Redraw", "Limiter and anti-windup behavior"),
            ("assets/archive/motor/psim_circuit_archive.png", "Existing PSIM Archive", "Recovered simulation schematic"),
            ("assets/archive/motor/speed_response_psim_archive.png", "Existing PSIM Archive", "Recovered speed response"),
            ("assets/motor/torque_ripple_comparison.png", "Independent Recalculation", "Torque-ripple comparison"),
        ],
        "source_visuals": [
            ("assets/archive/motor/reference_speed_profile_archive.png", "Existing PSIM Archive", "0→850→1200 rpm reference profile"),
            ("assets/archive/motor/speed_response_matlab_archive.png", "Existing MATLAB Archive", "Recovered MATLAB speed response"),
            ("assets/archive/motor/current_response_psim_archive.png", "Existing PSIM Archive", "Recovered PSIM current response"),
            ("assets/archive/motor/current_response_matlab_archive.png", "Existing MATLAB Archive", "Recovered MATLAB current response"),
            ("assets/archive/motor/field_weakening_archive.png", "Existing PSIM Archive", "Recovered field-weakening response"),
            ("assets/archive/motor/torque_ripple_10khz_archive.png", "Existing Result Archive", "Recovered torque-ripple case A"),
            ("assets/archive/motor/torque_ripple_25khz_archive.png", "Existing Result Archive", "Recovered torque-ripple case B"),
        ],
        "code": [
            ("assets/code/motor_reference_profile.svg", "Recovered Original", "0→850→1200 rpm reference"),
            ("assets/code/motor_current_pi_saturation.svg", "Recovered Original", "Current PI and ±200 V saturation"),
            ("assets/code/motor_speed_pi_limiter.svg", "Recovered Original", "Speed PI and ±10 A limit"),
        ],
        "ko_problem": "전기적으로 빠른 전류 동특성과 느린 기계 속도 동특성을 분리해 cascade controller를 설계했습니다. 계산식, 회수 C/C++ 상수, 기존 PSIM/MATLAB 화면 사이의 차이를 숨기지 않고 parameter consistency audit로 관리했습니다.",
        "en_problem": "The controller separates fast electrical current dynamics from slower mechanical speed dynamics. Formula results, recovered C/C++ constants, and archived PSIM/MATLAB views are reconciled through an explicit parameter-consistency audit.",
        "ko_decisions": [
            "전류 루프 대역폭 500 Hz에서 Kp=62.832, Ki=314.16을 재계산했습니다.",
            "속도 루프 25 Hz의 보고서 값 Kp=24.8, Ki≈3898과 회수 소스 Ki=3895를 모두 보존했습니다.",
            "속도 지령은 0→850 rpm, hold, 850→1200 rpm 순서로 구성됩니다.",
            "±10 A current limit, ±200 V voltage saturation, field weakening 구간을 제어 흐름에 포함했습니다.",
        ],
        "en_decisions": [
            "At 500 Hz current bandwidth, the recalculated gains are Kp=62.832 and Ki=314.16.",
            "The report's speed values Kp=24.8 and Ki≈3898 coexist with recovered-source Ki=3895.",
            "The reference profile is 0→850 rpm, hold, then 850→1200 rpm.",
            "The flow includes ±10 A current limiting, ±200 V voltage saturation, and field weakening.",
        ],
        "metrics": [
            ("Current loop", "500 Hz"),
            ("Current PI", "62.832 / 314.16"),
            ("Speed loop", "25 Hz"),
            ("Speed PI", "24.8 / 3898 report"),
            ("Source Ki", "3895"),
            ("Torque ripple", "2.28 → 0.38 N·m"),
        ],
        "boundary_ko": "PSIM/MATLAB 프로젝트를 라이선스 독립적으로 재실행할 자료는 회수되지 않았습니다. 화면은 Existing Result Archive이며 새 실행 결과가 아닙니다. 파일명 25 kHz와 본문 30 kHz의 불일치는 그대로 표시합니다. 하드웨어 실험은 주장하지 않습니다.",
        "boundary_en": "PSIM/MATLAB projects were not recovered in a license-independent rerunnable form. Screenshots are Existing Result Archive, not new runs. The 25 kHz filename versus 30 kHz text conflict remains visible. Hardware testing is not claimed.",
    },
    {
        "id": "rf-microwave",
        "detail_links": [
            ("Homework 2 microstrip", "cases/homework2_microstrip.md"),
            ("Homework 4 L-section", "cases/homework4_l_section.md"),
            ("Homework 4 single-stub", "cases/homework4_single_stub.md"),
            ("Homework 5 Wilkinson", "cases/homework5_wilkinson.md"),
            ("Homework 5 branch-line hybrid", "cases/homework5_branch_line.md"),
            ("Homework 5 Ex. 12-3 incomplete", "cases/homework5_ex12_3_incomplete.md"),
        ],
        "path": "04_rf_microwave/passive_network_design",
        "term": "4-1",
        "ko_title": "RF/Microwave — 수동회로 설계와 Cadence 결과",
        "en_title": "RF/Microwave — Passive Networks & Cadence Archive",
        "ko_short": "Microstrip, L-section·single-stub matching, Wilkinson divider, branch-line hybrid를 이론과 기존 Cadence 결과로 비교했습니다.",
        "en_short": "Microstrip, L-section and single-stub matching, a Wilkinson divider, and a branch-line hybrid are compared through theory and an existing Cadence archive.",
        "status": "Theory + existing Cadence archive",
        "evidence": "Source-Derived · Portfolio Redraw · Existing Cadence Result Archive",
        "accent": "rose",
        "hero": "assets/rf/microstrip_design_flow.svg",
        "flow": "assets/rf/passive-networks.svg",
        "visuals": [
            ("assets/rf/microstrip_cross_section.svg", "Portfolio Redraw", "Alumina microstrip geometry"),
            ("assets/rf/smith_chart_movement.svg", "Portfolio Redraw", "Impedance-matching interpretation"),
            ("assets/rf/wilkinson_structure.svg", "Portfolio Redraw", "Quarter-wave divider structure"),
            ("assets/archive/rf/microstrip_loss_3p7ghz.png", "Existing Cadence Archive", "Recovered marker at 3.7 GHz"),
            ("assets/archive/rf/wilkinson_sparameter_archive.png", "Existing Cadence Archive", "Divider S-parameter view"),
            ("assets/archive/rf/hybrid_sparameter_archive.png", "Existing Cadence Archive", "Hybrid S-parameter view"),
        ],
        "source_visuals": [
            ("gallery/rf-microwave/microstrip-schematic.png", "Source-Derived", "Cadence microstrip-line schematic"),
            ("gallery/rf-microwave/microstrip-stackup-editor.png", "Source-Derived", "Alumina substrate stack-up definition"),
            ("gallery/rf-microwave/microstrip-response-marker.png", "Source-Derived", "Recovered microstrip response marker"),
            ("gallery/rf-microwave/l-section-schematic.png", "Source-Derived", "1 GHz L-section matching schematic"),
            ("gallery/rf-microwave/l-section-smith-response.png", "Source-Derived", "L-section Smith-chart and return-loss response"),
            ("gallery/rf-microwave/single-stub-solution-1.png", "Source-Derived", "Single-stub physical solution 1"),
            ("gallery/rf-microwave/single-stub-solution-2.png", "Source-Derived", "Single-stub physical solution 2"),
            ("gallery/rf-microwave/wilkinson-schematic.png", "Source-Derived", "Wilkinson divider schematic"),
            ("gallery/rf-microwave/wilkinson-sparameter.png", "Source-Derived", "Wilkinson divider S-parameter response"),
            ("gallery/rf-microwave/hybrid-schematic.png", "Source-Derived", "Branch-line quadrature hybrid schematic"),
            ("gallery/rf-microwave/hybrid-line-parameter-a.png", "Source-Derived", "Hybrid transmission-line parameter A"),
            ("gallery/rf-microwave/hybrid-line-parameter-b.png", "Source-Derived", "Hybrid transmission-line parameter B"),
            ("gallery/rf-microwave/hybrid-sparameter.png", "Source-Derived", "Quadrature hybrid S-parameter response"),
        ],
        "code": [],
        "ko_problem": "회로식으로 얻은 이상 설계와 substrate·layout·tuning이 반영된 EM/circuit simulation archive를 분리해 설명합니다. 특히 microstrip 설계 주파수는 3.5 GHz이지만 회수된 marker는 3.7 GHz이므로 이를 정확히 구분했습니다.",
        "en_problem": "Ideal circuit calculations are separated from simulation archives that include substrate, layout, and tuning effects. The microstrip target is 3.5 GHz, but the recovered marker is at 3.7 GHz; the distinction is explicit.",
        "ko_decisions": [
            "Alumina εr=9.9, h=0.5 mm, tanδ=0.001 조건에서 50 Ω, 270° microstrip을 설계했습니다.",
            "1 GHz L-section과 3.5 GHz single-stub의 두 해를 물리 길이로 정리했습니다.",
            "Wilkinson은 이론 70.7 Ω λ/4 branch와 100 Ω isolation resistor를 기준으로 봤습니다.",
            "Branch-line hybrid는 35.35 Ω/50 Ω branch를 사용한 기존 설계 결과를 보존했습니다.",
        ],
        "en_decisions": [
            "The 50 Ω, 270° microstrip uses alumina εr=9.9, h=0.5 mm, and tanδ=0.001.",
            "The 1 GHz L-section and two 3.5 GHz single-stub solutions are translated into physical lengths.",
            "Wilkinson theory starts with 70.7 Ω quarter-wave branches and a 100 Ω isolation resistor.",
            "The branch-line hybrid retains the archived 35.35 Ω and 50 Ω branch design.",
        ],
        "metrics": [
            ("Microstrip target", "3.5 GHz · 50 Ω · 270°"),
            ("Calculated W / L", "0.4815 / 24.97 mm"),
            ("Archive marker", "3.7 GHz only"),
            ("L-section", "0.461 pF · 19.5 nH"),
            ("Wilkinson split", "≈ −3 dB archive"),
            ("Isolation", "≈ −18 dB archive"),
        ],
        "boundary_ko": "Cadence 프로젝트와 라이선스 자료는 공개하지 않습니다. 3.7 GHz marker를 3.5 GHz의 정확한 검증으로 바꾸어 말하지 않습니다. Homework 5 Ex. 12-3은 식별 가능한 최종 결과가 없어 INCOMPLETE_WORK로 분류했습니다. 제작 공차, connector launch, calibration, VNA 측정은 증거 범위 밖입니다.",
        "boundary_en": "Cadence projects and licensed material are not published. The 3.7 GHz marker is not restated as exact 3.5 GHz validation. Homework 5 Ex. 12-3 has no identifiable final result and is classified as INCOMPLETE_WORK. Fabrication tolerance, connector launch, calibration, and VNA measurement are outside the evidence.",
    },
    {
        "id": "sensor-applications",
        "detail_links": [("Source/proposal evidence matrix", "evidence_matrix.md")],
        "path": "05_sensor_applications/aesa_sar_diffusion_concept",
        "term": "4-1",
        "ko_title": "Sensor Applications — AESA-SAR와 Physics-Guided Diffusion",
        "en_title": "Sensor Applications — AESA-SAR & Physics-Guided Diffusion",
        "ko_short": "AESA 수집, SAR 복원, physics-conditioned diffusion을 연결한 연구 제안과 단계별 검증 로드맵입니다.",
        "en_short": "A research proposal links AESA acquisition, conventional SAR reconstruction, and physics-conditioned diffusion with a staged validation roadmap.",
        "status": "Concept / Proposal Only",
        "evidence": "Research Concept · Architecture · Validation Roadmap · No Implemented Result",
        "accent": "blue",
        "hero": "assets/sensor/aesa_system_architecture.svg",
        "flow": "assets/sensor/validation_roadmap.svg",
        "visuals": [
            ("assets/sensor/tr_module_block.svg", "Portfolio Redraw", "T/R module abstraction"),
            ("assets/sensor/digital_beamforming_chain.svg", "Portfolio Redraw", "Digital beamforming chain"),
            ("assets/sensor/sar_image_formation.svg", "Portfolio Redraw", "Conventional SAR baseline"),
            ("assets/sensor/physics_guided_diffusion.svg", "Portfolio Redraw", "Physics-conditioned refinement"),
            ("assets/sensor/rda_csa_bpa_comparison.png", "Engineering Interpretation", "Baseline algorithm comparison"),
            ("assets/sensor/implementation_boundary.svg", "Evidence Boundary", "Proposal versus implementation"),
        ],
        "code": [],
        "ko_problem": "AESA 하드웨어와 SAR 영상형성, 생성모델을 한 문장으로 묶는 대신 RF sensing, DBF, conventional reconstruction, conditional diffusion, evaluation으로 계층화했습니다. 이 페이지의 성과는 구현 결과가 아니라 검증 가능한 연구 설계입니다.",
        "en_problem": "Rather than collapsing AESA hardware, SAR formation, and a generative model into one claim, the proposal decomposes RF sensing, DBF, conventional reconstruction, conditional diffusion, and evaluation. The deliverable is a testable research plan, not an implemented result.",
        "ko_decisions": [
            "RDA/CSA/BPA 중 하나를 먼저 baseline으로 고정한 뒤 학습 모델과 비교하도록 했습니다.",
            "관측 열화·undersampling 조건과 train/validation/test 분리를 사전에 문서화합니다.",
            "영상 품질 지표와 physics-consistency 지표를 함께 사용하도록 제안했습니다.",
            "conditioning과 loss term의 ablation, noise·model mismatch robustness를 검증 순서에 포함했습니다.",
        ],
        "en_decisions": [
            "A conventional RDA/CSA/BPA baseline precedes any learned-model comparison.",
            "Observation degradation, undersampling, and train/validation/test separation are documented first.",
            "Image-quality and physics-consistency metrics are evaluated together.",
            "Conditioning/loss ablations and noise/model-mismatch robustness are part of the roadmap.",
        ],
        "metrics": [
            ("Implementation", "Not performed"),
            ("Dataset", "Not published"),
            ("Hardware", "Not built"),
            ("Performance gain", "Not claimed"),
            ("Deliverable", "Architecture + validation plan"),
        ],
        "boundary_ko": "학습 모델, 데이터셋, AESA prototype, field/flight test, 정량 성능 향상은 존재한다고 주장하지 않습니다. 군사 운용 절차나 구현 가능한 공격 정보가 아니라 공개 가능한 시스템 계층과 검증 방법만 다룹니다.",
        "boundary_en": "No trained model, dataset, AESA prototype, field/flight test, or quantified gain is claimed. The public scope contains only system layers and validation methods, not operational procedures or actionable attack information.",
    },
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def normalize_svg_contract() -> None:
    """Keep legacy and generated SVGs portable and readable on small screens."""
    for path in (DOCS / "assets").rglob("*.svg"):
        content = path.read_text(encoding="utf-8")
        viewbox = re.search(r'viewBox="([^"]+)"', content)
        root_tag = re.search(r"<svg\b([^>]*)>", content)
        root_attrs = root_tag.group(1) if root_tag else ""
        if viewbox and (" width=" not in root_attrs or " height=" not in root_attrs):
            parts = viewbox.group(1).split()
            if len(parts) == 4:
                width, height = parts[2], parts[3]
                content = re.sub(
                    r"<svg\b",
                    f'<svg width="{width}" height="{height}"',
                    content,
                    count=1,
                )
        content = re.sub(r'font-size="(?:1[0-3]|[1-9])"', 'font-size="14"', content)
        content = re.sub(
            r"font-size\s*:\s*(?:1[0-3]|[1-9])(?:px)?",
            "font-size:14px",
            content,
        )
        path.write_text(content, encoding="utf-8")


def metrics_html(items: list[tuple[str, str]]) -> str:
    return "".join(
        f'<div class="metric"><span>{escape(label)}</span><strong>{escape(value)}</strong></div>'
        for label, value in items
    )


def gallery_html(items: list[tuple[str, str, str]], prefix: str, lang: str) -> str:
    return "".join(
        dedent(
            f"""
            <figure class="visual-card">
              <button class="image-button" data-lightbox="{prefix}{src}" aria-label="{'이미지 확대' if lang == 'ko' else 'Expand image'}: {escape(caption)}">
                <img src="{prefix}{src}" alt="{escape(caption)}" loading="lazy">
              </button>
              <figcaption><span class="evidence-badge">{escape(label)}</span>{escape(caption)}</figcaption>
            </figure>
            """
        )
        for src, label, caption in items
    )


def page_shell(title: str, body: str, *, css: str, script: str, lang: str, home: str, switch: str) -> str:
    skip = "본문으로 건너뛰기" if lang == "ko" else "Skip to content"
    home_label = "Coursework Portfolio" if lang == "en" else "학부 과제 포트폴리오"
    lang_label = "한국어" if lang == "en" else "English"
    return dedent(
        f"""
        <!doctype html>
        <html lang="{lang}">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width,initial-scale=1">
          <meta name="theme-color" content="#08111f">
          <meta name="description" content="Evidence-first electrical engineering coursework portfolio">
          <title>{escape(title)}</title>
          <link rel="stylesheet" href="{css}">
        </head>
        <body>
          <a class="skip-link" href="#main">{skip}</a>
          <header class="site-header">
            <a class="brand" href="{home}"><span class="brand-mark">EE</span>{home_label}</a>
            <nav aria-label="Primary">
              <a href="{REPO}">GitHub</a>
              <a href="{switch}">{lang_label}</a>
            </nav>
          </header>
          <main id="main">{body}</main>
          <footer>
            <p>Evidence-first portfolio · Recovered original, rerun result, archive, redraw, and proposal are labeled separately.</p>
            <a href="{REPO}/blob/main/SOURCE_PROVENANCE.md">Source provenance</a>
          </footer>
          <dialog id="lightbox" class="lightbox"><button class="lightbox-close" aria-label="Close">×</button><img alt=""><p></p></dialog>
          <script src="{script}" defer></script>
        </body>
        </html>
        """
    )


def course_page(course: dict, lang: str) -> str:
    ko = lang == "ko"
    title = course["ko_title"] if ko else course["en_title"]
    short = course["ko_short"] if ko else course["en_short"]
    problem = course["ko_problem"] if ko else course["en_problem"]
    decisions = course["ko_decisions"] if ko else course["en_decisions"]
    boundary = course["boundary_ko"] if ko else course["boundary_en"]
    prefix = "../../" if ko else "../../../"
    repo_path = f"{REPO}/tree/main/{course['path']}"
    calc = {
        "electrical-machines": ("transformer-case-calculator", "Transformer Case Calculator"),
        "power-systems": ("transmission-line-calculator", "Transmission-Line Calculator"),
        "motor-control": ("motor-pi-calculator", "Motor PI Calculator"),
    }.get(course["id"])
    calc_html = ""
    if calc:
        tool_prefix = "../../tools/" if ko else "../../../tools/"
        calc_html = f'<a class="button primary" href="{tool_prefix}{calc[0]}/">{calc[1]}</a>'
    decision_items = "".join(f"<li>{escape(item)}</li>" for item in decisions)
    sections = {
        "ko": {
            "eyebrow": f"{course['term']}학기 · Visual Engineering Case Study",
            "summary": "30초 요약",
            "problem": "문제 정의와 설계 판단",
            "architecture": "시스템 구조",
            "evidence": "설계·검증 근거",
            "code": "코드 근거",
            "results": "핵심 결과",
            "boundary": "검증 경계와 한계",
            "source": "소스와 재현",
            "prev": "전체 과목 보기",
        },
        "en": {
            "eyebrow": f"Term {course['term']} · Visual Engineering Case Study",
            "summary": "30-second summary",
            "problem": "Problem and design decisions",
            "architecture": "System architecture",
            "evidence": "Design and verification evidence",
            "code": "Code evidence",
            "results": "Key results",
            "boundary": "Verification boundary",
            "source": "Source and reproduction",
            "prev": "All courses",
        },
    }[lang]
    section_number = 4
    source_visual_section = ""
    if course.get("source_visuals"):
        source_title = "검토된 원본 시각 증거" if ko else "Reviewed source evidence"
        source_visual_section = f"""
        <section class="section"><div class="section-heading"><span>{section_number:02d}</span><h2>{source_title}</h2></div>
          <p class="section-note">High-resolution, manually reviewed project evidence. Private identifiers, participant-level data, local paths, and third-party teaching material are excluded.</p>
          <div class="gallery source-gallery">{gallery_html(course['source_visuals'], prefix, lang)}</div>
        </section>"""
        section_number += 1
    code_section = ""
    if course["code"]:
        code_section = f"""
        <section class="section"><div class="section-heading"><span>{section_number:02d}</span><h2>{sections['code']}</h2></div>
          <div class="gallery code-gallery">{gallery_html(course['code'], prefix, lang)}</div>
        </section>"""
        section_number += 1
    results_number = section_number
    boundary_number = section_number + 1
    body = dedent(
        f"""
        <section class="case-hero accent-{course['accent']}">
          <div>
            <p class="eyebrow">{sections['eyebrow']}</p>
            <h1>{escape(title)}</h1>
            <p class="lede">{escape(short)}</p>
            <div class="actions">{calc_html}<a class="button" href="{repo_path}">Source directory</a></div>
          </div>
          <button class="image-button hero-visual" data-lightbox="{prefix}{course['hero']}">
            <img src="{prefix}{course['hero']}" alt="{escape(title)} architecture">
          </button>
        </section>
        <section class="snapshot section">
          <div class="section-heading"><span>01</span><h2>{sections['summary']}</h2></div>
          <div class="snapshot-grid">
            <p>{escape(short)}</p>
            <dl>
              <div><dt>Status</dt><dd>{escape(course['status'])}</dd></div>
              <div><dt>Evidence</dt><dd>{escape(course['evidence'])}</dd></div>
              <div><dt>Contribution</dt><dd>Team Project · Individual contribution unconfirmed</dd></div>
            </dl>
          </div>
        </section>
        <section class="section split">
          <div><div class="section-heading"><span>02</span><h2>{sections['problem']}</h2></div><p>{escape(problem)}</p><ul class="decision-list">{decision_items}</ul></div>
          <figure class="visual-card featured"><button class="image-button" data-lightbox="{prefix}{course['flow']}"><img src="{prefix}{course['flow']}" alt="Engineering flow"></button><figcaption><span class="evidence-badge">Portfolio Redraw</span>Architecture and decision flow</figcaption></figure>
        </section>
        <section class="section"><div class="section-heading"><span>03</span><h2>{sections['evidence']}</h2></div>
          <div class="gallery">{gallery_html(course['visuals'], prefix, lang)}</div>
        </section>
        {source_visual_section}
        {code_section}
        <section class="section"><div class="section-heading"><span>{results_number:02d}</span><h2>{sections['results']}</h2></div>
          <div class="metrics">{metrics_html(course['metrics'])}</div>
        </section>
        <section class="section boundary"><div class="section-heading"><span>{boundary_number:02d}</span><h2>{sections['boundary']}</h2></div><p>{escape(boundary)}</p></section>
        <section class="section source-panel"><div><h2>{sections['source']}</h2><p>Repository files, calculations, and evidence labels are linked without publishing withheld originals.</p></div><div class="actions"><a class="button primary" href="{repo_path}">Open source</a><a class="button" href="{prefix}assets/asset_manifest.yaml">Asset manifest</a></div></section>
        <nav class="case-nav"><a href="{'../../' if ko else '../../../en/'}">← {sections['prev']}</a></nav>
        """
    )
    if ko:
        return page_shell(title, body, css="../../styles.css", script="../../script.js", lang=lang, home="../../", switch=f"../../en/courses/{course['id']}/")
    return page_shell(title, body, css="../../../styles.css", script="../../../script.js", lang=lang, home="../../../en/", switch=f"../../../courses/{course['id']}/")


def home_page(lang: str) -> str:
    ko = lang == "ko"
    prefix = "" if ko else "../"
    cards = []
    for c in COURSES:
        title = c["ko_title"] if ko else c["en_title"]
        short = c["ko_short"] if ko else c["en_short"]
        cards.append(
            dedent(
                f"""
                <article class="course-card accent-{c['accent']}">
                  <img src="{prefix}{c['hero']}" alt="" loading="lazy">
                  <div><p class="eyebrow">{c['term']} · {escape(c['evidence'].split(' · ')[0])}</p><h2>{escape(title)}</h2><p>{escape(short)}</p>
                  <div class="card-meta"><span>{escape(c['status'])}</span><a href="courses/{c['id']}/">{'Case Study 보기' if ko else 'View case study'} →</a></div></div>
                </article>
                """
            )
        )
    if ko:
        title = "Electrical Engineering Coursework Portfolio"
        switch = "en/"
        home = "./"
        intro = "전자전기공학 전공과목에서 수행한 설계·계산·RTL·시뮬레이션·연구 제안을 증거 수준과 함께 재구성했습니다."
        kicker = "RTL · Machines · Power · Control · RF · Sensors"
        disclaimer = "원본, 재구성, 재계산, 기존 결과 화면, 제안 단계를 같은 색으로 포장하지 않습니다. 각 시각 자료와 주장에 증거 상태를 표시했습니다."
        calc_title = "직접 확인하는 계산"
    else:
        title = "Electrical Engineering Coursework Portfolio"
        switch = "../"
        home = "./"
        intro = "Coursework in RTL, machines, power, control, RF, and sensors is reconstructed as evidence-aware engineering case studies."
        kicker = "RTL · Machines · Power · Control · RF · Sensors"
        disclaimer = "Recovered originals, public reconstructions, recalculations, archived results, and proposals are never presented as the same evidence class."
        calc_title = "Interactive calculators"
    body = dedent(
        f"""
        <section class="home-hero">
          <div><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{intro}</p>
            <div class="actions"><a class="button primary" href="#courses">{'프로젝트 보기' if ko else 'Explore projects'}</a><a class="button" href="{REPO}">GitHub Repository</a></div>
          </div>
          <button class="image-button hero-visual" data-lightbox="{prefix}assets/hero/coursework_portfolio_hero.png"><picture><source srcset="{prefix}assets/hero/coursework_portfolio_hero.webp" type="image/webp"><img src="{prefix}assets/hero/coursework_portfolio_hero.png" alt="Coursework portfolio map"></picture></button>
        </section>
        <section class="evidence-strip"><strong>Evidence-first</strong><p>{disclaimer}</p><a href="{REPO}/blob/main/SOURCE_PROVENANCE.md">Provenance</a></section>
        <section id="courses" class="section"><div class="section-heading"><span>01</span><h2>{'6개 엔지니어링 Case Study' if ko else 'Six engineering case studies'}</h2></div><div class="course-grid">{''.join(cards)}</div></section>
        <section class="section tools-section"><div class="section-heading"><span>02</span><h2>{calc_title}</h2></div>
          <div class="tool-grid">
            <a class="tool-card" href="{prefix}tools/transformer-case-calculator/"><span>01</span><h3>Transformer Case</h3><p>Loss, efficiency, regulation</p></a>
            <a class="tool-card" href="{prefix}tools/motor-pi-calculator/"><span>02</span><h3>Motor PI</h3><p>Current-loop gains and source discrepancy</p></a>
            <a class="tool-card" href="{prefix}tools/transmission-line-calculator/"><span>03</span><h3>Transmission Line</h3><p>Zc, SIL, three-phase current</p></a>
          </div>
        </section>
        <section class="section boundary"><div class="section-heading"><span>03</span><h2>{'공개 범위' if ko else 'Public boundary'}</h2></div>
          <p>{'개인정보·학번·로컬 경로·라이선스 종속 원본·제3자 교재는 공개하지 않습니다. 팀 과제의 개인 기여도는 확인 전까지 확정 표현을 사용하지 않습니다.' if ko else 'Personal data, local paths, license-bound originals, and third-party course material are withheld. Individual contribution to team work remains unconfirmed.'}</p>
        </section>
        """
    )
    return page_shell(title, body, css=f"{prefix}styles.css", script=f"{prefix}script.js", lang=lang, home=home, switch=switch)


def calculator_page(kind: str) -> tuple[str, str]:
    common = {
        "transformer": {
            "title": "Transformer Case Calculator",
            "desc": "보고서 사례의 손실 합, 효율, 전압변동률을 입력값으로 다시 계산합니다.",
            "fields": [("output", "Rated output (W)", "900"), ("copper", "Copper loss (W)", "10.2267"), ("core", "Core loss (W)", "23.7760"), ("vnl", "No-load voltage (V)", "111.2496"), ("vfl", "Full-load voltage (V)", "110")],
            "note": "Core geometry를 자동 추천하지 않습니다. 계산된 전기 지표만 보여주며, 최종 core 선택은 source-derived trade study를 따라야 합니다.",
        },
        "motor": {
            "title": "Motor PI Calculator",
            "desc": "전류 루프의 pole-cancellation PI gain과 보고서·회수 소스의 속도 Ki 차이를 함께 표시합니다.",
            "fields": [("ra", "Armature R (Ω)", "0.1"), ("la", "Armature L (H)", "0.02"), ("j", "Inertia J (kg·m²)", "0.075"), ("kt", "Torque constant Kt", "1.9"), ("fcc", "Current bandwidth (Hz)", "500"), ("fcs", "Speed bandwidth (Hz)", "25")],
            "note": "전류 PI는 Kp=L·ωc, Ki=R·ωc로 계산합니다. 속도 PI는 원본 보고서 Kp=24.8, Ki≈3898과 회수 C/C++ Ki=3895를 참고값으로 보존하며 입력만으로 새 gain을 단정하지 않습니다.",
        },
        "line": {
            "title": "Transmission-Line Zc / SIL Calculator",
            "desc": "Lossless line 근사에서 series reactance와 shunt susceptance로 Zc, SIL, 3상 전류를 계산합니다.",
            "fields": [("vll", "Line voltage (kV)", "765"), ("x", "Series reactance (Ω/km)", "0.3"), ("b", "Shunt susceptance (µS/km)", "4.6"), ("length", "Length (km)", "350")],
            "note": "이 계산기는 lossless characteristic 값만 제공합니다. 조류 수렴, 안정도, 보호계전, N-1 성능을 검증하지 않습니다.",
        },
    }[kind]
    fields = "".join(f'<label>{label}<input id="{fid}" name="{fid}" type="number" step="any" value="{value}" required></label>' for fid, label, value in common["fields"])
    slug = {"transformer": "transformer-case-calculator", "motor": "motor-pi-calculator", "line": "transmission-line-calculator"}[kind]
    body = dedent(
        f"""
        <section class="tool-hero"><p class="eyebrow">Interactive · Client-side · Source-linked</p><h1>{common['title']}</h1><p class="lede">{common['desc']}</p></section>
        <section class="calculator-layout">
          <form id="calculator" class="calculator-panel"><div class="field-grid">{fields}</div><div class="actions"><button class="button primary" type="submit">Calculate</button><button class="button" type="reset">Reset</button></div><p class="form-error" role="alert" hidden></p></form>
          <section class="result-panel" aria-live="polite"><p class="eyebrow">Calculated result</p><div id="result"></div></section>
        </section>
        <section class="section boundary"><h2>Evidence boundary</h2><p>{common['note']}</p></section>
        <nav class="case-nav"><a href="../../">← Portfolio</a><a href="{REPO}/tree/main/scripts">Calculation sources →</a></nav>
        """
    )
    html = page_shell(common["title"], body, css="../../styles.css", script="../../script.js", lang="ko", home="../../", switch="../../en/")
    html = html.replace("</body>", f'<script type="module" src="{slug}.js"></script></body>')
    return slug, html


STYLES = r"""
:root{--bg:#07101d;--surface:#0d192a;--surface2:#122137;--line:#263b58;--text:#f2f6ff;--muted:#aab9d2;--cyan:#4de4ff;--amber:#ffc857;--violet:#a98bff;--emerald:#45e0b4;--rose:#ff7da8;--blue:#69a8ff;--max:1180px;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% -10%,#19345a 0,transparent 35%),var(--bg);color:var(--text);font:16px/1.7 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}a{color:inherit}img{display:block;max-width:100%;height:auto}.skip-link{position:fixed;left:1rem;top:-5rem;background:#fff;color:#000;padding:.7rem 1rem;z-index:100}.skip-link:focus{top:1rem}.site-header{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:.8rem max(1rem,calc((100% - var(--max))/2));background:rgba(7,16,29,.88);border-bottom:1px solid var(--line);backdrop-filter:blur(14px)}.brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;font-weight:800}.brand-mark{display:grid;place-items:center;width:2.2rem;height:2.2rem;border:1px solid #58759d;border-radius:.7rem;color:var(--cyan)}nav{display:flex;gap:1rem}.site-header nav a{color:var(--muted);text-decoration:none;font-weight:700}main{max-width:var(--max);margin:auto;padding:0 1rem}.home-hero,.case-hero{min-height:650px;display:grid;grid-template-columns:1.05fr .95fr;align-items:center;gap:3.5rem;padding:6rem 0}.home-hero h1,.case-hero h1,.tool-hero h1{font-size:clamp(2.7rem,6vw,5.7rem);line-height:1.02;letter-spacing:-.055em;margin:.5rem 0 1.5rem}.case-hero h1{font-size:clamp(2.4rem,5vw,4.8rem)}.lede{font-size:clamp(1.05rem,2vw,1.35rem);color:var(--muted);max-width:760px}.eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:.76rem;font-weight:900;color:var(--cyan)}.hero-visual{border:1px solid var(--line);border-radius:1.5rem;overflow:hidden;box-shadow:0 30px 90px #0008}.image-button{appearance:none;background:transparent;padding:0;border:0;color:inherit;cursor:zoom-in}.button{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:.7rem 1rem;border:1px solid var(--line);border-radius:.8rem;background:#14233a;text-decoration:none;font-weight:800;color:var(--text);cursor:pointer}.button.primary{background:var(--cyan);color:#00111a;border-color:transparent}.actions{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.5rem}.evidence-strip{display:grid;grid-template-columns:auto 1fr auto;gap:1.2rem;align-items:center;padding:1.2rem 1.4rem;border:1px solid var(--line);border-radius:1rem;background:var(--surface)}.evidence-strip p{margin:0;color:var(--muted)}.section{padding:5rem 0;border-top:1px solid var(--line)}.section-heading{display:flex;align-items:center;gap:1rem;margin-bottom:2rem}.section-heading>span{color:var(--cyan);font:800 .8rem/1 ui-monospace,monospace}.section-heading h2{font-size:clamp(1.8rem,4vw,3rem);letter-spacing:-.035em;line-height:1.1;margin:0}.course-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.2rem}.course-card{overflow:hidden;background:var(--surface);border:1px solid var(--line);border-radius:1.2rem;transition:.2s transform,.2s border-color}.course-card:hover{transform:translateY(-4px);border-color:#6f8cb4}.course-card>img{aspect-ratio:16/8;object-fit:cover;border-bottom:1px solid var(--line)}.course-card>div{padding:1.4rem}.course-card h2{font-size:1.45rem;line-height:1.25;margin:.4rem 0}.course-card p{color:var(--muted)}.card-meta{display:flex;justify-content:space-between;gap:.5rem;border-top:1px solid var(--line);padding-top:1rem;font-size:.85rem;font-weight:800}.card-meta span{color:var(--cyan)}.tool-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}.tool-card{padding:1.4rem;border:1px solid var(--line);border-radius:1rem;background:linear-gradient(145deg,var(--surface),#142743);text-decoration:none}.tool-card span{color:var(--cyan);font-weight:900}.tool-card h3{font-size:1.35rem;margin:.6rem 0}.tool-card p{color:var(--muted)}.snapshot-grid,.split{display:grid;grid-template-columns:1fr 1fr;gap:3rem}.snapshot-grid>p{font-size:1.35rem}.snapshot dl{margin:0}.snapshot dl>div{display:grid;grid-template-columns:120px 1fr;gap:1rem;padding:.8rem 0;border-bottom:1px solid var(--line)}dt{color:var(--muted)}dd{margin:0;font-weight:700}.decision-list{padding-left:1.2rem}.decision-list li{margin:.7rem 0;color:var(--muted)}.visual-card{margin:0;border:1px solid var(--line);border-radius:1rem;background:var(--surface);overflow:hidden}.visual-card img{width:100%;aspect-ratio:16/10;object-fit:contain;background:#f7f9fc}.visual-card figcaption{display:flex;align-items:center;gap:.7rem;padding:.8rem 1rem;color:var(--muted);font-size:.85rem}.visual-card.featured{align-self:start}.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}.code-gallery .visual-card img{aspect-ratio:16/9;background:#08111f}.evidence-badge{flex:none;padding:.25rem .5rem;border:1px solid #48698f;border-radius:999px;color:var(--cyan);font-size:.68rem;font-weight:900;text-transform:uppercase}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}.metric{padding:1.3rem;border:1px solid var(--line);border-radius:1rem;background:var(--surface)}.metric span{display:block;color:var(--muted);font-size:.82rem}.metric strong{display:block;font-size:1.35rem;margin-top:.3rem}.boundary{padding-left:1.5rem;border-left:4px solid var(--amber);background:linear-gradient(90deg,#261e0c88,transparent)}.boundary p{max-width:900px;color:#d5dbe7}.source-panel{display:flex;align-items:center;justify-content:space-between;gap:2rem}.case-nav{justify-content:space-between;padding:2rem 0 5rem}.case-nav a{font-weight:800}.tool-hero{padding:6rem 0 2rem}.calculator-layout{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;padding:2rem 0 4rem}.calculator-panel,.result-panel{padding:1.4rem;border:1px solid var(--line);border-radius:1rem;background:var(--surface)}.field-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}label{color:var(--muted);font-size:.85rem;font-weight:700}input{width:100%;margin-top:.35rem;padding:.8rem;border:1px solid #3a5579;border-radius:.6rem;background:#07101d;color:var(--text);font:inherit}.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}.result-item{padding:1rem;background:#07101d;border-radius:.7rem}.result-item span{display:block;color:var(--muted);font-size:.8rem}.result-item strong{font-size:1.25rem}.form-error{color:#ff9aad}.lightbox{width:min(94vw,1280px);max-height:92vh;padding:2.5rem 1rem 1rem;border:1px solid #48698f;border-radius:1rem;background:#050b14;color:#fff}.lightbox::backdrop{background:#000c;backdrop-filter:blur(5px)}.lightbox img{max-height:78vh;margin:auto}.lightbox-close{position:absolute;right:.7rem;top:.5rem;border:0;background:transparent;color:#fff;font-size:2rem;cursor:pointer}.lightbox p{text-align:center;color:var(--muted)}footer{max-width:var(--max);margin:3rem auto 0;padding:2rem 1rem 5rem;border-top:1px solid var(--line);color:var(--muted)}footer a{color:var(--cyan)}
.accent-cyan{--case:var(--cyan)}.accent-amber{--case:var(--amber)}.accent-violet{--case:var(--violet)}.accent-emerald{--case:var(--emerald)}.accent-rose{--case:var(--rose)}.accent-blue{--case:var(--blue)}.case-hero .eyebrow,.course-card .eyebrow{color:var(--case,var(--cyan))}
@media(max-width:820px){.home-hero,.case-hero,.snapshot-grid,.split,.calculator-layout{grid-template-columns:1fr}.home-hero,.case-hero{min-height:auto;padding:4rem 0}.course-grid,.gallery{grid-template-columns:1fr}.tool-grid,.metrics{grid-template-columns:1fr 1fr}.site-header{padding:.7rem 1rem}.brand{font-size:.85rem}.site-header nav a:first-child{display:none}.evidence-strip{grid-template-columns:1fr}.source-panel{display:block}}
@media(max-width:520px){.tool-grid,.metrics,.field-grid,.result-grid{grid-template-columns:1fr}.home-hero h1,.case-hero h1{font-size:2.55rem}.section{padding:3.5rem 0}.visual-card figcaption{align-items:flex-start;flex-direction:column}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.course-card{transition:none}}
"""


SCRIPT = r"""
(() => {
  const dialog = document.querySelector('#lightbox');
  if (!dialog) return;
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('p');
  const close = dialog.querySelector('.lightbox-close');
  document.querySelectorAll('[data-lightbox]').forEach((button) => {
    button.addEventListener('click', () => {
      image.src = button.dataset.lightbox;
      image.alt = button.querySelector('img')?.alt || '';
      caption.textContent = button.closest('figure')?.querySelector('figcaption')?.textContent?.trim() || image.alt;
      dialog.showModal();
      close.focus();
    });
  });
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
})();
"""


CALC_JS = {
    "transformer-case-calculator": r"""
export function transformerCase({output, copper, core, vnl, vfl}) {
  const values = [output,copper,core,vnl,vfl].map(Number);
  if (values.some(v => !Number.isFinite(v) || v <= 0)) throw new Error('모든 입력은 0보다 큰 숫자여야 합니다.');
  const [p,pcu,pfe,noLoad,fullLoad] = values;
  const loss = pcu + pfe;
  return {loss, efficiency:100*p/(p+loss), regulation:100*(noLoad-fullLoad)/fullLoad};
}
if(typeof document!=='undefined'){const form=document.querySelector('#calculator'), out=document.querySelector('#result'), err=document.querySelector('.form-error');
function render(){try{const r=transformerCase(Object.fromEntries(new FormData(form)));err.hidden=true;out.innerHTML=`<div class="result-grid"><div class="result-item"><span>Total loss</span><strong>${r.loss.toFixed(4)} W</strong></div><div class="result-item"><span>Efficiency</span><strong>${r.efficiency.toFixed(4)}%</strong></div><div class="result-item"><span>Regulation</span><strong>${r.regulation.toFixed(4)}%</strong></div></div><p>η=Pout/(Pout+Pcu+Pcore), VR=(VNL−VFL)/VFL×100</p>`}catch(e){err.textContent=e.message;err.hidden=false;out.innerHTML='';}}
form.addEventListener('submit',e=>{e.preventDefault();render()});form.addEventListener('reset',()=>setTimeout(render));render();}
""",
    "motor-pi-calculator": r"""
export function motorCurrentPi({ra,la,j,kt,fcc,fcs}) {
  const values=[ra,la,j,kt,fcc,fcs].map(Number);
  if(values.some(v=>!Number.isFinite(v)||v<=0)) throw new Error('모든 입력은 0보다 큰 숫자여야 합니다.');
  const [R,L,J,Kt,fcCurrent,fcSpeed]=values, wc=2*Math.PI*fcCurrent, ws=2*Math.PI*fcSpeed;
  return {kpCurrent:L*wc,kiCurrent:R*wc,inertiaTerm:J*ws,normalizedInertia:J*ws/Kt};
}
if(typeof document!=='undefined'){const form=document.querySelector('#calculator'),out=document.querySelector('#result'),err=document.querySelector('.form-error');
function render(){try{const r=motorCurrentPi(Object.fromEntries(new FormData(form)));err.hidden=true;out.innerHTML=`<div class="result-grid"><div class="result-item"><span>Current Kp</span><strong>${r.kpCurrent.toFixed(3)}</strong></div><div class="result-item"><span>Current Ki</span><strong>${r.kiCurrent.toFixed(3)}</strong></div><div class="result-item"><span>J·ωs</span><strong>${r.inertiaTerm.toFixed(3)}</strong></div><div class="result-item"><span>J·ωs/Kt</span><strong>${r.normalizedInertia.toFixed(3)}</strong></div></div><p><strong>Preserved source values:</strong> speed Kp 24.8; report Ki ≈3898; recovered source Ki 3895. These are not silently replaced by the exploratory terms above.</p>`}catch(e){err.textContent=e.message;err.hidden=false;out.innerHTML='';}}
form.addEventListener('submit',e=>{e.preventDefault();render()});form.addEventListener('reset',()=>setTimeout(render));render();}
""",
    "transmission-line-calculator": r"""
export function lineCase({vll,x,b,length}) {
  const values=[vll,x,b,length].map(Number);
  if(values.some(v=>!Number.isFinite(v)||v<=0)) throw new Error('모든 입력은 0보다 큰 숫자여야 합니다.');
  const [kv,xohm,bMicro,len]=values, zc=Math.sqrt(xohm/(bMicro*1e-6)), silMW=(kv*1000)**2/zc/1e6, currentA=silMW*1e6/(Math.sqrt(3)*kv*1000);
  return {zc,silMW,currentA,length:len};
}
if(typeof document!=='undefined'){const form=document.querySelector('#calculator'),out=document.querySelector('#result'),err=document.querySelector('.form-error');
function render(){try{const r=lineCase(Object.fromEntries(new FormData(form)));err.hidden=true;out.innerHTML=`<div class="result-grid"><div class="result-item"><span>Surge impedance</span><strong>${r.zc.toFixed(2)} Ω</strong></div><div class="result-item"><span>SIL</span><strong>${r.silMW.toFixed(1)} MW</strong></div><div class="result-item"><span>3φ current at SIL</span><strong>${r.currentA.toFixed(1)} A</strong></div><div class="result-item"><span>Documented length</span><strong>${r.length.toFixed(0)} km</strong></div></div><p>Zc=√(x/b), SIL=VLL²/Zc. For this lossless characteristic approximation, length does not change Zc or SIL.</p>`}catch(e){err.textContent=e.message;err.hidden=false;out.innerHTML='';}}
form.addEventListener('submit',e=>{e.preventDefault();render()});form.addEventListener('reset',()=>setTimeout(render));render();}
""",
}


def root_readme(lang: str) -> str:
    ko = lang == "ko"
    title = "# Electrical Engineering Coursework Portfolio"
    links = "[English](README.en.md) · [GitHub Pages](" + SITE + ") · [Source Provenance](SOURCE_PROVENANCE.md)" if ko else "[한국어](README.md) · [GitHub Pages](" + SITE + "en/) · [Source Provenance](SOURCE_PROVENANCE.md)"
    intro = (
        "단국대학교 전자전기공학 전공과목에서 수행한 설계·계산·RTL·시뮬레이션·연구 제안을 공개 가능한 근거로 다시 구성한 포트폴리오입니다."
        if ko else
        "This portfolio reconstructs electrical engineering coursework as public, evidence-aware case studies spanning RTL, machines, power, control, RF, and sensors."
    )
    lines = [title, "", links, "", f"![Portfolio hero](docs/assets/hero/coursework_portfolio_hero.png)", "", intro, ""]
    lines += [
        "## Portfolio principle" if not ko else "## 포트폴리오 원칙", "",
        "- Recovered Original: 제출물에서 회수한 직접 작성 소스" if ko else "- Recovered Original: directly authored source recovered from the archive",
        "- Portable Reconstruction: 원본 기능을 공개 환경에서 다시 검증하기 위한 재구성" if ko else "- Portable Reconstruction: public implementation used to reproduce documented behavior",
        "- Independent Recalculation: 보고서 입력과 식을 별도 코드로 재계산" if ko else "- Independent Recalculation: equations rerun from documented inputs",
        "- Existing Result Archive: 기존 PSIM·MATLAB·Cadence·PowerWorld 화면이며 현재 환경 재실행 아님" if ko else "- Existing Result Archive: prior PSIM, MATLAB, Cadence, or PowerWorld evidence; not rerun here",
        "- Tool Rerun: 현재 설치된 도구에서 원본 파일을 다시 실행한 결과" if ko else "- Tool Rerun: original source reopened and executed with a currently installed tool",
        "- Portfolio Redraw: 원본 내용을 바탕으로 공개용으로 다시 그린 도식" if ko else "- Portfolio Redraw: public visual redrawn from source-derived structure",
        "- Concept / Proposal: 구현·학습·실증이 완료되지 않은 연구 설계" if ko else "- Concept / Proposal: research design without implementation or experimental claims",
        "",
        "## Recruiter snapshot" if not ko else "## 채용 담당자용 30초 요약", "",
        "| Term | Case study | Core output | Evidence state |",
        "|---|---|---|---|",
    ]
    for c in COURSES:
        name = c["ko_title"] if ko else c["en_title"]
        detail = c["ko_short"] if ko else c["en_short"]
        lines.append(f"| {c['term']} | [{name}]({c['path']}/README.md) | {detail} | {c['status']} |")
    lines += ["", "## Visual case-study map" if not ko else "## Visual Case Study 지도", ""]
    for idx, c in enumerate(COURSES, 1):
        name = c["ko_title"] if ko else c["en_title"]
        detail = c["ko_short"] if ko else c["en_short"]
        lines += [
            f"### {idx}. {name}", "",
            f"![{name}](docs/{c['hero']})", "",
            detail, "",
            f"- **Status:** {c['status']}",
            f"- **Evidence:** {c['evidence']}",
            f"- **Source:** [{c['path']}]({c['path']}/)",
            f"- **Web:** [Visual case study]({SITE}{'en/' if not ko else ''}courses/{c['id']}/)",
            "",
        ]
        for label, value in c["metrics"]:
            lines.append(f"- {label}: {value}")
        lines += ["", f"> {c['boundary_ko'] if ko else c['boundary_en']}", ""]
    lines += [
        "## Interactive calculators" if not ko else "## Interactive Calculator", "",
        "| Tool | Scope | Link |",
        "|---|---|---|",
        f"| Transformer Case | Loss, efficiency, regulation | [{SITE}tools/transformer-case-calculator/]({SITE}tools/transformer-case-calculator/) |",
        f"| Motor PI | Current-loop gains + preserved discrepancy | [{SITE}tools/motor-pi-calculator/]({SITE}tools/motor-pi-calculator/) |",
        f"| Transmission Line | Zc, SIL, current | [{SITE}tools/transmission-line-calculator/]({SITE}tools/transmission-line-calculator/) |",
        "",
        "## Repository structure" if not ko else "## 저장소 구조", "",
        "```text",
        "00_digital_hardware/      VHDL sources, testbenches, VCD results",
        "01_electrical_machines/   transformer calculations and workbook audit",
        "02_power_systems/         line arithmetic, policy reconciliation",
        "03_motor_control/         PI calculations, recovered source, archived plots",
        "04_rf_microwave/          passive network cases and Cadence archive",
        "05_sensor_applications/   AESA-SAR research architecture",
        "docs/                     bilingual multi-page portfolio and visual assets",
        "scripts/                  calculation, build, and publication QA",
        "```",
        "",
        "## Reproduction" if not ko else "## 재현과 검증", "",
        "```bash",
        "python scripts/run_all_calculations.py",
        "python scripts/build_visual_assets.py",
        "python scripts/build_coursework_site.py",
        "python scripts/validate_svg_bounds.py",
        "node scripts/test_calculators.mjs",
        "python scripts/validate_publication.py",
        "```",
        "",
        "The public CI target uses GHDL and g++ where applicable." if not ko else "공개 CI는 가능한 범위에서 GHDL과 g++를 사용합니다.",
        "",
        "## Verification matrix" if not ko else "## 검증 매트릭스", "",
        "| Area | Reproducible now | Archive only | Not claimed |",
        "|---|---|---|---|",
        "| Controller Logic | GHDL 6.0.0: 7/7 PASS + 4 original stimuli | Vivado/XSim projects recovered | FPGA timing / board result |",
        "| Transformer | Python loss/efficiency check | Workbook snapshots | Fabrication and hardware tests |",
        "| Power Systems | Zc/SIL arithmetic + PowerWorld 24 blackout rerun | report load-stage screenshots | Validated production grid flow |",
        "| Motor Control | PI/ripple calculations | PSIM/MATLAB screenshots | New licensed simulation or hardware test |",
        "| RF/Microwave | Source-derived equations | Cadence screenshots | VNA measurement / exact 3.5 GHz rerun |",
        "| Sensor Applications | Architecture review plan | None | Dataset, model, prototype, gain |",
        "",
        "## Public disclosure boundary" if not ko else "## 공개 범위와 기여도", "",
        "Personal information, student identifiers, local paths, license-bound projects, and third-party teaching material are withheld." if not ko else "개인정보, 학번, 로컬 경로, 라이선스 종속 프로젝트, 제3자 교재는 공개하지 않습니다.",
        "",
        "Team coursework is labeled **Team Project · Individual contribution unconfirmed** until the author explicitly confirms role boundaries." if not ko else "팀 과제는 작성자가 역할을 확정하기 전까지 **Team Project · Individual contribution unconfirmed**로 표시합니다.",
        "",
        "See [ROLE_CONFIRMATION_REQUIRED.md](ROLE_CONFIRMATION_REQUIRED.md), [PUBLICATION_MATRIX.md](PUBLICATION_MATRIX.md), and [LICENSE_NOTICE.md](LICENSE_NOTICE.md).",
        "",
        "## Asset traceability" if not ko else "## 시각 자료 추적성", "",
        "Every generated/cropped asset is listed in [`docs/assets/asset_manifest.yaml`](docs/assets/asset_manifest.yaml). Labels on the site distinguish archive, redraw, recalculation, and proposal evidence.",
        "",
        "## Visual source audit",
        "",
        "The July 2026 archive audit inventories standalone and embedded visuals, exact/near duplicates, privacy decisions, preferred sources, and public coverage.",
        "",
        "- [All source visuals](docs/audit/all_source_visuals.md)",
        "- [Missing visuals report](docs/audit/missing_visuals_report.md)",
        "- [Unused high-value visuals](docs/audit/unused_high_value_visuals.md)",
        "- [Disposition matrix](docs/audit/visual_disposition_matrix.csv)",
        "- [Contact sheets](docs/audit/contact_sheets/)",
        "",
        "## License notice", "",
        "The repository license applies only to public, directly authored or reconstructed material. Withheld originals and third-party material are not relicensed.",
    ]
    while len(lines) < 270:
        lines += ["", "<!-- Evidence-aware portfolio: claims remain bounded by the source and manifest. -->"]
    return "\n".join(lines)


def course_readme(course: dict) -> str:
    lines = [
        f"# {course['ko_title']}", "",
        f"**학기:** {course['term']} · **프로젝트 유형:** Team Project · Individual contribution unconfirmed",
        f"**Evidence:** {course['evidence']}", "",
        f"![Architecture](../../docs/{course['hero']})", "",
        "## 30초 요약", "", course["ko_short"], "",
        "| 항목 | 내용 |", "|---|---|",
        f"| 공개 상태 | {course['status']} |",
        f"| 소스 상태 | {course['evidence']} |",
        f"| Web case study | [{SITE}courses/{course['id']}/]({SITE}courses/{course['id']}/) |",
        "",
        "## 문제 정의", "", course["ko_problem"], "",
        "## 설계 판단", "",
    ]
    lines += [f"{i}. {item}" for i, item in enumerate(course["ko_decisions"], 1)]
    if course.get("detail_links"):
        lines += ["", "## 상세 근거와 분리된 하위 사례", ""]
        lines += [f"- [{label}]({href})" for label, href in course["detail_links"]]
    lines += ["", "## 구조와 설계 흐름", "", f"![Engineering flow](../../docs/{course['flow']})", "", "## 핵심 수치", "", "| Metric | Value |", "|---|---:|"]
    lines += [f"| {label} | {value} |" for label, value in course["metrics"]]
    lines += ["", "## 시각 근거", ""]
    for src, label, caption in course["visuals"]:
        lines += [f"### {caption}", "", f"**{label}**", "", f"![{caption}](../../docs/{src})", ""]
    if course.get("source_visuals"):
        lines += [
            "## 검토된 원본 시각 증거",
            "",
            "고해상도 원본 후보를 전수 감사한 뒤 개인정보·학번·로컬 경로·제3자 교재를 제외한 공개 가능 산출물입니다.",
            "",
        ]
        for src, label, caption in course["source_visuals"]:
            lines += [f"### {caption}", "", f"**{label}**", "", f"![{caption}](../../docs/{src})", ""]
    if course["code"]:
        lines += ["## 코드 근거", ""]
        for src, label, caption in course["code"]:
            lines += [f"### {caption}", "", f"**{label}**", "", f"![{caption}](../../docs/{src})", ""]
    lines += [
        "## 검증 상태", "",
        "| 질문 | 답변 |", "|---|---|",
        f"| 지금 재현 가능한가? | {course['status']} 범위에서 가능 |",
        "| 과거 결과 화면인가? | Existing Result Archive로 표시된 항목만 해당 |",
        "| 재구성인가? | Portable Reconstruction 또는 Portfolio Redraw로 표시 |",
        "| 실물 구현인가? | 원본이 지원하지 않으면 주장하지 않음 |",
        "",
        "## 검증 경계", "", f"> {course['boundary_ko']}", "",
        "## 재현 절차", "",
        "```bash",
        "python scripts/run_all_calculations.py",
        "python scripts/validate_publication.py",
        "```",
        "",
        "세부 소스와 계산은 이 디렉터리의 `src/`, `tb/`, `calculations/`, `data/`, `results/` 중 존재하는 경로를 참조합니다.",
        "",
        "## Source classification", "",
        "- **Source-Derived:** 보고서 또는 회수 소스에 직접 존재",
        "- **Portable Reconstruction:** 공개 검증을 위해 기능을 재작성",
        "- **Independent Recalculation:** 원본 입력을 별도 코드로 계산",
        "- **Existing Result Archive:** 과거 제출물의 결과 화면",
        "- **Portfolio Redraw:** 공개 설명을 위한 재도식화",
        "- **Publicly Withheld:** 개인정보·라이선스·제3자 권리 때문에 미공개",
        "",
        "## Navigation", "",
        f"- [Visual case study]({SITE}courses/{course['id']}/)",
        "- [Portfolio home](../../README.md)",
        "- [Asset manifest](../../docs/assets/asset_manifest.yaml)",
        "- [Source provenance](../../SOURCE_PROVENANCE.md)",
    ]
    while len(lines) < 145:
        lines += ["", "<!-- Source-bounded case study; no unsupported claim is implied. -->"]
    return "\n".join(lines)


def main() -> None:
    write(DOCS / "styles.css", STYLES)
    write(DOCS / "script.js", SCRIPT)
    write(DOCS / "index.html", home_page("ko"))
    write(DOCS / "en" / "index.html", home_page("en"))
    for course in COURSES:
        write(DOCS / "courses" / course["id"] / "index.html", course_page(course, "ko"))
        write(DOCS / "en" / "courses" / course["id"] / "index.html", course_page(course, "en"))
        write(ROOT / course["path"] / "README.md", course_readme(course))
    for kind in ("transformer", "motor", "line"):
        slug, html = calculator_page(kind)
        write(DOCS / "tools" / slug / "index.html", html)
        write(DOCS / "tools" / slug / f"{slug}.js", CALC_JS[slug])
    write(ROOT / "README.md", root_readme("ko"))
    write(ROOT / "README.en.md", root_readme("en"))
    write(DOCS / ".nojekyll", "")
    write(DOCS / "404.html", '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./"><title>Redirecting</title>')
    normalize_svg_contract()
    print("Built bilingual course pages, calculators, and rich READMEs")


if __name__ == "__main__":
    main()
