from enum import Enum
class FindingClassification(str, Enum):
    VULNERABILITY: str = "Vulnerability"
    INFORMATION: str = "Information"

    @staticmethod
    def getMember(value: str):
        for member in FindingClassification:
            if member.value == value:
                return member