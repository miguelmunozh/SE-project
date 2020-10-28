from datetime import datetime, date

from bson import ObjectId
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap
from analyst.analyst import Analyst
from analyst.role import Role
from database.databaseHandler import DatabaseHandler
from event.event import Event
from event.eventType import EventType
from event.eventClassification import EventClassification
from system.system import System
from forms import *
from Helper import *

from task.subtask import Subtask
from task.task import Task

app = Flask(__name__)
Bootstrap(app)
# needed for flask-wtforms
app.config['SECRET_KEY'] = 'encrypted'

# get instance of db
db = DatabaseHandler()

# analyst to pass as parameter to the updateEvent function,(will be deleted when we can know which analyst entered
# the system)
analyst = Analyst("jonathan", "roman", "jr", ["jr", "sr"], Role.LEAD)
notEvent = False
events = db.getAllEvents()

# check if there is an event in the db
if len(events) == 0:
    notEvent = True
    event = None
# check if there is a non archived event, is so set it as current event
for e in events:
    if not e.getArchiveStatus():
        event = e


@app.route('/', methods=['GET', 'POST'])
def SetupContentView():
    form = SetupContentViewForm()
    # checks if the submit btn in SetupContentView page has been pressed
    if 'LogCreateEvent' in request.form:
        # check if there is an event that is not archived, if so we use that event through the entire app
        # redirect to the right page depending on the user selection
        if form.SUCVSelection.data == 'create':
            return redirect(url_for("CreateEvent"))

        elif form.SUCVSelection.data == 'sync':
            # if you try to sync, and there is not an event, then you get a error message
            if notEvent:
                notEventError = "There is not an event in your local system"
                return render_template('SetupContentView.html', form=form, notEventError=notEventError)

            if is_valid_ipv4_address(form.SUCVIpAddress.data) or is_valid_ipv6_address(form.SUCVIpAddress.data):
                return redirect(url_for("EventView"))

            else:
                # show an error message for invalid ip address
                ipError = "The Ip Address is not valid"
                return render_template('SetupContentView.html', form=form, ipError=ipError)

    return render_template('SetupContentView.html', form=form)


@app.route('/CreateAnalyst', methods=['GET', 'POST'])
def CreateAnalyst():
    events = db.getAllEvents()
    for e in events:
        if not e.getArchiveStatus():
            event = e
    form = CreateAnalystForm()
    if 'createAnalyst' in request.form:
        a = Analyst(form.CreateAnalystFName.data, form.CreateAnalystLName.data,
                    form.CreateAnalystInitials.data, "title",
                    form.CreateAnalystRole.data)
        db.updateAnalyst(a)
        # add this analyst to the event team of actual event
        event.getEventTeam().append(a.getInitial())
        db.updateEvent(analyst, event)
        return redirect(url_for("EventView"))

    return render_template('CreateAnalyst.html', form=form)


# function to delete analyst initials from event and db
@app.route('/EventView/<string:initial>', methods=['GET', 'POST'])
def deleteAnalyst(initial):
    global analyst
    events = db.getAllEvents()
    for e in events:
        if e.getArchiveStatus() == False:
            event = e
    # get the event list of analyst initials and remove the selected one (will change when we store a list of
    # analysts instead of a list of initials)
    event.getEventTeam().remove(initial)
    db.updateEvent(analyst, event)
    # delete analyst object from the db as well?
    for analyst in db.getAllAnalyst():
        if analyst.getInitial() == initial:
            db.deleteAnalyst(analyst)
    return redirect(url_for('EventView'))


@app.route('/EventView', methods=['GET', 'POST'])
def EventView():
    global analyst
    global notEvent
    events = db.getAllEvents()
    for e in events:
        if e.getArchiveStatus() == False:
            event = e
    if notEvent:
        event = None
    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveEvent' in request.form:
        # event.setArchiveStatus(True)
        # db.updateEvent(analyst, event)
        # delete event and its systems, tasks, etc since well deal only with one event at a time
        for system in db.getAllSystems():
            db.deleteSystem(analyst, system)
        for analyst in db.getAllAnalyst():
            db.deleteAnalyst(analyst)
        for event in db.getAllEvents():
            db.deleteEvent(analyst, event)
        return redirect(url_for('SetupContentView'))

    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=event, db=db)


