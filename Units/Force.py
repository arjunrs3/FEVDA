from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"N": 1,
               "lbf": 4.44822,
               }


class Force(Unit):
    """stores units explicitly for force scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.N = value * conversions[unit]
        self.lbf = self.N / conversions["lbf"]
        super().__init__(primary_unit="N")


