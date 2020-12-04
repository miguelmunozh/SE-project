from enum import Enum
from security_objectives.integrity import Integrity
from security_objectives.availability import Availability
from security_objectives.confidentiality import Confidentiality


class System:

    def __init__(self, name: str = "",
                 description: str = "",
                 location: list = [],
                 router: list = [],
                 switch: list = [],
                 room: list = [],
                 testPlan: str = "",
                 archiveStatus: bool = False,
                 confidentiality: Confidentiality = Confidentiality.INFO,
                 integrity: Integrity = Integrity.INFO,
                 availability: Availability = Availability.INFO, id = -1):

        self.__id = id
        self.__name = name
        self.__description = description
        self.__location = location
        self.__router = router
        self.__switch = switch
        self.__room = room
        self.__testPlan = testPlan
        self.__archiveStatus = archiveStatus
        self.__confidentiality = confidentiality
        self.__integrity = integrity
        self.__availability = availability


    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getLocation(self):
        return self.__location

    def getRouter(self):
        return self.__router

    def getSwitch(self):
        return self.__switch

    def getRoom(self):
        return self.__room

    def getTestPlan(self):
        return self.__testPlan

    def getArchiveStatus(self):
        return self.__archiveStatus

    def getConfidentiality(self):
        return self.__confidentiality

    def getIntegrity(self):
        return self.__integrity

    def getAvailability(self):
        return self.__availability


    def setId(self, id):
        self.__id = id

    def setName(self, name: str):
        self.__name = name

    def setDescription(self, description: str):
        self.__description = description

    def setLocation(self, location: list):
        self.__location = location

    def setRouter(self, router: list):
        self.__router = router

    def setSwitch(self, switch: list):
        self.__switch = switch

    def setRoom(self, room: list):
        self.__room = room

    def setTestplan(self, testPlan: str):
        self.__testPlan = testPlan

    def setArchiveStatus(self, archiveStatus: bool):
        self.__archiveStatus = archiveStatus

    def setConfidentiality(self, confidentiality):
        self.__confidentiality = confidentiality

    def setIntegrity(self, integrity):
        self.__integrity = integrity

    def setAvailability(self, availability):
        self.__availability = availability

    @staticmethod
    def convertDocument(document):

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
        system.setConfidentiality(Confidentiality.getMember(document["confidentiality"]))
        system.setIntegrity(Integrity.getMember(document["integrity"]))
        system.setAvailability(Availability.getMember((document["availability"])))

        return system


    def toDocument(self):
        if self.getId() == -1:
            systemDoc = {
                "name": self.getName(),
                "description": self.getDescription(),
                "location": self.getLocation(),
                "router": self.getRouter(),
                "switch": self.getSwitch(),
                "room": self.getRoom(),
                "testPlan": self.getTestPlan(),
                "archiveStatus": self.getArchiveStatus(),
                "confidentiality": self.getConfidentiality(),
                "integrity": self.getIntegrity(),
                "availability": self.getAvailability()}
            return systemDoc
        else:
            systemDoc = {
                "_id": self.getId(),
                "name": self.getName(),
                "description": self.getDescription(),
                "location": self.getLocation(),
                "router": self.getRouter(),
                "switch": self.getSwitch(),
                "room": self.getRoom(),
                "testPlan": self.getTestPlan(),
                "archiveStatus": self.getArchiveStatus(),
                "confidentiality": self.getConfidentiality(),
                "integrity": self.getIntegrity(),
                "availability": self.getAvailability()
            }
            return systemDoc