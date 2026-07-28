#!/usr/bin/env python3
"""Build public, evidence-labelled visual assets for the coursework portfolio.

The script only turns already-audited source, reproduced VCD output, and
source-derived numeric values into portfolio assets.  Original assignment PDFs
and workbooks are never copied into the public repository.
"""

from __future__ import annotations

import html
import math
import os
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
ASSETS = REPO / "docs" / "assets"
WORK = REPO.parents[1] / "coursework_visual_highres"
FONT_FAMILY = (
    '"Pretendard","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",'
    '"Segoe UI",Arial,sans-serif'
)
MONO_FAMILY = '"Cascadia Mono","Consolas","SFMono-Regular",monospace'


def mkdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write(path: Path, content: str) -> None:
    mkdir(path.parent)
    path.write_text(content, encoding="utf-8", newline="\n")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def lines(text: str, width: int = 26) -> list[str]:
    words = text.split()
    out: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > width:
            out.append(current)
            current = word
        else:
            current = candidate
    if current:
        out.append(current)
    return out[:3]


def flow_svg(
    path: Path,
    title: str,
    subtitle: str,
    nodes: list[tuple[str, str]],
    accent: str = "#38bdf8",
) -> None:
    width = 1440
    height = 520
    count = len(nodes)
    gap = 34
    card_w = (width - 120 - gap * (count - 1)) / count
    card_y = 188
    card_h = 210
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" '
        'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" '
        f'fill="{accent}"/></marker>',
        "</defs>",
        '<rect width="1440" height="520" rx="32" fill="#07111f"/>',
        f'<text x="60" y="68" fill="#f8fafc" font-family="{esc(FONT_FAMILY)}" '
        'font-size="34" font-weight="700">',
        esc(title),
        "</text>",
        f'<text x="60" y="112" fill="#94a3b8" font-family="{esc(FONT_FAMILY)}" '
        'font-size="18">',
        esc(subtitle),
        "</text>",
    ]
    for index, (heading, body) in enumerate(nodes):
        x = 60 + index * (card_w + gap)
        if index:
            x1 = x - gap + 6
            x2 = x - 8
            parts.append(
                f'<line x1="{x1:.1f}" y1="{card_y + card_h / 2:.1f}" '
                f'x2="{x2:.1f}" y2="{card_y + card_h / 2:.1f}" '
                f'stroke="{accent}" stroke-width="4" marker-end="url(#arrow)"/>'
            )
        parts.extend(
            [
                f'<rect x="{x:.1f}" y="{card_y}" width="{card_w:.1f}" height="{card_h}" '
                'rx="20" fill="#101d31" stroke="#29415f" stroke-width="2"/>',
                f'<rect x="{x:.1f}" y="{card_y}" width="{card_w:.1f}" height="10" '
                f'rx="5" fill="{accent}"/>',
                f'<text x="{x + 24:.1f}" y="{card_y + 58}" fill="#f8fafc" '
                f'font-family="{esc(FONT_FAMILY)}" font-size="23" font-weight="700">',
                esc(heading),
                "</text>",
            ]
        )
        for row, fragment in enumerate(lines(body, 24)):
            parts.extend(
                [
                    f'<text x="{x + 24:.1f}" y="{card_y + 100 + row * 31}" '
                    f'fill="#cbd5e1" font-family="{esc(FONT_FAMILY)}" font-size="17">',
                    esc(fragment),
                    "</text>",
                ]
            )
    parts.extend(
        [
            f'<text x="60" y="472" fill="{accent}" font-family="{esc(FONT_FAMILY)}" '
            'font-size="16" font-weight="700">PORTFOLIO REDRAW</text>',
            '<text x="260" y="472" fill="#64748b" '
            f'font-family="{esc(FONT_FAMILY)}" font-size="16">'
            "Source-derived architecture; not a measured result</text>",
            "</svg>",
        ]
    )
    write(path, "".join(parts))


