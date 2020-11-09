import os
from datetime import datetime
from bson import ObjectId
from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from database.databaseHandler import DatabaseHandler
from forms import *
from Helper import *
from objectsHandler import *

import xlsxwriter

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
    errorMessage = ''
    initialsCoalition = False
    events = db.getAllEvents()
    for e in events:
        if not e.getArchiveStatus():
            event = e
    form = CreateAnalystForm()

    if 'createAnalyst' in request.form:
        # get the string from the user input, transform to list
        titleList = list(form.CreateAnalystTitle.data.split("-"))

        # check for initials in db to avoid collisions
        for init in db.getAllAnalyst():
            if form.CreateAnalystInitials.data == init.getInitial():
                initialsCoalition = True
                errorMessage = "initials already exist in the Data Base"

                return redirect(url_for("CreateAnalyst"))
        # if there is not collition in the db, then create the new analyst
        if initialsCoalition == False:
            a = createAnalyst(form.CreateAnalystFName.data,
                              form.CreateAnalystLName.data,
                              form.CreateAnalystInitials.data,
                              titleList,
                              form.CreateAnalystRole.data)
            db.updateAnalyst(a)

        # add this analyst to the event team of actual event
        event.getEventTeam().append(a.getInitial())
        db.updateEvent(analyst, event)
        return redirect(url_for("EventView"))

    return render_template('CreateAnalyst.html', form=form, errorMessage=errorMessage)


@app.route('/EditAnalyst/<initial>', methods=['GET', 'POST'])
def EditAnalyst(initial):
    global analyst
    for a in db.getAllAnalyst():
        if a.getInitial() == initial:
            m = a

    form = EditAnalystForm()

    if request.method == 'GET':
        # get the list, make it a string to display it when pre populating the form
        titleList = "-".join(m.getTitle())
        print(titleList)

        # TO DO: pre populate the edit analyst form
        # pre populate form (is not working... why)
        form.EditAnalystFName.data = m.getFirstName()
        form.EditAnalystLName.data = m.getLastName()
        form.EditAnalystTitle.data = titleList
        form.EditAnalystInitials.data = m.getInitial()
        form.EditAnalystRole.data = m.getRole()

    if 'EditAnalyst' in request.form:
        # we have edited the analyst object so far, now update the event list of initials
        if initial in event.getEventTeam():
            event.getEventTeam().remove(initial)
            event.getEventTeam().append(form.EditAnalystInitials.data)
            db.updateEvent(analyst, event)

        titles = form.EditAnalystTitle.data
        titleList = list(titles.split("-"))
        print(titleList)

        m.setFirstName(form.EditAnalystFName.data)
        m.setLastName(form.EditAnalystLName.data)
        m.setTitle(titleList)
        m.setInitial(form.EditAnalystInitials.data)
        m.setRole(form.EditAnalystRole.data)
        db.updateAnalyst(m)
        return redirect(url_for('EventView'))

    return render_template('EditAnalyst.html', form=form, analys=m.getInitial())


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
    if initial in event.getEventTeam():
        event.getEventTeam().remove(initial)
        db.updateEvent(analyst, event)

    # delete analyst object from the db as well
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
    # get lists of analysts initials to display in event view
    leadList = []
    for ana in db.getAllAnalyst():
        if ana.getRole() == Role.LEAD:
            leadList.append(ana.getInitial())

    nonleadList = []
    for ana in db.getAllAnalyst():
        if ana.getRole() != Role.LEAD:
            nonleadList.append(ana.getInitial())

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveEvent' in request.form:
        # event.setArchiveStatus(True)
        # db.updateEvent(analyst, event)
        # delete event and its systems, tasks, etc since well deal only with one event at a time
        for subtask in db.getAllSubtasks():
            db.deleteSubtask(analyst, subtask)
        for task in db.getAllTasks():
            db.deleteTask(analyst, task)
        for system in db.getAllSystems():
            db.deleteSystem(analyst, system)
        for analyst in db.getAllAnalyst():
            db.deleteAnalyst(analyst)
        for event in db.getAllEvents():
            db.deleteEvent(analyst, event)
        return redirect(url_for('SetupContentView'))

    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=event, db=db, leadList=leadList, nonleadList=nonleadList)


