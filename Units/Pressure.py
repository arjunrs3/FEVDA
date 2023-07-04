from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"pa": 1,
               "kpa": 1000,
               "psi": 6894.76,
               "bar": 10 ** 5
               }


class Pressure(Unit):
    """stores units explicitly for pressure scales with attribute style access"""

    def __init__(self, unit, value):
        self.pa = value * conversions[unit]
        self.kpa = self.pa / conversions["kpa"]
        self.psi = self.pa / conversions["psi"]
        self.bar = self.pa / conversions["bar"]

        super().__init__(primary_unit="pa")