DIAGRAMS: dict[str, tuple[str, str, list[tuple[str, str]], str]] = {
    "digital/controller_logic_progression.svg": (
        "Controller Logic Progression",
        "Combinational building blocks to stateful RTL",
        [
            ("Boolean Logic", "1-bit full adder"),
            ("Hierarchy", "4-bit ripple carry"),
            ("Selection", "decoder and mux"),
            ("State", "Mealy 101 detector"),
            ("Data Path", "universal shift register"),
        ],
        "#38bdf8",
    ),
    "digital/one_bit_full_adder_gate.svg": (
        "1-bit Full Adder",
        "XOR/AND/OR Boolean implementation",
        [("Inputs", "a, b, cin"), ("Propagate", "t1 = a xor b"), ("Sum", "s = t1 xor cin"), ("Carry", "cout = ab + t1·cin")],
        "#38bdf8",
    ),
    "digital/four_bit_ripple_carry.svg": (
        "4-bit Ripple-Carry Adder",
        "Four full-adder components with explicit carry chain",
        [("FA0", "a0 b0 cin"), ("FA1", "a1 b1 c1"), ("FA2", "a2 b2 c2"), ("FA3", "a3 b3 c3")],
        "#38bdf8",
    ),
    "digital/decoder_3to8.svg": (
        "3-to-8 Decoder",
        "One-hot decode for all three-bit select values",
        [("Select", "s2 s1 s0"), ("Decode", "one of eight"), ("One-hot", "y0 … y7"), ("Verify", "8 truth cases")],
        "#38bdf8",
    ),
    "digital/decoder_based_mux_8to1.svg": (
        "8-to-1 Multiplexer",
        "Selection path and observed output contract",
        [("Inputs", "d0 … d7"), ("Select", "s[2:0]"), ("Mux", "selected bit"), ("Output", "y")],
        "#38bdf8",
    ),
    "digital/mux_4bit_hierarchy.svg": (
        "4-bit Bus Multiplexer",
        "Four parallel 8-to-1 instances share one select",
        [("8 × 4-bit", "input buses"), ("Shared Select", "three bits"), ("4 Lanes", "parallel muxes"), ("Output", "4-bit bus")],
        "#38bdf8",
    ),
    "digital/mealy_101_state_diagram.svg": (
        "Mealy 101 Sequence Detector",
        "Overlapping sequence recognition",
        [("ST0", "no prefix"), ("ST1", "seen 1"), ("ST2", "seen 10"), ("Detect", "input 1 → dout=1")],
        "#38bdf8",
    ),
    "digital/sequence_detection_timeline.svg": (
        "Sequence Detection Timeline",
        "Output is asserted on the final input edge",
        [("Reset", "state ST0"), ("Input 1", "ST0 → ST1"), ("Input 0", "ST1 → ST2"), ("Input 1", "ST2 → ST1, dout=1")],
        "#38bdf8",
    ),
    "digital/universal_shift_register.svg": (
        "Universal Shift Register",
        "Hold, shift-right, shift-left, and parallel-load modes",
        [("00", "hold"), ("01", "shift right"), ("10", "shift left"), ("11", "parallel load")],
        "#38bdf8",
    ),
    "digital/usr_mode_timeline.svg": (
        "USR Mode Timeline",
        "Mode-select contract exercised in portable regression",
        [("Clear", "q = 0000"), ("Load", "p_in → q"), ("Shift R", "d_in enters MSB"), ("Shift L", "d_in enters LSB")],
        "#38bdf8",
    ),
    "transformer/core_geometry_flow.svg": (
        "Transformer Core Geometry Flow",
        "Requirements to window/core feasibility",
        [("Power", "Pt and electrical factor"), ("Geometry", "required Kg"), ("Core", "UI / EI / DU cases"), ("Window", "Ku and wire fit")],
        "#f59e0b",
    ),
    "transformer/transformer_winding_architecture.svg": (
        "Winding Architecture",
        "Selected 900 W, 300 Hz isolation-transformer case",
        [("Primary", "220 V · 180 turns"), ("Core", "silicon steel · 1.5 T"), ("Secondary", "110 V · 93 turns"), ("Load", "900 W")],
        "#f59e0b",
    ),
    "transformer/ui_ei_du_core_comparison.svg": (
        "UI · EI · DU Core Trade-off",
        "Case comparison is source-derived; no automatic core recommendation",
        [("UI", "selected report case"), ("EI", "alternate workbook"), ("DU", "comparison case"), ("Decision", "window, loss, manufacturability")],
        "#f59e0b",
    ),
    "transformer/turns_and_wire_flow.svg": (
        "Turns and Wire Selection",
        "Electrical stress to winding implementation",
        [("Voltage/Frequency", "220 V · 300 Hz"), ("Flux Limit", "Bm = 1.5 T"), ("Turns", "Np 180 · Ns 93"), ("Wire", "current density and window")],
        "#f59e0b",
    ),
    "power/transmission_line_pi_model.svg": (
        "765 kV Transmission-Line π Model",
        "350 km line represented by series impedance and shunt admittance",
        [("Sending Bus", "765 kV"), ("Shunt Y/2", "charging branch"), ("Series Z", "R + jωL"), ("Receiving Bus", "load boundary")],
        "#22c55e",
    ),
    "power/zc_sil_formula_flow.svg": (
        "Zc and SIL Formula Flow",
        "Independent recalculation of the coursework case",
        [("Per-unit Length", "R, L, G, C"), ("Characteristic Z", "sqrt(Z′/Y′)"), ("Voltage", "line-to-line RMS"), ("SIL", "VLL² / |Zc|")],
        "#22c55e",
    ),
    "power/non_convergence_diagnosis.svg": (
        "PowerWorld Non-Convergence Diagnosis",
        "Solver failure is retained as an engineering result boundary",
        [("Model", "bus, line, load"), ("Run", "power-flow solve"), ("Symptoms", "unrealistic voltage / divergence"), ("Next Check", "units, slack, load, limits")],
        "#22c55e",
    ),
    "power/model_result_boundary.svg": (
        "Theory–Model–Solver Boundary",
        "Analytical line values do not guarantee a converged network case",
        [("Theory", "Zc and SIL"), ("Model", "π equivalent"), ("Solver", "PowerWorld settings"), ("Evidence", "convergence state separated")],
        "#22c55e",
    ),
    "power/transmission_and_storage_roadmap.svg": (
        "Transmission and Storage Roadmap",
        "Report-based policy review; dates and capacities require source verification",
        [("Grid", "HVDC and transmission expansion"), ("Storage", "ESS and pumped hydro"), ("Flexibility", "DR and distributed energy"), ("Market", "regional and real-time signals")],
        "#22c55e",
    ),
    "motor/dc_motor_system_architecture.svg": (
        "DC Motor Control Architecture",
        "Reference profile through cascaded loops and H-bridge plant",
        [("Speed Ref", "0→850→1200 rpm"), ("Speed PI", "current reference"), ("Current PI", "voltage command"), ("Plant", "H-bridge and DC motor")],
        "#a78bfa",
    ),
    "motor/h_bridge_power_stage.svg": (
        "H-Bridge Power Stage",
        "Bidirectional armature-voltage command with ±200 V limit",
        [("DC Link", "200 V boundary"), ("PWM", "switch command"), ("H-Bridge", "four-quadrant stage"), ("Armature", "Ia and speed")],
        "#a78bfa",
    ),
    "motor/cascaded_pi_controller.svg": (
        "Cascaded PI Controller",
        "Outer speed loop and inner current loop",
        [("Speed Error", "ω* − ω"), ("Speed PI", "Ia*"), ("±10 A Limit", "anti-windup gate"), ("Current PI", "Vt + back-EMF")],
        "#a78bfa",
    ),
    "motor/speed_loop_design.svg": (
        "Speed-Loop Design",
        "Mechanical bandwidth is below the current-loop bandwidth",
        [("J, Kt", "mechanical parameters"), ("ωcs", "speed bandwidth"), ("Kps", "proportional gain"), ("Kis", "integral gain")],
        "#a78bfa",
    ),
    "motor/current_loop_design.svg": (
        "Current-Loop Design",
        "Electrical pole and selected current-loop bandwidth",
        [("Ra, La", "armature model"), ("ωcc", "current bandwidth"), ("Kpc", "La·ωcc"), ("Kic", "Ra·ωcc")],
        "#a78bfa",
    ),
    "motor/saturation_anti_windup.svg": (
        "Saturation and Anti-Windup",
        "Integrator updates only while the unsaturated command is accepted",
        [("PI Candidate", "calculate command"), ("Limit", "±10 A / ±200 V"), ("Saturated?", "compare bounds"), ("Integrator", "update only if inside")],
        "#a78bfa",
    ),
    "motor/field_weakening_flow.svg": (
        "Field-Weakening Analysis",
        "Existing report archive; not independently rerun",
        [("Base Speed", "rated flux"), ("Voltage Limit", "available armature voltage"), ("Field Command", "reduce excitation"), ("High Speed", "torque capability decreases")],
        "#a78bfa",
    ),
    "rf/microstrip_cross_section.svg": (
        "Microstrip Cross-Section",
        "Alumina substrate case used for the 3.5 GHz design",
        [("Copper", "width W"), ("Substrate", "εr 9.9 · h 0.5 mm"), ("Ground", "reference plane"), ("Target", "50 Ω")],
        "#fb7185",
    ),
    "rf/microstrip_design_flow.svg": (
        "270° Microstrip Design Flow",
        "Calculator result, Cadence setup, and archive marker kept distinct",
        [("Target", "3.5 GHz · 50 Ω · 270°"), ("Synthesis", "W and L"), ("Cadence", "stackup and ports"), ("Archive", "loss / phase at 3.7 GHz marker")],
        "#fb7185",
    ),
    "rf/l_section_matching.svg": (
        "L-Section Matching",
        "Two reactive elements move the load to the 100 Ω line",
        [("Load", "200 − j100 Ω"), ("Shunt C", "admittance move"), ("Series L", "reactance move"), ("Match", "center of Smith chart")],
        "#fb7185",
    ),
    "rf/smith_chart_movement.svg": (
        "Smith-Chart Movement",
        "Portfolio redraw of the matching path",
        [("Normalize", "zL / Z0"), ("Admittance", "rotate to y-plane"), ("Shunt Move", "constant conductance"), ("Series Move", "constant resistance")],
        "#fb7185",
    ),
    "rf/single_stub_two_solutions.svg": (
        "Single-Stub: Two Solutions",
        "Two valid line/stub length combinations from the same load",
        [("Load", "normalize"), ("Move 1", "intersection A"), ("Move 2", "intersection B"), ("Stub", "cancel susceptance")],
        "#fb7185",
    ),
    "rf/wilkinson_structure.svg": (
        "Wilkinson Divider",
        "Equal split with output-port isolation",
        [("Port 1", "50 Ω input"), ("Quarter-Wave Arms", "≈70.7 Ω"), ("Ports 2/3", "≈−3 dB"), ("Isolation", "100 Ω ideal, 94 Ω tuned")],
        "#fb7185",
    ),
    "rf/quadrature_hybrid_structure.svg": (
        "Branch-Line Quadrature Hybrid",
        "Four-port equal split with quadrature phase relationship",
        [("Input", "port excitation"), ("Series Arms", "quarter-wave"), ("Shunt Arms", "quarter-wave"), ("Outputs", "equal magnitude, 90°")],
        "#fb7185",
    ),
    "sensor/aesa_system_architecture.svg": (
        "AESA–SAR Research Architecture",
        "Proposal-only system decomposition",
        [("AESA Front End", "T/R modules"), ("Digital Beamforming", "channel calibration"), ("SAR Processing", "range and azimuth"), ("Enhancement", "physics-guided diffusion")],
        "#2dd4bf",
    ),
    "sensor/tr_module_block.svg": (
        "T/R Module Block",
        "Concept architecture, not a built hardware prototype",
        [("Phase/Gain", "per-element control"), ("PA/LNA", "Tx/Rx chains"), ("Switch/Circulator", "duplex path"), ("Element", "array interface")],
        "#2dd4bf",
    ),
    "sensor/digital_beamforming_chain.svg": (
        "Digital Beamforming Chain",
        "Element channels to calibrated beams",
        [("ADC Channels", "I/Q samples"), ("Calibration", "gain and phase"), ("Weights", "steering vector"), ("Beam Output", "range profiles")],
        "#2dd4bf",
    ),
    "sensor/processing_hierarchy.svg": (
        "Processing Hierarchy",
        "Hardware, radar processing, and image enhancement layers",
        [("RF Layer", "array and T/R"), ("Signal Layer", "range/Doppler"), ("Image Layer", "SAR formation"), ("AI Layer", "diffusion restoration")],
        "#2dd4bf",
    ),
    "sensor/interface_and_clocking.svg": (
        "Interface and Clocking",
        "Proposal interface map; implementation details are not claimed",
        [("Clock", "channel coherence"), ("Control", "beam weights"), ("Data", "high-rate samples"), ("Compute", "FPGA/GPU boundary")],
        "#2dd4bf",
    ),
    "sensor/sar_image_formation.svg": (
        "SAR Image Formation",
        "Concept processing path",
        [("Raw Echo", "platform aperture"), ("Range Compression", "matched filtering"), ("RCMC", "migration correction"), ("Azimuth Focus", "complex image")],
        "#2dd4bf",
    ),
    "sensor/physics_guided_diffusion.svg": (
        "Physics-Guided Diffusion",
        "Research proposal, not a reported training result",
        [("Degraded SAR", "input"), ("Forward Model", "physics constraint"), ("Denoiser", "conditional diffusion"), ("Candidate Output", "validate with PSNR/SSIM later")],
        "#2dd4bf",
    ),
    "sensor/atr_integration.svg": (
        "ATR Integration Concept",
        "Restoration output to downstream target analysis",
        [("SAR Image", "focused input"), ("Enhancement", "candidate restoration"), ("Detector", "ATR model"), ("Evaluation", "task and image metrics")],
        "#2dd4bf",
    ),
    "sensor/validation_roadmap.svg": (
        "Validation Roadmap",
        "Evidence gates before any performance claim",
        [("Dataset", "public or approved"), ("Baselines", "RDA / CSA / BPA"), ("Image Metrics", "PSNR / SSIM"), ("Task Metrics", "ATR and robustness")],
        "#2dd4bf",
    ),
    "sensor/implementation_boundary.svg": (
        "Implementation Boundary",
        "What is proposed versus what is demonstrated",
        [("Reviewed", "AESA/SAR literature"), ("Designed", "system decomposition"), ("Proposed", "physics-guided diffusion"), ("Not Implemented", "training and hardware prototype")],
        "#2dd4bf",
    ),
}


