from enum import Enum
class FindingStatus(str, Enum):
    OPEN: str = "Open"
    CLOSED: str = "Closed"

    @staticmethod
    def getMember(value: str):
        for member in FindingStatus:
            if member.value == value:
                return member
