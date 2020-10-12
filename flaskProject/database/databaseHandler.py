from flaskProject.database.analyst import Analyst
from flaskProject.database.event import Event, EventType, EventClassification
from flaskProject.database.system import System
from flaskProject.database.log import LogEntry
from flaskProject.database.db import Db
import datetime


class DatabaseHandler:
    def __init__(self):
        self.__db = Db.getInstance()
        return


    def updateAnalyst(self, analyst):
        analystDocument = self.__fromAnalystToDocument(analyst)
        self.__db.storeAnalyst(analystDocument)
        return

    def updateEvent(self, analyst, event):
        eventDoc = self.__fromEventToDocument(event)
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.storeEvent(eventDoc, analystDoc)
        return

    def updateSystem(self, analyst, system):
        systemDoc = self.__fromSystemToDocument(system)
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.storeSystem(systemDoc, analystDoc)

    def deleteEvent(self, analyst, event):
        eventDoc = self.__fromEventToDocument(event)
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.removeEvent(eventDoc, analystDoc)
        return

    def deleteAnalyst(self, analyst):
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.removeAnalyst(analystDoc)
        return

    def getEvent(self, event):
        eventDoc = self.__fromEventToDocument(event)
        return self.__fromDocumentToEvent(self.__db.findEvent(eventDoc))

    def getAnalyst(self, analyst):
        analystDoc = self.__fromAnalystToDocument(analyst)
        return self.__fromDocumentToAnalyst(self.__db.findAnalyst(analystDoc))

    def deleteSystem(self, analyst, system):
        systemDoc = self.__fromSystemToDocument(system)
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.removeSystem(systemDoc, analystDoc)
        return


    def getAllAnalyst(self):
        docListAnalyst = self.__db.getAllAnalyst()
        analystList = []
        for document in docListAnalyst:
            analystList.append(self.__fromDocumentToAnalyst(document))

        return analystList

    def getAllEvents(self):
        docListEvents = self.__db.getAllEvents()
        eventList = []
        for document in docListEvents:
            eventList.append(self.__fromDocumentToEvent(document))

        return eventList

    def getLogEntry(self, logEntry):
        logEntryDoc = logEntry.toDocument()
        return self.__fromDocumentToLogEntry(self.__db.findLogEntry(logEntryDoc))


    def getSystem(self, system):
        systemDoc = self.__fromSystemToDocument(system)
        return self.__fromDocumentToSystem(self.__db.findSystem(systemDoc))


    def getAllLogs(self):
        docLogList = self.__db.getAllLogs()
        logList = []
        for document in docLogList:
            logList.append(self.__fromDocumentToLogEntry(document))
        return logList

    def getAllSystems(self):
        docSystemList = self.__db.getAllSystems()
        systemList = []
        for document in docSystemList:
            systemList.append(self.__fromDocumentToSystem(document))
        return systemList

    def __fromDocumentToLogEntry(self, document):
        log = LogEntry(document["actionPerformed"]
                       , document["analystInitials"]
                       , datetime.datetime.strptime(document["logTime"], "%m/%d/%Y, %H:%M:%S"), document["_id"])
        return log


    def __fromSystemToDocument(self, system):
        if system.getId() == -1:
            systemDoc = {
                "name": system.getName(),
                "description": system.getDescription(),
                "location": system.getLocation(),
                "router": system.getRouter(),
                "switch": system.getSwitch(),
                "room": system.getRoom(),
                "testPlan": system.getTestPlan(),
                "archiveStatus": system.getArchiveStatus(),
                "confidentiality": system.getConfidentiality(),
                "integrity": system.getIntegrity(),
                "availability": system.getAvailability()}
            return systemDoc
        else:
            systemDoc = {
                "_id": system.getId(),
                "name": system.getName(),
                "description": system.getDescription(),
                "location": system.getLocation(),
                "router": system.getRouter(),
                "switch": system.getSwitch(),
                "room": system.getRoom(),
                "testPlan": system.getTestPlan(),
                "archiveStatus": system.getArchiveStatus(),
                "confidentiality": system.getConfidentiality(),
                "integrity": system.getIntegrity(),
                "availability": system.getAvailability()
            }
            return systemDoc

    def __fromDocumentToSystem(self, document):

        system = System()
        system.setId(document["_id"])
        system.setName(document["name"])
        system.setDescription(document["description"])
        system.setRoom(document["room"])
        system.setRouter(document["router"])
        system.setSwitch(document["switch"])
        system.setLocation(document["location"])
        system.setTestplan(document["testPlan"])
        system.setArchiveStatus(document["archiveStatus"])
        system.setConfidentiality(document["confidentiality"])
        system.setIntegrity(document["integrity"])
        system.setAvailability(document["availability"])

        return system

    def __fromAnalystToDocument(self, analyst):
        if analyst.getId() == -1:
            analystDoc = {
                "firstName": analyst.getFirstName(),
                "lastName": analyst.getLastName(),
                "initial": analyst.getInitial(),
                "title": analyst.getTitle(),
                "role": analyst.getRole()}
            return analystDoc
        else:
            analystDoc = {
                "_id": analyst.getId(),
                "firstName": analyst.getFirstName(),
                "lastName": analyst.getLastName(),
                "initial": analyst.getInitial(),
                "title": analyst.getTitle(),
                "role": analyst.getRole()}
            return analystDoc


    def __fromDocumentToAnalyst(self, document):

        analyst = Analyst()
        analyst.setId(document["_id"])
        analyst.setFirstName(document["firstName"])
        analyst.setLastName(document["lastName"])
        analyst.setInitial(document["initial"])
        analyst.setTitle(document["title"])
        analyst.setRole(document["role"])

        return analyst

    def __fromDocumentToEvent(self, document):
        event = Event()
        event.setId(document["_id"])
        event.setName(document["name"])
        event.setDescription(document["description"])
        event.setType(document["type"])
        event.setVersion(document["version"])
        event.setDate(document["date"])
        event.setOrganizationName(document["organizationName"])
        event.setClassifiedBy(document["classifiedBy"])
        event.setDerivedFrom(document["derivedFrom"])
        event.setSecurityClassificationTitleGuide(document["securityClassificationTitleGuide"])
        event.setEventClassification(document["eventClassification"])
        event.setDeclassificationDate(document["declassificationDate"])
        event.setCustomerName(document["customerName"])
        event.setArchiveStatus(document["archiveStatus"])
        event.setEventTeam(document["eventTeam"])
        return event

    def __fromEventToDocument(self, event):
        if event.getId() == -1:
            eventData = {
                "name": event.getName(),
                "description": event.getDescription(),
                "type": event.getType(),
                "version": event.getVersion(),
                "date": event.getDate(),
                "organizationName": event.getOrganizationName(),
                "securityClassificationTitleGuide": event.getSecurityClassificationTitleGuide(),
                "eventClassification": event.getEventClassification(),
                "classifiedBy": event.getClassifiedBy(),
                "derivedFrom": event.getDerivedFrom(),
                "declassificationDate": event.getDeclassificationDate(),
                "customerName": event.getCustomerName(),
                "archiveStatus": event.getArchiveStatus(),
                "eventTeam": event.getEventTeam()
            }
            return eventData
        else:
            eventData = {
                "_id": event.getId(),
                "name": event.getName(),
                "description": event.getDescription(),
                "type": event.getType(),
                "version": event.getVersion(),
                "date": event.getDate(),
                "organizationName": event.getOrganizationName(),
                "securityClassificationTitleGuide": event.getSecurityClassificationTitleGuide(),
                "eventClassification": event.getEventClassification(),
                "classifiedBy": event.getClassifiedBy(),
                "derivedFrom": event.getDerivedFrom(),
                "declassificationDate": event.getDeclassificationDate(),
                "customerName": event.getCustomerName(),
                "archiveStatus": event.getArchiveStatus(),
                "eventTeam": event.getEventTeam()
            }
            return eventData

