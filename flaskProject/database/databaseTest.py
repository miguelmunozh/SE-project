from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.database.event import Event, EventType, EventClassification
from flaskProject.database.analyst import Analyst, Role
from flaskProject.database.system import System, Availability, Confidentiality, Integrity
from flaskProject.database.log import LogEntry
from datetime import date
from datetime import datetime

dbHandler = DatabaseHandler()


list = dbHandler.getAllSystems()
system = list[0]

print(system.getId())
print(system.getName())
print(system.getLocation())
print(system.getRouter())
print(system.getSwitch())
print(system.getRoom())
print(system.getTestPlan())
print(system.getArchiveStatus())
print(system.getConfidentiality())
print(system.getIntegrity())
print(system.getAvailability())

# log = list2[0]
# log2 = dbHandler.getLogEntry(log)
# system2 = dbHandler.getSystem(system)
# print(log2.getId())
# print(log2.getTime().strftime("%m/%d/%Y, %H:%M:%S"))
# print(log2.getAction())
# print(log2.getAnalystInitials())
# print("**************************")
# print(system2.getId())
# print(system2.getName())
# print(system2.getLocation())
# print(system2.getRouter())
# print(system2.getSwitch())
# print(system2.getRoom())
# print(system2.getTestPlan())
# print(system2.getArchiveStatus())

# initials = []
# for analyst in lists:
#     initials.append(analyst.getInitial())

# print(lists)

# analyst = Analyst("jonathan", "roman", "jr", ["jr","sr"], Role.LEAD.value)
# event = Event("eventName",
#               "eventDescription",
#               EventType.VERIFICATION_OF_FIXES.value,
#               "1.0",
#               date(2020, 12, 31).strftime("%m/%d/%Y"),
#               "orgName",
#               "SCTG",
#               EventClassification.UNCLASSIFIED.value,
#               date(2021, 12, 31).strftime("%m/%d/%Y"),
#               "wells Fargo",
#               False,
#               ["jr, cj"])
#
# system = System("NAME", "DESC", ["loc1" , "loc2"], ["router1", "router2"], ["switch1", "switch2"], ["room1", "room2"], "testPLAN")
# dbHandler.updateEvent(analyst, event)
# dbHandler.updateSystem(analyst, system)

# loglist = dbHandler.getAllLogs()
# for log in loglist:
#     print(log.getId())
#     print(log.getTime().strftime("%m/%d/%Y"))
#     print(log.getAction())
#     print(log.getAnalystInitials())

# systemList = dbHandler.getAllSystems()
# for system in systemList:
#     print(system2.getId())
#     print(system2.getName())
#     print(system2.getLocation())
#     print(system2.getRouter())
#     print(system2.getSwitch())
#     print(system2.getRoom())
#     print(system2.getTestPlan())
#     print(system2.getArchiveStatus())




# analystList = dbHandler.getAllAnalyst()
# eventList = dbHandler.getAllEvents()
# shows that there are 3 events in the db
# print(eventList)
# analyst = analystList[0]
# analyst.setFirstName("joe")
# print(analyst.getId())
# print(analyst.getFirstName())
# print(analyst.getLastName())
# print(analyst.getInitial())
# print(analyst.getRole())
# print(analyst.getTitle())
# dbHandler.updateAnalyst(analyst)
# event = eventList[0]
# print(event.getName())
# event.setName("test name")
# print(event.getName())
# dbHandler.updateEvent(event)
# print(event.getId())
# print(event.getName())
# dbHandler.updateEvent(event)

# for analyst in analystList:
#      dbHandler.updateAnalyst(analyst)
# for event in eventList:
#     dbHandler.updateEvent(event)

# dbHandler.updateEvent(event)
# dbHandler.updateAnalyst(analyst)
