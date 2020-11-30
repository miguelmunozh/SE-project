from flaskProject.analyst.analyst import Analyst
from flaskProject.event.event import Event
from flaskProject.log.log import LogEntry
from flaskProject.database.db import Db


class DatabaseHandler:
    def __init__(self):
        self.__db = Db.getInstance()
        return




    def deleteEvent(self, analyst, event):
        eventDoc = event.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.removeEvent(eventDoc, analystDoc)
        return

    def deleteAnalyst(self, analyst):
        analystDoc = analyst.toDocument()
        self.__db.removeAnalyst(analystDoc)
        return


    def deleteSystem(self, analyst, system):
        systemDoc = system.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.removeSystem(systemDoc, analystDoc)
        return

    def deleteTask(self, analyst, task):
        taskDoc = task.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.removeTask(taskDoc, analystDoc)
        return

    def deleteSubtask(self, analyst, subtask):
        subtaskDoc = subtask.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.removeSubtask(subtaskDoc, analystDoc)
        return










