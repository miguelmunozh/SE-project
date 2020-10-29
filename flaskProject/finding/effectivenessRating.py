from enum import Enum

class EffectivenessRating(int, Enum):
    VERYHIGH: int = 10
    HIGH_9: int = 9
    HIGH_8: int = 8
    HIGH_7: int = 7
    MODERATE_6: int = 6
    MODERATE_5: int = 5
    MODERATE_4: int = 4
    LOW_3: int = 3
    LOW_2: int = 2
    LOW_1: int = 1
    VERYLOW_0:int = 0

    @staticmethod
    def getMember(value: int):
        for member in EffectivenessRating:
            if member.value == value:
                return member
