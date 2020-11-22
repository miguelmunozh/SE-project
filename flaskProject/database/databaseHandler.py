from flaskProject.analyst.analyst import Analyst
from flaskProject.analyst.role import Role
from flaskProject.event.event import Event
from flaskProject.event.eventType import EventType
from flaskProject.event.eventClassification import EventClassification
from flaskProject.system.system import System
from flaskProject.database.log import LogEntry
from flaskProject.database.db import Db
from flaskProject.task.task import Task
from flaskProject.task.subtask import Subtask
from flaskProject.finding.Finding import Finding
from flaskProject.attachment.attachment import Attachment
import datetime


class DatabaseHandler:
    def __init__(self):
        self.__db = Db.getInstance()
        return


    def storeAttachment(self, attachmentPath, file_name: str):
        id = self.__db.insertAttachment(attachmentPath, file_name)
        return id

    def findAttachment(self, attachementQuery):
        file = self.__db.findAttachent(attachementQuery)
        return file

    def retrieveAttachment(self, attachmentID):
        file = self.__db.retrieveAttachment(attachmentID)
        return file

    def findAttachment(self, query: dict):
        file = self.__db.findAttachment(query)
        return file


    def updateAnalyst(self, analyst):
        analystDocument = analyst.toDocument()
        self.__db.storeAnalyst(analystDocument)
        return

    def updateEvent(self, analyst, event):
        eventDoc = event.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.storeEvent(eventDoc, analystDoc)
        return

    def updateSystem(self, analyst, system):
        systemDoc = system.toDocument()
        analystDoc = analyst.toDocument()
        item_id =self.__db.storeSystem(systemDoc, analystDoc)
        return item_id

    def updateTask(self, analyst, task):
        taskDoc = task.toDocument()
        analystDoc = analyst.toDocument()
        item_id = self.__db.storeTask(taskDoc, analystDoc)
        return item_id

    def updateSubtask(self, analyst, subTask):
        subtaskDoc = subTask.toDocument()
        analystDoc = analyst.toDocument()
        item_id = self.__db.storeSubtask(subtaskDoc, analystDoc)
        return item_id

    def updateFinding(self, analyst, finding):
        findingDoc = finding.toDocument()
        analystDoc = analyst.toDocument()
        item_id = self.__db.storeFinding(findingDoc, analystDoc)
        return item_id


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

    def deleteFinding(self, analyst, finding):
        findingDoc = finding.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.removeFinding(findingDoc, analystDoc)
        return

    def getEvent(self, event):
        eventDoc = event.toDocument()
        return Event.convertDocument(self.__db.findEvent(eventDoc))

    def getAnalyst(self, analyst):
        analystDoc = analyst.toDocument()
        return Analyst.convertDocument(self.__db.findAnalyst(analystDoc))


    def getLogEntry(self, logEntry):
        logEntryDoc = logEntry.toDocument()
        return LogEntry.convertDocument(self.__db.findLogEntry(logEntryDoc))


    def getSystem(self, system):
        systemDoc = system.toDocument()
        return System.convertDocument(self.__db.findSystem(systemDoc))

    def getTask(self, task):
        taskDoc = task.toDocument()
        return Task.convertDocument(self.__db.findTask(taskDoc))


    def getSubtask(self, subtask):
        subtaskDoc = subtask.toDocument()
        return Subtask.convertDocument(self.__db.findSubtask(subtaskDoc))


    def getFinding(self, finding):
        findingDoc = finding.toDocument()
        return Finding.convertDocument(self.__db.findFinding(findingDoc))
        pass


    def getAllTasks(self):
        taskDocList = self.__db.getAllTasks()
        taskList = []
        for document in taskDocList:
            taskList.append(Task.convertDocument(document))
        return taskList



    def getAllSubtasks(self):
        subtaskDocList = self.__db.getAllSubtasks()
        subtaskList = []
        for document in subtaskDocList:
            subtaskList.append(Subtask.convertDocument(document))
        return subtaskList


    def getAllFindings(self):
        findingDocList = self.__db.getAllFindings()
        findingList = []
        for document in findingDocList:
            findingList.append(Finding.convertDocument(document))
        return findingList


    def getAllAnalyst(self):
        docListAnalyst = self.__db.getAllAnalyst()
        analystList = []
        for document in docListAnalyst:
            analystList.append(Analyst.convertDocument(document))

        return analystList

    def getAllEvents(self):
        docListEvents = self.__db.getAllEvents()
        eventList = []
        for document in docListEvents:
            eventList.append(Event.convertDocument(document))

        return eventList


    def getAllLogs(self):
        docLogList = self.__db.getAllLogs()
        logList = []
        for document in docLogList:
            logList.append(LogEntry.convertDocument(document))
        return logList


    def getAllSystems(self):
        docSystemList = self.__db.getAllSystems()
        systemList = []
        for document in docSystemList:
            systemList.append(System.convertDocument(document))
        return systemList

