from enum import Enum


class EventType(str,Enum):

    COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT: str = 'Cooperative Vulnerability Penetration Assessment(CVPA)'
    COOPERATIVE_VULNERABILITY_INVESTIGATION:str = 'Cooperative Vulnerability Investigation (CVI)'
    VERIFICATION_OF_FIXES:str = 'Verification of Fixes (VOF)'

    @staticmethod
    def getMember(value: str):
        for member in EventType:
            if member.value == value:
                return member