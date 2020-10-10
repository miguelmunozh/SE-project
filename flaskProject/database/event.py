from enum import Enum


class EventType(Enum):
    COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT = 'Cooperative Vulnerability Penetration Assessment(CVPA)'
    COOPERATIVE_VULNERABILITY_INVESTIGATION = 'Cooperative Vulnerability Investigation (CVI)'
    VERIFICATION_OF_FIXES = 'Verification of Fixes (VOF)'


class EventClassification(Enum):
    TOP_SECRET = 'Top secret'
    SECRET = 'Secret'
    CONFIDENTIAL = 'Confidential'
    CLASSIFIED = 'Classified'
    UNCLASSIFIED = 'Unclassified'


class Event:

    def __init__(self, name=None, description=None, type=None, version=None, date=None,
                 organizationName=None, securityClassificationTitleGuide=None,
                 eventClassification=None, declassificationDate=None,
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

    def getDeclassificationDate(self):
        return self.__declassificationDate

    def getCustomerName(self):
        return self.__customerName

    def getArchiveStatus(self):
        return self.__archiveStatus

    def getEventTeam(self):
        return self.__eventTeam