@app.route('/EditEvent', methods=['GET', 'POST'])
def EditEvent():
    # events = db.getAllEvents()
    # for e in events:
    #     if not e.getArchiveStatus():
    #         event = e
    form = EditEventForm()
    # populate the form with the data of the actual event
    if request.method == 'GET':
        form.EditEventName.data = event.getName()
        form.EditEventDescription.data = event.getDescription()
        form.EditEventType.data = event.getType()
        form.EditEventVersion.data = event.getVersion()
        form.EditEventOrganizationName.data = event.getOrganizationName()
        form.EditEventCustomerName.data = event.getCustomerName()
        # form.EditEventAssessmentDate.data = datetime.strptime(event.getDate(), '%m/%d/%Y')
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
        # event.setDate(form.EditEventAssessmentDate.data.strftime('%m/%d/%Y'))
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
    # create a form from the forms.py file (need to import the file)
    form = CreateEventForm()

    # check if the create event button has been pressed, if so create an event obj
    if 'createEvent' in request.form:
        # delete current event, systems, everything from the db, to handle only one event at a time
        for subtask in db.getAllSubtasks():
            db.deleteSubtask(analyst, subtask)
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

        newEvent = createEvent(form.EventName.data,
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

        system = createSystem(form.systemName.data,
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
        task = createTask(form.taskName.data,
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
    # display names of associated tasks instead of the id numbers stored in db
    # if we dont store the unique id number we might get repeated tasks/analysts if they have the same name...
    taskName = []
    for task0 in task1.getAssociationToTask():
        for t in db.getAllTasks():
            if ObjectId(task0) == t.getId():
                taskName.append(t.getTitle())

    # check if archive task button has been pressed, if so, set it to be archived and redirect
    if 'ArchiveTask' in request.form:
        task1.setArchiveStatus(True)
        db.updateTask(analyst, task1)
        return redirect(url_for('Tasks'))

    if 'DemoteTask' in request.form:
        subtask = createSubtask(task1.getTitle(),
                                task1.getDescription(),
                                task1.getProgress(),
                                task1.getDueDate(),
                                task1.getAttachment(),
                                task1.getAssociationToTask(),
                                task1.getAnalystAssigment(),
                                task1.getCollaboratorAssignment(), False)
        db.updateSubtask(analyst, subtask)
        db.deleteTask(analyst, task1)
        return redirect(url_for('Tasks'))

    return render_template('TaskView.html', task=task1, taskName=taskName)


@app.route('/DemoteTask/<task>', methods=['GET', 'POST'])
def DemoteTask(task):
    for t in db.getAllTasks():
        if t.getId() == ObjectId(task):
            task1 = db.getTask(t)
    subtask = createSubtask(task1.getTitle(),
                            task1.getDescription(),
                            task1.getProgress(),
                            task1.getDueDate(),
                            task1.getAttachment(),
                            task1.getAssociationToTask(),
                            task1.getAnalystAssigment(),
                            task1.getCollaboratorAssignment(), False)
    db.updateSubtask(analyst, subtask)
    db.deleteTask(analyst, task1)
    return redirect(url_for('Tasks'))


@app.route('/EditTask/<task>', methods=['GET', 'POST'])
def EditTask(task):
    for t in db.getAllTasks():
        if t.getId() == ObjectId(task):
            task1 = db.getTask(t)
    form = EditTaskForm()

    form.associationToTask.choices = [(c.getId(), c.getTitle()) for c in db.getAllTasks()]
    form.taskAnalystAssignment.choices = [(c.getInitial(), c.getInitial()) for c in db.getAllAnalyst()]
    form.taskCollaboratorAssignment.choices = [(c.getInitial(), c.getInitial()) for c in db.getAllAnalyst()]
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


@app.route('/RestoreTask/<task>', methods=['GET', 'POST'])
def RestoreTask(task):
    for r in db.getAllTasks():
        if r.getId() == ObjectId(task):
            r.setArchiveStatus(False)
            db.updateTask(analyst, r)
            return redirect(url_for('ArchiveContentView'))
    return redirect(url_for('ArchiveContentView'))


@app.route('/CreateSubTask', methods=['GET', 'POST'])
def CreateSubTask():
    form = CreateSubtaskForm(subtasks=db.getAllSubtasks(), analysts=db.getAllAnalyst(),
                             collaborators=db.getAllAnalyst())

    if 'createSubtask' in request.form:
        subtask = createSubtask(form.subTaskName.data,
                                form.subTaskDescription.data,
                                Progress.getMember(form.subTaskProgress.data),
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
    form.subTaskAnalystAssignment.choices = [(c.getInitial(), c.getInitial()) for c in db.getAllAnalyst()]
    form.subTaskCollaboratorAssignment.choices = [(c.getInitial(), c.getInitial()) for c in db.getAllAnalyst()]

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
        subT.setProgress(form.subTaskProgress.data)
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

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveSubtask' in request.form:
        subT.setArchiveStatus(True)
        db.updateSubtask(analyst, subT)
        return redirect(url_for('Subtasks'))
    if 'PromoteToTask' in request.form:
        task = createTask(subT.getTitle(),
                          subT.getDescription(),
                          Priority.MEDIUM.value,
                          subT.getProgress(),
                          subT.getDueDate(),
                          subT.getAttachment(),
                          subT.getAssociationToTask(),
                          subT.getAnalystAssigment(),
                          subT.getCollaboratorAssignment(),
                          False)
        db.updateTask(analyst, task)
        db.deleteSubtask(analyst, subT)
        return redirect(url_for('Tasks'))

    return render_template('SubTaskView.html', subtask=subT, subtaskName=subtaskName)


@app.route('/PromoteToTask/<subtask>', methods=['GET', 'POST'])
def PromoteToTask(subtask):
    for sub in db.getAllSubtasks():
        if sub.getId() == ObjectId(subtask):
            subT = sub
    task = createTask(subT.getTitle(),
                      subT.getDescription(),
                      Priority.MEDIUM.value,
                      subT.getProgress(),
                      subT.getDueDate(),
                      subT.getAttachment(),
                      subT.getAssociationToTask(),
                      subT.getAnalystAssigment(),
                      subT.getCollaboratorAssignment(),
                      False)
    db.updateTask(analyst, task)
    db.deleteSubtask(analyst, subT)
    return redirect(url_for('Subtasks'))


@app.route('/Subtasks')
def Subtasks():
    subTasksList = []
    for subtask in db.getAllSubtasks():
        if subtask.getArchiveStatus() == False:
            subTasksList.append(subtask)

        # analystAssg = []
        # for initials in subtask.getAnalystAssigment():
        #     for anal in db.getAllAnalyst():
        #         if ObjectId(initials) == anal.getId():
        #             analystAssg.append(anal.getInitial())
        #             for initials in subtask.getCollaboratorAssignment():
        #                 if ObjectId(initials) == anal.getId():
        #                     analystAssg.append(anal.getInitial())
        #                     print(analystAssg)

    return render_template('Subtasks.html', subTasksList=subTasksList)


# function to archive a system from event and db
@app.route('/Subtasks/<subtask>', methods=['GET', 'POST'])
def ArchiveSubtask(subtask):
    for y in db.getAllSubtasks():
        if y.getId() == ObjectId(subtask):
            y.setArchiveStatus(True)
            db.updateSubtask(analyst, y)
            return redirect(url_for('Subtasks'))
    return redirect(url_for('Subtasks'))


@app.route('/RestoreSubtask/<subtask>', methods=['GET', 'POST'])
def RestoreSubtask(subtask):
    for s in db.getAllSubtasks():
        if s.getId() == ObjectId(subtask):
            s.setArchiveStatus(False)
            db.updateSubtask(analyst, s)
            return redirect(url_for('ArchiveContentView'))
    return redirect(url_for('ArchiveContentView'))


@app.route('/CreateFinding', methods=['GET', 'POST'])
def CreateFinding():
    # TO-DO: create lists of non-archived objects
    form = CreateFindingForm(findings=db.getAllFindings(), analysts=db.getAllAnalyst(),
                             collaborators=db.getAllAnalyst())
    if 'createFinding' in request.form:
        # if I just pass form.findingPosture.data we would get the same result, so what is the diff?
        # print(Posture.getMember(form.findingPosture.data))
        # cast this to enum type
        finding = createFinding(form.findingHostName.data,
                                form.findingIPPort.data,
                                form.findingDescription.data,
                                FindingStatus.getMember(form.findingStatus.data),
                                FindingType.getMember(form.findingType.data),
                                FindingClassification.getMember(form.findingClassification.data),
                                form.associationToFinding.data,
                                form.findingEvidence.data,
                                False,
                                Confidentiality.getMember(form.findingConfidentiality.data),
                                Integrity.getMember(form.findingIntegrity.data),
                                Availability.getMember(form.findingAvailability.data),
                                form.findingAnalystAssignment.data,
                                Posture.getMember(form.findingPosture.data),
                                form.mitigationBriefDescription.data,
                                form.mitigationLongDescription.data,
                                Relevance.getMember(int(form.findingThreatRelevance.data)),
                                EffectivenessRating.getMember(int(form.findingEffectivenessRating.data)),
                                form.impactDescription.data,
                                ImpactLevel.getMember(int(form.impactLevel.data)),
                                SeverityCategoryCode.getMember(int(form.severityCategoryCode.data)),
                                form.findingLongDescription.data,
                                form.findingCollaboratorAssignment.data)
        db.updateFinding(analyst, finding)
        return redirect(url_for("FindingsView"))

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
        if f.getid() == ObjectId(finding):
            find = f
    # display names of associated subtasks
    findingsName = []
    for finding in find.getAssociationTo():
        for t in db.getAllFindings():
            if ObjectId(finding) == t.getid():
                findingsName.append(t.getHostName())

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveFinding' in request.form:
        find.setArchiveStatus(True)
        db.updateFinding(analyst, find)
        return redirect(url_for('FindingsView'))

    if 'DeleteFinding' in request.form:
        db.deleteFinding(analyst, find)
        return redirect(url_for('FindingsView'))

    return render_template('FindingView.html', finding=find, findingsName=findingsName)


@app.route('/EditFinding/<finding>', methods=['GET', 'POST'])
def EditFinding(finding):
    for f in db.getAllFindings():
        if f.getid() == ObjectId(finding):
            find = f
    form = EditFindingForm()
    form.associationToFinding.choices = [(c.getid(), c.getHostName()) for c in db.getAllFindings()]
    form.findingAnalystAssignment.choices = [(c.getId(), c.getInitial()) for c in db.getAllAnalyst()]
    form.findingCollaboratorAssignment.choices = [(c.getId(), c.getInitial()) for c in db.getAllAnalyst()]
    # populate the form with the data of the system to edit
    if request.method == 'GET':
        form.findingHostName.data = find.getHostName()
        form.findingIPPort.data = find.getIpPort()
        form.findingDescription.data = find.getDescription()
        form.findingLongDescription.data = find.getLongDescription()
        form.findingStatus.data = find.getStatus()
        form.findingType.data = find.getType()
        # cannot set relevance impact level and severity code to pre populate the form
        # print(Relevance.getMember(find.getRelevance().value))
        # print(find.getRelevance())
        # print(type(find.getRelevance().value))
        form.findingClassification.data = find.getClassification()
        form.associationToFinding.data = find.getAssociationTo()
        form.findingEvidence.data = find.getEvidence()
        form.findingAnalystAssignment.data = find.getAnalystAssigned()
        form.findingCollaboratorAssignment.data = find.getCollaboratorsAssigned()
        form.findingPosture.data = find.getPosture()
        form.mitigationBriefDescription.data = find.getMitigationBriefDescription()
        form.mitigationLongDescription.data = find.getMitigationLongDescription()
        form.findingThreatRelevance.data = find.getRelevance()
        form.findingEffectivenessRating.data = find.getCountermeasureEffectivenessRating()
        form.impactDescription.data = find.getImpactDescription()
        form.impactLevel.data = find.getImpactLevel()
        form.severityCategoryCode.data = find.getSeverityCategoryCode()

    if 'editFinding' in request.form:
        find.setHostName(form.findingHostName.data)
        find.setIpPort(form.findingIPPort.data)
        find.setDescription(form.findingDescription.data)
        find.setLongDescription(form.findingLongDescription.data)
        find.setStatus(form.findingStatus.data)
        find.setType(form.findingType.data)
        find.setClassification(form.findingClassification.data)
        find.setAssociationTo(form.associationToFinding.data)
        find.setEvidence(form.findingEvidence.data)
        find.setAnalystAssigned(form.findingAnalystAssignment.data)
        find.setCollaboratorAssigned(form.findingCollaboratorAssignment.data)
        find.setPosture(form.findingPosture.data)
        find.setMitigationBriefDescription(form.mitigationBriefDescription.data)
        find.setMitigationLongDescription(form.mitigationLongDescription.data)
        find.setRelevance(Relevance.getMember(int(form.findingThreatRelevance.data)))
        find.setCountermeasureEffectivenessRating(
            EffectivenessRating.getMember(int(form.findingEffectivenessRating.data)))
        find.setImpactDescription(form.impactDescription.data)
        find.setImpactLevel(ImpactLevel.getMember(int(form.impactLevel.data)))
        find.setSeverityCategoryCode(SeverityCategoryCode.getMember(int(form.severityCategoryCode.data)))

        db.updateFinding(analyst, find)
        return redirect(url_for("FindingView", finding=find.getid()))
    return render_template('EditFinding.html', form=form, finding=find)


# function to archive a system from event and db
@app.route('/ArchiveFinding/<finding>', methods=['GET', 'POST'])
def ArchiveFinding(finding):
    for y in db.getAllFindings():
        if y.getid() == ObjectId(finding):
            y.setArchiveStatus(True)
            db.updateFinding(analyst, y)
            return redirect(url_for('FindingsView'))
    return redirect(url_for('FindingsView'))


@app.route('/RestoreFinding/<finding>', methods=['GET', 'POST'])
def RestoreFinding(finding):
    for r in db.getAllFindings():
        if r.getid() == ObjectId(finding):
            r.setArchiveStatus(False)
            db.updateFinding(analyst, r)
            return redirect(url_for('ArchiveContentView'))
    return redirect(url_for('ArchiveContentView'))


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
    archivedSubtasksList = []
    for archivedSubtask in db.getAllSubtasks():
        if archivedSubtask.getArchiveStatus() == True:
            archivedSubtasksList.append(archivedSubtask)

    archivedFindingsList = []
    for archivedFinding in db.getAllFindings():
        if archivedFinding.getArchiveStatus() == True:
            archivedFindingsList.append(archivedFinding)
    return render_template('ArchiveContentView.html', archivedSystemList=archivedSystemList,
                           archivedTasksList=archivedTasksList, archivedSubtasksList=archivedSubtasksList,
                           archivedFindingsList=archivedFindingsList)


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


# REPORTS

@app.route('/RiskMatrixReport')
def RiskMatrixReport():
    print(RiskMatrixReport)
    return render_template('FindingsView.html')


@app.route('/ERBReport')
def ERBReport():
    print("ERBReport")
    return render_template('FindingsView.html')


@app.route('/FinalTechnicalReport')
def FinalTechnicalReport():
    print("FinalTechnicalReport")
    return render_template('FindingsView.html')


@app.route('/AnalystProgressSummaryContentView/<initials>', methods=['GET', 'POST'])
def AnalystProgressSummaryContentView(initials):
    for analyst in db.getAllAnalyst():
        if analyst.getInitial() == initials:
            a = analyst

    findingsList = []
    for finding in db.getAllFindings():
        for aanalyst in finding.getAnalystAssigned():
            if a.getInitial() == aanalyst:
                findingsList.append(finding)

    tasksList = []
    for task in db.getAllTasks():
        for aanalyst in task.getAnalystAssigment():
            if a.getInitial() == aanalyst:
                tasksList.append(task)

    subTasksList = []
    for subtask in db.getAllSubtasks():
        for aanalyst in subtask.getAnalystAssigment():
            if a.getInitial() == aanalyst:
                subTasksList.append(subtask)

    return render_template('AnalystProgressSummaryContentView.html', findingsList=findingsList, tasksList=tasksList,
                           subTasksList=subTasksList)


if __name__ == '__main__':
    app.run(debug=True)  # runs the application
