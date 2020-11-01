from flask_wtf import FlaskForm, validators
from wtforms import *
from wtforms.validators import DataRequired, IPAddress, Optional
from wtforms.fields.html5 import DateField
from security_objectives.integrity import Integrity
from security_objectives.availability import Availability
from security_objectives.confidentiality import Confidentiality
from event.eventClassification import EventClassification
from event.eventType import EventType
from analyst.role import Role
from task.progress import Progress
from task.priority import Priority
from finding.findingStatus import FindingStatus
from finding.findingType import FindingType
from finding.findingClassification import FindingClassification
from finding.posture import Posture
from finding.relevance import Relevance
from finding.effectivenessRating import EffectivenessRating
from finding.impactLevel import ImpactLevel
from finding.severityCategoryCode import SeverityCategoryCode

# These forms are created using flask-wdt (need pip installation)
# each form creates the fields we need for the form, we still need the html file and each form is represented as a class


class SetupContentViewForm(FlaskForm):
    # field to input a string with the label of 'Event Name'
    SUCVInitials = StringField('Initials', validators=[DataRequired()])
    SUCVSelection = SelectField('Select an option',
                                choices=[('create', 'Create a new event (any existing event will be archived.'),
                                         ('sync', 'First time sync with lead analyst.')])
    SUCVIpAddress = StringField('Lead Analyst Ip Address')


class CreateEventForm(FlaskForm):
    # field to input a string with the label of 'Event Name'
    EventName = StringField('Event Name', validators=[DataRequired()])
    EventDescription = StringField('Event Description')

    EventType = SelectField('Event Type',
                            choices=[(EventType.COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT.value,
                                      "Cooperative Vulnerability Penetration Assessment"),
                                     (EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION.value,
                                      "Cooperative Vulnerability Investigation"),
                                     (EventType.VERIFICATION_OF_FIXES.value, "Verification Of Fixes")],
                            validators=[DataRequired()])
    OrganizationName = StringField('Organization Name', validators=[DataRequired()])
    CustomerName = StringField('Customer Name', validators=[DataRequired()])
    AssessmentDate = DateField('Assessment Date', validators=[DataRequired()])
    DeclassificationDate = DateField('Declassification Date', validators=[DataRequired()])
    SCTG = StringField('Security Classification Title Guide', validators=[DataRequired()])
    EventClassification = SelectField('Event Classification',
                                      choices=[(EventClassification.TOP_SECRET.value,
                                                "Top Secret"),
                                               (EventClassification.SECRET.value, "Secret"),
                                               (EventClassification.CONFIDENTIAL.value,
                                                "Confidential"),
                                               (EventClassification.CLASSIFIED.value,
                                                "Classified"),
                                               (EventClassification.UNCLASSIFIED.value,
                                                "Unclassified")],
                                      validators=[DataRequired()])
    # For event team in event class
    EventLeadAnalysts = StringField('Event Lead Analysts', validators=[DataRequired()])
    EventAnalysts = StringField('Event Analysts', validators=[DataRequired()])

    EventClassifiedBy = StringField('Classified by', validators=[DataRequired()])
    EventDerivedFrom = StringField('Derived from', validators=[DataRequired()])


class EditEventForm(FlaskForm):
    EditEventName = StringField('Event Name')
    EditEventDescription = StringField('Event Description')
    EditEventVersion = StringField('Event Version', validators=[DataRequired()])
    EditEventType = SelectField('Event Type',
                                choices=[(EventType.COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT.value,
                                          "Cooperative Vulnerability Penetration Assessment"),
                                         (EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION.value,
                                          "Cooperative Vulnerability Investigation"),
                                         (EventType.VERIFICATION_OF_FIXES.value, "Verification Of Fixes")],
                                validators=[DataRequired()])
    EditEventOrganizationName = StringField('Organization Name')
    EditEventCustomerName = StringField('Customer name')
    # EditEventAssessmentDate = DateField('Assessment date')
    EditEventDeclassificationDate = DateField('Declassification date')
    EditEventSCTG = StringField('Security Classification Title Guide')
    EditEventClassification = SelectField('Event Classification',
                                          choices=[(EventClassification.TOP_SECRET.value,
                                                    "Top Secret"),
                                                   (EventClassification.SECRET.value, "Secret"),
                                                   (EventClassification.CONFIDENTIAL.value,
                                                    "Confidential"),
                                                   (EventClassification.CLASSIFIED.value,
                                                    "Classified"),
                                                   (EventClassification.UNCLASSIFIED.value,
                                                    "Unclassified")])
    EditEventClassifiedBy = StringField('Classified by')
    EditEventDerivedFrom = StringField('Derived from')


