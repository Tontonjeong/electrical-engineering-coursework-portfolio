#!/usr/bin/env python3
"""Run all portable calculations and fail fast on any validation error."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = (
    ROOT
    / "01_electrical_machines"
    / "transformer_design"
    / "calculations"
    / "validate_transformer.py",
    ROOT
    / "02_power_systems"
    / "transmission_line_and_policy"
    / "calculations"
    / "surge_impedance.py",
    ROOT
    / "03_motor_control"
    / "dc_motor_pi_control"
    / "calculations"
    / "calculate_pi_gains.py",
    ROOT
    / "03_motor_control"
    / "dc_motor_pi_control"
    / "calculations"
    / "calculate_torque_ripple.py",
)


def main() -> None:
    for script in SCRIPTS:
        print(f"==> {script.relative_to(ROOT)}", flush=True)
        subprocess.run([sys.executable, str(script)], check=True, cwd=ROOT)
    print(f"PASS: {len(SCRIPTS)} calculation modules")


if __name__ == "__main__":
    main()
