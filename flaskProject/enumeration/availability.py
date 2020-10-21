from enum import Enum

class Availability(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"
    INFO: str = "Information"

    @staticmethod
    def getMember(value: str):
        for member in Availability:
            if member.value == value:
                return member