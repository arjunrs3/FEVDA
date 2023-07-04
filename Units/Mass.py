from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"kg": 1,
               "lb": 0.453592,
               }


class Mass(Unit):
    """stores units explicitly for mass scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.kg = value * conversions[unit]
        self.lb = self.kg / conversions["lb"]
        super().__init__(primary_unit="kg")


