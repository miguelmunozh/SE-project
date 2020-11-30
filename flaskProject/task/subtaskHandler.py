from flaskProject.task.subtask import Subtask, Progress, datetime
from flaskProject.database.db import Db
from flaskProject.analyst.analyst import Analyst

class SubtaskHandler:

    def __init__(self, subtask= []):
        self.__database = Db.getInstance()
        self.__subtask = subtask

    def getSubtask(self, subtaskId):
        for item in self.__subtask:
            if item.getId() == subtaskId:
                return item

    # return all findings
    def getAllsubTask(self):
        return self.__subtask

    # add a finding to the end of the list
    def appendSubtask(self, analyst: Analyst,
                   title: str,
                   description: str,
                   progress: Progress,
                   dueDate: datetime,
                   associationToTask: list,
                   analystAssignment: list,
                   collaboratorAssignment: list,
                   archiveStatus: bool,
                   attachment = [],
                   parentId = -1):

        new_subtask = Subtask(title=title,
                        description=description,
                        progress=progress,
                        dueDate=dueDate,
                        associationToTask=associationToTask,
                        analystAssignment=analystAssignment,
                        collaboratorAssignment=collaboratorAssignment,
                        archiveStatus=archiveStatus, attachment=attachment,
                        parentId= parentId)

        new_subtask.setId(self.__updateSubtask(analyst=analyst, subTask=new_subtask))
        self.__subtask.append(new_subtask)
        return

    # update a specified finding that is in the list
    def updateSubtask(self, subtask: Subtask, analyst: Analyst):

        index = 0
        while index < len(self.__subtask):
            if self.__subtask[index].getId() == subtask.getId():
                self.__subtask[index] = subtask
                self.__updateDatabase(subtask=subtask, analyst=analyst)
                return
            index += 1

    def loadSubtask(self):
        self.__subtask = self.__getAllSubtasks()

    def __updateDatabase(self, subtask: Subtask, analyst: Analyst):
        id = self.__updateSubtask(subTask=subtask, analyst=analyst)
        return id

    def __updateSubtask(self, analyst, subTask):
        subtaskDoc = subTask.toDocument()
        analystDoc = analyst.toDocument()
        item_id = self.__database.storeSubtask(subtaskDoc, analystDoc)
        return item_id

    def __getSubtask(self, subtask):
        subtaskDoc = subtask.toDocument()
        return Subtask.convertDocument(self.__database.findSubtask(subtaskDoc))

    def __getAllSubtasks(self):
        subtaskDocList = self.__database.getAllSubtasks()
        subtaskList = []
        for document in subtaskDocList:
            subtaskList.append(Subtask.convertDocument(document))
        return subtaskList