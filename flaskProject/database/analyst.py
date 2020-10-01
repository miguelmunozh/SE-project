from enum import Enum

class Role(Enum):
    LEAD = 'lead'
    ANALYST = 'analyst'
    COLLABORATOR = 'collaborator'

class Analyst:

    def __init__(self, firstName = None, lastName = None, initial = None, title = None, role = None):
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

    def setRole(self, role = Role):
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



