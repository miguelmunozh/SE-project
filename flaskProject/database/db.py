import pymongo
from pymongo import MongoClient


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
        else:
            raise Exception("You cannot create another SingletonGovt class")

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

    def __addNewEvent(self, eventDoc):
        self.__eventCollection.insert_one(eventDoc)
        return

    def storeAnalyst(self, analystDoc):
        try:
            self.__addNewAnalyst(analystDoc)
        except pymongo.errors.DuplicateKeyError:
            self.__updateAnalyst(analystDoc)
            return

    def storeEvent(self, eventDoc):
        try:
            self.__addNewEvent(eventDoc)
        except pymongo.errors.DuplicateKeyError:
            self.__updateEvent(eventDoc)

    def getAllAnalyst(self):
        analystList = []
        for document in self.__analystCollection.find():
            analystList.append(document)

        return analystList

    def getAllEvents(self):
        eventList = []
        for document in self.__eventCollection.find():
            eventList.append(document)

        return eventList

    def removeEvent(self, eventDoc):
        query = {"_id": eventDoc["_id"]}
        self.__eventCollection.delete_one(query)
        pass

    def removeAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        self.__analystCollection.delete_one(query)
        pass
