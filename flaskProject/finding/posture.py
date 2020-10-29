from enum import Enum

class Posture(str, Enum):
    INSIDER: str = "Insider"
    INSIDER_NEARSIDER: str = "Insider_Nearsider"
    OUTSIDER: str = "Outsider"
    NEARSIDER: str = "Nearsider"
    NEARSIDER_OUTSIDER: str = "Nearsider_Outsider"

    @staticmethod
    def getMember(value: str):
        for member in Posture:
            if member.value == value:
                return member