class CreateAnalystForm(FlaskForm):
    CreateAnalystFName = StringField('Analyst First Name', validators=[DataRequired()])
    CreateAnalystLName = StringField('Analyst Last Name')
    CreateAnalystInitials = StringField('Initials', validators=[DataRequired()])
    CreateAnalystRole = SelectField('Analyst role',
                                    choices=[(Role.ANALYST.value, Role.ANALYST.name),
                                             (Role.LEAD.value, Role.LEAD.name),
                                             (Role.COLLABORATOR.value, Role.COLLABORATOR.name)],
                                    validators=[DataRequired()])


class EditAnalystForm(FlaskForm):
    EditAnalystFName = StringField('Analyst First Name', validators=[DataRequired()])
    EditAnalystLName = StringField('Analyst Last Name')
    EditAnalystInitials = StringField('Initials', validators=[DataRequired()])
    EditAnalystRole = SelectField('Analyst role',
                                  choices=[(Role.ANALYST.value, Role.ANALYST.name),
                                           (Role.LEAD.value, Role.LEAD.name),
                                           (Role.COLLABORATOR.value, Role.COLLABORATOR.name)],
                                  validators=[DataRequired()])


class CreateSystemForm(FlaskForm):
    systemName = StringField("System Name", validators=[DataRequired()])
    systemDescription = StringField("system Description")
    systemLocation = StringField("System Location", validators=[DataRequired()])
    systemRouter = StringField("System Router", validators=[DataRequired()])
    systemSwitch = StringField("System Switch", validators=[DataRequired()])
    systemRoom = StringField("System Room", validators=[DataRequired()])
    systemTestPlan = StringField("System Test Plan", validators=[DataRequired()])
    # this one is for the button in system view, set as default at creation
    # archiveStatus = StringField()

    systemConfidentiality = SelectField("System Confidentiality",
                                        choices=[(Confidentiality.LOW.value, "Low"),
                                                 (Confidentiality.MEDIUM.value, "Medium"),
                                                 (Confidentiality.HIGH.value, "High"),
                                                 (Confidentiality.INFO.value, "Info")],
                                        validators=[DataRequired()])
    systemIntegrity = SelectField("System Integrity",
                                  choices=[(Integrity.LOW.value, "Low"),
                                           (Integrity.MEDIUM.value, "Medium"),
                                           (Integrity.HIGH.value, "High"),
                                           (Integrity.INFO.value, "Info")],
                                  validators=[DataRequired()])
    systemAvailability = SelectField("System Availability",
                                     choices=[(Availability.LOW.value, "Low"),
                                              (Availability.MEDIUM.value, "Medium"),
                                              (Availability.HIGH.value, "High"),
                                              (Availability.INFO.value, "Info")],
                                     validators=[DataRequired()])


class EditSystemForm(FlaskForm):
    EditSystemName = StringField("System Name")
    EditSystemDescription = StringField("System Description")
    EditSystemLocation = StringField("System Location")
    EditSystemRouter = StringField("System Router")
    EditSystemSwitch = StringField("System Switch")
    EditSystemRoom = StringField("System Room")
    EditSystemTestPlan = StringField("System Test Plan")


