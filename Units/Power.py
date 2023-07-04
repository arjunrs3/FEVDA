from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"W": 1,
               "kW": 1000
               }


class Power(Unit):
    """stores units explicitly for power scales with attribute style access"""

    def __init__(self, unit, value):
        self.W = value * conversions[unit]
        self.kW = self.W / conversions["kW"]
        super().__init__(primary_unit="W")


