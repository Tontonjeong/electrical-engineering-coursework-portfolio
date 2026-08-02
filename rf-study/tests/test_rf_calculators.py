import importlib.util
import math
import unittest
from pathlib import Path


MODULE = Path(__file__).parents[1] / "calculators" / "rf_calculators.py"
SPEC = importlib.util.spec_from_file_location("rf_calculators", MODULE)
rf = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(rf)


class RFCalculatorTests(unittest.TestCase):
    def test_dbm(self):
        self.assertAlmostEqual(rf.dbm_to_watt(20), 0.1)
        self.assertAlmostEqual(rf.watt_to_dbm(1), 30)

    def test_reflection(self):
        result = rf.reflection(100 + 0j)
        self.assertAlmostEqual(abs(result["gamma"]), 1 / 3)
        self.assertAlmostEqual(result["vswr"], 2)

    def test_quarter_wave(self):
        result = rf.quarter_wave(50, 100, 3.5e9, 6)
        self.assertAlmostEqual(result["impedance_ohm"], math.sqrt(5000))

    def test_noise_figure(self):
        self.assertAlmostEqual(rf.cascade_noise_figure([(15, 2), (10, 8)]), 2.437315, places=5)

    def test_splits(self):
        self.assertAlmostEqual(rf.equal_split(20, 2), 16.9897, places=4)
        result = rf.unequal_wilkinson(50, 1)
        self.assertAlmostEqual(result["z02_ohm"], math.sqrt(5000))
        self.assertAlmostEqual(result["z03_ohm"], math.sqrt(5000))
        self.assertAlmostEqual(result["resistor_ohm"], 100)


if __name__ == "__main__":
    unittest.main()
