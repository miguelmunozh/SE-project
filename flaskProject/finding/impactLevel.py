from enum import Enum

class ImpactLevel(int, Enum):
    VH = 5
    H = 4
    M = 3
    L = 2
    VL = 1
    INFORMATION = 0

    @staticmethod
    def getMember(value: int):
        for member in ImpactLevel:
            if member.value == value:
                return member

    def getDisplayValue(self):
        if self.value == 0:
            return "Information"
        elif self.value == 1:
            return "VL"
        elif self.value == 2:
            return "L"
        elif self.value == 3:
            return "M"
        elif self.value == 4:
            return "H"
        elif self.value == 5:
            return "VH"