class CreateTaskForm(FlaskForm):
    taskName = StringField("Task Name", validators=[DataRequired()])
    taskDescription = StringField("Task Description", validators=[DataRequired()])
    taskPriority = SelectField("Task Priority",
                               choices=[(Priority.LOW.value, "Low"),
                                        (Priority.MEDIUM.value, "Medium"),
                                        (Priority.HIGH.value, "High")], validators=[DataRequired()])
    # Editable if the task has no subtask.
    taskProgress = SelectField("Task Progress", validators=[DataRequired()],
                               choices=[(Progress.NOT_STARTED.value, "Not Started"),
                                        (Progress.ASSIGNED.value, "Assigned"),
                                        (Progress.TRANSFERRED.value, "Transferred"),
                                        (Progress.IN_PROGRESS.value, "In Progress"),
                                        (Progress.COMPLETE.value, "Complete"),
                                        (Progress.NOT_APPLICABLE.value, "Not Applicable")])

    taskDueDate = DateField('Task Due Date', validators=[DataRequired()])
    taskAttachment = StringField("Task Attachment")
    # task associated to another task?    # these 3 are lists
    # MAYBE SHOW A LIST OF TASKS AND ANALYSTS TO SELECT ONE FROM THEM
    associationToTask = SelectMultipleField("Association to Task", choices=[])
    taskAnalystAssignment = SelectMultipleField("Task Analyst Assignment", choices=[])
    taskCollaboratorAssignment = SelectMultipleField("Task Collaborator Assignment", choices=[])

    def __init__(self, tasks=None, analysts=None, collaborators=None):
        super().__init__()  # calls the base initialisation and then...
        if tasks:
            self.associationToTask.choices = [(task.getId(), task.getTitle()) for task in tasks]
        if analysts:
            self.taskAnalystAssignment.choices = [(analyst.getId(), analyst.getInitial()) for analyst in analysts]
        if collaborators:
            self.taskCollaboratorAssignment.choices = [(collaborator.getId(), collaborator.getInitial()) for
                                                       collaborator in collaborators]


class EditTaskForm(FlaskForm):
    taskName = StringField("Task Name", validators=[DataRequired()])
    taskDescription = StringField("Task Description", validators=[DataRequired()])
    taskPriority = SelectField("Task Priority",
                               choices=[(Priority.LOW.value, "Low"),
                                        (Priority.MEDIUM.value, "Medium"),
                                        (Priority.HIGH.value, "High")], validators=[DataRequired()])
    # Editable if the task has no subtask.
    taskProgress = SelectField("Task Progress", validators=[DataRequired()],
                               choices=[(Progress.NOT_STARTED.value, "Not Started"),
                                        (Progress.ASSIGNED.value, "Assigned"),
                                        (Progress.TRANSFERRED.value, "Transferred"),
                                        (Progress.IN_PROGRESS.value, "In Progress"),
                                        (Progress.COMPLETE.value, "Complete"),
                                        (Progress.NOT_APPLICABLE.value, "Not Applicable")])
    taskDueDate = DateField('Task Due Date', validators=[DataRequired()])
    taskAttachment = StringField("Task Attachment")
    # task associated to another task? show a list of tasks with the same parent system
    # select field populated with those tasks and a default value
    associationToTask = SelectMultipleField("Association to Task", choices=[])
    taskAnalystAssignment = SelectMultipleField("Task Analyst Assignment", choices=[])
    # selectable list?
    taskCollaboratorAssignment = SelectMultipleField("Task Collaborator Assignment", choices=[])


