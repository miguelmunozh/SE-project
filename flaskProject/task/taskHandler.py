from task.task import Task
from task.progress import Progress
from task.priority import Priority
from task.task import datetime
from database.db import Db
from analyst.analyst import Analyst

class TaskHandler:
    def __init__(self, task: list = []):
        self.__database = Db.getInstance()
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

        new_task.setId(self.__updateTask(analyst= analyst, task= new_task))
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
        self.__task = self.__getAllTasks()

    def __updateDatabase(self, task: Task, analyst: Analyst):
        id = self.__updateTask(task=task , analyst= analyst)
        return id

    def __getTask(self, task):
        taskDoc = task.toDocument()
        return Task.convertDocument(self.__database.findTask(taskDoc))

    def __getAllTasks(self):
        taskDocList = self.__database.getAllTasks()
        taskList = []
        for document in taskDocList:
            taskList.append(Task.convertDocument(document))
        return taskList

    def __updateTask(self, analyst, task):
        taskDoc = task.toDocument()
        analystDoc = analyst.toDocument()
        item_id = self.__database.storeTask(taskDoc, analystDoc)
        return item_id
