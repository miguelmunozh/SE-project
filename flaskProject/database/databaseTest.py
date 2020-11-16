from bson import ObjectId
from PIL import Image

from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.event.event import Event
from flaskProject.event.eventType import EventType
from flaskProject.event.eventClassification import EventClassification
from flaskProject.analyst.analyst import Analyst
from flaskProject.analyst.role import Role
from flaskProject.finding.Finding import Finding
from flaskProject.finding.findingStatus import FindingStatus
from flaskProject.finding.findingType import FindingType
from flaskProject.finding.findingClassification import FindingClassification
from flaskProject.finding.posture import Posture
from flaskProject.finding.relevance import Relevance
from flaskProject.finding.effectivenessRating import EffectivenessRating
from flaskProject.finding.impactLevel import ImpactLevel
from flaskProject.finding.severityCategoryCode import SeverityCategoryCode
from flaskProject.system.system import System, Availability, Confidentiality, Integrity
from datetime import date
from datetime import datetime

from flaskProject.task.priority import Priority
from flaskProject.task.progress import Progress
from flaskProject.task.subtask import Subtask
from flaskProject.task.task import Task
from flaskProject.attachment.attachment import Attachment
from flaskProject.attachment.attachmentHandler import AttachmentHandler

dbHandler = DatabaseHandler()
attHandler = AttachmentHandler()
attHandler.appendAttachment('C:\\Users\\jonat\\Desktop\\software2Team\\flaskProject\\images\\Capture.PNG', "Capture.PNG")
attHandler.find_and_open_attachment("Capture.PNG")
# dbHandler.storeAttachment()

# file = dbHandler.retrieveAttachment()
# Image.open(file).show()
file = dbHandler.findAttachment({"file_name": "Capture.PNG"})

print(type(file))
att = Attachment(attachment=file, file_name="Capture.PNG")
print(file.file_name)
print(type(file._id))
att.viewFile()
# Image.open(file).show()

# list = dbHandler.getAllSystems()
# system = list[0]
#
# print(system.getId())
# print(system.getName())
# print(system.getLocation())
# print(system.getRouter())
# print(system.getSwitch())
# print(system.getRoom())
# print(system.getTestPlan())
# print(system.getArchiveStatus())
# print(system.getConfidentiality())
# print(system.getIntegrity())
# print(system.getAvailability())

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

# analyst = Analyst("jonathan", "roman", "jr", ["jr","sr"], Role.LEAD)
# finding = Finding("form.findingHostName.data",
#                           "form.findingIPPort.data",
#                           "form.findingDescription.data",
#                           FindingStatus.CLOSED,
#                           FindingType.PHYSICAL_SECURITY,
#                           FindingClassification.INFORMATION,
#                           ["jr","sr"],
#                           "form.findingEvidence.data",
#                           False,
#                           Confidentiality.MEDIUM,
#                           Integrity.MEDIUM,
#                           Availability.MEDIUM,
#                           ["jr","sr"],
#                           Posture.NEARSIDER,
#                           "form.mitigationBriefDescription.data",
#                           "form.mitigationLongDescription.data",
#                           Relevance.POSSIBLE,
#                           EffectivenessRating.VERYHIGH,
#                           "form.impactDescription.data",
#                           ImpactLevel.VL,
#                           SeverityCategoryCode.II,
#                           "form.findingLongDescription.data",
#                           ["jr","sr"])
# dbHandler.updateFinding(analyst, finding)
# # finding.setDescription("aasasdsdasd edited description")
# # dbHandler.updateFinding(analyst, finding)
#
# dbHandler.deleteFinding(analyst,finding)

# for log in dbHandler.getAllLogs():
#     print(log.getTime())


# event = Event("eventName",
#               "eventDescription",
#               EventType.VERIFICATION_OF_FIXES,
#               "1.0",
#               date(2020, 12, 31).strftime("%m/%d/%Y"),
#               "orgName",
#               "SCTG",
#               EventClassification.UNCLASSIFIED,
#               date(2021, 12, 31).strftime("%m/%d/%Y"),
#               "wells Fargo",
#               False,
#               ["jr, cj"])
# task = Task("form.taskName.data",
#                     "form.taskDescription.data",
#                     Priority.MEDIUM.value,
#                     Progress.NOT_APPLICABLE.value,
#                     date(2020, 12, 31).strftime("%m/%d/%Y"),
#                     "form.taskAttachment.data",
#                     ["jr, cj"],
#                     ["jr, cj"],
#                     ["jr, cj"],
#                     False)
# dbHandler.updateTask(analyst, task)

# system = System("NAME", "DESC", ["loc1" , "loc2"], ["router1", "router2"], ["switch1", "switch2"], ["room1", "room2"], "testPLAN")
# dbHandler.updateEvent(analyst, event)

# subtask = Subtask("form.subTaskName.data",
#                   "form.subTaskDescription.data",
#                   Progress.NOT_APPLICABLE.value,
#                   date(2020, 12, 31).strftime("%m/%d/%Y"),
#                   "form.subTaskAttachment.data",
#                   ["jr, cj"],
#                   ["jr, cj"],
#                   ["jr, cj"], False)
# dbHandler.updateSubtask(analyst, subtask)
# subtask.setTitle("changed")
# print(subtask.getTitle())

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
