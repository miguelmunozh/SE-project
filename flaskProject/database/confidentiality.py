from enum import Enum

class Confidentiality(str, Enum):
    LOW: str = "Low"
    MEDIUM: str = "Medium"
    HIGH: str = "High"
    INFO: str = "Information"