class CreateSubtaskForm(FlaskForm):
    subTaskName = StringField("Subtask Name", validators=[DataRequired()])
    subTaskDescription = StringField("Subtask Description", validators=[DataRequired()])
    # number? to use as var for progress
    # set 0 as default and 1 would be that the subtask is complete
    subTaskProgress = SelectField("Subtask Progress", validators=[DataRequired()],
                                  choices=[(Progress.NOT_STARTED.value, "Not Started"),
                                           (Progress.ASSIGNED.value, "Assigned"),
                                           (Progress.TRANSFERRED.value, "Transferred"),
                                           (Progress.IN_PROGRESS.value, "In Progress"),
                                           (Progress.COMPLETE.value, "Complete"),
                                           (Progress.NOT_APPLICABLE.value, "Not Applicable")])
    subTaskDueDate = DateField('Subtask Due Date', validators=[DataRequired()])
    subTaskAttachment = StringField("Subtask Attachment")
    # task associated to another task
    associationToSubtask = SelectMultipleField("Association to Task", choices=[])
    subTaskAnalystAssignment = SelectMultipleField("Subtask Analyst Assignment", choices=[])
    subTaskCollaboratorAssignment = SelectMultipleField("Subtask Collaborator Assignment", choices=[])

    # this is to populate the select fields with info from the db
    def __init__(self, subtasks=None, analysts=None, collaborators=None):
        super().__init__()  # calls the base initialisation and then...
        if subtasks:
            self.associationToSubtask.choices = [(task.getId(), task.getTitle()) for task in subtasks]
        if analysts:
            self.subTaskAnalystAssignment.choices = [(analyst.getId(), analyst.getInitial()) for analyst in
                                                     analysts]
        if collaborators:
            self.subTaskCollaboratorAssignment.choices = [(collaborator.getId(), collaborator.getInitial()) for
                                                          collaborator in collaborators]


class EditSubtaskForm(FlaskForm):
    subTaskName = StringField("Subtask Name", validators=[DataRequired()])
    subTaskDescription = StringField("Subtask Description", validators=[DataRequired()])
    # Editable if the task has no subtask. number? to use as var for progress
    # set 0 as default
    subTaskProgress = SelectField("Task Progress", validators=[DataRequired()],
                                  choices=[(Progress.NOT_STARTED.value, "Not Started"),
                                           (Progress.ASSIGNED.value, "Assigned"),
                                           (Progress.TRANSFERRED.value, "Transferred"),
                                           (Progress.IN_PROGRESS.value, "In Progress"),
                                           (Progress.COMPLETE.value, "Complete"),
                                           (Progress.NOT_APPLICABLE.value, "Not Applicable")])
    subTaskDueDate = DateField('Subtask Due Date', validators=[DataRequired()])
    subTaskAttachment = StringField("Subtask Attachment")
    # subtask associated to another subtask? it is a list of subtasks with the same task as parent
    # select field populated with those tasks and a default value
    associationToSubtask = SelectMultipleField("Association to Task", choices=[])
    subTaskAnalystAssignment = SelectMultipleField("Subtask Analyst Assignment", choices=[])
    subTaskCollaboratorAssignment = SelectMultipleField("Subtask Collaborator Assignment", choices=[])