def code_card(path: Path, title: str, source_label: str, code: str, start_line: int) -> None:
    selected = code.strip("\n").splitlines()[:22]
    height = 150 + len(selected) * 28
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" '
        f'viewBox="0 0 1280 {height}">',
        f'<rect width="1280" height="{height}" rx="28" fill="#07111f"/>',
        '<rect x="0" y="0" width="14" height="100%" fill="#38bdf8"/>',
        f'<text x="48" y="55" fill="#f8fafc" font-family="{esc(FONT_FAMILY)}" '
        f'font-size="28" font-weight="700">{esc(title)}</text>',
        f'<text x="48" y="92" fill="#94a3b8" font-family="{esc(FONT_FAMILY)}" '
        f'font-size="16">{esc(source_label)} · source-derived code card</text>',
    ]
    keywords = re.compile(
        r"\b(if|else|case|when|process|begin|end|signal|double|static|return|"
        r"architecture|entity|port|map|for|while|def|import|from)\b",
        re.IGNORECASE,
    )
    for index, raw in enumerate(selected):
        number = start_line + index
        y = 132 + index * 28
        clean = raw.replace("\t", "    ")
        colour = "#cbd5e1"
        if clean.lstrip().startswith(("--", "//", "#")):
            colour = "#64748b"
        elif keywords.search(clean):
            colour = "#a5b4fc"
        parts.append(
            f'<text x="48" y="{y}" fill="#475569" font-family="{esc(MONO_FAMILY)}" '
            f'font-size="16">{number:>3}</text>'
        )
        parts.append(
            f'<text x="100" y="{y}" fill="{colour}" font-family="{esc(MONO_FAMILY)}" '
            f'font-size="16" xml:space="preserve">{esc(clean[:105])}</text>'
        )
    parts.extend(
        [
            f'<text x="48" y="{height - 22}" fill="#38bdf8" '
            f'font-family="{esc(FONT_FAMILY)}" font-size="14" font-weight="700">'
            "CODE CARD · LINKED TO PUBLIC SOURCE</text>",
            "</svg>",
        ]
    )
    write(path, "".join(parts))


