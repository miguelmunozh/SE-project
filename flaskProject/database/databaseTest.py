from bson import ObjectId
from PIL import Image

from system.systemHandler import SystemHandler
from finding.findingHandler import FindingHandler
from task.taskHandler import TaskHandler
from task.subtaskHandler import SubtaskHandler
from log.logHandler import LogHandler
from analyst.analystHandler import AnalystHandler
from event.eventHandler import EventHandler
from log.log import LogEntry

from database.databaseHandler import DatabaseHandler, Db
from event.event import Event
from event.eventType import EventType
from event.eventClassification import EventClassification
from analyst.analyst import Analyst
from analyst.role import Role
from finding.Finding import Finding
from finding.findingStatus import FindingStatus
from finding.findingType import FindingType
from finding.findingClassification import FindingClassification
from finding.posture import Posture
from finding.relevance import Relevance
from finding.effectivenessRating import EffectivenessRating
from finding.impactLevel import ImpactLevel
from finding.severityCategoryCode import SeverityCategoryCode
from system.system import System, Availability, Confidentiality, Integrity
from datetime import date
from datetime import datetime

from task.priority import Priority
from task.progress import Progress
from task.subtask import Subtask
from task.task import Task
from attachment.attachment import Attachment
from attachment.attachmentHandler import AttachmentHandler

# dbHandler = DatabaseHandler()
attHandler = AttachmentHandler()
# attHandler.appendAttachment('C:\\Users\\jonat\\Desktop\\software2Team\\flaskProject\\images\\Capture.PNG', "Capture.PNG")
# attHandler.find_and_open_attachment("Capture.PNG")
# dbHandler.storeAttachment()


analyst = Analyst("jonathan", "roman", "jr", ["jr","sr"], Role.LEAD)

analyst2 = Analyst("jonathan2", "roman2", "jr2", ["jr2","sr2"], Role.COLLABORATOR)

task_handler = TaskHandler()
finding_handler = FindingHandler()
subtask_handler = SubtaskHandler()
system_handler = SystemHandler()
log_handler = LogHandler()
analyst_handler = AnalystHandler()
event_handler = EventHandler()

analyst_handler.appendAnalyst("jonathan3", "roman3", "jr3", ["jr3","sr3"], Role.COLLABORATOR)

analysts = analyst_handler.getAllAnalyst()
for analyst in analysts:
    print(analyst.getFirstName())

# task_handler.appendTask(analyst=analyst,
#                         title="test_title",
#                         description="test_description",
#                         priority=Priority.HIGH,
#                         progress=Progress.ASSIGNED,
#                         dueDate=datetime.today().strftime("%m/%d/%Y"),
#                         associationToTask=[],
#                         analystAssignment= ["jr", "ls"],
#                         collaboratorAssignment=["jK"],
#                         archiveStatus=False,
#                         attachment=[],
#                         associationToSystem= "system_test"
#                         )
# tasks = task_handler.loadTask()
# tasks = task_handler.getAllTask()
# task_id = -1
# for task in tasks:
#     testid = attHandler.appendAttachment('C:\\Users\\jonat\\Desktop\\software2Team\\flaskProject\\images\\Capture.PNG',
#                                          "Capture.PNG")
#     task.appendAttachment(testid)
#     task_handler.updateTask(analyst=analyst, task=task)
#     attHandler.loadAttachments(task.getAttachment())
#     # attHandler.find_and_open_attachment(testid)
#     task_id = task.getId()

# finding_handler.appendFinding(analyst=analyst,
#                               hostName="test_hostname",
#                               ipPort="test_ipPort",
#                               description="test_description",
#                               status=FindingStatus.OPEN,
#                               type=FindingType.AUTHENTICATION_BYPASS,
#                               classification= FindingClassification.INFORMATION,
#                               associationToFinding=["test_association"],
#                               evidence="evidence_test",
#                               archiveStatus=False,
#                               confidentiality=Confidentiality.INFO,
#                               integrity=Integrity.INFO,
#                               availability=Availability.INFO,
#                               analystAssigned=["jr", "jk"],
#                               posture=Posture.INSIDER,
#                               mitigationBriefDescription= "brief_description_test",
#                               mitigationLongDescription= "long_description_test",
#                               relevance=Relevance.CONFIRMED,
#                               countermeasureEffectivenessRating=EffectivenessRating.MODERATE_6,
#                               impactDescription="Impact_description_test",
#                               impactLevel=ImpactLevel.L,
#                               severityCategoryCode=SeverityCategoryCode.III,
#                               longDescription="long_description_test",
#                               collaboratorAssigned= ["Test1", "Test2"]
#                               )
# findings = finding_handler.getAllFindings()
# for finding in findings:
#     finding.setDescription("test_description_2")
#     finding_handler.updateFinding(analyst=analyst, finding=finding)
# finding_handler.loadFindings()
# findings = finding_handler.getAllFindings()
# for finding in findings:
#     finding2 = finding_handler.getFinding(finding.getid())
#     print(finding2.getid())
#     print(finding2.getDescription())

