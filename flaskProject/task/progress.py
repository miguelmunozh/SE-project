from enum import Enum

class Progress(str, Enum):
    NOT_STARTED: str = "Not Started"
    ASSIGNED: str = "Assigned"
    TRANSFERRED: str = "Transferred"
    IN_PROGRESS: str = "In Progress"
    COMPLETE: str = "Complete"
    NOT_APPLICABLE: str = "Not Applicable"

    @staticmethod
    def getMember(value: str):
        for member in Progress:
            if member.value == value:
                return member
