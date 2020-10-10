import datetime

class LogEntry:

    def __init__(self, action: str = "", initials: str = "", date: datetime = datetime.datetime.now()):
        __logId = -1
        __logtime = date
        __actionPerformed = action
        __analystInitials = initials

    def setId(self, id):
        __logId = id

    def getId(self):
        return self.__logId

    def getTime(self):
        return self.__logtime

    def getAction(self):
        return self.__actionPerformed

    def getAnalystInitials(self):
        return self.__analystInitials

    def toDocument(self):
        if self.getId() == -1:
            logDoc = {
                "actionPerformed": self.getTime(),
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
