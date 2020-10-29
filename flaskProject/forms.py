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
                                      EventType.COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT.name),
                                     (EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION.value,
                                      EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION.name),
                                     (EventType.VERIFICATION_OF_FIXES.value, EventType.VERIFICATION_OF_FIXES.name)],
                            validators=[DataRequired()])
    OrganizationName = StringField('Organization Name', validators=[DataRequired()])
    CustomerName = StringField('Customer Name', validators=[DataRequired()])
    AssessmentDate = DateField('Assessment Date', validators=[DataRequired()])
    DeclassificationDate = DateField('Declassification Date', validators=[DataRequired()])
    SCTG = StringField('Security Classification Title Guide', validators=[DataRequired()])
    EventClassification = SelectField('Event Classification',
                                      choices=[
                                          (EventClassification.TOP_SECRET.value, EventClassification.TOP_SECRET.name),
                                          (EventClassification.SECRET.value, EventClassification.SECRET.name),
                                          (EventClassification.CONFIDENTIAL.value,
                                           EventClassification.CONFIDENTIAL.name),
                                          (EventClassification.CLASSIFIED.value, EventClassification.CLASSIFIED.name),
                                          (EventClassification.UNCLASSIFIED.value,
                                           EventClassification.UNCLASSIFIED.name)],
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
                                          EventType.COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT.name),
                                         (EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION.value,
                                          EventType.COOPERATIVE_VULNERABILITY_INVESTIGATION.name),
                                         (EventType.VERIFICATION_OF_FIXES.value, EventType.VERIFICATION_OF_FIXES.name)],
                                validators=[DataRequired()])
    EditEventOrganizationName = StringField('Organization Name')
    EditEventCustomerName = StringField('Customer name')
    EditEventAssessmentDate = DateField('Assessment date')
    EditEventDeclassificationDate = DateField('Declassification date')
    EditEventSCTG = StringField('Security Classification Title Guide')
    EditEventClassification = SelectField('Event Classification',
                                          choices=[(EventClassification.TOP_SECRET.value,
                                                    EventClassification.TOP_SECRET.name),
                                                   (EventClassification.SECRET.value, EventClassification.SECRET.name),
                                                   (EventClassification.CONFIDENTIAL.value,
                                                    EventClassification.CONFIDENTIAL.name),
                                                   (EventClassification.CLASSIFIED.value,
                                                    EventClassification.CLASSIFIED.name),
                                                   (EventClassification.UNCLASSIFIED.value,
                                                    EventClassification.UNCLASSIFIED.name)])
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
                                        choices=[(Confidentiality.LOW.value, Confidentiality.LOW.name),
                                                 (Confidentiality.MEDIUM.value, Confidentiality.MEDIUM.name),
                                                 (Confidentiality.HIGH.value, Confidentiality.HIGH.name),
                                                 (Confidentiality.INFO.value, Confidentiality.INFO.name)],
                                        validators=[DataRequired()])
    systemIntegrity = SelectField("System Integrity",
                                  choices=[(Integrity.LOW.value, Integrity.LOW.name),
                                           (Integrity.MEDIUM.value, Integrity.MEDIUM.name),
                                           (Integrity.HIGH.value, Integrity.HIGH.name),
                                           (Integrity.INFO.value, Integrity.INFO.name)],
                                  validators=[DataRequired()])
    systemAvailability = SelectField("System Availability",
                                     choices=[(Availability.LOW.value, Availability.LOW.name),
                                              (Availability.MEDIUM.value, Availability.MEDIUM.name),
                                              (Availability.HIGH.value, Availability.HIGH.name),
                                              (Availability.INFO.value, Availability.INFO.name)],
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
                               choices=[(Priority.LOW.value, Priority.LOW.name),
                                        (Priority.MEDIUM.value, Priority.MEDIUM.name),
                                        (Priority.HIGH.value, Priority.HIGH.name)], validators=[DataRequired()])
    # Editable if the task has no subtask.
    taskProgress = SelectField("Task Progress", validators=[DataRequired()],
                               choices=[(Progress.NOT_STARTED.value, Progress.NOT_STARTED.name),
                                        (Progress.ASSIGNED.value, Progress.ASSIGNED.name),
                                        (Progress.TRANSFERRED.value, Progress.TRANSFERRED.name),
                                        (Progress.IN_PROGRESS.value, Progress.IN_PROGRESS.name),
                                        (Progress.COMPLETE.value, Progress.COMPLETE.name),
                                        (Progress.NOT_APPLICABLE.value, Progress.NOT_APPLICABLE.name)])

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
            self.associationToTask.choices = [(task.getTitle(), task.getTitle()) for task in tasks]
        if analysts:
            self.taskAnalystAssignment.choices = [(analyst.getInitial(), analyst.getInitial()) for analyst in analysts]
        if collaborators:
            self.taskCollaboratorAssignment.choices = [(collaborator.getInitial(), collaborator.getInitial()) for
                                                       collaborator in collaborators]


