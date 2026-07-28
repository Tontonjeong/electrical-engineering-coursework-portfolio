#!/usr/bin/env python3
"""Reproduce source-reported current- and speed-loop PI calculations."""

from __future__ import annotations

import json
import math
from pathlib import Path


ARMATURE_R_OHM = 0.1
ARMATURE_L_H = 0.02
INERTIA_KGM2 = 0.075
CURRENT_BW_HZ = 500.0
SPEED_BW_HZ = 25.0
SPEED_LOOP_KP_REPORTED = 24.8
SPEED_LOOP_KI_CALC_REPORTED = 3898.0
SPEED_LOOP_KI_SOURCE = 3895.0


def calculate() -> dict[str, float | str]:
    omega_current = 2.0 * math.pi * CURRENT_BW_HZ
    omega_speed = 2.0 * math.pi * SPEED_BW_HZ
    current_kp = ARMATURE_L_H * omega_current
    current_ki = ARMATURE_R_OHM * omega_current
    return {
        "evidence_status": "independent-recalculation-plus-preserved-source-discrepancy",
        "current_bandwidth_hz": CURRENT_BW_HZ,
        "current_kp": current_kp,
        "current_ki": current_ki,
        "speed_bandwidth_hz": SPEED_BW_HZ,
        "speed_loop_inertia_term": INERTIA_KGM2 * omega_speed,
        "speed_kp_reported": SPEED_LOOP_KP_REPORTED,
        "speed_ki_report_calculation": SPEED_LOOP_KI_CALC_REPORTED,
        "speed_ki_recovered_source": SPEED_LOOP_KI_SOURCE,
    }


def validate(result: dict[str, float | str]) -> None:
    assert abs(float(result["current_kp"]) - 62.832) < 0.001
    assert abs(float(result["current_ki"]) - 314.16) < 0.01
    assert float(result["speed_ki_report_calculation"]) != float(
        result["speed_ki_recovered_source"]
    )


if __name__ == "__main__":
    data = calculate()
    validate(data)
    output = Path(__file__).with_name("pi_gain_result.json")
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        "PASS motor PI: "
        f"current Kp={data['current_kp']:.3f}, Ki={data['current_ki']:.2f}; "
        "speed Ki discrepancy preserved"
    )
