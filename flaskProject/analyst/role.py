from enum import Enum

class Role(str, Enum):
    LEAD: str = "Lead"
    ANALYST: str = "Analyst"
    COLLABORATOR: str = "Collaborator"

    @staticmethod
    def getMember(value: str):
        for member in Role:
            if member.value == value:
                return member