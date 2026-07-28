#!/usr/bin/env python3
"""Calculate the two source-reported torque-ripple cases."""

from __future__ import annotations

import csv
from pathlib import Path


TORQUE_CONSTANT_NM_PER_A = 1.9
CASES = (
    ("10 kHz", 1.2, "FAIL"),
    ("30 kHz report text", 0.2, "PASS"),
)


def calculate() -> list[dict[str, str | float]]:
    return [
        {
            "case": label,
            "current_ripple_a": current_ripple,
            "torque_ripple_nm": TORQUE_CONSTANT_NM_PER_A * current_ripple,
            "reported_decision": decision,
        }
        for label, current_ripple, decision in CASES
    ]


if __name__ == "__main__":
    rows = calculate()
    assert abs(float(rows[0]["torque_ripple_nm"]) - 2.28) < 1e-9
    assert abs(float(rows[1]["torque_ripple_nm"]) - 0.38) < 1e-9
    output = Path(__file__).with_name("torque_ripple_result.csv")
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("PASS torque ripple: 2.28 N m (FAIL), 0.38 N m (PASS)")
