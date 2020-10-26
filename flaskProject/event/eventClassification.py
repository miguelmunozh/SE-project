from enum import Enum

class EventClassification(str, Enum):
    TOP_SECRET:str = 'Top secret'
    SECRET:str = 'Secret'
    CONFIDENTIAL:str = 'Confidential'
    CLASSIFIED:str = 'Classified'
    UNCLASSIFIED:str = 'Unclassified'

    @staticmethod
    def getMember(value: str):
        for member in EventClassification:
            if member.value == value:
                return member