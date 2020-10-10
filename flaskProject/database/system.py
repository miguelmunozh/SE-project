

class System:

    def __init__(self, name: str = "", description: str = "", location: list = [], router: list = [], switch: list = [], room: list = [], testPlan: str = "", archiveStatus: bool = False ):
        self.__id = -1
        self.__name = name
        self.__description = description
        self.__location = location
        self.__router = router
        self.__switch = switch
        self.__room = room
        self.__testPlan = testPlan
        self.__archiveStatus = archiveStatus


    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getLocation(self):
        return self.__location

    def getRouter(self):
        return self.__router

    def getSwitch(self):
        return self.__switch

    def getRoom(self):
        return self.__room

    def getTestPlan(self):
        return self.__testPlan

    def getArchiveStatus(self):
        return self.__archiveStatus


    def setId(self, id):
        self.__id = id

    def setName(self, name: str):
        self.__name = name

    def setDescription(self, description: str):
        self.__description = description

    def setLocation(self, location: list):
        self.__location = location

    def setRouter(self, router: list):
        self.__router = router

    def setSwitch(self, switch: list):
        self.__switch = switch

    def setRoom(self, room: list):
        self.__room = room

    def setTestplan(self, testPlan: str):
        self.__testPlan = testPlan

    def setArchiveStatus(self, archiveStatus: bool):
        self.__archiveStatus = archiveStatus