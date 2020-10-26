import unittest
from flaskProject.analyst.analyst import Analyst, Role
from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.event.event import Event
from flaskProject.event.eventClassification import EventClassification
from flaskProject.event.eventType import EventType
from flaskProject.system.system import System, Confidentiality, Availability, Integrity
from flaskProject.task.task import Task, Progress, Priority
from flaskProject.task.subtask import Subtask
from flaskProject.finding.Finding import Finding, FindingClassification, FindingStatus, FindingType

from datetime import datetime, date


class TestDatabaseOperations(unittest.TestCase):

    def test_insertEvent(self):
        database = DatabaseHandler()
        analyst = Analyst("FirstName", "lastname", "initial", "title", Role.LEAD)
        event = Event("EventName"
                      , "description"
                      , EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION
                      , "1.0"
                      , datetime.now().strftime("%m/%d/%Y")
                      , "organization_name"
                      , "security_classification_title_guide"
                      , EventClassification.UNCLASSIFIED
                      , "classifiedBy"
                      , "derivedFrom"
                      , date(2021, 12, 31).strftime("%m/%d/%Y")
                      , "customer name"
                      , False
                      , ["jr", "MM", "cj"])

        database.updateEvent(analyst, event)

        events = database.getAllEvents()
        event2 = events[0]

        self.assertEqual(event.getName(), event2.getName())
        self.assertEqual(event.getDescription(), event2.getDescription())
        self.assertEqual(event.getType(), event2.getType())
        self.assertEqual(event.getDate(), event2.getDate())
        self.assertEqual(event.getOrganizationName(), event2.getOrganizationName())
        self.assertEqual(event.getSecurityClassificationTitleGuide(), event2.getSecurityClassificationTitleGuide())
        self.assertEqual(event.getEventClassification(), event2.getEventClassification())
        self.assertEqual(event.getClassifiedBy(), event2.getClassifiedBy())
        self.assertEqual(event.getDerivedFrom(), event2.getDerivedFrom())
        self.assertEqual(event.getDeclassificationDate(), event2.getDeclassificationDate())
        self.assertEqual(event.getCustomerName(), event2.getCustomerName())
        self.assertEqual(event.getArchiveStatus(), event2.getArchiveStatus())
        self.assertEqual(event.getEventTeam(), event2.getEventTeam())

    def test_insertSystem(self):
        database = DatabaseHandler()
        analyst = Analyst("FirstName", "lastname", "initial", "title", Role.LEAD)
        system = System("systemName", "Description", ["location1", "Location2"], ["switch1", "Switch2"],
                        ["room1", "room2"], "testPlan1", False, Confidentiality.LOW, Integrity.MEDIUM,
                        Availability.HIGH)

        database.updateSystem(analyst, system)

        systems = database.getAllSystems()
        system2 = systems[0]
        self.assertEqual(system.getName(), system2.getName())
        self.assertEqual(system.getDescription(), system2.getDescription())
        self.assertEqual(system.getLocation(), system2.getLocation())
        self.assertEqual(system.getRouter(), system2.getRouter())
        self.assertEqual(system.getSwitch(), system2.getSwitch())
        self.assertEqual(system.getRoom(), system2.getRoom())
        self.assertEqual(system.getTestPlan(), system2.getTestPlan())
        self.assertEqual(system.getArchiveStatus(), system2.getArchiveStatus())
        self.assertEqual(system.getConfidentiality(), system2.getConfidentiality())
        self.assertEqual(system.getIntegrity(), system2.getIntegrity())
        self.assertEqual(system.getAvailability(), system2.getAvailability())

    def test_insertAnalyst(self):
        database = DatabaseHandler()
        analyst = Analyst("FirstName", "lastname", "initial", "title", Role.LEAD)

        database.updateAnalyst(analyst)
        analysts = database.getAllAnalyst()
        analyst2 = analysts[0]

        self.assertEqual(analyst.getFirstName(), analyst2.getFirstName())
        self.assertEqual(analyst.getLastName(), analyst2.getLastName())
        self.assertEqual(analyst.getInitial(), analyst2.getInitial())
        self.assertEqual(analyst.getTitle(), analyst2.getTitle())
        self.assertEqual(analyst.getRole(), analyst2.getRole())

    def test_insertTask(self):
        database = DatabaseHandler()
        analyst = Analyst("FirstName", "lastname", "initial", "title", Role.LEAD)
        task = Task("Title"
                    , "description"
                    , Priority.LOW
                    , Progress.ASSIGNED
                    , date(2021, 12, 31).strftime("%m/%d/%Y")
                    , "attachment"
                    , ["task1", "task2"]
                    , ["analyst1", "analyst2"]
                    , ["collaborator1, collaborator2"]
                    , False)

        database.updateTask(analyst, task)

        tasks = database.getAllTasks()

        task2 = tasks[0]

        self.assertEqual(task.getTitle(), task2.getTitle())
        self.assertEqual(task.getDescription(), task2.getDescription())
        self.assertEqual(task.getPriority(), task2.getPriority())
        self.assertEqual(task.getProgress(), task2.getProgress())
        self.assertEqual(task.getDueDate(), task2.getDueDate())
        self.assertEqual(task.getAttachment(), task2.getAttachment())
        self.assertEqual(task.getAssociationToTask(), task2.getAssociationToTask())
        self.assertEqual(task.getAnalystAssigment(), task2.getAnalystAssigment())
        self.assertEqual(task.getCollaboratorAssignment(), task2.getCollaboratorAssignment())
        self.assertEqual(task.getArchiveStatus(), task2.getArchiveStatus())

    def test_insertSubtask(self):
        database = DatabaseHandler()
        analyst = Analyst("FirstName", "lastname", "initial", "title", Role.LEAD)
        subtask = Subtask("Title"
                          , "description"
                          , Progress.ASSIGNED
                          , date(2021, 12, 31).strftime("%m/%d/%Y")
                          , "attachment"
                          , ["task1", "task2"]
                          , ["analyst1", "analyst2"]
                          , ["collaborator1, collaborator2"]
                          , False)

        database.updateSubtask(analyst, subtask)

        subtasks = database.getAllSubtasks()

        subtask2 = subtasks[0]

        self.assertEqual(subtask.getTitle(), subtask2.getTitle())
        self.assertEqual(subtask.getDescription(), subtask2.getDescription())
        self.assertEqual(subtask.getPriority(), subtask2.getPriority())
        self.assertEqual(subtask.getProgress(), subtask2.getProgress())
        self.assertEqual(subtask.getDueDate(), subtask2.getDueDate())
        self.assertEqual(subtask.getAttachment(), subtask2.getAttachment())
        self.assertEqual(subtask.getAssociationToTask(), subtask2.getAssociationToTask())
        self.assertEqual(subtask.getAnalystAssigment(), subtask2.getAnalystAssigment())
        self.assertEqual(subtask.getCollaboratorAssignment(), subtask2.getCollaboratorAssignment())
        self.assertEqual(subtask.getArchiveStatus(), subtask2.getArchiveStatus())

    def test_insertFinding(self):
        database = DatabaseHandler()
        analyst = Analyst("FirstName", "lastname", "initial", "title", Role.LEAD)

        finding = Finding("hostName"
                          , "IpPort"
                          , "description"
                          , "long_description"
                          , FindingStatus.OPEN
                          , FindingType.AUTHENTICATION_BYPASS
                          , FindingClassification.INFORMATION
                          , ["association1", "association2"]
                          , "evidence"
                          , False)

        database.updateFinding(analyst, finding)

        findings = database.getAllFindings()

        finding2 = findings[0]

        self.assertEqual(finding.getHostName(), finding2.getHostName())
        self.assertEqual(finding.getIpPort(), finding2.getIpPort())
        self.assertEqual(finding.getDescription(), finding2.getDescription())
        self.assertEqual(finding.getLongDescription(), finding2.getLongDescription())
        self.assertEqual(finding.getStatus(), finding2.getStatus())
        self.assertEqual(finding.getClassification(), finding2.getClassification())
        self.assertEqual(finding.getAssociationTo(), finding2.getAssociationTo())
        self.assertEqual(finding.getEvidence(), finding2.getEvidence())
        self.assertEqual(finding.getArchioveStatus(), finding2.getArchioveStatus())