def source_slice(path: Path, start: int, end: int) -> str:
    values = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(values[start - 1 : end])


def build_code_cards() -> None:
    cards = ASSETS / "code"
    specs = [
        (
            cards / "vhdl_full_adder.svg",
            "1-bit Full Adder Boolean Logic",
            "src/original/fulladd.vhd",
            REPO / "00_digital_hardware/controller_logic/src/original/fulladd.vhd",
            36,
            48,
        ),
        (
            cards / "vhdl_ripple_carry.svg",
            "4-bit Ripple-Carry Instantiation",
            "src/original/add_4bits.vhd",
            REPO / "00_digital_hardware/controller_logic/src/original/add_4bits.vhd",
            39,
            57,
        ),
        (
            cards / "vhdl_mealy_fsm.svg",
            "Mealy 101 State Transition",
            "src/original/mealy_101.vhd",
            REPO / "00_digital_hardware/controller_logic/src/original/mealy_101.vhd",
            50,
            71,
        ),
        (
            cards / "vhdl_usr_mode.svg",
            "Universal Shift Register Modes",
            "src/portable_reconstruction/usr_4bit.vhd",
            REPO / "00_digital_hardware/controller_logic/src/portable_reconstruction/usr_4bit.vhd",
            24,
            38,
        ),
        (
            cards / "motor_reference_profile.svg",
            "Reference Speed Profile",
            "src/recovered/motor_controller.c",
            REPO / "03_motor_control/dc_motor_pi_control/src/recovered/motor_controller.c",
            47,
            64,
        ),
        (
            cards / "motor_speed_pi_limiter.svg",
            "Speed PI, Current Limit, Anti-Windup",
            "src/recovered/motor_controller.c",
            REPO / "03_motor_control/dc_motor_pi_control/src/recovered/motor_controller.c",
            71,
            91,
        ),
        (
            cards / "motor_current_pi_saturation.svg",
            "Current PI and Voltage Saturation",
            "src/recovered/motor_controller.c",
            REPO / "03_motor_control/dc_motor_pi_control/src/recovered/motor_controller.c",
            94,
            116,
        ),
        (
            cards / "calc_transformer.svg",
            "Transformer Validation",
            "calculations/validate_transformer.py",
            REPO / "01_electrical_machines/transformer_design/calculations/validate_transformer.py",
            1,
            20,
        ),
        (
            cards / "calc_transmission.svg",
            "Zc / SIL Recalculation",
            "calculations/surge_impedance.py",
            REPO / "02_power_systems/transmission_line_and_policy/calculations/surge_impedance.py",
            1,
            20,
        ),
        (
            cards / "calc_motor_pi.svg",
            "Motor PI Gain Calculation",
            "calculations/calculate_pi_gains.py",
            REPO / "03_motor_control/dc_motor_pi_control/calculations/calculate_pi_gains.py",
            1,
            20,
        ),
        (
            cards / "calc_torque_ripple.svg",
            "Torque Ripple Calculation",
            "calculations/calculate_torque_ripple.py",
            REPO / "03_motor_control/dc_motor_pi_control/calculations/calculate_torque_ripple.py",
            1,
            20,
        ),
    ]
    for output, title, source_label, source, start, end in specs:
        code_card(output, title, source_label, source_slice(source, start, end), start)


