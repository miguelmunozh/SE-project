from enum import Enum
from analyst.role import Role

class Analyst:

    def __init__(self, firstName = None, lastName = None, initial = None, title = None, role:Role = Role.COLLABORATOR):
        self.__id = -1
        self.__firstName = firstName
        self.__lastName = lastName
        self.__initial = initial
        self.__title = title
        self.__role = role

    def setId(self, id):
        self.__id = id

    def setFirstName(self, firstName):
        self.__firstName = firstName

    def setLastName(self, lastName):
        self.__lastName = lastName

    def setInitial(self, initial):
        self.__initial = initial

    def setTitle(self, title):
        self.__title = title

    def setRole(self, role):
        self.__role = role

    #getters

    def getId(self):
        return self.__id

    def getFirstName(self):
        return self.__firstName


    def getLastName(self):
        return self.__lastName

    def getInitial(self):
        return self.__initial

    def getTitle(self):
        return self.__title

    def getRole(self):
        return self.__role


    def toDocument(self):
        if self.getId() == -1:
            analystDoc = {
                "firstName": self.getFirstName(),
                "lastName": self.getLastName(),
                "initial": self.getInitial(),
                "title": self.getTitle(),
                "role": self.getRole()}
            return analystDoc
        else:
            analystDoc = {
                "_id": self.getId(),
                "firstName": self.getFirstName(),
                "lastName": self.getLastName(),
                "initial": self.getInitial(),
                "title": self.getTitle(),
                "role": self.getRole()}
            return analystDoc

    @staticmethod
    def convertDocument(document):

        analyst = Analyst()
        analyst.setId(document["_id"])
        analyst.setFirstName(document["firstName"])
        analyst.setLastName(document["lastName"])
        analyst.setInitial(document["initial"])
        analyst.setTitle(document["title"])
        analyst.setRole(Role.getMember(document["role"]))

        return analyst