class CreateFindingForm(FlaskForm):
    findingHostName = StringField("Finding Host Name", validators=[DataRequired()])
    findingIPPort = StringField("Finding IP Port", validators=[DataRequired()])
    findingDescription = StringField("Finding Description", validators=[DataRequired()])
    findingLongDescription = StringField("Finding Long Description")
    findingStatus = SelectField("Finding Status",
                                choices=[(FindingStatus.OPEN.value, "Open"),
                                         (FindingStatus.CLOSED.value, "Closed")],
                                validators=[DataRequired()])
    findingType = SelectField("Finding Type",
                              choices=[
                                  (FindingType.CREDENTIALS_COMPLEXITY.value, "Credentials Complexity"),
                                  (FindingType.MANUFACTURER_DEFAULT_CREDS.value,
                                   "Manufacturer Default Creds"),
                                  (FindingType.LACK_OF_AUTHENTICATION.value, "Lack Of Authentication"),
                                  (FindingType.PLAIN_TEXT_PROTOCOLS.value, "Plain Text Protocols"),
                                  (FindingType.PLAIN_TEXT_WEB_LOGIN.value, "Plain Text Web Login"),
                                  (FindingType.ENCRYPTION.value, "Encryption"),
                                  (FindingType.AUTHENTICATION_BYPASS.value, "Authentication Bypass"),
                                  (FindingType.PORT_SECURITY.value, "Port Security"),
                                  (FindingType.ACCESS_CONTROL.value, "Access Control"),
                                  (FindingType.LEAST_PRIVILEGE.value, "Least Privilege"),
                                  (FindingType.PRIVILEGE_ESCALATION.value, "Privilege Escalation"),
                                  (FindingType.MISSING_PATCHES.value, "Missing Patches"),
                                  (FindingType.PHYSICAL_SECURITY.value, "Physical Security"),
                                  (FindingType.INFORMATION_DISCLOSURE.value, "Information Disclosure")],
                              validators=[DataRequired()])

    findingClassification = SelectField("Finding Classification",
                                        choices=[(FindingClassification.VULNERABILITY.value,
                                                  "Vulnerability"),
                                                 (FindingClassification.INFORMATION.value,
                                                  "Information")], validators=[DataRequired()])
    associationToFinding = SelectMultipleField("Finding Association To Finding", choices=[])
    # EVIDENCE IS A FILE NOT A STRING
    findingEvidence = StringField("Finding Evidence", validators=[DataRequired()])

    # Finding Impact
    findingConfidentiality = SelectField("Finding Confidentiality",
                                         choices=[(Confidentiality.LOW.value, "Low"),
                                                  (Confidentiality.MEDIUM.value, "Medium"),
                                                  (Confidentiality.HIGH.value, "High"),
                                                  (Confidentiality.INFO.value, "Info")],
                                         validators=[DataRequired()])
    findingIntegrity = SelectField("Finding Integrity",
                                   choices=[(Integrity.LOW.value, "Low"),
                                            (Integrity.MEDIUM.value, "Medium"),
                                            (Integrity.HIGH.value, "High"),
                                            (Integrity.INFO.value, "Info")],
                                   validators=[DataRequired()])
    findingAvailability = SelectField("Finding Availability",
                                      choices=[(Availability.LOW.value, "Low"),
                                               (Availability.MEDIUM.value, "Medium"),
                                               (Availability.HIGH.value, "High"),
                                               (Availability.INFO.value, "Info")],
                                      validators=[DataRequired()])
    # Finding Analyst Information
    # it could be a multiple selection and then from the list out of that
    findingAnalystAssignment = SelectMultipleField("Finding Analyst Assignment", validators=[DataRequired()])
    findingCollaboratorAssignment = SelectMultipleField("Finding Collaborator Assignment")
    findingPosture = SelectField("Finding Posture", validators=[DataRequired()],
                                 choices=[(Posture.INSIDER.value, 'Insider'),
                                          (Posture.INSIDER_NEARSIDER.value, 'Insider-nearsider'),
                                          (Posture.OUTSIDER.value, 'Outsider'),
                                          (Posture.NEARSIDER.value, 'Nearsider'),
                                          (Posture.NEARSIDER_OUTSIDER.value, 'Nearsider-outsider')])
    # Finding Mitigation
    mitigationBriefDescription = StringField("Mitigation Brief Description", validators=[DataRequired()])
    mitigationLongDescription = StringField("Finding Analyst Assignment", validators=[DataRequired()])

    # Threat Relevance
    findingThreatRelevance = SelectField("Finding Threat Relevance",
                                         choices=[(Relevance.CONFIRMED.value, 'Confirmed'),
                                                  (Relevance.EXPECTED.value, 'Expected'),
                                                  (Relevance.ANTICIPATED.value, 'Anticipated'),
                                                  (Relevance.PREDICTED.value, 'Predicted'),
                                                  (Relevance.POSSIBLE.value, 'Possible')], validators=[DataRequired()])

    # Finding Countermeasure
    findingEffectivenessRating = SelectField("Finding Effectiveness Rating",
                                             choices=[(EffectivenessRating.VERYLOW_0.value,
                                                       '0 - Countermeasure implemented is effective'),
                                                      (EffectivenessRating.LOW_1.value,
                                                       '1 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      (EffectivenessRating.LOW_2.value,
                                                       '2 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      (EffectivenessRating.LOW_3.value,
                                                       '3 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      (EffectivenessRating.MODERATE_4.value,
                                                       '4 - Countermeasure is implemented but MODERATELY effective'),
                                                      (EffectivenessRating.MODERATE_5.value,
                                                       '5 - Countermeasure is implemented but MODERATELY effective'),
                                                      (EffectivenessRating.MODERATE_6.value,
                                                       '6 - Countermeasure is implemented but MODERATELY effective'),
                                                      (EffectivenessRating.HIGH_7.value,
                                                       '7 - Countermeasure is implemented but MINIMALLY effective'),
                                                      (EffectivenessRating.HIGH_8.value,
                                                       '8 - Countermeasure is implemented but MINIMALLY effective'),
                                                      (EffectivenessRating.HIGH_9.value,
                                                       '9 - Countermeasure is implemented but MINIMALLY effective'),
                                                      (EffectivenessRating.VERYHIGH.value,
                                                       '10 - Countermeasure not implemented')],
                                             validators=[DataRequired()])

    # Finding Impact
    impactDescription = StringField("Finding Impact Description", validators=[DataRequired()])
    impactLevel = SelectField("Finding Impact Level",
                              choices=[(ImpactLevel.VH.value, 'VH'),
                                       (ImpactLevel.H.value, 'H'),
                                       (ImpactLevel.M.value, 'M'),
                                       (ImpactLevel.L.value, 'L'),
                                       (ImpactLevel.VL.value, 'VL'),
                                       (ImpactLevel.INFORMATION.value, 'Information')], validators=[DataRequired()])
    # Finding Severity
    severityCategoryCode = SelectField("Finding Severity Category Code",
                                       choices=[(SeverityCategoryCode.I.value, 'I'),
                                                (SeverityCategoryCode.II.value, 'II'),
                                                (SeverityCategoryCode.III.value, 'III')], validators=[DataRequired()])

    # this is to populate the select fields with info from the db


    def __init__(self, findings=None, analysts=None, collaborators=None):
        super().__init__()
        if findings:
            self.associationToFinding.choices = [(finding.getid(), finding.getHostName()) for finding in findings]
        if analysts:
            self.findingAnalystAssignment.choices = [(analyst.getId(), analyst.getInitial()) for analyst in
                                                     analysts]
        if collaborators:
            self.findingCollaboratorAssignment.choices = [(collaborator.getId(), collaborator.getInitial()) for
                                                          collaborator in collaborators]