def parse_vcd(path: Path) -> tuple[list[tuple[str, str, int]], dict[str, list[tuple[int, str]]], int]:
    scopes: list[str] = []
    variables: list[tuple[str, str, int]] = []
    selected_ids: set[str] = set()
    changes: dict[str, list[tuple[int, str]]] = {}
    current = 0
    definitions = True
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if definitions:
            if line.startswith("$scope"):
                scopes.append(line.split()[2])
            elif line.startswith("$upscope") and scopes:
                scopes.pop()
            elif line.startswith("$var") and len(scopes) == 1:
                fields = line.split()
                width = int(fields[2])
                ident = fields[3]
                name = fields[4].split("[")[0]
                if name not in {item[1] for item in variables}:
                    variables.append((ident, name, width))
                    selected_ids.add(ident)
                    changes[ident] = []
            elif line.startswith("$enddefinitions"):
                definitions = False
            continue
        if line.startswith("#"):
            current = int(line[1:])
        elif line.startswith("b"):
            bits, ident = line[1:].split()
            if ident in selected_ids:
                changes[ident].append((current, bits))
        elif line and line[0] in "01xXzZ":
            ident = line[1:]
            if ident in selected_ids:
                changes[ident].append((current, line[0].lower()))
    return variables[:8], changes, max(current, 1)


def waveform_svg(vcd: Path, output: Path, title: str) -> None:
    variables, changes, maximum = parse_vcd(vcd)
    width = 1440
    left = 220
    right = 60
    top = 132
    row_h = 64
    height = top + row_h * len(variables) + 86
    usable = width - left - right

    def sx(t: int) -> float:
        return left + usable * t / maximum

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" rx="28" fill="#07111f"/>',
        f'<text x="48" y="52" fill="#f8fafc" font-family="{esc(FONT_FAMILY)}" '
        f'font-size="30" font-weight="700">{esc(title)}</text>',
        f'<text x="48" y="88" fill="#34d399" font-family="{esc(FONT_FAMILY)}" '
        'font-size="16" font-weight="700">PORTABLE GHDL REGRESSION RESULT</text>',
    ]
    for tick in range(0, 11):
        x = left + usable * tick / 10
        parts.append(
            f'<line x1="{x:.1f}" y1="{top - 20}" x2="{x:.1f}" y2="{height - 62}" '
            'stroke="#1e293b" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{height - 35}" text-anchor="middle" fill="#64748b" '
            f'font-family="{esc(MONO_FAMILY)}" font-size="14">{tick * maximum / 10 / 1e6:.1f}</text>'
        )
    for row, (ident, name, signal_width) in enumerate(variables):
        y = top + row * row_h
        parts.append(
            f'<text x="48" y="{y + 26}" fill="#cbd5e1" font-family="{esc(MONO_FAMILY)}" '
            f'font-size="18">{esc(name)}</text>'
        )
        values = changes.get(ident, [])
        if not values:
            continue
        if signal_width == 1:
            current_value = values[0][1]
            current_time = values[0][0]
            points: list[str] = []
            for change_time, value in values[1:] + [(maximum, current_value)]:
                y_value = y + (8 if current_value == "1" else 42)
                points.append(f"{sx(current_time):.1f},{y_value:.1f}")
                points.append(f"{sx(change_time):.1f},{y_value:.1f}")
                if change_time < maximum:
                    new_y = y + (8 if value == "1" else 42)
                    points.append(f"{sx(change_time):.1f},{new_y:.1f}")
                current_time = change_time
                current_value = value
            parts.append(
                f'<polyline points="{" ".join(points)}" fill="none" stroke="#38bdf8" '
                'stroke-width="3" stroke-linejoin="round"/>'
            )
        else:
            for index, (change_time, value) in enumerate(values):
                end_time = values[index + 1][0] if index + 1 < len(values) else maximum
                x1, x2 = sx(change_time), sx(end_time)
                parts.append(
                    f'<rect x="{x1:.1f}" y="{y + 8}" width="{max(2, x2 - x1):.1f}" '
                    'height="36" rx="5" fill="#10243a" stroke="#38bdf8"/>'
                )
                if x2 - x1 > 38:
                    parts.append(
                        f'<text x="{(x1 + x2) / 2:.1f}" y="{y + 32}" text-anchor="middle" '
                        f'fill="#e2e8f0" font-family="{esc(MONO_FAMILY)}" font-size="14">'
                        f"{esc(value)}</text>"
                    )
    parts.extend(
        [
            f'<text x="{left}" y="{height - 12}" fill="#64748b" '
            f'font-family="{esc(FONT_FAMILY)}" font-size="13">time (ns; VCD source retained)</text>',
            "</svg>",
        ]
    )
    write(output, "".join(parts))


def build_waveforms() -> None:
    root = REPO / "00_digital_hardware/controller_logic/results/vcd"
    output = mkdir(ASSETS / "results/digital")
    for vcd in sorted(root.glob("*.vcd")):
        title = vcd.stem.removeprefix("tb_").replace("_", " ").title()
        waveform_svg(vcd, output / f"{vcd.stem}_waveform.svg", title)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def chart_png(
    path: Path,
    title: str,
    labels: list[str],
    values: list[float],
    unit: str,
    accent: tuple[int, int, int],
    note: str,
) -> None:
    width, height = 1280, 720
    image = Image.new("RGB", (width, height), "#07111f")
    draw = ImageDraw.Draw(image)
    draw.text((56, 44), title, fill="#f8fafc", font=font(34, True))
    draw.text((56, 96), note, fill="#94a3b8", font=font(18))
    x0, y0, x1, y1 = 110, 170, 1210, 610
    draw.line((x0, y1, x1, y1), fill="#475569", width=2)
    maximum = max(values) * 1.18 if max(values) else 1
    bar_space = (x1 - x0) / len(values)
    for index, (label, value) in enumerate(zip(labels, values)):
        bar_w = bar_space * 0.55
        bx = x0 + index * bar_space + (bar_space - bar_w) / 2
        bh = (y1 - y0) * value / maximum
        draw.rounded_rectangle(
            (bx, y1 - bh, bx + bar_w, y1),
            radius=12,
            fill=accent,
        )
        value_text = f"{value:,.2f}".rstrip("0").rstrip(".") + f" {unit}"
        draw.text((bx + bar_w / 2, y1 - bh - 36), value_text, anchor="mm", fill="#f8fafc", font=font(18, True))
        draw.text((bx + bar_w / 2, y1 + 34), label, anchor="mm", fill="#cbd5e1", font=font(17))
    draw.text((56, 676), "INDEPENDENT RECALCULATION / SOURCE-DERIVED CHART", fill=accent, font=font(15, True))
    mkdir(path.parent)
    image.save(path, optimize=True)


