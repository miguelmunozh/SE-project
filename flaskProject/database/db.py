import pymongo
from pymongo import MongoClient
from datetime import date
from database.log import LogEntry
import datetime
import overload


class Db:
    __instance__ = None

    @staticmethod
    def getInstance():
        """ Static method to fetch the current instance.
      """
        if not Db.__instance__:
            Db()
        return Db.__instance__

    def __init__(self):
        """ Constructor.
       """
        if Db.__instance__ is None:
            Db.__instance__ = self
            self.__client = MongoClient(port=27017)
            self.__database = self.__client.FRIC
            self.__analystCollection = self.__database.analyst
            self.__eventCollection = self.__database.event
            self.__systemCollection = self.__database.system
            self.__logCollection = self.__database.log
        else:
            raise Exception("You cannot create another Db class")

    def findAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        return self.__analystCollection.find_one(query)

    def findEvent(self, eventDoc):
        query = {"_id": eventDoc["_id"]}
        return self.__eventCollection.find_one(query)

    def __updateAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        result = self.__analystCollection.find_one_and_replace(query, analystDoc)

    def __updateEvent(self, eventDoc):
        query = {"_id": eventDoc["_id"]}
        result = self.__eventCollection.find_one_and_replace(query, eventDoc)

    def __addNewAnalyst(self, analystDoc):
        insertDocid = self.__analystCollection.insert_one(analystDoc)
        return

    def __logAction(self, logDoc):
        self.__logCollection.insert_one(logDoc)
        return


    def __addNewEvent(self, eventDoc):
        self.__eventCollection.insert_one(eventDoc)
        return

    def __addNewSystem(self, systemDoc):
        self.__systemCollection.insert_one(systemDoc)
        return

    def __updateSystem(self, systemDoc):
        query = {"_id": systemDoc["_id"]}
        result = self.__systemCollection.find_one_and_replace(query, systemDoc)
        return

    def storeSystem(self, systemDoc, analystDoc):
        try:
            self.__addNewSystem(systemDoc)
            self.__logAction(LogEntry("Added new system: " + systemDoc["name"], analystDoc["initial"]).toDocument())
        except pymongo.errors.DuplicateKeyError:
            self.__updateSystem(systemDoc)
            self.__logAction(LogEntry("Updated system: " + systemDoc["name"], analystDoc["initial"]).toDocument())
        return

    def storeAnalyst(self, analystDoc):
        try:
            self.__addNewAnalyst(analystDoc)
        except pymongo.errors.DuplicateKeyError:
            self.__updateAnalyst(analystDoc)
        return

    def storeEvent(self, eventDoc, analystDoc):
        try:
            self.__addNewEvent(eventDoc)
            self.__logAction(LogEntry("Started new event: " + eventDoc["name"], analystDoc["initial"]).toDocument())
        except pymongo.errors.DuplicateKeyError:
            self.__updateEvent(eventDoc)
            self.__logAction(LogEntry("Updated system: " + eventDoc["name"], analystDoc["initial"]).toDocument())

    def getAllAnalyst(self):
        analystList = []
        for document in self.__analystCollection.find():
            analystList.append(document)

        return analystList

    def getAllSystems(self):
        systemList = []
        for document in self.__systemCollection.find():
            systemList.append(document)

        return systemList

    def getAllEvents(self):
        eventList = []
        for document in self.__eventCollection.find():
            eventList.append(document)

        return eventList

    def getAllLogs(self):
        logList = []
        for document in self.__logCollection.find():
            logList.append(document)
        return logList

    def removeEvent(self, eventDoc):
        query = {"_id": eventDoc["_id"]}
        self.__eventCollection.delete_one(query)
        pass

    def removeAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        self.__analystCollection.delete_one(query)
        pass
