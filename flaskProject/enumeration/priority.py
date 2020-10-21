from enum import Enum

class Priority(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"