def matrix_png(path: Path, title: str, rows: list[tuple[str, str, str]]) -> None:
    width = 1400
    row_h = 82
    height = 150 + row_h * (len(rows) + 1)
    image = Image.new("RGB", (width, height), "#07111f")
    draw = ImageDraw.Draw(image)
    draw.text((54, 38), title, fill="#f8fafc", font=font(32, True))
    headers = ["Case", "Evidence", "Boundary"]
    columns = [54, 420, 900, 1346]
    top = 110
    for col in range(3):
        draw.rectangle((columns[col], top, columns[col + 1], top + row_h), fill="#17253a", outline="#334155")
        draw.text((columns[col] + 18, top + 27), headers[col], fill="#f8fafc", font=font(18, True))
    for row_index, row in enumerate(rows):
        y = top + row_h * (row_index + 1)
        fill = "#0d1a2c" if row_index % 2 == 0 else "#101f33"
        for col, value in enumerate(row):
            draw.rectangle((columns[col], y, columns[col + 1], y + row_h), fill=fill, outline="#334155")
            draw.text((columns[col] + 18, y + 24), value, fill="#cbd5e1", font=font(16))
    mkdir(path.parent)
    image.save(path, optimize=True)


def build_charts() -> None:
    chart_png(
        ASSETS / "transformer/core_tradeoff_chart.png",
        "Transformer Case Efficiency Comparison",
        ["Selected 900 W", "UI workbook", "General workbook"],
        [96.36, 98.3, 94.8],
        "%",
        (245, 158, 11),
        "Different source cases; values are not interchangeable",
    )
    chart_png(
        ASSETS / "transformer/loss_breakdown.png",
        "Selected Transformer Loss Breakdown",
        ["Copper", "Core", "Total"],
        [10.2267, 23.7760, 33.9998],
        "W",
        (245, 158, 11),
        "900 W · 300 Hz · UI-100 report case",
    )
    chart_png(
        ASSETS / "transformer/efficiency_regulation_chart.png",
        "Selected Transformer Validation",
        ["Efficiency", "Regulation", "Window Use"],
        [96.360, 1.136, 31.2],
        "%",
        (245, 158, 11),
        "Independent recalculation of the selected report case",
    )
    chart_png(
        ASSETS / "power/demand_forecast_chart.png",
        "2038 Electricity Demand: Baseline vs Managed",
        ["Energy baseline", "Energy target"],
        [735.1, 624.5],
        "TWh",
        (34, 197, 94),
        "11th Basic Plan review; source-derived report values",
    )
    chart_png(
        ASSETS / "power/peak_demand_chart.png",
        "2038 Peak Demand: Baseline vs Managed",
        ["Peak baseline", "Peak target"],
        [145.6, 129.3],
        "GW",
        (34, 197, 94),
        "Demand-management difference: 16.3 GW",
    )
    chart_png(
        ASSETS / "power/generation_mix_chart.png",
        "2038 Rated-Capacity Share",
        ["Renewables", "LNG", "Nuclear", "Coal", "Other"],
        [47, 25, 13, 8, 7],
        "%",
        (34, 197, 94),
        "Report-based policy review; rounded shares",
    )
    chart_png(
        ASSETS / "power/effective_capacity_chart.png",
        "2038 Confirmed Effective Capacity",
        ["Nuclear", "Coal", "LNG", "Renew.", "Storage"],
        [31.7, 22.3, 66.5, 13.3, 10.4],
        "GW",
        (34, 197, 94),
        "Source-derived report values; effective capacity basis",
    )
    matrix_png(
        ASSETS / "power/policy_evidence_matrix.png",
        "Power Policy Evidence Matrix",
        [
            ("Demand", "735.1→624.5 TWh", "report + official-plan review"),
            ("Peak", "145.6→129.3 GW", "source-derived target"),
            ("Grid", "HVDC / 765 kV expansion", "policy roadmap, not built result"),
            ("Storage", "ESS / pumped hydro", "planned capacity, not measured"),
        ],
    )
    chart_png(
        ASSETS / "motor/torque_ripple_comparison.png",
        "Torque Ripple Comparison",
        ["10 kHz", "30 kHz archive"],
        [1.20, 0.20],
        "N·m",
        (167, 139, 250),
        "Existing result archive; provenance conflict retained for the higher-frequency case",
    )
    matrix_png(
        ASSETS / "rf/rf_course_result_matrix.png",
        "RF/Microwave Case Matrix",
        [
            ("270° Microstrip", "Cadence loss/phase archive", "marker at 3.7 GHz, design target 3.5 GHz"),
            ("L-Section", "schematic + Smith movement", "existing Cadence archive"),
            ("Single Stub", "two solution archives", "existing Cadence archive"),
            ("Wilkinson", "S-parameter archive", "3.5 GHz design"),
            ("Branch-Line", "S-parameter archive", "quadrature design"),
        ],
    )
    matrix_png(
        ASSETS / "sensor/rda_csa_bpa_comparison.png",
        "SAR Formation Algorithm Comparison",
        [
            ("RDA", "frequency-domain efficiency", "range migration assumptions"),
            ("CSA", "chirp-scaling correction", "model-dependent phase terms"),
            ("BPA", "time-domain back-projection", "high computation cost"),
        ],
    )
    matrix_png(
        ASSETS / "sensor/gan_vs_diffusion.png",
        "GAN vs Diffusion: Proposal Trade-off",
        [
            ("GAN", "fast inference", "training instability / hallucination risk"),
            ("Diffusion", "iterative denoising", "higher compute and validation burden"),
            ("Physics-Guided", "forward-model constraint", "proposal only"),
        ],
    )


def crop_norm(source: Path, target: Path, bounds: tuple[float, float, float, float]) -> None:
    if not source.exists():
        return
    image = Image.open(source).convert("RGB")
    w, h = image.size
    box = tuple(int(value * axis) for value, axis in zip(bounds, (w, h, w, h)))
    result = image.crop(box)
    result = ImageOps.autocontrast(result, cutoff=0.25)
    if result.width > 1800:
        ratio = 1800 / result.width
        result = result.resize((1800, int(result.height * ratio)), Image.Resampling.LANCZOS)
    mkdir(target.parent)
    result.save(target, optimize=True)


