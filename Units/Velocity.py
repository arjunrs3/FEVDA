from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"ms": 1,
               "mph": 0.44704,
               }


class Velocity(Unit):
    """stores units explicitly for mass scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.ms = value * conversions[unit]
        self.mph = self.ms / conversions["mph"]
        super().__init__(primary_unit="ms")


