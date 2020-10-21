from enum import Enum

class Progress(str, Enum):
    NOTSTARTED: str = "Not Started"
    ASSIGNED: str = "Assigned"
    TRANSFERRED: str = "Transferred"
    INPROGRESS: str = "In Progress"
    COMPLETE: str = "Complete"
    NOTAPPLICABLE: str = "Not Applicable"
