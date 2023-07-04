from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"rad": 1,
               "deg": 0.0174533,
               }


class Angle(Unit):
    """stores units explicitly for angle scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.rad = value * conversions[unit]
        self.deg = self.rad / conversions["deg"]

        super().__init__(primary_unit="rad")


