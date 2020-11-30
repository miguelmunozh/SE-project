from flaskProject.database.db import LogEntry
from flaskProject.database.db import Db

class LogHandler:
    def __init__(self):
        self.__log = []
        self.__database = Db.getInstance()
        self.updateLogHandler()

    def updateLogHandler(self):
        self.__log = self.__getAllLogsFromDatabase()
        return

    def getAllLogs(self):
        return self.__log

    def findLogEntry(self, LogEntry):
        return self.__getLogEntry(LogEntry)

    def __getLogEntry(self, logEntry):
        logEntryDoc = logEntry.toDocument()
        return LogEntry.convertDocument(self.__database.findLogEntry(logEntryDoc))

    def __getAllLogsFromDatabase(self):
        docLogList = self.__database.getAllLogs()
        logList = []
        for document in docLogList:
            logList.append(LogEntry.convertDocument(document))
        return logList
