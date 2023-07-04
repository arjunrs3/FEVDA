from abc import ABC


class Unit(ABC):
    def __init__(self, primary_unit: str):
        self.primary_unit = primary_unit

    def __add__(self, other):
        if self.__class__ == other.__class__:
            new_primary_value = getattr(self, self.primary_unit) + getattr(other, other.primary_unit)
            return self.__class__(self.primary_unit, new_primary_value)
        elif isinstance(other, (int, float)):
            new_primary_value = getattr(self, self.primary_unit) + other
            return self.__class__(self.primary_unit, new_primary_value)

    def __sub__(self, other):
        if self.__class__ == other.__class__:
            new_primary_value = getattr(self, self.primary_unit) - getattr(other, other.primary_unit)
            return self.__class__(self.primary_unit, new_primary_value)
        elif isinstance(other, (int, float)):
            new_primary_value = getattr(self, self.primary_unit) - other
            return self.__class__(self.primary_unit, new_primary_value)