class EditTaskForm(FlaskForm):
    taskName = StringField("Task Name", validators=[DataRequired()])
    taskDescription = StringField("Task Description", validators=[DataRequired()])
    taskPriority = SelectField("Task Priority",
                               choices=[(Priority.LOW.value, Priority.LOW.name),
                                        (Priority.MEDIUM.value, Priority.MEDIUM.name),
                                        (Priority.HIGH.value, Priority.HIGH.name)], validators=[DataRequired()])
    # Editable if the task has no subtask.
    taskProgress = SelectField("Task Progress", validators=[DataRequired()],
                               choices=[(Progress.NOT_STARTED.value, Progress.NOT_STARTED.name),
                                        (Progress.ASSIGNED.value, Progress.ASSIGNED.name),
                                        (Progress.TRANSFERRED.value, Progress.TRANSFERRED.name),
                                        (Progress.IN_PROGRESS.value, Progress.IN_PROGRESS.name),
                                        (Progress.COMPLETE.value, Progress.COMPLETE.name),
                                        (Progress.NOT_APPLICABLE.value, Progress.NOT_APPLICABLE.name)])
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
                                  choices=[(Progress.NOT_STARTED.value, Progress.NOT_STARTED.name),
                                           (Progress.ASSIGNED.value, Progress.ASSIGNED.name),
                                           (Progress.TRANSFERRED.value, Progress.TRANSFERRED.name),
                                           (Progress.IN_PROGRESS.value, Progress.IN_PROGRESS.name),
                                           (Progress.COMPLETE.value, Progress.COMPLETE.name),
                                           (Progress.NOT_APPLICABLE.value, Progress.NOT_APPLICABLE.name)])
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
            self.associationToSubtask.choices = [(task.getTitle(), task.getTitle()) for task in subtasks]
        if analysts:
            self.subTaskAnalystAssignment.choices = [(analyst.getInitial(), analyst.getInitial()) for analyst in
                                                     analysts]
        if collaborators:
            self.subTaskCollaboratorAssignment.choices = [(collaborator.getInitial(), collaborator.getInitial()) for
                                                          collaborator in collaborators]


class EditSubtaskForm(FlaskForm):
    subTaskName = StringField("Subtask Name", validators=[DataRequired()])
    subTaskDescription = StringField("Subtask Description", validators=[DataRequired()])
    # Editable if the task has no subtask. number? to use as var for progress
    # set 0 as default
    subTaskProgress = SelectField("Task Progress", validators=[DataRequired()],
                                  choices=[(Progress.NOT_STARTED.value, Progress.NOT_STARTED.name),
                                           (Progress.ASSIGNED.value, Progress.ASSIGNED.name),
                                           (Progress.TRANSFERRED.value, Progress.TRANSFERRED.name),
                                           (Progress.IN_PROGRESS.value, Progress.IN_PROGRESS.name),
                                           (Progress.COMPLETE.value, Progress.COMPLETE.name),
                                           (Progress.NOT_APPLICABLE.value, Progress.NOT_APPLICABLE.name)])
    subTaskDueDate = DateField('Subtask Due Date', validators=[DataRequired()])
    subTaskAttachment = StringField("Subtask Attachment")
    # subtask associated to another subtask? it is a list of subtasks with the same task as parent
    # select field populated with those tasks and a default value
    associationToSubtask = SelectMultipleField("Association to Task", choices=[])
    subTaskAnalystAssignment = SelectMultipleField("Subtask Analyst Assignment", choices=[])
    subTaskCollaboratorAssignment = SelectMultipleField("Subtask Collaborator Assignment", choices=[])


