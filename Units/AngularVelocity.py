from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"rads": 1,
               "degs": 0.0174533,
               }


class AngularVelocity(Unit):
    """stores units explicitly for angular velocity scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.rads = value * conversions[unit]
        self.degs = self.rads / conversions["degs"]
        super().__init__(primary_unit="rads")


