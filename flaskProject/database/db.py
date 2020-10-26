import pymongo
from pymongo import MongoClient
from datetime import date
from flaskProject.database.log import LogEntry
import datetime


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
            self.__taskCollection = self.__database.task
            self.__subtaskCollection = self.__database.subtask
            self.__findingCollection = self.__database.finding
            self.__logCollection = self.__database.log
        else:
            raise Exception("You cannot create another Db class")

    def findAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        return self.__analystCollection.find_one(query)


    def findSystem(self, systemDoc):
        query = {"_id": systemDoc["_id"]}
        return self.__systemCollection.find_one(query)


    def findLogEntry(self, logDoc):
        query = {"_id": logDoc["_id"]}
        return self.__logCollection.find_one(query)


    def findEvent(self, eventDoc):
        query = {"_id": eventDoc["_id"]}
        return self.__eventCollection.find_one(query)


    def findTask(self, taskDoc):
        query = {"_id": taskDoc}
        return self.__taskCollection.find_one(query)


    def findSubtask(self, subtaskDoc):
        query = {"_id": subtaskDoc}
        return self.__subtaskCollection.find_one(query)


    def findFinding(self, findingDoc):
        query = {"_id": findingDoc}
        return self.__findingCollection.find_one(query)


    def __updateTask(self, taskDoc):
        query = {"_id": taskDoc}
        self.__taskCollection.find_one_and_replace(query, taskDoc)
        return


    def __updateSubtask(self, subtaskDoc):
        query = {"_id": subtaskDoc}
        self.__subtaskCollection.find_one_and_replace(query, subtaskDoc)
        return


    def __updateFinding(self, findingDoc):
        query = {"_id": findingDoc}
        self.__findingCollection.find_one_and_replace(query, findingDoc)
        return


    def __updateAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        result = self.__analystCollection.find_one_and_replace(query, analystDoc)
        return


    def __updateEvent(self, eventDoc):
        query = {"_id": eventDoc["_id"]}
        result = self.__eventCollection.find_one_and_replace(query, eventDoc)
        return


    def __updateSystem(self, systemDoc):
        query = {"_id": systemDoc["_id"]}
        result = self.__systemCollection.find_one_and_replace(query, systemDoc)
        return



    def __logAction(self, logDoc):
        self.__logCollection.insert_one(logDoc)
        return


    def __addNewAnalyst(self, analystDoc):
        insertDocid = self.__analystCollection.insert_one(analystDoc)
        return


    def __addNewTask(self, taskDoc):
        insertDocid = self.__taskCollection.insert_one(taskDoc)
        return


    def __addNewSubtask(self, subtaskDoc):
        insertDocid = self.__subtaskCollection.insert_one(subtaskDoc)
        return


    def __addNewFinding(self, findingDoc):
        insertDocid = self.__findingCollection.insert_one(findingDoc)
        return


    def __addNewEvent(self, eventDoc):
        self.__eventCollection.insert_one(eventDoc)
        return


    def __addNewSystem(self, systemDoc):
        self.__systemCollection.insert_one(systemDoc)
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
            self.__logAction(LogEntry("Added new event: " + eventDoc["name"], analystDoc["initial"]).toDocument())
        except pymongo.errors.DuplicateKeyError:
            self.__updateEvent(eventDoc)
            self.__logAction(LogEntry("Updated event: " + eventDoc["name"], analystDoc["initial"]).toDocument())
        return

    def storeTask(self, taskDoc, analystDoc):
        try:
            self.__addNewTask(taskDoc)
            self.__logAction(LogEntry("Added new task: " + taskDoc["title"], analystDoc["initial"]).toDocument())
        except pymongo.errors.DuplicateKeyError:
            self.__updateTask(taskDoc)
            self.__logAction(LogEntry("Updated task: " + taskDoc["title"], analystDoc["initial"]).toDocument())
        return


    def storeSubtask(self, subtaskDoc, analystDoc):
        try:
            self.__addNewSubtask(subtaskDoc)
            self.__logAction(LogEntry("Added new subtask: " + subtaskDoc["title"], analystDoc["initial"]).toDocument())
        except pymongo.errors.DuplicateKeyError:
            self.__updateSubtask(subtaskDoc)
            self.__logAction(LogEntry("Updated subtask: " + subtaskDoc["title"], analystDoc["initial"]).toDocument())
        return


    def storeFinding(self, findingDoc, analystDoc):
        try:
            self.__addNewFinding(findingDoc)
            self.__logAction(LogEntry("Added new finding: " + findingDoc["description"], analystDoc["initial"]).toDocument())
        except pymongo.errors.DuplicateKeyError:
            self.__updateFinding(findingDoc)
            self.__logAction(LogEntry("Updated finding: " + findingDoc["description"], analystDoc["initial"]).toDocument())
        return


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


    def getAllTasks(self):
        taskList = []
        for document in self.__taskCollection.find():
            taskList.append(document)

        return taskList


    def getAllSubtasks(self):
        subtaskList = []
        for document in self.__subtaskCollection.find():
            subtaskList.append(document)

        return subtaskList


    def getAllFindings(self):
        findingsList = []
        for document in self.__findingCollection.find():
            findingsList.append(document)

        return findingsList


    def getAllLogs(self):
        logList = []
        for document in self.__logCollection.find():
            logList.append(document)

        return logList


    def removeEvent(self, eventDoc, analystDoc):
        query = {"_id": eventDoc["_id"]}
        self.__eventCollection.delete_one(query)
        self.__logAction(LogEntry("Deleted event: " + eventDoc["name"], analystDoc["initial"]).toDocument())
        return


    def removeAnalyst(self, analystDoc):
        query = {"_id": analystDoc["_id"]}
        self.__analystCollection.delete_one(query)
        return


    def removeSystem(self, systemDoc, analystDoc):
        query = {"_id": systemDoc["_id"]}
        self.__systemCollection.delete_one(query)
        self.__logAction(LogEntry("Deleted system: " + systemDoc["name"], analystDoc["initial"]).toDocument())
        return


    def removeTask(self, taskDoc, analystDoc):
        query = {"_id": taskDoc["_id"]}
        self.__taskCollection.delete_one(query)
        self.__logAction(LogEntry("Deleted task: " + taskDoc["name"], analystDoc["initial"]).toDocument())
        return


    def removeSubtask(self, subtaskDoc, analystDoc):
        query = {"_id": subtaskDoc["_id"]}
        self.__subtaskCollection.delete_one(query)
        self.__logAction(LogEntry("Deleted subtask: " + subtaskDoc["name"], analystDoc["initial"]).toDocument())
        return


    def removeFinding(self, findingDoc, analystDoc):
        query = {"_id": findingDoc["_id"]}
        self.__findingCollection.delete_one(query)
        self.__logAction(LogEntry("Deleted finding: " + findingDoc["name"], analystDoc["initial"]).toDocument())
        return


