from task.progress import Progress
from task.priority import Priority
from attachment.attachment import Attachment
from datetime import datetime

class Task:

    def __init__(self, title: str, description: str, priority: Priority, progress: Progress, dueDate: datetime,
                 associationToTask: list, analystAssignment: list, collaboratorAssignment: list, archiveStatus: bool,associationToSystem , attachment:list = [],parentId = -1 ,id =-1):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__priority = priority
        self.__progress = progress
        self.__dueDate = dueDate
        self.__attachment = attachment
        self.__associatedParent = parentId
        self.__associationToTask = associationToTask
        self.__analystAssignment = analystAssignment
        self.__collaboratorAssignment = collaboratorAssignment
        self.__archiveStatus = archiveStatus
        self.__associationToSystem = associationToSystem


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

    def setAssociatedParent(self, parent_id):
        self.__associatedParent = parent_id
        return

    def setAssociationToSystem(self, associationToSystem):
        self.__associationToSystem = associationToSystem
        return


    def getAssociationToSystem(self):
        return self.__associationToSystem

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

    def getAssociatedParent(self):
        return self.__associatedParent


    def toDocument(self):
        if self.__id == -1:
            taskDoc = {
                "title": self.__title,
                "description": self.__description,
                "priority": self.__priority,
                "progress": self.__progress,
                "dueDate": self.__dueDate,
                "attachment": self.__attachment,
                "association": self.__associationToTask,
                "system_Association": self.__associationToSystem,
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
                "attachment": self.__attachment,
                "association": self.__associationToTask,
                "system_Association": self.__associationToSystem,
                "analyst_Assignment": self.__analystAssignment,
                "collaborator_Assignment": self.__collaboratorAssignment,
                "archive_status": self.__archiveStatus
            }
            return taskDoc

    @staticmethod
    def convertDocument(document):
        return Task(title=document["title"],
                    description=document["description"],
                    priority=Priority.getMember(document["priority"]),
                    progress=Progress.getMember(document["progress"]),
                    dueDate=document["dueDate"],
                    attachment=document["attachment"],
                    associationToTask=document["association"],
                    analystAssignment=document["analyst_Assignment"],
                    collaboratorAssignment=document["collaborator_Assignment"],
                    archiveStatus=document["archive_status"],
                    associationToSystem=document["system_Association"],
                    id=document["_id"])