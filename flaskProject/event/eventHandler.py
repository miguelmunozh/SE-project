from database.db import Db
from event.event import Event
from event.eventType import EventType
from event.eventClassification import EventClassification


class EventHandler:
    def __init__(self, event = None):
        self.__event = event
        self.__database = Db.getInstance()
        self.__loadEventFromDatabase()

    def getEvent(self):
        return self.__event

    def createEvent(self, analyst, name=None, description=None, type: EventType=EventType.VERIFICATION_OF_FIXES, version=None, date=None,
                    organizationName=None, securityClassificationTitleGuide=None,
                    eventClassification: EventClassification=EventClassification.TOP_SECRET, classifiedBy=None, derivedFrom=None,
                    declassificationDate=None,
                    customerName=None, archiveStatus=None, eventTeam=None):
        event = Event(name=name, description=description, type=type, version=version, date=date,
                      organizationName=organizationName,
                      securityClassificationTitleGuide= securityClassificationTitleGuide,
                      eventClassification=eventClassification, classifiedBy=classifiedBy, derivedFrom=derivedFrom,
                      declassificationDate=declassificationDate, customerName=customerName, archiveStatus=archiveStatus,
                      eventTeam=eventTeam)

        event.setId(self.updateEvent(analyst=analyst, event=event))
        self.__event = event
        return

    def __loadEventFromDatabase(self):
        events = self.__getAllEvents()
        for event in events:
            self.__event = event
            return

    def updateEvent(self, analyst, event):
        eventDoc = event.toDocument()
        analystDoc = analyst.toDocument()
        return self.__database.storeEvent(eventDoc, analystDoc)

    def getEventFromDatabase(self):
        events = self.__getAllEvents()
        for event in events:
            return event


    def __getAllEvents(self):
        docListEvents = self.__database.getAllEvents()
        eventList = []
        for document in docListEvents:
            eventList.append(Event.convertDocument(document))

        return eventList


