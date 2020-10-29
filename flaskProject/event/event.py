from enum import Enum
from flaskProject.event.eventClassification import EventClassification
from flaskProject.event.eventType import EventType


class Event:
    def __init__(self, name=None, description=None, type=None, version=None, date=None,
                 organizationName=None, securityClassificationTitleGuide=None,
                 eventClassification=None, classifiedBy=None, derivedFrom=None,
                 declassificationDate=None,
                 customerName=None, archiveStatus=None, eventTeam=None):
        self.__id = -1
        self.__name = name
        self.__description = description
        self.__type = type
        self.__version = version
        self.__date = date
        self.__organizationName = organizationName
        self.__securityClassificationTitleGuide = securityClassificationTitleGuide
        self.__eventClassification = eventClassification
        self.__classifiedBy = classifiedBy
        self.__derivedFrom = derivedFrom
        self.__declassificationDate = declassificationDate
        self.__customerName = customerName
        self.__archiveStatus = archiveStatus
        self.__eventTeam = eventTeam
        return

    #  Setters
    def setId(self, id):
        self.__id = id

    def setName(self, name):
        self.__name = name

    def setDescription(self, description):
        self.__description = description

    def setType(self, type=EventType):
        self.__type = type

    def setVersion(self, version):
        self.__version = version

    def setDate(self, dateSelected):
        self.__date = dateSelected

    def setOrganizationName(self, organizationName):
        self.__organizationName = organizationName

    def setSecurityClassificationTitleGuide(self, securityClassificationTitleGuide):
        self.__securityClassificationTitleGuide = securityClassificationTitleGuide

    def setEventClassification(self, eventClassification):
        self.__eventClassification = eventClassification

    def setClassifiedBy(self, classifiedBy):
        self.__classifiedBy = classifiedBy

    def setDerivedFrom(self, derivedFrom):
        self.__derivedFrom = derivedFrom

    def setDeclassificationDate(self, declassificationDate):
        self.__declassificationDate = declassificationDate

    def setCustomerName(self, customerName):
        self.__customerName = customerName

    def setArchiveStatus(self, status=bool):
        self.__archiveStatus = status

    def setEventTeam(self, team):
        self.__eventTeam = team

    # Getters
    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getType(self):
        return self.__type

    def getVersion(self):
        return self.__version

    def getDate(self):
        return self.__date

    def getOrganizationName(self):
        return self.__organizationName

    def getSecurityClassificationTitleGuide(self):
        return self.__securityClassificationTitleGuide

    def getEventClassification(self):
        return self.__eventClassification

    def getClassifiedBy(self):
        return self.__classifiedBy

    def getDerivedFrom(self):
        return self.__derivedFrom

    def getDeclassificationDate(self):
        return self.__declassificationDate

    def getCustomerName(self):
        return self.__customerName

    def getArchiveStatus(self):
        return self.__archiveStatus

    def getEventTeam(self):
        return self.__eventTeam

    def toDocument(self):
        if self.getId() == -1:
            eventData = {
                "name": self.__name,
                "description": self.__description,
                "type": self.__type,
                "version": self.__version,
                "date": self.__date,
                "organizationName": self.__organizationName,
                "securityClassificationTitleGuide": self.__securityClassificationTitleGuide,
                "eventClassification": self.__eventClassification,
                "classifiedBy": self.__classifiedBy,
                "derivedFrom": self.__derivedFrom,
                "declassificationDate": self.__declassificationDate,
                "customerName": self.__customerName,
                "archiveStatus": self.__archiveStatus,
                "eventTeam": self.__eventTeam
            }
            return eventData

        else:
            eventData = {
                "_id": self.__id,
                "name": self.__name,
                "description": self.__description,
                "type": self.__type,
                "version": self.__version,
                "date": self.__version,
                "organizationName": self.__organizationName,
                "securityClassificationTitleGuide": self.__securityClassificationTitleGuide,
                "eventClassification": self.__eventClassification,
                "classifiedBy": self.__classifiedBy,
                "derivedFrom": self.__derivedFrom,
                "declassificationDate": self.__declassificationDate,
                "customerName": self.__customerName,
                "archiveStatus": self.__archiveStatus,
                "eventTeam": self.__eventTeam
            }
            return eventData

    @staticmethod
    def convertDocument(document):
        event = Event()
        event.setId(document["_id"])
        event.setName(document["name"])
        event.setDescription(document["description"])
        event.setType(EventType.getMember(document["type"]))
        event.setVersion(document["version"])
        event.setDate(document["date"])
        event.setOrganizationName(document["organizationName"])
        event.setClassifiedBy(document["classifiedBy"])
        event.setDerivedFrom(document["derivedFrom"])
        event.setSecurityClassificationTitleGuide(document["securityClassificationTitleGuide"])
        event.setEventClassification(EventClassification.getMember(document["eventClassification"]))
        event.setDeclassificationDate(document["declassificationDate"])
        event.setCustomerName(document["customerName"])
        event.setArchiveStatus(document["archiveStatus"])
        event.setEventTeam(document["eventTeam"])
        return event
