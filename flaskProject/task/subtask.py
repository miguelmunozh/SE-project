from task.task import Task
from task.progress import Progress
from datetime import datetime


class Subtask(Task):

    def __init__(self,
                 title: str,
                 description: str,
                 progress: Progress,
                 dueDate: datetime,
                 associationToTask: list,
                 analystAssignment: list,
                 collaboratorAssignment: list,
                 archiveStatus: bool,
                 attachment: list = [],
                 parentId=-1,
                 id=-1):

        super().__init__(title=title, description=description, priority=None, progress=progress, dueDate=dueDate,
                         attachment=attachment,associationToTask=associationToTask, analystAssignment=analystAssignment,
                         collaboratorAssignment=collaboratorAssignment, archiveStatus=archiveStatus,
                         associationToSystem= -1, parentId= parentId, id= id )


    def getParentTask(self):
        pass

    def setParentTask(self, parentTask):
        self.__parentTaskId = parentTask
        return

    def toDocument(self):
        if self.getId() == -1:
            taskDoc = {
                "title": self.getTitle(),
                "description": self.getDescription(),
                "priority": self.getPriority(),
                "progress": self.getProgress(),
                "dueDate": self.getDueDate(),
                "attachment": self.getAttachment(),
                "association": self.getAssociationToTask(),
                "system_Association": self.getAssociationToSystem(),
                "parent_task": self.getParentTask(),
                "analyst_Assignment": self.getAnalystAssigment(),
                "collaborator_Assignment": self.getCollaboratorAssignment(),
                "archive_status": self.getArchiveStatus()
            }
            return taskDoc
        else:
            taskDoc = {
                "_id": self.getId(),
                "title": self.getTitle(),
                "description": self.getDescription(),
                "priority": self.getPriority(),
                "progress": self.getProgress(),
                "dueDate": self.getDueDate(),
                "attachment": self.getAttachment(),
                "association": self.getAssociationToTask(),
                "system_Association": self.getAssociationToSystem(),
                "parent_task": self.getParentTask(),
                "analyst_Assignment": self.getAnalystAssigment(),
                "collaborator_Assignment": self.getCollaboratorAssignment(),
                "archive_status": self.getArchiveStatus()
            }
            return taskDoc

    @staticmethod
    def convertDocument(document):
        return Task(title=document["title"],
                    description=document["description"],
                    priority= document["priority"],
                    progress=Progress.getMember(document["progress"]),
                    dueDate=document["dueDate"],
                    attachment=document["attachment"],
                    associationToTask=document["association"],
                    analystAssignment=document["analyst_Assignment"],
                    collaboratorAssignment=document["collaborator_Assignment"],
                    archiveStatus=document["archive_status"],
                    associationToSystem=document["system_Association"],
                    parentId= document["parent_task"],
                    id=document["_id"])