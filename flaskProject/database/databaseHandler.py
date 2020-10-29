from flaskProject.analyst.analyst import Analyst
from flaskProject.analyst.role import Role
from flaskProject.event.event import Event, EventType, EventClassification
from flaskProject.system.system import System
from flaskProject.database.log import LogEntry
from flaskProject.database.db import Db
from flaskProject.task.task import Task
from flaskProject.task.subtask import Subtask
from flaskProject.finding.Finding import Finding
import datetime


class DatabaseHandler:
    def __init__(self):
        self.__db = Db.getInstance()
        return


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
        self.__db.storeSystem(systemDoc, analystDoc)
        return

    def updateTask(self, analyst, task):
        taskDoc = task.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.storeTask(taskDoc, analystDoc)
        return

    def updateSubtask(self, analyst, subTask):
        subtaskDoc = subTask.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.storeSubtask(subtaskDoc, analystDoc)
        return

    def updateFinding(self, analyst, finding):
        findingDoc = finding.toDocument()
        analystDoc = analyst.toDocument()
        self.__db.storeFinding(findingDoc, analystDoc)
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

    # def __fromDocumentToLogEntry(self, document):
    #     log = LogEntry(document["actionPerformed"]
    #                    , document["analystInitials"]
    #                    , datetime.datetime.strptime(document["logTime"], "%m/%d/%Y, %H:%M:%S"), document["_id"])
    #     return log
    #
    #
    # def __fromSystemToDocument(self, system):
    #     if system.getId() == -1:
    #         systemDoc = {
    #             "name": system.getName(),
    #             "description": system.getDescription(),
    #             "location": system.getLocation(),
    #             "router": system.getRouter(),
    #             "switch": system.getSwitch(),
    #             "room": system.getRoom(),
    #             "testPlan": system.getTestPlan(),
    #             "archiveStatus": system.getArchiveStatus(),
    #             "confidentiality": system.getConfidentiality(),
    #             "integrity": system.getIntegrity(),
    #             "availability": system.getAvailability()}
    #         return systemDoc
    #     else:
    #         systemDoc = {
    #             "_id": system.getId(),
    #             "name": system.getName(),
    #             "description": system.getDescription(),
    #             "location": system.getLocation(),
    #             "router": system.getRouter(),
    #             "switch": system.getSwitch(),
    #             "room": system.getRoom(),
    #             "testPlan": system.getTestPlan(),
    #             "archiveStatus": system.getArchiveStatus(),
    #             "confidentiality": system.getConfidentiality(),
    #             "integrity": system.getIntegrity(),
    #             "availability": system.getAvailability()
    #         }
    #         return systemDoc
    #
    # def __fromDocumentToSystem(self, document):
    #
    #     system = System()
    #     system.setId(document["_id"])
    #     system.setName(document["name"])
    #     system.setDescription(document["description"])
    #     system.setRoom(document["room"])
    #     system.setRouter(document["router"])
    #     system.setSwitch(document["switch"])
    #     system.setLocation(document["location"])
    #     system.setTestplan(document["testPlan"])
    #     system.setArchiveStatus(document["archiveStatus"])
    #     system.setConfidentiality(document["confidentiality"])
    #     system.setIntegrity(document["integrity"])
    #     system.setAvailability(document["availability"])
    #
    #     return system
    #
    # def __fromAnalystToDocument(self, analyst):
    #     if analyst.getId() == -1:
    #         analystDoc = {
    #             "firstName": analyst.getFirstName(),
    #             "lastName": analyst.getLastName(),
    #             "initial": analyst.getInitial(),
    #             "title": analyst.getTitle(),
    #             "role": analyst.getRole()}
    #         return analystDoc
    #     else:
    #         analystDoc = {
    #             "_id": analyst.getId(),
    #             "firstName": analyst.getFirstName(),
    #             "lastName": analyst.getLastName(),
    #             "initial": analyst.getInitial(),
    #             "title": analyst.getTitle(),
    #             "role": analyst.getRole()}
    #         return analystDoc
    #
    #
    # def __fromDocumentToAnalyst(self, document):
    #
    #     analyst = Analyst()
    #     analyst.setId(document["_id"])
    #     analyst.setFirstName(document["firstName"])
    #     analyst.setLastName(document["lastName"])
    #     analyst.setInitial(document["initial"])
    #     analyst.setTitle(document["title"])
    #     analyst.setRole(document["role"])
    #
    #     return analyst
    #
    # def __fromDocumentToEvent(self, document):
    #     event = Event()
    #     event.setId(document["_id"])
    #     event.setName(document["name"])
    #     event.setDescription(document["description"])
    #     event.setType(document["type"])
    #     event.setVersion(document["version"])
    #     event.setDate(document["date"])
    #     event.setOrganizationName(document["organizationName"])
    #     event.setClassifiedBy(document["classifiedBy"])
    #     event.setDerivedFrom(document["derivedFrom"])
    #     event.setSecurityClassificationTitleGuide(document["securityClassificationTitleGuide"])
    #     event.setEventClassification(document["eventClassification"])
    #     event.setDeclassificationDate(document["declassificationDate"])
    #     event.setCustomerName(document["customerName"])
    #     event.setArchiveStatus(document["archiveStatus"])
    #     event.setEventTeam(document["eventTeam"])
    #     return event
    #
    # def __fromEventToDocument(self, event):
    #     if event.getId() == -1:
    #         eventData = {
    #             "name": event.getName(),
    #             "description": event.getDescription(),
    #             "type": event.getType(),
    #             "version": event.getVersion(),
    #             "date": event.getDate(),
    #             "organizationName": event.getOrganizationName(),
    #             "securityClassificationTitleGuide": event.getSecurityClassificationTitleGuide(),
    #             "eventClassification": event.getEventClassification(),
    #             "classifiedBy": event.getClassifiedBy(),
    #             "derivedFrom": event.getDerivedFrom(),
    #             "declassificationDate": event.getDeclassificationDate(),
    #             "customerName": event.getCustomerName(),
    #             "archiveStatus": event.getArchiveStatus(),
    #             "eventTeam": event.getEventTeam()
    #         }
    #         return eventData
    #     else:
    #         eventData = {
    #             "_id": event.getId(),
    #             "name": event.getName(),
    #             "description": event.getDescription(),
    #             "type": event.getType(),
    #             "version": event.getVersion(),
    #             "date": event.getDate(),
    #             "organizationName": event.getOrganizationName(),
    #             "securityClassificationTitleGuide": event.getSecurityClassificationTitleGuide(),
    #             "eventClassification": event.getEventClassification(),
    #             "classifiedBy": event.getClassifiedBy(),
    #             "derivedFrom": event.getDerivedFrom(),
    #             "declassificationDate": event.getDeclassificationDate(),
    #             "customerName": event.getCustomerName(),
    #             "archiveStatus": event.getArchiveStatus(),
    #             "eventTeam": event.getEventTeam()
    #         }
    #         return eventData