class EditFindingForm(FlaskForm):
    findingHostName = StringField("Finding Host Name", validators=[DataRequired()])
    findingIPPort = StringField("Finding IP Port", validators=[DataRequired()])
    findingDescription = StringField("Finding Description", validators=[DataRequired()])
    findingLongDescription = StringField("Finding Long Description", validators=[DataRequired()])
    findingStatus = SelectField("Finding status",
                                choices=[(FindingStatus.OPEN.value, "Open"),
                                         (FindingStatus.CLOSED.value, "Closed")],
                                validators=[DataRequired()])
    findingType = SelectField("Finding Type",
                              choices=[
                                  (FindingType.CREDENTIALS_COMPLEXITY.value, "Credentials Complexity"),
                                  (FindingType.MANUFACTURER_DEFAULT_CREDS.value,
                                   "Manufacturer Default Creds"),
                                  (FindingType.LACK_OF_AUTHENTICATION.value, "Lack Of Authentication"),
                                  (FindingType.PLAIN_TEXT_PROTOCOLS.value, "Plain Text Protocols"),
                                  (FindingType.PLAIN_TEXT_WEB_LOGIN.value, "Plain Text Web Login"),
                                  (FindingType.ENCRYPTION.value, "Encryption"),
                                  (FindingType.AUTHENTICATION_BYPASS.value, "Authentication Bypass"),
                                  (FindingType.PORT_SECURITY.value, "Port Security"),
                                  (FindingType.ACCESS_CONTROL.value, "Access Control"),
                                  (FindingType.LEAST_PRIVILEGE.value, "Least Privilege"),
                                  (FindingType.PRIVILEGE_ESCALATION.value, "Privilege Escalation"),
                                  (FindingType.MISSING_PATCHES.value, "Missing Patches"),
                                  (FindingType.PHYSICAL_SECURITY.value, "Physical Security"),
                                  (FindingType.INFORMATION_DISCLOSURE.value, "Information Disclosure")],
                              validators=[DataRequired()])

    findingClassification = SelectField("Finding Classification",
                                        choices=[(FindingClassification.VULNERABILITY.value,
                                                  "Vulnerability"),
                                                 (FindingClassification.INFORMATION.value,
                                                  "Information")], validators=[DataRequired()])

    associationToFinding = StringField("Finding Association To Finding")
    # EVIDENCE IS A FILE NOT A STRING
    findingEvidence = StringField("Finding Evidence", validators=[DataRequired()])

    # Finding Analyst Information
    findingAnalystAssignment = StringField("Finding Analyst Assignment", validators=[DataRequired()])
    findingCollaboratorAssignment = StringField("Finding Collaborator Assignment")
    findingPosture = SelectField("Finding Posture", validators=[DataRequired()],
                                 choices=[(Posture.INSIDER.value, 'Insider'),
                                         (Posture.INSIDER_NEARSIDER.value, 'Insider-nearsider'),
                                         (Posture.OUTSIDER.value, 'Outsider'),
                                         (Posture.NEARSIDER.value, 'Nearsider'),
                                         (Posture.NEARSIDER_OUTSIDER.value, 'Nearsider-outsider')])
    # Finding Mitigation
    mitigationBriefDescription = StringField("Mitigation Brief Description", validators=[DataRequired()])
    mitigationLongDescription = StringField("Mitigation Long Description", validators=[DataRequired()])

    # Threat Relevance
    findingThreatRelevance = SelectField("Finding Threat Relevance",
                                         choices=[(Relevance.CONFIRMED.value, 'Confirmed'),
                                                  (Relevance.EXPECTED.value, 'Expected'),
                                                  (Relevance.ANTICIPATED.value, 'Anticipated'),
                                                  (Relevance.PREDICTED.value, 'Predicted'),
                                                  (Relevance.POSSIBLE.value, 'Possible')], validators=[DataRequired()])

    # Finding Countermeasure
    findingEffectivenessRating = SelectField("Finding Effectiveness",
                                             choices=[(EffectivenessRating.VERYLOW_0.value, '0 - Countermeasure implemented is effective'),
                                                      (EffectivenessRating.LOW_1.value,
                                                       '1 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      (EffectivenessRating.LOW_2.value,
                                                       '2 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      (EffectivenessRating.LOW_3.value,
                                                       '3 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      (EffectivenessRating.MODERATE_4.value,
                                                       '4 - Countermeasure is implemented but MODERATELY effective'),
                                                      (EffectivenessRating.MODERATE_5.value,
                                                       '5 - Countermeasure is implemented but MODERATELY effective'),
                                                      (EffectivenessRating.MODERATE_6.value,
                                                       '6 - Countermeasure is implemented but MODERATELY effective'),
                                                      (EffectivenessRating.HIGH_7.value,
                                                       '7 - Countermeasure is implemented but MINIMALLY effective'),
                                                      (EffectivenessRating.HIGH_8.value,
                                                       '8 - Countermeasure is implemented but MINIMALLY effective'),
                                                      (EffectivenessRating.HIGH_9.value,
                                                       '9 - Countermeasure is implemented but MINIMALLY effective'),
                                                      (EffectivenessRating.VERYHIGH.value, '10 - Countermeasure not implemented')],
                                             validators=[DataRequired()])

    # Finding Impact
    impactDescription = StringField("Finding Impact Description", validators=[DataRequired()])
    impactLevel = SelectField("Finding Impact Level",
                              choices=[(ImpactLevel.VH.value, 'VH'),
                                       (ImpactLevel.H.value, 'H'),
                                       (ImpactLevel.M.value, 'M'),
                                       (ImpactLevel.L.value, 'L'),
                                       (ImpactLevel.VL.value, 'VL'),
                                       (ImpactLevel.INFORMATION.value, 'Information')], validators=[DataRequired()])
    # Finding Severity
    severityCategoryCode = SelectField("Finding Severity Category Code",
                                       choices=[(SeverityCategoryCode.I.value, 'I'),
                                                (SeverityCategoryCode.II.value, 'II'),
                                                (SeverityCategoryCode.III.value, 'III')], validators=[DataRequired()])
