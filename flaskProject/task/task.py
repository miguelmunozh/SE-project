from flaskProject.task.progress import Progress
from flaskProject.task.priority import Priority
from flaskProject.attachment.attachment import Attachment
from datetime import datetime

class Task:

    def __init__(self, title: str, description: str, priority: Priority, progress: Progress, dueDate: datetime,
                 associationToTask: list, analystAssignment: list, collaboratorAssignment: list, archiveStatus: bool, attachment:list = [], id =-1):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__priority = priority
        self.__progress = progress
        self.__dueDate = dueDate
        self.__attachment = attachment
        self.__associationToTask = associationToTask
        self.__analystAssignment = analystAssignment
        self.__collaboratorAssignment = collaboratorAssignment
        self.__archiveStatus = archiveStatus


    def setId(self, id):
        self.__id = id

    def setTitle(self, title: str):
        self.__title = title
        return

    def setDescription(self, description: str):
        self.__description = description
        return

    def setPriority(self, priority: Priority):
        self.__priority = priority
        return

    def setProgress(self, progress: Progress):
        self.__progress = progress
        return

    def setDueDate(self, dueDate: datetime):
        self.__dueDate = dueDate
        return

    def appendAttachment(self, attachment: Attachment):
        self.__attachment.append(attachment)
        return

    def setAssociationToTask(self, associationToTask: list):
        self.__associationToTask = associationToTask
        return

    def setAnalystAssigment(self, analysts: list):
        self.__analystAssignment = analysts
        return

    def setCollaboratorAssignment(self, collaborators: list):
        self.__collaboratorAssignment = collaborators
        return

    def setArchiveStatus(self, status: bool):
        self.__archiveStatus = status
        return




    def getId(self):
        return self.__id

    def getTitle(self):
        return self.__title

    def getDescription(self):
        return self.__description

    def getPriority(self):
        return self.__priority

    def getProgress(self):
        return self.__progress

    def getDueDate(self):
        return self.__dueDate

    def getAttachment(self):
        return self.__attachment

    def getAssociationToTask(self):
        return self.__associationToTask

    def getAnalystAssigment(self):
        return self.__analystAssignment

    def getCollaboratorAssignment(self):
        return self.__collaboratorAssignment

    def getArchiveStatus(self):
        return self.__archiveStatus


    def toDocument(self):
        if self.__id == -1:
            taskDoc = {
                "title": self.__title,
                "description": self.__description,
                "priority": self.__priority,
                "progress": self.__progress,
                "dueDate": self.__dueDate,
                "attachement": self.__attachment,
                "association": self.__associationToTask,
                "analyst_Assignment": self.__analystAssignment,
                "collaborator_Assignment": self.__collaboratorAssignment,
                "archive_status": self.__archiveStatus
            }
            return taskDoc
        else:
            taskDoc = {
                "_id": self.__id,
                "title": self.__title,
                "description": self.__description,
                "priority": self.__priority,
                "progress": self.__progress,
                "dueDate": self.__dueDate,
                "attachement": self.__attachment,
                "association": self.__associationToTask,
                "analyst_Assignment": self.__analystAssignment,
                "collaborator_Assignment": self.__collaboratorAssignment,
                "archive_status": self.__archiveStatus
            }
            return taskDoc

    @staticmethod
    def convertDocument(document):
        return Task(document["title"],
                    document["description"],
                    Priority.getMember(document["priority"]),
                    Progress.getMember(document["progress"]),
                    document["dueDate"],
                    document["attachement"],
                    document["association"],
                    document["analyst_Assignment"],
                    document["collaborator_Assignment"],
                    document["archive_status"],
                    document["_id"])