def build_archive_crops() -> None:
    rf = mkdir(ASSETS / "archive/rf")
    power = mkdir(ASSETS / "archive/power")
    crop_specs = [
        (WORK / "rf2/page-09.png", rf / "microstrip_calculator_result.png", (0.31, 0.21, 0.69, 0.50)),
        (WORK / "rf2/page-09.png", rf / "microstrip_cadence_schematic.png", (0.30, 0.54, 0.70, 0.82)),
        (WORK / "rf2/page-10.png", rf / "microstrip_stackup_properties.png", (0.12, 0.00, 0.88, 0.70)),
        (WORK / "rf2/page-12.png", rf / "microstrip_loss_3p7ghz.png", (0.27, 0.08, 0.73, 0.35)),
        (WORK / "rf2/page-12.png", rf / "microstrip_phase_3p7ghz.png", (0.27, 0.34, 0.73, 0.62)),
        (WORK / "rf4/page-15.png", rf / "l_section_circuit_archive.png", (0.24, 0.20, 0.77, 0.51)),
        (WORK / "rf4/page-15.png", rf / "l_section_smith_archive.png", (0.24, 0.56, 0.77, 0.87)),
        (WORK / "rf4/page-19.png", rf / "single_stub_solution1_archive.png", (0.10, 0.10, 0.90, 0.88)),
        (WORK / "rf4/page-20.png", rf / "single_stub_solution2_archive.png", (0.10, 0.10, 0.90, 0.88)),
        (WORK / "rf5/page-15.png", rf / "wilkinson_schematic_archive.png", (0.12, 0.04, 0.88, 0.44)),
        (WORK / "rf5/page-16.png", rf / "wilkinson_sparameter_archive.png", (0.12, 0.18, 0.88, 0.73)),
        (WORK / "rf5/page-18.png", rf / "hybrid_schematic_archive.png", (0.10, 0.10, 0.90, 0.63)),
        (WORK / "rf5/page-19.png", rf / "hybrid_sparameter_archive.png", (0.10, 0.12, 0.90, 0.77)),
        (WORK / "powerline/page-05.png", power / "powerworld_one_line_archive.png", (0.08, 0.43, 0.58, 0.88)),
        (WORK / "powerline/page-06.png", power / "powerworld_case_setup_archive.png", (0.08, 0.20, 0.92, 0.86)),
        (WORK / "powerline/page-07.png", power / "powerworld_nonconvergence_archive.png", (0.10, 0.10, 0.90, 0.58)),
    ]
    for source, target, bounds in crop_specs:
        crop_norm(source, target, bounds)


def requirements_card() -> None:
    image = Image.new("RGB", (1280, 720), "#07111f")
    draw = ImageDraw.Draw(image)
    draw.text((56, 48), "900 W Transformer Design Requirements", fill="#f8fafc", font=font(34, True))
    items = [
        ("Voltage", "220 V → 110 V"),
        ("Output", "900 W"),
        ("Frequency", "300 Hz"),
        ("Core", "Silicon steel"),
        ("Flux Density", "Bm = 1.5 T"),
        ("Selected Case", "UI-100"),
    ]
    for index, (label, value) in enumerate(items):
        col, row = index % 3, index // 3
        x, y = 56 + col * 408, 150 + row * 210
        draw.rounded_rectangle((x, y, x + 370, y + 160), radius=22, fill="#142035", outline="#f59e0b", width=3)
        draw.text((x + 24, y + 28), label, fill="#94a3b8", font=font(18))
        draw.text((x + 24, y + 80), value, fill="#f8fafc", font=font(25, True))
    draw.text((56, 674), "SOURCE-DERIVED REQUIREMENT CARD", fill="#f59e0b", font=font(15, True))
    mkdir(ASSETS / "transformer")
    image.save(ASSETS / "transformer/transformer_requirements_card.png", optimize=True)


def calculator_snapshot_cards() -> None:
    chart_png(
        ASSETS / "calculators/transformer_case_snapshot.png",
        "Transformer Case Calculator",
        ["Efficiency", "Regulation", "Window use"],
        [96.36, 1.136, 31.2],
        "%",
        (245, 158, 11),
        "Verified 900 W report preset",
    )
    chart_png(
        ASSETS / "calculators/zc_sil_calculator_snapshot.png",
        "Transmission-Line Calculator",
        ["|Zc|", "SIL"],
        [265.77, 2202.0],
        "",
        (34, 197, 94),
        "Units: Ω and MW · 765 kV coursework preset",
    )
    chart_png(
        ASSETS / "calculators/motor_pi_calculator_snapshot.png",
        "Motor PI Calculator",
        ["Kpc", "Kic", "Kps", "Kis"],
        [62.83, 314.16, 24.8, 3895.0],
        "",
        (167, 139, 250),
        "Report/source comparison; Kis discrepancy is shown in the live tool",
    )


def copy_motor_archive() -> None:
    source = REPO / "03_motor_control/dc_motor_pi_control/figures/archive"
    target = mkdir(ASSETS / "archive/motor")
    for item in source.glob("*.png"):
        shutil.copy2(item, target / item.name)


