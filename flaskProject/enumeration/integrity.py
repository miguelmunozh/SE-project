from enum import Enum

class Integrity(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"
    INFO: str = "Information"

    @staticmethod
    def getMember(value: str):
        for member in Integrity:
            if member.value == value:
                return member