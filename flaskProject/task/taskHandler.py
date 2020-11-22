from flaskProject.task.task import Task, Progress, Priority, datetime
from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.analyst.analyst import Analyst

class TaskHandler:
    def __init__(self, task: list = []):
        self.__database = DatabaseHandler()
        self.__task = task

    def getTask(self, taskId):
        for item in self.__task:
            if item.getId() == taskId:
                return item

    #return all findings
    def getAllTask(self):
        return self.__task

    #add a finding to the end of the list
    def appendTask(self, analyst, title: str, description: str, priority: Priority, progress: Progress, dueDate: datetime,
                 associationToTask: list, analystAssignment: list, collaboratorAssignment: list, archiveStatus: bool, associationToSystem,attachment:list = [],parentId = -1 ,id =-1):

        new_task = Task(title=title,
                        description= description,
                        priority=priority,
                        progress=progress,
                        dueDate=dueDate,
                        associationToTask=associationToTask,
                        analystAssignment=analystAssignment,
                        collaboratorAssignment=collaboratorAssignment,
                        archiveStatus=archiveStatus, attachment=attachment,
                        parentId=parentId, associationToSystem=associationToSystem,id=id)

        new_task.setId(self.__database.updateTask(analyst= analyst, task= new_task))
        self.__task.append(new_task)
        return

    #update a specified finding that is in the list
    def updateTask(self, task: Task, analyst: Analyst):

        index = 0
        while index < len(self.__task):
            if self.__task[index].getId() == task.getId():
                self.__task[index] = task
                self.__updateDatabase(task= task, analyst=analyst)
                return
            index += 1


    def loadTask(self):
        self.__task = self.__database.getAllTasks()

    def __updateDatabase(self, task: Task, analyst: Analyst):
        id = self.__database.updateTask(task=task , analyst= analyst)
        return id