@app.route('/EditEvent', methods=['GET', 'POST'])
def EditEvent():
    events = db.getAllEvents()
    for e in events:
        if not e.getArchiveStatus():
            event = e
    form = EditEventForm()
    # populate the form with the data of the actual event
    if request.method == 'GET':
        form.EditEventName.data = event.getName()
        form.EditEventDescription.data = event.getDescription()
        form.EditEventType.data = event.getType()
        form.EditEventVersion.data = event.getVersion()
        form.EditEventOrganizationName.data = event.getOrganizationName()
        form.EditEventCustomerName.data = event.getCustomerName()
        form.EditEventAssessmentDate.data = datetime.strptime(event.getDate(), '%m/%d/%Y')
        form.EditEventClassifiedBy.data = event.getClassifiedBy()
        form.EditEventDerivedFrom.data = event.getDerivedFrom()
        form.EditEventDeclassificationDate.data = datetime.strptime(event.getDeclassificationDate(), '%m/%d/%Y')
        form.EditEventSCTG.data = event.getSecurityClassificationTitleGuide()
        form.EditEventClassification.data = event.getEventClassification()

    if 'editEvent' in request.form:
        event.setName(form.EditEventName.data)
        event.setType(form.EditEventType.data)
        event.setDescription(form.EditEventDescription.data)
        event.setVersion(form.EditEventVersion.data)
        event.setCustomerName(form.EditEventCustomerName.data)
        event.setOrganizationName(form.EditEventOrganizationName.data)
        event.setDate(form.EditEventAssessmentDate.data.strftime('%m/%d/%Y'))
        event.setClassifiedBy(form.EditEventClassifiedBy.data)
        event.setDerivedFrom(form.EditEventDerivedFrom.data)
        event.setDeclassificationDate(form.EditEventDeclassificationDate.data.strftime('%m/%d/%Y'))
        event.setSecurityClassificationTitleGuide(form.EditEventSCTG.data)
        event.setEventClassification(form.EditEventClassification.data)

        db.updateEvent(analyst, event)
        return redirect(url_for("EventView"))

    return render_template('EditEvent.html', event=event, form=form)  # pass parameter to populate with placeholders


@app.route('/CreateEvent', methods=['GET', 'POST'])
def CreateEvent():
    global analyst
    # global notEvent
    # events = db.getAllEvents()
    # for e in events:
    #     if not e.getArchiveStatus():
    #         event = e
    #         notEvent = False
    # create a form from the forms.py file (need to import the file)
    form = CreateEventForm()

    # check if the create event button has been pressed, if so create an event obj
    if 'createEvent' in request.form:
        # delete current event, systems, everything from the db, to handle only one event at a time
        for task in db.getAllTasks():
            db.deleteTask(analyst, task)
        for system in db.getAllSystems():
            db.deleteSystem(analyst, system)
        for analyst in db.getAllAnalyst():
            db.deleteAnalyst(analyst)
        for event in db.getAllEvents():
            db.deleteEvent(analyst, event)

        # get analysts lists together, (will change when we store a list of analysts instead of a list of initials)
        lead = form.EventLeadAnalysts.data
        list1 = list(lead.split("-"))

        nonLead = form.EventAnalysts.data
        list2 = list(nonLead.split("-"))
        # represents the event team which is a list including lead and non-lead analysts
        initialsList = list1 + list2

        # list of analyst objects (to use later, when we change initials for analysts objects)
        eventTeam = []
        # create an analyst per each pair of initials entered by the user when the event is created
        for initials in initialsList:
            analyst = Analyst(None, None, initials, None, None)
            db.updateAnalyst(analyst)
            # list of analysts to be passed as eventName parameter in event creation
            eventTeam.append(analyst)

        newEvent = Event(form.EventName.data,
                         form.EventDescription.data,
                         form.EventType.data,
                         1.0,
                         form.AssessmentDate.data.strftime('%m/%d/%Y'),
                         form.SCTG.data,
                         form.OrganizationName.data,
                         form.EventClassification.data,
                         form.EventClassifiedBy.data,
                         form.EventDerivedFrom.data,
                         form.DeclassificationDate.data.strftime('%m/%d/%Y'),
                         form.CustomerName.data,
                         False,
                         initialsList)
        db.updateEvent(analyst, newEvent)
        # redirect to the right page after creating the form
        return redirect(url_for("EventView", event=event))

    return render_template('CreateEvent.html', form=form)


