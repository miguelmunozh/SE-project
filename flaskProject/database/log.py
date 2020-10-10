import datetime

class LogEntry:

    def __init__(self, action: str = "", initials: str = "", date: datetime = datetime.datetime.now(), logId =-1):
        self.__id = logId
        self.__logtime = date
        self.__actionPerformed = action
        self.__analystInitials = initials

    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def getTime(self):
        return self.__logtime

    def getAction(self):
        return self.__actionPerformed

    def getAnalystInitials(self):
        return self.__analystInitials

    def toDocument(self):
        if self.__id == -1:
            logDoc = {
                "actionPerformed": self.getAction(),
                "analystInitials": self.getAnalystInitials(),
                "logTime": self.getTime().strftime("%m/%d/%Y, %H:%M:%S")
            }
        else:
            logDoc = {
                "_id": self.getId(),
                "actionPerformed": self.getTime(),
                "analystInitials": self.getAnalystInitials(),
                "logTime": self.getTime().strftime("%m/%d/%Y, %H:%M:%S")
            }
        return logDoc
