from enum import Enum

class Relevance(int, Enum):
    CONFIRMED: int = 4
    EXPECTED: int = 3
    ANTICIPATED: int = 2
    PREDICTED: int = 1
    POSSIBLE: int = 0

    @staticmethod
    def getMember(value: int):
        for member in Relevance:
            if member.value == value:
                return member

    def getDisplayValue(self):
        if self.value == 0:
            return "Possible"
        elif self.value == 1:
            return "Predicted"
        elif self.value == 2:
            return "Anticipated"
        elif self.value == 3:
            return "Expected"
        elif self.value == 4:
            return "Confirmed"