@app.route('/CreateSystem', methods=['GET', 'POST'])
def CreateSystem():
    # create a form from the forms.py file (need to import the file)
    form = CreateSystemForm()

    # check if the create event button has been pressed, if so create an event obj
    if 'createSystem' in request.form:
        # GET THE LIST VALUES (make them real lists to pass as parameters)
        locations = form.systemLocation.data
        locationsList = list(locations.split("-"))

        routers = form.systemRouter.data
        routersList = list(routers.split("-"))

        switches = form.systemSwitch.data
        switchesList = list(switches.split("-"))

        rooms = form.systemRoom.data
        roomsList = list(rooms.split("-"))

        system = System(form.systemName.data,
                        form.systemDescription.data,
                        locationsList,
                        routersList,
                        switchesList,
                        roomsList,
                        form.systemTestPlan.data,
                        False,
                        form.systemConfidentiality.data,
                        form.systemIntegrity.data,
                        form.systemAvailability.data)

        db.updateSystem(analyst, system)
        return redirect(url_for("Systems"))

    return render_template('CreateSystem.html', form=form)


@app.route('/SystemView/<system>', methods=['GET', 'POST'])
def SystemView(system):
    for s in db.getAllSystems():
        if s.getId() == ObjectId(system):
            sys = db.getSystem(s)

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveSystem' in request.form:
        sys.setArchiveStatus(True)
        db.updateSystem(analyst, sys)
        return redirect(url_for('Systems'))

    return render_template('SystemView.html', system=sys)


@app.route('/EditSystem/<system>', methods=['GET', 'POST'])
def EditSystem(system):
    for s in db.getAllSystems():
        if s.getId() == ObjectId(system):
            sys = db.getSystem(s)

    form = EditSystemForm()
    # populate the form with the data of the system to edit
    if request.method == 'GET':
        # fix the lists, (NEED SOME WORK)
        locations = "-".join(sys.getLocation())
        routers = "-".join(sys.getRouter())
        switches = "-".join(sys.getSwitch())
        rooms = "-".join(sys.getRoom())

        form.EditSystemName.data = sys.getName()
        form.EditSystemDescription.data = sys.getDescription()
        form.EditSystemLocation.data = str(locations)
        form.EditSystemRouter.data = str(routers)
        form.EditSystemSwitch.data = str(switches)
        form.EditSystemRoom.data = str(rooms)
        form.EditSystemTestPlan.data = sys.getTestPlan()

    if 'editSystem' in request.form:
        # GET THE LIST VALUES (make them real lists to pass as parameters)
        locations = form.EditSystemLocation.data
        locationsList = list(locations.split("-"))

        routers = form.EditSystemRouter.data
        routersList = list(routers.split("-"))

        switches = form.EditSystemSwitch.data
        switchesList = list(switches.split("-"))

        rooms = form.EditSystemRoom.data
        roomsList = list(rooms.split("-"))

        sys.setName(form.EditSystemName.data)
        sys.setDescription(form.EditSystemDescription.data)
        sys.setLocation(locationsList)
        sys.setRouter(routersList)
        sys.setSwitch(switchesList)
        sys.setRoom(roomsList)
        sys.setTestplan(form.EditSystemTestPlan.data)

        db.updateSystem(analyst, sys)
        return redirect(url_for("SystemView", system=sys.getId()))

    return render_template('EditSystem.html', form=form, system=sys)


@app.route('/Systems')
def Systems():
    # get list of systems for this event and pass them as parameter (currently returning all systems in db)
    systemList = []
    for system in db.getAllSystems():
        if system.getArchiveStatus() == False:
            systemList.append(system)

    return render_template('Systems.html', systemList=systemList)


# function to archive a system from event and db
@app.route('/Systems/<system>', methods=['GET', 'POST'])
def ArchiveSystem(system):
    for s in db.getAllSystems():
        if s.getId() == ObjectId(system):
            s.setArchiveStatus(True)
            db.updateSystem(analyst, s)
            return redirect(url_for('Systems'))
    return redirect(url_for('Systems'))


