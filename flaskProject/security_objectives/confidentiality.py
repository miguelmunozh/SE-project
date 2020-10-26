from enum import Enum

class Confidentiality(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"
    INFO: str = "Information"

    @staticmethod
    def getMember(value: str):
        for member in Confidentiality:
            if member.value == value:
                return member