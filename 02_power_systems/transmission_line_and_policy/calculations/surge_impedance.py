#!/usr/bin/env python3
"""Recalculate surge impedance, SIL, and line current from report inputs."""

from __future__ import annotations

import json
import math
from pathlib import Path


V_LL_V = 765_000.0
SERIES_REACTANCE_OHM_PER_KM = 0.3
SHUNT_SUSCEPTANCE_S_PER_KM = 4.6e-6


def calculate() -> dict[str, float | str]:
    surge_impedance = math.sqrt(
        SERIES_REACTANCE_OHM_PER_KM / SHUNT_SUSCEPTANCE_S_PER_KM
    )
    sil_w = V_LL_V**2 / surge_impedance
    current_a = sil_w / (math.sqrt(3.0) * V_LL_V)
    return {
        "evidence_status": "independent-recalculation",
        "line_voltage_v": V_LL_V,
        "series_reactance_ohm_per_km": SERIES_REACTANCE_OHM_PER_KM,
        "shunt_susceptance_s_per_km": SHUNT_SUSCEPTANCE_S_PER_KM,
        "surge_impedance_ohm": surge_impedance,
        "sil_mw": sil_w / 1e6,
        "sil_current_a": current_a,
    }


def validate(result: dict[str, float | str]) -> None:
    assert 255.0 < float(result["surge_impedance_ohm"]) < 256.0
    assert 2280.0 < float(result["sil_mw"]) < 2300.0
    assert 1720.0 < float(result["sil_current_a"]) < 1740.0


if __name__ == "__main__":
    data = calculate()
    validate(data)
    output = Path(__file__).with_name("surge_impedance_result.json")
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        "PASS transmission line: "
        f"Zc={data['surge_impedance_ohm']:.2f} ohm, "
        f"SIL={data['sil_mw']:.1f} MW, "
        f"I={data['sil_current_a']:.1f} A"
    )