# subtask_handler.appendSubtask(analyst=analyst,
#                               title="test_tittle",
#                               description="test_description",
#                               progress=Progress.IN_PROGRESS,
#                               dueDate=datetime.today().strftime("%m/%d/%Y"),
#                               associationToTask=["test1", "test2"],
#                               analystAssignment=["jr", "ls"],
#                               collaboratorAssignment=["jk", "jr"],
#                               archiveStatus=False)
#
# subtasks = subtask_handler.getAllsubTask()
# for subtask in subtasks:
#     testid = attHandler.appendAttachment('C:\\Users\\jonat\\Desktop\\software2Team\\flaskProject\\images\\Capture.PNG',
#                                          "Capture.PNG")
#     subtask.appendAttachment(testid)
#     subtask_handler.updateSubtask(analyst=analyst, subtask=subtask)
#     attHandler.loadAttachments(subtask.getAttachment())
#     # attHandler.find_and_open_attachment(testid)


# finding_handler.appendFinding(analyst=analyst,
#                               hostName= "hostname_test",
#                               ipPort= "ipPort",
#                               description= "description_test",
#                               status= FindingStatus.OPEN,
#                               type= FindingType.AUTHENTICATION_BYPASS,
#                               classification= FindingClassification.INFORMATION,
#                               associationToFinding=["finding_1","finding_2"],
#                               evidence= [],
#                               archiveStatus=False,
#                               confidentiality=Confidentiality.INFO,
#                               integrity=Integrity.INFO,
#                               availability=Availability.INFO,
#                               analystAssigned=["analyst_1", "analyst_2"],
#                               posture=Posture.INSIDER,
#                               mitigationBriefDescription="mitigation_test",
#                               mitigationLongDescription="mititgation_long_test",
#                               relevance=Relevance.CONFIRMED,
#                               countermeasureEffectivenessRating=EffectivenessRating.LOW_2,
#                               impactDescription="impact_description",
#                               impactLevel=ImpactLevel.L,
#                               severityCategoryCode=SeverityCategoryCode.II,
#                               longDescription="long_description",
#                               collaboratorAssigned=["jk","tr"]
#                               )
#
# findings = finding_handler.getAllFindings()
# for finding in findings:
#     testid = attHandler.appendAttachment('C:\\Users\\jonat\\Desktop\\software2Team\\flaskProject\\images\\Capture.PNG', "Capture.PNG")
#     finding.appendEvidence(testid)
#     finding_handler.updateFinding(analyst=analyst, finding=finding)
#     attHandler.loadAttachments(finding.getAllEvidence())
#     attHandler.find_and_open_attachment(testid)


#
# system_handler.appendSystem(analyst=analyst,
#                             name="test_system",
#                             description="test_description",
#                             location=["location_1", "location_2"],
#                             router=["router_1", "router_2"],
#                             switch=["switch1", "switch2"],
#                             room=["room1, room2"],
#                             testPlan="test_plan_test",
#                             archiveStatus=False,
#                             confidentiality=Confidentiality.INFO,
#                             integrity=Integrity.INFO,
#                             availability=Availability.INFO)
# system_handler.loadSystems()
# systems = system_handler.getAllSystems()
# for system in systems:
#     print(system.getId())
#     system2 = system_handler.getSystem(system.getId())
#     print(system2.getId())
#     system2.setDescription("test_description_3")
#     system_handler.updateSystem(analyst=analyst, system=system2)
# log_handler.updateLogHandler()
# logs = log_handler.getAllLogs()
# # for log in logs:
# #     print(log.getAction())
#
# analysts = analyst_handler.getAllAnalyst()
# for analyst in analysts:
#     print(analyst.getId())
#     print(analyst.setFirstName("test_name"))
#     analyst_handler.updateAnalyst(analyst)
#
# event_handler = EventHandler()
# event = event_handler.getEvent()
# print(event.getId())
# print(event.getName())

# event_handler.createEvent(analyst=analyst, name= "name_test", description= "description",
#                           type= EventType.VERIFICATION_OF_FIXES, version= 1.0,
#                           date= datetime.today().strftime("%m/%d/%Y"), organizationName="org_name",
#                           securityClassificationTitleGuide= "guide", eventClassification=EventClassification.TOP_SECRET,
#                           classifiedBy= ["thisguy", "thatguy"], derivedFrom=["item_derivedby"],
#                           declassificationDate= datetime.today().strftime("%m/%d/%Y"),
#                           customerName="customer_name", archiveStatus=False,
#                           eventTeam=["jr","jt", "ct"])

    # task_handler.updateTask(task = task, analyst= analyst)
# task2 = task_handler.getTask(task_id)
# print(task2.getDescription())

# db =Db()
# finding = {"name": "test",
#            "description": "test"
# }
# db.storeFinding(finding, analyst.toDocument())

# file = dbHandler.retrieveAttachment()
# Image.open(file).show()
# file = dbHandler.findAttachment({"file_name": "Capture.PNG"})
#
# print(type(file))
# att = Attachment(attachment=file, file_name="Capture.PNG")
# print(file.file_name)
# print(type(file._id))
# att.viewFile()
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