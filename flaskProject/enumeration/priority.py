from enum import Enum

class Priority(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"

    @staticmethod
    def getMember(value: str):
        for member in Priority:
            if member.value == value:
                return member