# function to restore a system from event and db
@app.route('/ArchiveContentView/<system>', methods=['GET', 'POST'])
def RestoreSystem(system):
    for s in db.getAllSystems():
        if s.getId() == ObjectId(system):
            s.setArchiveStatus(False)
            db.updateSystem(analyst, s)
            return redirect(url_for('ArchiveContentView'))
    return redirect(url_for('ArchiveContentView'))


@app.route('/CreateTask', methods=['GET', 'POST'])
def CreateTask():
    # pass these lists as arguments to populate select fields with data from the db
    form = CreateTaskForm(tasks=db.getAllTasks(), analysts=db.getAllAnalyst(), collaborators=db.getAllAnalyst())

    if 'createTask' in request.form:
        task = Task(form.taskName.data,
                    form.taskDescription.data,
                    form.taskPriority.data,
                    form.taskProgress.data,
                    form.taskDueDate.data.strftime('%m/%d/%Y'),
                    form.taskAttachment.data,
                    form.associationToTask.data,
                    form.taskAnalystAssignment.data,
                    form.taskCollaboratorAssignment.data,
                    False)
        db.updateTask(analyst, task)
        return redirect(url_for("Tasks"))

    return render_template('CreateTask.html', form=form)


@app.route('/TaskView/<task>', methods=['GET', 'POST'])
def TaskView(task):
    for t in db.getAllTasks():
        if t.getId() == ObjectId(task):
            # task1 = db.getTask(t)
            task1 = t
    # display names of associated tasks instead of the id numbers
    taskName = []
    for task0 in task1.getAssociationToTask():
        for t in db.getAllTasks():
            if ObjectId(task0) == t.getId():
                taskName.append(t.getTitle())

    # array of initials
    analystAssg = []
    for task2 in task1.getAnalystAssigment():
        for t in db.getAllAnalyst():
            if ObjectId(task2) == t.getId():
                analystAssg.append(t.getInitial())

    # array of initials for collaborators
    collaborators = []
    for task3 in task1.getCollaboratorAssignment():
        for t in db.getAllAnalyst():
            if ObjectId(task3) == t.getId():
                collaborators.append(t.getInitial())

    # check if archive task button has been pressed, if so, set it to be archived and redirect
    if 'ArchiveTask' in request.form:
        task1.setArchiveStatus(True)
        db.updateTask(analyst, task1)
        return redirect(url_for('Tasks'))

    return render_template('TaskView.html', task=task1, taskName=taskName, analystAssg=analystAssg,
                           collaborators=collaborators)


@app.route('/EditTask/<task>', methods=['GET', 'POST'])
def EditTask(task):
    for t in db.getAllTasks():
        if t.getId() == ObjectId(task):
            task1 = db.getTask(t)
    form = EditTaskForm()

    form.associationToTask.choices = [(c.getId(), c.getTitle()) for c in db.getAllTasks()]
    form.taskAnalystAssignment.choices = [(c.getId(), c.getInitial()) for c in db.getAllAnalyst()]
    form.taskCollaboratorAssignment.choices = [(c.getId(), c.getInitial()) for c in db.getAllAnalyst()]
    # populate the form with the data of the task to edit
    if request.method == 'GET':
        form.taskName.data = task1.getTitle()
        form.taskDescription.data = task1.getDescription()
        form.taskPriority.data = task1.getPriority()
        form.taskProgress.data = task1.getProgress()
        form.taskDueDate.data = datetime.strptime(task1.getDueDate(), '%m/%d/%Y')
        form.taskAttachment.data = task1.getAttachment()
        form.associationToTask.data = task1.getAssociationToTask()
        form.taskAnalystAssignment.data = task1.getAnalystAssigment()
        form.taskCollaboratorAssignment.data = task1.getCollaboratorAssignment()

    if 'editTask' in request.form:
        task1.setTitle(form.taskName.data)
        task1.setDescription(form.taskDescription.data)
        task1.setPriority(form.taskPriority.data)
        task1.setProgress(form.taskProgress.data)
        task1.setDueDate(form.taskDueDate.data.strftime('%m/%d/%Y'))
        task1.setAttachment(form.taskAttachment.data)
        task1.setAssociationToTask(form.associationToTask.data)
        task1.setAnalystAssigment(form.taskAnalystAssignment.data)
        task1.setCollaboratorAssignment(form.taskCollaboratorAssignment.data)

        db.updateTask(analyst, task1)
        return redirect(url_for("TaskView", task=task1.getId()))

    return render_template('EditTask.html', form=form, task=task1)


