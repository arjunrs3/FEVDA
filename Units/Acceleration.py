from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"ms2": 1
               }


class Acceleration(Unit):
    """stores units explicitly for acceleration scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.ms2 = value * conversions[unit]
        super().__init__(primary_unit="ms2")


