from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"m": 1,
               "cm": 0.01,
               "mm": 0.001,
               "km": 1000,
               "mi": 1609.34,
               "ft": 0.3048,
               "inch": 0.0254}


class Length(Unit):
    """stores units explicitly for length scales with attribute style access"""
    # stores the conversions from meter to other units

    def __init__(self, unit, value):
        self.m = value * conversions[unit]
        self.cm = self.m / conversions["cm"]
        self.mm = self.m / conversions["mm"]
        self.km = self.m / conversions["km"]
        self.mi = self.m / conversions["mi"]
        self.ft = self.m / conversions["ft"]
        self.inch = self.m / conversions["inch"]
        super().__init__(primary_unit="m")