@app.route('/Tasks')
def Tasks():
    # get list of systems for this event and pass them as parameter (currently returning all systems in db)
    tasksList = []
    for task in db.getAllTasks():
        if task.getArchiveStatus() == False:
            tasksList.append(task)
    return render_template('Tasks.html', tasksList=tasksList)


# function to archive a system from event and db
@app.route('/Tasks/<task>', methods=['GET', 'POST'])
def ArchiveTask(task):
    for y in db.getAllTasks():
        if y.getId() == ObjectId(task):
            y.setArchiveStatus(True)
            db.updateTask(analyst, y)
            return redirect(url_for('Tasks'))
    return redirect(url_for('Tasks'))


@app.route('/ArchiveContentView/<task>', methods=['GET', 'POST'])
def RestoreTask(task):
    if 'restoretask' in request.form:
        for r in db.getAllTasks():
            if r.getId() == ObjectId(task):
                r.setArchiveStatus(False)
                db.updateTask(analyst, r)
                return redirect(url_for('ArchiveContentView'))
    return redirect(url_for('ArchiveContentView'))


@app.route('/Tasks/<task>', methods=['GET', 'POST'])
def DemoteTask(task):
    for y in db.getAllTasks():
        if y.getId() == ObjectId(task):
            taskToDemote = y
            subtask = Subtask(taskToDemote.getTitle(),
                              taskToDemote.getDescription(),
                              taskToDemote.getProgress(),
                              taskToDemote.getDueDate(),
                              taskToDemote.getAttachment(),
                              taskToDemote.getAssociationToTask(),
                              taskToDemote.getAnalystAssigment(),
                              taskToDemote.getCollaboratorAssignment(), False)
            db.updateSubtask(analyst, subtask)
            db.deleteTask(analyst, taskToDemote)

            return redirect(url_for('Tasks'))
    return redirect(url_for('Tasks'))


@app.route('/CreateSubTask', methods=['GET', 'POST'])
def CreateSubTask():
    form = CreateSubtaskForm(subtasks=db.getAllSubtasks(), analysts=db.getAllAnalyst(),
                             collaborators=db.getAllAnalyst())

    if 'createSubtask' in request.form:
        subtask = Subtask(form.subTaskName.data,
                          form.subTaskDescription.data,
                          form.subTaskProgress.data,
                          form.subTaskDueDate.data.strftime('%m/%d/%Y'),
                          form.subTaskAttachment.data,
                          form.associationToSubtask.data,
                          form.subTaskAnalystAssignment.data,
                          form.subTaskCollaboratorAssignment.data, False)
        db.updateSubtask(analyst, subtask)
        return redirect(url_for("Subtasks"))

    return render_template('CreateSubTask.html', form=form)


@app.route('/EditSubTask/<subtask>', methods=['GET', 'POST'])
def EditSubTask(subtask):
    for sub in db.getAllSubtasks():
        if sub.getId() == ObjectId(subtask):
            subT = db.getSubtask(sub)
    form = EditSubtaskForm()
    form.associationToSubtask.choices = [(c.getId(), c.getTitle()) for c in db.getAllSubtasks()]
    form.subTaskAnalystAssignment.choices = [(c.getId(), c.getInitial()) for c in db.getAllAnalyst()]
    form.subTaskCollaboratorAssignment.choices = [(c.getId(), c.getInitial()) for c in db.getAllAnalyst()]

    # populate the form with the data of the system to edit
    if request.method == 'GET':
        form.subTaskName.data = subT.getTitle()
        form.subTaskDescription.data = subT.getDescription()
        form.subTaskProgress.data = subT.getProgress()
        form.subTaskDueDate.data = datetime.strptime(subT.getDueDate(), '%m/%d/%Y')
        form.subTaskAttachment.data = subT.getAttachment()
        form.associationToSubtask.data = subT.getAssociationToTask()
        form.subTaskAnalystAssignment.data = subT.getAnalystAssigment()
        form.subTaskCollaboratorAssignment.data = subT.getCollaboratorAssignment()

    if 'editSubtask' in request.form:
        subT.setTitle(form.subTaskName.data)
        subT.setDescription(form.subTaskDescription.data)
        subT.setDescription(form.subTaskProgress.data)
        subT.setDueDate(form.subTaskDueDate.data.strftime('%m/%d/%Y'))
        subT.setAttachment(form.subTaskAttachment.data)
        subT.setAssociationToTask(form.associationToSubtask.data)
        subT.setAnalystAssigment(form.subTaskAnalystAssignment.data)
        subT.setCollaboratorAssignment(form.subTaskCollaboratorAssignment.data)
        db.updateSubtask(analyst, subT)
        return redirect(url_for("SubTaskView", subtask=subT.getId()))

    return render_template('EditSubTask.html', form=form, subtask=subT)