class CreateFindingForm(FlaskForm):
    # ID is autogenerated
    # findingID = StringField("Finding ID", validators=[DataRequired()])
    findingHostName = StringField("Finding Host Name", validators=[DataRequired()])
    findingIPPort = StringField("Finding IP Port", validators=[DataRequired()])
    findingDescription = StringField("Finding Description", validators=[DataRequired()])
    findingLongDescription = StringField("Finding Long Description")
    findingStatus = SelectField("Finding Status",
                                choices=[(FindingStatus.OPEN.value, FindingStatus.OPEN.name),
                                         (FindingStatus.CLOSED.value, FindingStatus.CLOSED.name)],
                                validators=[DataRequired()])
    findingType = SelectField("Finding Type",
                              choices=[
                                  (FindingType.CREDENTIALS_COMPLEXITY.value, FindingType.CREDENTIALS_COMPLEXITY.name),
                                  (FindingType.MANUFACTURER_DEFAULT_CREDS.value,
                                   FindingType.MANUFACTURER_DEFAULT_CREDS.name),
                                  (FindingType.LACK_OF_AUTHENTICATION.value, FindingType.LACK_OF_AUTHENTICATION.name),
                                  (FindingType.PLAIN_TEXT_PROTOCOLS.value, FindingType.PLAIN_TEXT_PROTOCOLS.name),
                                  (FindingType.PLAIN_TEXT_WEB_LOGIN.value, FindingType.PLAIN_TEXT_WEB_LOGIN.name),
                                  (FindingType.ENCRYPTION.value, FindingType.ENCRYPTION.name),
                                  (FindingType.AUTHENTICATION_BYPASS.value, FindingType.AUTHENTICATION_BYPASS.name),
                                  (FindingType.PORT_SECURITY.value, FindingType.PORT_SECURITY.name),
                                  (FindingType.ACCESS_CONTROL.value, FindingType.ACCESS_CONTROL.name),
                                  (FindingType.LEAST_PRIVILEGE.value, FindingType.LEAST_PRIVILEGE.name),
                                  (FindingType.PRIVILEGE_ESCALATION.value, FindingType.PRIVILEGE_ESCALATION.name),
                                  (FindingType.MISSING_PATCHES.value, FindingType.MISSING_PATCHES.name),
                                  (FindingType.PHYSICAL_SECURITY.value, FindingType.PHYSICAL_SECURITY.name),
                                  (FindingType.INFORMATION_DISCLOSURE.value, FindingType.INFORMATION_DISCLOSURE.name)],
                              validators=[DataRequired()])

    findingClassification = SelectField("Finding Classification",
                                        choices=[(FindingClassification.VULNERABILITY.value,
                                                  FindingClassification.VULNERABILITY.name),
                                                 (FindingClassification.INFORMATION.value,
                                                  FindingClassification.INFORMATION.name)], validators=[DataRequired()])
    associationToFinding = StringField("Finding Association To Finding")
    # EVIDENCE IS A FILE NOT A STRING
    findingEvidence = StringField("Finding Evidence", validators=[DataRequired()])

    # Finding Impact
    findingConfidentiality = SelectField("Finding Confidentiality",
                                         choices=[(Confidentiality.LOW.value, Confidentiality.LOW.name),
                                                  (Confidentiality.MEDIUM.value, Confidentiality.MEDIUM.name),
                                                  (Confidentiality.HIGH.value, Confidentiality.HIGH.name),
                                                  (Confidentiality.INFO.value, Confidentiality.INFO.name)],
                                         validators=[DataRequired()])
    findingIntegrity = SelectField("Finding Integrity",
                                   choices=[(Integrity.LOW.value, Integrity.LOW.name),
                                            (Integrity.MEDIUM.value, Integrity.MEDIUM.name),
                                            (Integrity.HIGH.value, Integrity.HIGH.name),
                                            (Integrity.INFO.value, Integrity.INFO.name)],
                                   validators=[DataRequired()])
    findingAvailability = SelectField("Finding Availability",
                                      choices=[(Availability.LOW.value, Availability.LOW.name),
                                               (Availability.MEDIUM.value, Availability.MEDIUM.name),
                                               (Availability.HIGH.value, Availability.HIGH.name),
                                               (Availability.INFO.value, Availability.INFO.name)],
                                      validators=[DataRequired()])
    # Finding Analyst Information
    # it could be a multiple selection and then from the list out of that
    findingAnalystAssignment = StringField("Finding Analyst Assignment", validators=[DataRequired()])
    findingCollaboratorAssignment = StringField("Finding Collaborator Assignment")
    findingPosture = SelectField("Finding Posture", validators=[DataRequired()],
                                 hoices=[('Insider', 'Insider'),
                                         ('Insider-nearsider', 'nsider-nearsider'),
                                         ('Outsider', 'Outsider'),
                                         ('Nearsider', 'Nearsider'),
                                         ('Nearsider-outsider', 'Nearsider-outsider')])
    # Finding Mitigation
    mitigationBriefDescription = StringField("Mitigation Brief Description", validators=[DataRequired()])
    mitigationLongDescription = StringField("Finding Analyst Assignment", validators=[DataRequired()])

    # Threat Relevance
    findingThreatRelevance = SelectField("Finding Threat Relevance",
                                         choices=[('Confirmed', 'Confirmed'),
                                                  ('Expected', 'Expected'),
                                                  ('Anticipated', 'Anticipated'),
                                                  ('Predicted', 'Predicted'),
                                                  ('Possible', 'Possible')], validators=[DataRequired()])

    # Finding Countermeasure
    findingEffectivenessRating = SelectField("Finding Threat Relevance",
                                             choices=[('Very Low', '0 - Countermeasure implemented is effective'),
                                                      ('Low',
                                                       '1 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      ('Low',
                                                       '2 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      ('Low',
                                                       '3 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      ('Moderate',
                                                       '4 - Countermeasure is implemented but MODERATELY effective'),
                                                      ('Moderate',
                                                       '5 - Countermeasure is implemented but MODERATELY effective'),
                                                      ('Moderate',
                                                       '6 - Countermeasure is implemented but MODERATELY effective'),
                                                      ('High',
                                                       '7 - Countermeasure is implemented but MINIMALLY effective'),
                                                      ('High',
                                                       '8 - Countermeasure is implemented but MINIMALLY effective'),
                                                      ('High',
                                                       '9 - Countermeasure is implemented but MINIMALLY effective'),
                                                      ('Very High', '10 - Countermeasure not implemented')],
                                             validators=[DataRequired()])

    # Finding Impact
    impactDescription = StringField("Finding Impact Description", validators=[DataRequired()])
    impactLevel = SelectField("Finding Impact Level",
                              choices=[('VH', 'VH'),
                                       ('H', 'H'),
                                       ('M', 'M'),
                                       ('L', 'L'),
                                       ('VL', 'VL'),
                                       ('Information', 'Information')], validators=[DataRequired()])
    # Finding Severity
    severityCategoryCode = SelectField("Finding Security Category Code",
                                       choices=[('I', 'I'),
                                                ('II', 'II'),
                                                ('III', 'III')], validators=[DataRequired()])
    # these three are set automatically on creation
    # securityCategoryScore = StringField("Finding Impact Description", validators=[DataRequired()])
    # vulnerabilitySeverity = StringField("Finding Impact Description", validators=[DataRequired()])
    # QuantitativeVulnerabilitySeverity = StringField("Finding Impact Description", validators=[DataRequired()])

    # Finding Risk
    # findingRisk = StringField("Finding Risk", validators=[DataRequired()])
    # findingLikelihood = StringField("Finding Likelihood", validators=[DataRequired()])

    # Finding Level Impact
    # ConfidentialityFindingImpactOnSystem
    # IntegrityFindingImpactOnSystem
    # AvailabilityFindingImpactOnSystem
    # impactScore = StringField("Finding Risk", validators=[DataRequired()])


