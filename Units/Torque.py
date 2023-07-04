from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"m2": 1,
               }


class Area(Unit):
    """stores units explicitly for area scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.m2 = value * conversions[unit]
        super().__init__(primary_unit="m2")