@app.route('/SubTaskView/<subtask>', methods=['GET', 'POST'])
def SubTaskView(subtask):
    for sub in db.getAllSubtasks():
        if sub.getId() == ObjectId(subtask):
            subT = sub
    # display names of associated subtasks
    subtaskName = []
    for subtask in subT.getAssociationToTask():
        for t in db.getAllSubtasks():
            if ObjectId(subtask) == t.getId():
                subtaskName.append(t.getTitle())

    # array of initials FOR ASSIGNED ANALYSTS
    analystAssg = []
    print(subT.getAnalystAssigment())
    for task2 in subT.getAnalystAssigment():
        for t in db.getAllAnalyst():
            if ObjectId(task2) == t.getId():
                print(t.getInitial())
                analystAssg.append(t.getInitial())
    print(analystAssg)

    # array of initials for collaborators
    collaborators = []
    for subtask in subT.getCollaboratorAssignment():
        for t in db.getAllAnalyst():
            if ObjectId(subtask) == t.getId():
                collaborators.append(t.getInitial())

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveSubtask' in request.form:
        subT.setArchiveStatus(True)
        db.updateSubtask(analyst, subT)
        return redirect(url_for('Subtasks'))

    return render_template('SubTaskView.html', subtask=subT, subtaskName=subtaskName, analystAssg=analystAssg,
                           collaborators=collaborators)


@app.route('/Subtasks')
def Subtasks():
    subTasksList = []
    for subtask in db.getAllSubtasks():
        if subtask.getArchiveStatus() == False:
            subTasksList.append(subtask)
    return render_template('Subtasks.html', subTasksList=subTasksList)


# HAVEN'T WORKED ON FINDINGS YET
@app.route('/CreateFinding')
def CreateFinding():
    form = CreateFindingForm()
    # if 'createFinding' in request.form:
    #     finding = Finding()
    #     db.updateFinding(analyst, finding)
    return render_template('CreateFinding.html', form=form)


@app.route('/FindingsView')
def FindingsView():
    findingsList = []
    for finding in db.getAllFindings():
        if finding.getArchiveStatus() == False:
            findingsList.append(finding)
    return render_template('FindingsView.html', findingsList=findingsList)


@app.route('/FindingView/<finding>', methods=['GET', 'POST'])
def FindingView(finding):
    for f in db.getAllFindings():
        if f.getId() == ObjectId(finding):
            find = db.getSubtask(f)
    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveFinding' in request.form:
        find.setArchiveStatus(True)
        db.updateFinding(analyst, find)
        return redirect(url_for('FindingsView'))

    return render_template('FindingView.html', finding=find)


