from flaskProject.database.task import Task
from flaskProject.enumeration.progress import Progress
from datetime import datetime


class Subtask(Task):

    def __init__(self, title: str,
                 description: str,
                 progress: Progress,
                 dueDate: datetime,
                 attachment,
                 associationToTask: list,
                 analystAssignment: list,
                 collaboratorAssignment: list,
                 archiveStatus: bool):

        Task.__init__(title, description, None, progress, dueDate, attachment,
                      associationToTask, analystAssignment, collaboratorAssignment, archiveStatus)