class EditFindingForm(FlaskForm):
    findingHostName = StringField("Finding Host Name", validators=[DataRequired()])
    findingIPPort = StringField("Finding IP Port", validators=[DataRequired()])
    findingDescription = StringField("Finding Description", validators=[DataRequired()])
    findingLongDescription = StringField("Finding Long Description", validators=[DataRequired()])
    findingStatus = SelectField("Finding status",
                                choices=[(FindingStatus.OPEN.value, FindingStatus.OPEN.name),
                                         (FindingStatus.CLOSED.value, FindingStatus.CLOSED.name)],
                                validators=[DataRequired()])
    findingType = SelectField("Finding Type",
                              choices=[
                                  (FindingType.CREDENTIALS_COMPLEXITY.value, FindingType.CREDENTIALS_COMPLEXITY.name),
                                  (FindingType.MANUFACTURER_DEFAULT_CREDS.value,
                                   FindingType.MANUFACTURER_DEFAULT_CREDS.name),
                                  (FindingType.LACK_OF_AUTHENTICATION.value, FindingType.LACK_OF_AUTHENTICATION.name),
                                  (FindingType.PLAIN_TEXT_PROTOCOLS.value, FindingType.PLAIN_TEXT_PROTOCOLS.name),
                                  (FindingType.PLAIN_TEXT_WEB_LOGIN.value, FindingType.PLAIN_TEXT_WEB_LOGIN.name),
                                  (FindingType.ENCRYPTION.value, FindingType.ENCRYPTION.name),
                                  (FindingType.AUTHENTICATION_BYPASS.value, FindingType.AUTHENTICATION_BYPASS.name),
                                  (FindingType.PORT_SECURITY.value, FindingType.PORT_SECURITY.name),
                                  (FindingType.ACCESS_CONTROL.value, FindingType.ACCESS_CONTROL.name),
                                  (FindingType.LEAST_PRIVILEGE.value, FindingType.LEAST_PRIVILEGE.name),
                                  (FindingType.PRIVILEGE_ESCALATION.value, FindingType.PRIVILEGE_ESCALATION.name),
                                  (FindingType.MISSING_PATCHES.value, FindingType.MISSING_PATCHES.name),
                                  (FindingType.PHYSICAL_SECURITY.value, FindingType.PHYSICAL_SECURITY.name),
                                  (FindingType.INFORMATION_DISCLOSURE.value, FindingType.INFORMATION_DISCLOSURE.name)],
                              validators=[DataRequired()])

    findingClassification = SelectField("Finding Classification",
                                        choices=[(FindingClassification.VULNERABILITY.value,
                                                  FindingClassification.VULNERABILITY.name),
                                                 (FindingClassification.INFORMATION.value,
                                                  FindingClassification.INFORMATION.name)], validators=[DataRequired()])

    associationToFinding = StringField("Finding Association To Finding")
    # EVIDENCE IS A FILE NOT A STRING
    findingEvidence = StringField("Finding Evidence", validators=[DataRequired()])

    # Finding Analyst Information
    findingAnalystAssignment = StringField("Finding Analyst Assignment", validators=[DataRequired()])
    findingCollaboratorAssignment = StringField("Finding Collaborator Assignment")
    findingPosture = SelectField("Finding Posture", validators=[DataRequired()],
                                 hoices=[('Insider', 'Insider'),
                                         ('Insider-nearsider', 'nsider-nearsider'),
                                         ('Outsider', 'Outsider'),
                                         ('Nearsider', 'Nearsider'),
                                         ('Nearsider-outsider', 'Nearsider-outsider')])
    # Finding Mitigation
    mitigationBriefDescription = StringField("Mitigation Brief Description", validators=[DataRequired()])
    mitigationLongDescription = StringField("Finding Analyst Assignment", validators=[DataRequired()])

    # Threat Relevance
    findingThreatRelevance = SelectField("Finding Threat Relevance",
                                         choices=[('Confirmed', 'Confirmed'),
                                                  ('Expected', 'Expected'),
                                                  ('Anticipated', 'Anticipated'),
                                                  ('Predicted', 'Predicted'),
                                                  ('Possible', 'Possible')], validators=[DataRequired()])

    # Finding Countermeasure
    findingEffectivenessRating = SelectField("Finding Threat Relevance",
                                             choices=[('Very Low', '0 - Countermeasure implemented is effective'),
                                                      ('Low',
                                                       '1 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      ('Low',
                                                       '2 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      ('Low',
                                                       '3 - Countermeasure is implemented HIGHLY effective but can be improved.'),
                                                      ('Moderate',
                                                       '4 - Countermeasure is implemented but MODERATELY effective'),
                                                      ('Moderate',
                                                       '5 - Countermeasure is implemented but MODERATELY effective'),
                                                      ('Moderate',
                                                       '6 - Countermeasure is implemented but MODERATELY effective'),
                                                      ('High',
                                                       '7 - Countermeasure is implemented but MINIMALLY effective'),
                                                      ('High',
                                                       '8 - Countermeasure is implemented but MINIMALLY effective'),
                                                      ('High',
                                                       '9 - Countermeasure is implemented but MINIMALLY effective'),
                                                      ('Very High', '10 - Countermeasure not implemented')],
                                             validators=[DataRequired()])

    # Finding Impact
    impactDescription = StringField("Finding Impact Description", validators=[DataRequired()])
    impactLevel = SelectField("Finding Impact Level",
                              choices=[('VH', 'VH'),
                                       ('H', 'H'),
                                       ('M', 'M'),
                                       ('L', 'L'),
                                       ('VL', 'VL'),
                                       ('Information', 'Information')], validators=[DataRequired()])
    # Finding Severity
    severityCategoryCode = SelectField("Finding Security Category Code",
                                       choices=[('I', 'I'),
                                                ('II', 'II'),
                                                ('III', 'III')], validators=[DataRequired()])
    # these three are set automatically on creation
    # securityCategoryScore = StringField("Finding Impact Description", validators=[DataRequired()])
    # vulnerabilitySeverity = StringField("Finding Impact Description", validators=[DataRequired()])
    # QuantitativeVulnerabilitySeverity = StringField("Finding Impact Description", validators=[DataRequired()])

    # Finding Risk
    # findingRisk = StringField("Finding Risk", validators=[DataRequired()])
    # findingLikelihood = StringField("Finding Likelihood", validators=[DataRequired()])
