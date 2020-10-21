from enum import Enum

class Availability(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"
    INFO: str = "Information"