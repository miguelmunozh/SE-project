from flaskProject.task.subtask import Subtask, Progress, datetime
from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.analyst.analyst import Analyst

class SubtaskHandler:

    def __init__(self, subtask= []):
        self.__database = DatabaseHandler()
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
                   attachment,
                   associationToTask: list,
                   analystAssignment: list,
                   collaboratorAssignment: list,
                   archiveStatus: bool,
                   parentTask = -1):

        new_subtask = Subtask(title=title,
                        description=description,
                        progress=progress,
                        dueDate=dueDate,
                        associationToTask=associationToTask,
                        analystAssignment=analystAssignment,
                        collaboratorAssignment=collaboratorAssignment,
                        archiveStatus=archiveStatus, attachment=attachment,
                        parentTask= parentTask)

        new_subtask.setId(self.__database.updateTask(analyst=analyst, task=new_subtask))
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
        self.__subtask = self.__database.getAllSubtasks()

    def __updateDatabase(self, subtask: Subtask, analyst: Analyst):
        id = self.__database.updateSubtask(subTask=subtask, analyst=analyst)
        return id