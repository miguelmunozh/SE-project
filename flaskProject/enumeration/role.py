from enum import Enum

class Role(str, Enum):
    LEAD: str = "Lead"
    ANALYST: str = "Analyst"
    COLLABORATOR: str = "Collaborator"