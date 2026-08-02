"""Small dependency-free RF study calculations.

These functions return idealized study values, not EM or measurement evidence.
"""

from __future__ import annotations

import cmath
import math


def dbm_to_watt(dbm: float) -> float:
    return 10 ** ((dbm - 30) / 10)


def watt_to_dbm(watt: float) -> float:
    if watt <= 0:
        raise ValueError("watt must be positive")
    return 10 * math.log10(watt * 1000)


def reflection(z_load: complex, z0: float = 50.0) -> dict[str, complex | float]:
    if z0 <= 0 or z_load + z0 == 0:
        raise ValueError("z0 must be positive and ZL + Z0 must be nonzero")
    gamma = (z_load - z0) / (z_load + z0)
    magnitude = abs(gamma)
    return {
        "gamma": gamma,
        "return_loss_db": math.inf if magnitude == 0 else -20 * math.log10(magnitude),
        "vswr": math.inf if magnitude >= 1 else (1 + magnitude) / (1 - magnitude),
    }


def quarter_wave(z0: float, z_load: float, frequency_hz: float, epsilon_eff: float) -> dict[str, float]:
    if min(z0, z_load, frequency_hz, epsilon_eff) <= 0 or epsilon_eff < 1:
        raise ValueError("positive impedance/frequency and epsilon_eff >= 1 required")
    wavelength = 299_792_458 / (frequency_hz * math.sqrt(epsilon_eff))
    return {"impedance_ohm": math.sqrt(z0 * z_load), "length_m": wavelength / 4}


def cascade_noise_figure(stages: list[tuple[float, float]]) -> float:
    """Return total NF in dB for (gain_dB, NF_dB) stages."""
    if not stages:
        raise ValueError("at least one stage is required")
    total_factor = 10 ** (stages[0][1] / 10)
    preceding_gain = 10 ** (stages[0][0] / 10)
    for gain_db, nf_db in stages[1:]:
        total_factor += (10 ** (nf_db / 10) - 1) / preceding_gain
        preceding_gain *= 10 ** (gain_db / 10)
    return 10 * math.log10(total_factor)


def equal_split(input_dbm: float, outputs: int, extra_loss_db: float = 0.0) -> float:
    if outputs < 2 or extra_loss_db < 0:
        raise ValueError("outputs >= 2 and nonnegative extra loss required")
    return input_dbm - 10 * math.log10(outputs) - extra_loss_db


def unequal_wilkinson(z0: float, power_ratio_p2_p3: float) -> dict[str, float]:
    if z0 <= 0 or power_ratio_p2_p3 <= 0:
        raise ValueError("z0 and power ratio must be positive")
    k = math.sqrt(power_ratio_p2_p3)
    return {
        "k": k,
        "z02_ohm": z0 * math.sqrt(k * (1 + k * k)),
        "z03_ohm": z0 * math.sqrt((1 + k * k) / k**3),
        "resistor_ohm": z0 * (k + 1 / k),
    }


def smith_coordinates(z_load: complex, z0: float = 50.0) -> tuple[float, float]:
    gamma = reflection(z_load, z0)["gamma"]
    assert isinstance(gamma, complex)
    return abs(gamma), math.degrees(cmath.phase(gamma))


if __name__ == "__main__":
    print("20 dBm =", dbm_to_watt(20), "W")
    print("50-to-100 ohm quarter-wave =", quarter_wave(50, 100, 3.5e9, 6))
