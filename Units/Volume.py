from Units.Unit import Unit

# stores conversions from secondary unit to primary unit
conversions = {"m3": 1,
               "cm3": 1 * 10 ** -6,
               "liter": 0.001,
               "gallon": 0.00378541,
               "ml": 1 * 10 ** -6,
               }


class Volume(Unit):
    """stores units explicitly for volume scales with attribute style access"""

    def __init__(self, unit, value):
        self.m3 = value * conversions[unit]
        self.cm3 = self.m3 / conversions["cm3"]
        self.liter = self.m3 / conversions["liter"]
        self.gallon = self.m3 / conversions["gallon"]
        self.ml = self.m3 / conversions["ml"]
        super().__init__(primary_unit="m3")