def build_hero() -> None:
    width, height = 1600, 760
    image = Image.new("RGB", (width, height), "#06101e")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((40, 40, 1560, 720), radius=40, fill="#0b1728", outline="#28405e", width=3)
    draw.text((92, 92), "Core Electrical Engineering Portfolio", fill="#f8fafc", font=font(46, True))
    draw.text((94, 160), "VHDL · Power · Control · RF · Sensor Systems", fill="#67e8f9", font=font(24, True))
    cards = [
        ("VHDL", "7 / 7 GHDL tests PASS", "#38bdf8"),
        ("POWER", "900 W transformer · 765 kV line", "#f59e0b"),
        ("CONTROL", "Cascaded PI · anti-windup", "#a78bfa"),
        ("RF", "Microstrip · matching · dividers", "#fb7185"),
        ("SENSOR", "AESA–SAR diffusion proposal", "#2dd4bf"),
    ]
    for index, (label, body, colour) in enumerate(cards):
        x = 92 + index * 294
        y = 268
        draw.rounded_rectangle((x, y, x + 260, y + 255), radius=24, fill="#111f33", outline=colour, width=3)
        draw.rectangle((x + 22, y + 24, x + 72, y + 32), fill=colour)
        draw.text((x + 22, y + 62), label, fill="#f8fafc", font=font(23, True))
        for row, fragment in enumerate(lines(body, 18)):
            draw.text((x + 22, y + 118 + row * 35), fragment, fill="#cbd5e1", font=font(18))
    draw.text((94, 615), "Actual archives, portable regressions, independent recalculation, and public boundaries", fill="#cbd5e1", font=font(20))
    draw.text((94, 662), "EVIDENCE-FIRST · BILINGUAL · REPRODUCIBLE", fill="#38bdf8", font=font(16, True))
    target = mkdir(ASSETS / "hero")
    image.save(target / "coursework_portfolio_hero.png", optimize=True)
    image.save(target / "coursework_portfolio_hero.webp", quality=88, method=6)


def manifest() -> None:
    content = """# Generated and source-derived public asset provenance.
assets:
  - id: coursework_hero
    course: portfolio
    title_ko: 전자전기공학 포트폴리오 Hero
    title_en: Core Electrical Engineering Portfolio Hero
    source_file: generated from public portfolio evidence
    source_page: null
    source_type: portfolio_redraw
    evidence_status: Concept Architecture
    public_file: docs/assets/hero/coursework_portfolio_hero.png
    crop_description: none
    privacy_action: no personal data included
    recreated: true
    actual_result: false
    caption_ko: 공개 증거 범주를 결합한 Portfolio Redraw
    caption_en: Portfolio redraw combining public evidence categories
  - id: ghdl_waveforms
    course: controller_logic
    title_ko: GHDL 회귀 파형 7종
    title_en: Seven GHDL Regression Waveforms
    source_file: 00_digital_hardware/controller_logic/results/vcd/*.vcd
    source_page: null
    source_type: reproduced_result
    evidence_status: Portable GHDL Regression Result
    public_file: docs/assets/results/digital/
    crop_description: signals rendered from retained VCD
    privacy_action: regenerated VCD contains no local user path
    recreated: true
    actual_result: true
    caption_ko: 실제 GHDL VCD를 렌더링한 파형
    caption_en: Waveforms rendered from executed GHDL VCD files
  - id: transformer_workbooks
    course: electrical_machines
    title_ko: 변압기 계산기 워크북 스냅샷
    title_en: Transformer Workbook Snapshots
    source_file: audited XLSX workbooks
    source_page: worksheet cells
    source_type: workbook_render
    evidence_status: Workbook Snapshot
    public_file: docs/assets/calculators/transformer_workbook_*.png
    crop_description: rendered from workbook cells, not Excel UI
    privacy_action: workbook metadata and formulas audited; original workbook withheld
    recreated: true
    actual_result: true
    caption_ko: Workbook Snapshot — rendered from workbook cells
    caption_en: Workbook Snapshot — rendered from workbook cells
  - id: motor_archives
    course: motor_control
    title_ko: PSIM·MATLAB 결과 아카이브
    title_en: PSIM and MATLAB Result Archive
    source_file: user-created motor-control report
    source_page: report result pages
    source_type: existing_result_archive
    evidence_status: Existing Result Archive
    public_file: docs/assets/archive/motor/
    crop_description: result regions only
    privacy_action: cover, team names, and local paths excluded
    recreated: false
    actual_result: true
    caption_ko: 기존 보고서에 보존된 결과이며 현재 재실행 결과가 아님
    caption_en: Preserved report result; not rerun in the current environment
  - id: rf_archives
    course: rf_microwave
    title_ko: Cadence 결과 아카이브
    title_en: Cadence Result Archive
    source_file: user-created RF homework reports
    source_page: 9-20 by case
    source_type: existing_result_archive
    evidence_status: Existing Cadence Virtuoso Result Archive
    public_file: docs/assets/archive/rf/
    crop_description: schematic, stackup, Smith chart, and S-parameter regions
    privacy_action: cover, student number, instructor name, and full report excluded
    recreated: false
    actual_result: true
    caption_ko: 3.5 GHz 설계와 3.7 GHz archive marker를 구분함
    caption_en: 3.5 GHz design target kept separate from the 3.7 GHz archive marker
  - id: powerworld_archives
    course: power_systems
    title_ko: PowerWorld 모델·비수렴 결과
    title_en: PowerWorld Model and Non-Convergence Archive
    source_file: user-created transmission-line report
    source_page: 5-7
    source_type: existing_result_archive
    evidence_status: Existing Result Archive
    public_file: docs/assets/archive/power/
    crop_description: one-line, setup, and solver-result regions
    privacy_action: cover, student number, and full report excluded
    recreated: false
    actual_result: true
    caption_ko: 비수렴을 실패가 아니라 모델·solver 경계 증거로 보존
    caption_en: Non-convergence retained as evidence of the model/solver boundary
  - id: sensor_redraws
    course: sensor_applications
    title_ko: AESA–SAR 연구 구조도
    title_en: AESA–SAR Research Redraws
    source_file: user-created proposal report
    source_page: concept sections
    source_type: portfolio_redraw
    evidence_status: Proposal Only
    public_file: docs/assets/sensor/
    crop_description: clean-room redraw
    privacy_action: no report pages or third-party figures copied
    recreated: true
    actual_result: false
    caption_ko: 제안 구조이며 학습 결과나 하드웨어 구현이 아님
    caption_en: Proposal architecture; not a training result or built prototype
"""
    write(ASSETS / "asset_manifest.yaml", content)


def main() -> None:
    for relative, (title, subtitle, nodes, accent) in DIAGRAMS.items():
        flow_svg(ASSETS / relative, title, subtitle, nodes, accent)
    build_code_cards()
    build_waveforms()
    build_charts()
    build_archive_crops()
    requirements_card()
    calculator_snapshot_cards()
    copy_motor_archive()
    build_hero()
    manifest()
    print(f"Built visual portfolio assets under {ASSETS}")


if __name__ == "__main__":
    main()
