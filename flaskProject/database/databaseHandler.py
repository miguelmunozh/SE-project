from flaskProject.database.analyst import Analyst
from flaskProject.database.event import Event, EventType, EventClassification
from flaskProject.database.db import Db


class DatabaseHandler:
    def __init__(self):
        self.__db = Db.getInstance()
        return

    def updateAnalyst(self, analyst):
        analystDocument = self.__fromAnalystToDocument(analyst)
        self.__db.storeAnalyst( analystDocument)
        return

    def updateEvent(self, event):
        eventDoc = self.__fromEventToDocument(event)
        self.__db.storeEvent(eventDoc)
        return

    def deleteEvent(self, event):
        eventDoc = self.__fromEventToDocument(event)
        self.__db.removeEvent(eventDoc)

        return

    def deleteAnalyst(self, analyst):
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.removeAnalyst(analystDoc)
        return

    def getEvent(self, event):
        eventDoc = self.__fromEventToDocument(event)
        self.__db.findEvent(eventDoc)
        return

    def getAnalyst(self, analyst):
        analystDoc = self.__fromAnalystToDocument(analyst)
        self.__db.findAnalyst(analystDoc)
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
        event.setDate(["date"])
        event.setOrganizationName(document["organizationName"])
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
                "declassificationDate": event.getDeclassificationDate(),
                "customerName": event.getCustomerName(),
                "archiveStatus": event.getArchiveStatus(),
                "eventTeam": event.getEventTeam()
            }
            return eventData