@app.route('/EditFinding/<finding>', methods=['GET', 'POST'])
def EditFinding(finding):
    for f in db.getAllFindings():
        if f.getId() == ObjectId(finding):
            find = db.getSubtask(f)
    form = EditFindingForm()
    # populate the form with the data of the system to edit
    if request.method == 'GET':
        form.findingHostName.data = find.getfindingHostName()
        form.findingIPPort.data = find.getfindingIPPort()
        form.findingDescription.data = find.getfindingDescription()
        form.findingLongDescription.data = find.getfindingLongDescription()
        form.findingStatus.data = find.getfindingStatus()
        form.findingType.data = find.getfindingType()
        form.findingClassification.data = find.findingClassification()
        form.associationToFinding.data = find.getassociationToFinding()
        form.findingEvidence.data = find.getfindingEvidence()
        form.findingConfidentiality.data = find.getfindingConfidentiality()
        form.findingIntegrity.data = find.getfindingIntegrity()
        form.findingAvailability.data = find.getfindingAvailability()
        form.findingAnalystAssignment.data = find.getfindingAnalystAssignment()
        form.findingCollaboratorAssignment.data = find.getfindingCollaboratorAssignment()
        form.findingPosture.data = find.getfindingPosture()
        form.mitigationBriefDescription.data = find.getmitigationBriefDescription()
        form.mitigationLongDescription.data = find.getmitigationLongDescription()
        form.findingThreatRelevance.data = find.getfindingThreatRelevance()
        form.findingEffectivenessRating.data = find.getfindingEffectivenessRating()
        form.impactDescription.data = find.getimpactDescription()
        form.impactLevel.data = find.getimpactLevel()
        form.severityCategoryCode.data = find.getseverityCategoryCode()

    if 'editFinding' in request.form:
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)
        find.setName(form.subTaskName.data)

        db.updateSubtask(analyst, find)
        return redirect(url_for("SubTaskView", finding=find.getId()))
    return render_template('EditFinding.html', form=form, finding=find)


@app.route('/GenerateReport')
def GenerateReport():
    return render_template('GenerateReport.html')


@app.route('/ArchiveContentView')
def ArchiveContentView():
    archivedSystemList = []
    for archivedsystem in db.getAllSystems():
        if archivedsystem.getArchiveStatus() == True:
            archivedSystemList.append(archivedsystem)
    archivedTasksList = []
    for archivedTask in db.getAllTasks():
        if archivedTask.getArchiveStatus() == True:
            archivedTasksList.append(archivedTask)
    return render_template('ArchiveContentView.html', archivedSystemList=archivedSystemList,
                           archivedTasksList=archivedTasksList)


@app.route('/ConfigurationContentView')
def ConfigurationContentView():
    return render_template('ConfigurationContentView.html')


@app.route('/ConfigurationFindingType')
def ConfigurationFindingType():
    return render_template('ConfigurationFindingType.html')


@app.route('/ConfigurationPostureTable')
def ConfigurationPostureTable():
    return render_template('ConfigurationPostureTable.html')


@app.route('/ConfigurationThreatLevel')
def ConfigurationThreatLevel():
    return render_template('ConfigurationThreatLevel.html')


@app.route('/ConfigurationImpactLevel')
def ConfigurationImpactLevel():
    return render_template('ConfigurationImpactLevel.html')


@app.route('/ConfigurationFindingClassification')
def ConfigurationFindingClassification():
    return render_template('ConfigurationFindingClassification.html')


@app.route('/ConfigurationCountermeasureTable')
def ConfigurationCountermeasureTable():
    return render_template('ConfigurationCountermeasureTable.html')


@app.route('/ConfigurationEventClassification')
def ConfigurationEventClassification():
    return render_template('ConfigurationEventClassification.html')


@app.route('/ConfigurationLevelTable')
def ConfigurationLevelTable():
    return render_template('ConfigurationLevelTable.html')


@app.route('/ConfigurationEventType')
def ConfigurationEventType():
    return render_template('ConfigurationEventType.html')


@app.route('/ConfigurationFindingImpact')
def ConfigurationFindingImpact():
    return render_template('ConfigurationFindingImpact.html')


@app.route('/ConfigurationSeverityCategory')
def ConfigurationSeverityCategory():
    return render_template('ConfigurationSeverityCategory.html')


@app.route('/ConfigurationProgressTable')
def ConfigurationProgressTable():
    return render_template('ConfigurationProgressTable.html')


@app.route('/ConfigurationEventRules')
def ConfigurationEventRules():
    return render_template('ConfigurationEventRules.html')


@app.route('/ConfigurationRiskMatrix')
def ConfigurationRiskMatrix():
    return render_template('ConfigurationRiskMatrix.html')


@app.route('/Help')
def Help():
    return render_template('Help.html')


@app.route('/Sync')
def Sync():
    return render_template('Sync.html')


@app.route('/EventTree')
def EventTree():
    return render_template('EventTree.html')


@app.route('/AnalystProgressSummaryContentView')
def AnalystProgressSummaryContentView():
    return render_template('AnalystProgressSummaryContentView.html')


if __name__ == '__main__':
    app.run(debug=True)  # runs the application
