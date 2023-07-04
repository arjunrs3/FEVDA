import unittest

import numpy as np

from Units.Length import Length
from Units.Angle import Angle
from Units.Mass import Mass
from Units.Volume import Volume
from Units.Velocity import Velocity
from Units.AngularVelocity import AngularVelocity
from Units.Force import Force
from Units.Pressure import Pressure
from Units.Power import Power


class UnitsTest(unittest.TestCase):

    def test_length(self):
        l_m = Length("m", 5)
        self.assertTrue(np.isclose(l_m.m, 5))
        self.assertTrue(np.isclose(l_m.cm, 500))
        self.assertTrue(np.isclose(l_m.mm, 5000))
        self.assertTrue(np.isclose(l_m.km, 0.005))
        self.assertTrue(np.isclose(l_m.mi, 0.00310686))
        self.assertTrue(np.isclose(l_m.ft, 16.4042))
        self.assertTrue(np.isclose(l_m.inch, 196.85))

        l_mi = Length("mi", 0.00310686)
        self.assertTrue(np.isclose(l_mi.m, 5))
        self.assertTrue(np.isclose(l_mi.km, 0.005))

        l_addition = l_m + l_mi
        self.assertTrue(np.isclose(l_addition.m, 10))

        l_subtraction = l_addition - l_mi
        self.assertTrue(np.isclose(l_subtraction.m, 5))

    def test_angle(self):
        angle_deg = Angle("deg", 180)
        angle_rad = Angle("rad", np.pi)
        self.assertTrue(np.isclose(angle_deg.rad, angle_rad.rad))
        self.assertTrue(np.isclose(angle_rad.deg, angle_deg.deg))

    def test_mass(self):
        mass_kg = Mass("kg", 5)
        mass_lb = Mass("lb", 11.0231)
        self.assertTrue(np.isclose(mass_kg.kg, mass_lb.kg))
        self.assertTrue(np.isclose(mass_lb.lb, mass_kg.lb))

    def test_volume(self):
        v_m3 = Volume("m3", 5)
        self.assertTrue(np.isclose(v_m3.m3, 5))
        self.assertTrue(np.isclose(v_m3.cm3, 5 * 10 ** 6))
        self.assertTrue(np.isclose(v_m3.ml, 5 * 10 ** 6))
        self.assertTrue(np.isclose(v_m3.liter, 5000))
        self.assertTrue(np.isclose(v_m3.gallon, 1320.86))

    def test_velocity(self):
        v_ms = Velocity("ms", 5)
        v_mph = Velocity("mph", 11.1847)
        self.assertTrue(np.isclose(v_ms.mph, v_mph.mph))

    def test_angular_velocity(self):
        av_rads = AngularVelocity("rads", 5)
        av_degs = AngularVelocity("degs", 286.479)
        self.assertTrue(np.isclose(av_rads.degs, av_degs.degs))

    def test_force(self):
        f_n = Force("N", 5)
        f_lbf = Force("lbf", 1.12404)
        self.assertTrue(np.isclose(f_n.lbf, f_lbf.lbf))

    def test_pressure(self):
        p_pa = Pressure("pa", 5)
        self.assertTrue(np.isclose(p_pa.kpa, 0.005))
        self.assertTrue(np.isclose(p_pa.psi, 0.000725189))
        self.assertTrue(np.isclose(p_pa.bar, 5 * 10 ** -5))

    def test_power(self):
        p_w = Power("W", 5)
        p_kw = Power("kW", 0.005)
        self.assertTrue(np.isclose(p_w.kW, p_kw.kW))


if __name__ == "__main__":
    unittest.main()
