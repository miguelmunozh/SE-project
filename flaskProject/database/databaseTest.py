from database.databaseHandler import DatabaseHandler
from database.event import Event, EventType, EventClassification
from database.analyst import Analyst, Role
from datetime import date
from datetime import datetime

dbHandler = DatabaseHandler()
# analyst = Analyst("jonathan", "roman", "jr", ["jr","sr"], Role.LEAD.value)
# event = Event("eventName",
#              "eventDescription",
#              EventType.VERIFICATION_OF_FIXES.value,
#              "1.0",
#              date(2020, 12, 31).strftime("%m/%d/%Y"),
#              "orgName",
#              "SCTG",
#              EventClassification.UNCLASSIFIED.value,
#              date(2021, 12, 31).strftime("%m/%d/%Y"),
#              "wells Fargo",
#              False,
#              ["jr", "ls", "cj"])

analystList = dbHandler.getAllAnalyst()
eventList = dbHandler.getAllEvents()
# shows that there are 3 events in the db
print(eventList)
analyst = analystList[0]
analyst.setFirstName("joe")
# print(analyst.getId())
# print(analyst.getFirstName())
# print(analyst.getLastName())
# print(analyst.getInitial())
# print(analyst.getRole())
# print(analyst.getTitle())
dbHandler.updateAnalyst(analyst)
event = eventList[0]
print(event.getName())
event.setName("test name")
print(event.getName())
dbHandler.updateEvent(event)
# print(event.getId())
# print(event.getName())
dbHandler.updateEvent(event)


# for analyst in analystList:
#      dbHandler.updateAnalyst(analyst)
# for event in eventList:
#     dbHandler.updateEvent(event)

dbHandler.updateEvent(event)
dbHandler.updateAnalyst(analyst)