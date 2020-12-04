from system.system import System
from security_objectives.confidentiality import Confidentiality
from security_objectives.availability import Availability
from security_objectives.integrity import Integrity
from database.db import Db
from analyst.analyst import Analyst

class SystemHandler:

    def __init__(self, system = []):
        self.__system = system
        self.__database = Db.getInstance()


    def getSystem(self, systemId):
        for item in self.__system:
            if item.getId() == systemId:
                return item

    # return all findings
    def getAllSystems(self):
        return self.__system

    # add a finding to the end of the list
    def appendSystem(self, analyst: Analyst,
                     name: str = "",
                     description: str = "",
                     location: list = [],
                     router: list = [],
                     switch: list = [],
                     room: list = [],
                     testPlan: str = "",
                     archiveStatus: bool = False,
                     confidentiality: Confidentiality = Confidentiality.INFO,
                     integrity: Integrity = Integrity.INFO,
                     availability: Availability = Availability.INFO,
                     id = -1):

        new_system = System(name=name,
                            description=description,
                            location=location,
                            router=router,
                            switch=switch,
                            room=room,
                            testPlan=testPlan,
                            archiveStatus=archiveStatus,
                            confidentiality=confidentiality,
                            integrity=integrity,
                            availability=availability, id=id)

        new_system.setId(self.__updateDatabase(analyst=analyst, system=new_system))
        self.__system.append(new_system)
        return

    # update a specified finding that is in the list
    def updateSystem(self, system: System, analyst: Analyst):

        index = 0
        while index < len(self.__system):
            if self.__system[index].getId() == system.getId():
                self.__system[index] = system
                self.__updateDatabase(system=system, analyst=analyst)
                return
            index += 1

    def loadSystems(self):
        self.__system = self.__getAllSystems()

    def __updateDatabase(self, system: System, analyst: Analyst):
        id = self.__updateSystem(system=system, analyst=analyst)
        return id

    def __getSystem(self, system):
        systemDoc = system.toDocument()
        return System.convertDocument(self.__database.findSystem(systemDoc))

    def __updateSystem(self, analyst, system):
        systemDoc = system.toDocument()
        analystDoc = analyst.toDocument()
        item_id =self.__database.storeSystem(systemDoc, analystDoc)
        return item_id

    def __getAllSystems(self):
        docSystemList = self.__database.getAllSystems()
        systemList = []
        for document in docSystemList:
            systemList.append(System.convertDocument(document))
        return systemList