from flaskProject.analyst.analyst import Analyst, Role
from flaskProject.database.db import Db

class AnalystHandler:
    def __init__(self):
        self.__database = Db.getInstance()
        self.__analyst = []
        self.__analyst = self.__getAllAnalyst()

    def getAllAnalyst(self):
        return self.__analyst

    def appendAnalyst(self, firstName = None, lastName = None, initial = None, title = None, role:Role = Role.COLLABORATOR, id = -1 ):
        analyst = Analyst(firstName=firstName, lastName= lastName, initial=initial, title=title, role=role, id=id )
        analyst.setId(self.__updateAnalyst(analyst.toDocument()))
        self.__analyst.append(analyst)

    def loadAllAnalystFromDatabase(self):
        self.__analyst = self.__getAllAnalyst()

    def __updateAnalyst(self, analyst):
        analystDocument = analyst.toDocument()
        self.__database.storeAnalyst(analystDocument)
        return

    def getAnalyst(self, analyst):
        analystDoc = analyst.toDocument()
        return Analyst.convertDocument(self.__database.findAnalyst(analystDoc))

    def __getAllAnalyst(self):
        docListAnalyst = self.__database.getAllAnalyst()
        analystList = []
        for document in docListAnalyst:
            analystList.append(Analyst.convertDocument(document))

        return analystList