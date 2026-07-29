#!/usr/bin/env python3
"""Publish manually reviewed, privacy-safe source visuals.

The private source archives remain outside Git. This script copies only a
small, reviewed allow-list from the temporary audit workspace, strips metadata,
and writes public evidence manifests to the correct repositories.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT.parents[1] / "visual_source_audit_20260729" / "audit_state.json"
PPG_REPO = ROOT.parent / "ppg-hrv"
RADAR_REPO = ROOT.parent / "fmcw-radar"

COURSEWORK: dict[str, tuple[str, str, str]] = {
    "COU-436f3751ab76": (
        "docs/gallery/controller-logic/full-adder-hierarchy.png",
        "4-bit ripple-carry adder: VHDL hierarchy and carry-chain mapping",
        "4-bit ripple-carry adder hierarchy and carry-chain mapping in the recovered presentation evidence.",
    ),
    "COU-6f036e432eb9": (
        "docs/gallery/controller-logic/full-adder-waveform.png",
        "4-bit full-adder directed test vectors and Vivado waveform",
        "Directed 4-bit addition cases with expected sum and carry compared against the Vivado waveform.",
    ),
    "COU-406801e8f887": (
        "docs/gallery/controller-logic/decoder-3to8-waveform.png",
        "3-to-8 decoder exhaustive waveform",
        "One-hot decoder outputs over the complete 3-bit input sequence.",
    ),
    "COU-675c2bbfe8b2": (
        "docs/gallery/controller-logic/mealy-101-waveform.png",
        "Overlapping 101 Mealy detector waveform",
        "Annotated state and output transitions for repeated, overlapping 101 input patterns.",
    ),
    "COU-455288b051f9": (
        "docs/gallery/controller-logic/universal-shift-register-waveform.png",
        "Universal shift-register mode waveform",
        "Hold, shift-right, shift-left, and parallel-load behavior annotated against the simulated output.",
    ),
    "COU-86611360e139": (
        "docs/gallery/power-systems/powerworld-baseline-case.png",
        "PowerWorld multi-area baseline model",
        "Source-derived multi-area one-line model used for loading and contingency studies.",
    ),
    "COU-6867edc9efa3": (
        "docs/gallery/power-systems/powerworld-overload-contingency.png",
        "PowerWorld overload and outage case",
        "Source-derived contingency screen retained as diagnostic evidence, not as a validated grid result.",
    ),
    "COU-ff2c82c306c0": (
        "docs/gallery/rf-microwave/microstrip-schematic.png",
        "Cadence microstrip-line schematic",
        "Recovered Cadence schematic for the microstrip transmission-line design case.",
    ),
    "COU-349ce2b220d5": (
        "docs/gallery/rf-microwave/microstrip-stackup-editor.png",
        "Microstrip substrate stack-up definition",
        "Recovered substrate editor showing conductor, alumina dielectric, and ground layers.",
    ),
    "COU-9c54b85fa193": (
        "docs/gallery/rf-microwave/microstrip-response-marker.png",
        "Microstrip AC-response marker",
        "Recovered Cadence response view; the archive marker is reported separately from the 3.5 GHz design target.",
    ),
    "COU-725732f7f445": (
        "docs/gallery/rf-microwave/l-section-schematic.png",
        "L-section impedance-matching schematic",
        "Recovered 1 GHz L-section matching circuit in Cadence.",
    ),
    "COU-38c6b2759b18": (
        "docs/gallery/rf-microwave/l-section-smith-response.png",
        "L-section Smith-chart and S-parameter response",
        "Recovered Smith-chart trajectory and return-loss response for the L-section case.",
    ),
    "COU-8328aad8813a": (
        "docs/gallery/rf-microwave/single-stub-solution-1.png",
        "Single-stub physical solution 1",
        "First recovered single-stub implementation with line and stub parameters.",
    ),
    "COU-c4a72d4144f6": (
        "docs/gallery/rf-microwave/single-stub-solution-2.png",
        "Single-stub physical solution 2",
        "Second recovered single-stub implementation demonstrating the alternative Smith-chart solution.",
    ),
    "COU-fb3ab9fd7b16": (
        "docs/gallery/rf-microwave/wilkinson-schematic.png",
        "Wilkinson divider schematic",
        "Recovered equal-split Wilkinson divider schematic with quarter-wave branches and isolation resistor.",
    ),
    "COU-3b161adce444": (
        "docs/gallery/rf-microwave/wilkinson-sparameter.png",
        "Wilkinson divider S-parameter response",
        "Recovered divider response used to inspect split, match, and isolation behavior.",
    ),
    "COU-3667bbeca788": (
        "docs/gallery/rf-microwave/hybrid-schematic.png",
        "Branch-line quadrature hybrid schematic",
        "Recovered branch-line hybrid topology with four ports and alternating line impedances.",
    ),
    "COU-d94c17e5a33b": (
        "docs/gallery/rf-microwave/hybrid-line-parameter-a.png",
        "Hybrid line-section parameter A",
        "Recovered element-property evidence for one branch-line hybrid transmission-line section.",
    ),
    "COU-f39336d0303a": (
        "docs/gallery/rf-microwave/hybrid-line-parameter-b.png",
        "Hybrid line-section parameter B",
        "Recovered element-property evidence for the complementary branch-line hybrid section.",
    ),
    "COU-74926fa0428e": (
        "docs/gallery/rf-microwave/hybrid-sparameter.png",
        "Quadrature hybrid S-parameter response",
        "Recovered multi-trace S-parameter view for the branch-line hybrid case.",
    ),
}

PPG: dict[str, tuple[str, str, str]] = {
    "PAP-d9c041cadc9d": (
        "docs/figures/results/aggregate-source-evidence/fold5-loss-history.png",
        "Fold 5 training and validation loss history",
        "Aggregate fold-level loss history; no participant-level signal is shown.",
    ),
    "PAP-74643d5699d1": (
        "docs/figures/results/aggregate-source-evidence/synthetic-low-group-hrv.png",
        "Synthetic low-performance subgroup HRV profile",
        "Synthetic subgroup time- and frequency-domain HRV features used to inspect the augmentation distribution.",
    ),
    "PAP-2261a196e6b3": (
        "docs/figures/results/aggregate-source-evidence/group-hrv-boxplots.png",
        "Group-level HRV feature distributions",
        "Aggregate RMSSD, SDNN, HF, and LF/HF distributions by performance group.",
    ),
    "PAP-65e09bf58aee": (
        "docs/figures/results/aggregate-source-evidence/group-hrv-heatmap.png",
        "Group-level mean HRV heat map",
        "Aggregate feature means by performance group; participant-level rows are not exposed.",
    ),
    "PAP-dfbf1b932d3a": (
        "docs/figures/results/aggregate-source-evidence/real-vs-synthetic-boxplots.png",
        "Real-versus-synthetic HRV distribution comparison",
        "Aggregate distribution comparison used to inspect whether synthetic balancing preserved feature ranges.",
    ),
    "PAP-8e2eb45b96d9": (
        "docs/figures/results/aggregate-source-evidence/accuracy-loss-history.png",
        "Training accuracy and loss history",
        "Aggregate model-learning curves without participant-level data.",
    ),
    "PAP-b3549b52d534": (
        "docs/figures/results/aggregate-source-evidence/kfold-confusion-matrix.png",
        "K-fold aggregate confusion matrix",
        "Aggregate class-count matrix across folds; raw subject predictions are not published.",
    ),
}

RADAR: dict[str, tuple[str, str, str]] = {
    "PAP-4cb5fef59360": (
        "docs/figures/paper-source/acquisition-to-aoac-workflow.png",
        "ECG·SCG·Radar 취득부터 AO/AC 비교까지의 논문 워크플로",
        "Paper-source overview from multimodal acquisition through beat alignment, candidate detection, and relative comparison.",
    ),
    "PAP-cab4d8e1222c": (
        "docs/figures/paper-source/ecg-scg-radar-waveform-excerpt.png",
        "동일 시간 구간의 ECG·SCG·Radar 정규화 파형",
        "Paper-source normalized waveform excerpt showing the three modalities on a common time interval.",
    ),
    "PAP-4f8d045cf93e": (
        "docs/figures/paper-source/beat-relative-aoac-landmarks.png",
        "ECG R-peak 기준 ECG·SCG·Radar landmark 예시",
        "Paper-source beat-relative ECG landmarks, SCG fiducials, and radar AO/AC candidate timings.",
    ),
    "PAP-a9b1f8768c0b": (
        "docs/figures/paper-source/scg-radar-relative-timing-boxplot.png",
        "SCG reference 대비 Radar AO/AC 상대 시점 차이",
        "Paper-source distribution of radar-minus-SCG relative AO and AC timing differences.",
    ),
}


def export_image(source: Path, target: Path) -> tuple[int, int]:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        if max(image.size) > 2400:
            image.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
        image.save(target, "PNG", optimize=True)
        return image.size


def publish(
    mapping: dict[str, tuple[str, str, str]],
    repo: Path,
    state: dict[str, Any],
    manifest_path: Path,
) -> None:
    items: list[dict[str, Any]] = []
    for asset_id, (relative, caption_ko, caption_en) in mapping.items():
        source_value = state["extracted_paths"].get(asset_id)
        if not source_value:
            raise KeyError(f"missing extracted source for {asset_id}")
        source = Path(source_value)
        if not source.exists():
            raise FileNotFoundError(source)
        target = repo / relative
        width, height = export_image(source, target)
        items.append(
            {
                "asset_id": asset_id,
                "public_path": relative,
                "width": width,
                "height": height,
                "caption_ko": caption_ko,
                "caption_en": caption_en,
                "source_policy": "Reviewed allow-list; metadata stripped; private archive path withheld",
            }
        )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "generated_by": "scripts/publish_selected_visuals.py",
                "privacy_policy": (
                    "Only reviewed project-level evidence is published. "
                    "Participant-level PPG signals, subject screenshots, student IDs, "
                    "local paths, and third-party teaching materials are excluded."
                ),
                "assets": items,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = parser.parse_args()
    state = json.loads(args.state.read_text(encoding="utf-8"))
    publish(COURSEWORK, ROOT, state, ROOT / "docs" / "gallery" / "visual_evidence_manifest.json")
    publish(
        PPG,
        PPG_REPO,
        state,
        PPG_REPO
        / "docs"
        / "figures"
        / "results"
        / "aggregate-source-evidence"
        / "visual_evidence_manifest.json",
    )
    publish(
        RADAR,
        RADAR_REPO,
        state,
        RADAR_REPO / "docs" / "figures" / "paper-source" / "visual_evidence_manifest.json",
    )
    print(
        "PASS published visuals: "
        f"coursework={len(COURSEWORK)}, ppg={len(PPG)}, radar={len(RADAR)}"
    )


if __name__ == "__main__":
    main()
