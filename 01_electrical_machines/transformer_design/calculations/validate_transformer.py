#!/usr/bin/env python3
"""Independent checks for the source-derived UI-100 transformer result."""

from __future__ import annotations

import json
from pathlib import Path


OUTPUT_W = 900.0
COPPER_LOSS_W = 10.2267
CORE_LOSS_W = 23.7760
REPORTED_TOTAL_LOSS_W = 33.9998
REPORTED_EFFICIENCY_PCT = 96.360
REPORTED_REGULATION_PCT = 1.136


def calculate() -> dict[str, float | str]:
    total_loss = COPPER_LOSS_W + CORE_LOSS_W
    efficiency = 100.0 * OUTPUT_W / (OUTPUT_W + total_loss)
    return {
        "evidence_status": "independent-recalculation",
        "output_w": OUTPUT_W,
        "copper_loss_w": COPPER_LOSS_W,
        "core_loss_w": CORE_LOSS_W,
        "calculated_total_loss_w": total_loss,
        "reported_total_loss_w": REPORTED_TOTAL_LOSS_W,
        "calculated_efficiency_pct": efficiency,
        "reported_efficiency_pct": REPORTED_EFFICIENCY_PCT,
        "reported_regulation_pct": REPORTED_REGULATION_PCT,
    }


def validate(result: dict[str, float | str]) -> None:
    assert abs(float(result["calculated_total_loss_w"]) - REPORTED_TOTAL_LOSS_W) < 0.01
    assert abs(float(result["calculated_efficiency_pct"]) - REPORTED_EFFICIENCY_PCT) < 0.01


if __name__ == "__main__":
    data = calculate()
    validate(data)
    output = Path(__file__).with_name("transformer_validation.json")
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        "PASS transformer: "
        f"loss={data['calculated_total_loss_w']:.4f} W, "
        f"efficiency={data['calculated_efficiency_pct']:.3f}%"
    )
