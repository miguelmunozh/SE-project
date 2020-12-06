import os

from bson import ObjectId
from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from forms import *
from Helper import *
from reportsHandler import generateERB, generateFinalTecReport, createRiskMatrixReport
from event.eventHandler import *
from system.systemHandler import *
from task.taskHandler import *
from task.subtaskHandler import *
from finding.findingHandler import *
from analyst.analystHandler import *

# get instance of handlers
eventHandler = EventHandler()
systemHandler = SystemHandler()
taskHandler = TaskHandler()
subtaskHandler = SubtaskHandler()
findingHandler = FindingHandler()
analystHandler = AnalystHandler()

app = Flask(__name__)
Bootstrap(app)
# needed for flask-wtforms
app.config['SECRET_KEY'] = 'encrypted'

# analyst to pass as parameter to the updateEvent function,(will be deleted when we can know which analyst entered
# the system)
analyst = Analyst("jonathan", "roman", "jr", ["jr", "sr"], Role.LEAD)
notEvent = False
events = eventHandler.getEvent()

# check if there is an event in the db
if events == None:
    notEvent = True
    event = None
else:
    event = events


# check if there is a non archived event, is so set it as current event
# for e in events:
#     if not e.getArchiveStatus():
#         event = e


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
    events = eventHandler.getEvent()
    if not events.getArchiveStatus():
        event = events

    form = CreateAnalystForm()

    if 'createAnalyst' in request.form:
        # get the string from the user input, transform to list
        titleList = list(form.CreateAnalystTitle.data.split("-"))

        # check for initials in db to avoid collisions
        for init in analystHandler.getAllAnalyst():
            if form.CreateAnalystInitials.data == init.getInitial():
                initialsCoalition = True
                errorMessage = "initials already exist in the Data Base"

                return redirect(url_for("CreateAnalyst"))
        # if there is not coalition in the db, then create the new analyst
        if initialsCoalition == False:
            analystHandler.appendAnalyst(form.CreateAnalystFName.data,
                                         form.CreateAnalystLName.data,
                                         form.CreateAnalystInitials.data,
                                         titleList,
                                         form.CreateAnalystRole.data)

            # add this analyst to the event team of actual event
            event.getEventTeam().append(form.CreateAnalystInitials.data)
            eventHandler.updateEvent(analyst, event)

        return redirect(url_for("EventView"))

    return render_template('CreateAnalyst.html', form=form, errorMessage=errorMessage)


@app.route('/EditAnalyst/<initial>', methods=['GET', 'POST'])
def EditAnalyst(initial):
    global analyst
    analystHandler.loadAllAnalystFromDatabase()
    for a in analystHandler.getAllAnalyst():
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
            eventHandler.updateEvent(analyst, event)

        titles = form.EditAnalystTitle.data
        titleList = list(titles.split("-"))
        print(titleList)

        m.setFirstName(form.EditAnalystFName.data)
        m.setLastName(form.EditAnalystLName.data)
        m.setTitle(titleList)
        m.setInitial(form.EditAnalystInitials.data)
        m.setRole(form.EditAnalystRole.data)

        analystHandler.updateAnalyst(m)
        return redirect(url_for('EventView'))

    return render_template('EditAnalyst.html', form=form, analys=m.getInitial())


# function to delete analyst initials from event and db
@app.route('/EventView/<string:initial>', methods=['GET', 'POST'])
def deleteAnalyst(initial):
    global analyst
    events = eventHandler.getEventFromDatabase()
    if events != None:
        event = events

    # get the event list of analyst initials and remove the selected one (will change when we store a list of
    # analysts instead of a list of initials)
    if initial in event.getEventTeam():
        event.getEventTeam().remove(initial)
        ana = analystHandler.getAllAnalyst()[0]
        eventHandler.updateEvent(ana, event)

    # delete analyst object from the db as well
    # for analyst in analystHandler.getAllAnalyst():
    #     if analyst.getInitial() == initial:
    #         db.removeAnalyst(analyst)

    return redirect(url_for('EventView', event=eventHandler.getEvent()))


@app.route('/CreateEvent', methods=['GET', 'POST'])
def CreateEvent():
    global analyst
    # create a form from the forms.py file (need to import the file)
    form = CreateEventForm()

    # check if the create event button has been pressed, if so create an event obj
    if 'createEvent' in request.form:
        # # delete current event, systems, everything from the db, to handle only one event at a time
        # for subtask in subtaskHandler.getAllsubTask():
        #     subtask.setArchiveStatus(True)
        # for task in taskHandler.getAllTask():
        #     task.setArchiveStatus(True)
        # for system in systemHandler.getAllSystems():
        #     system.setArchiveStatus(True)
        # for analyst in analystHandler.getAllAnalyst():
        #     db.deleteAnalyst(analyst)

        # if there is an event, delete to create the new one
        # e = eventHandler.getEvent()
        # if e != None:
        #     print("event deleted to create a new one")
        #     a = eventHandler.getEvent(e)
        #     a.setArchiveStatus(True)

        # get analysts lists together, (will change when we store a list of analysts instead of a list of initials)
        lead = form.EventLeadAnalysts.data
        list1 = list(lead.split("-"))

        nonLead = form.EventAnalysts.data
        list2 = list(nonLead.split("-"))
        # represents the event team which is a list including lead and non-lead analysts
        initialsList = list1 + list2

        # list of analyst objects (to use later, when we change initials for analysts objects)
        # create an analyst per each pair of initials entered by the user when the event is created
        for initials in list1:
            analystHandler.appendAnalyst(None, None, initials, None, Role.LEAD)

        for initials in list2:
            analystHandler.appendAnalyst(None, None, initials, None, Role.ANALYST)
            # list of analysts to be passed as eventName parameter in event creation

        eventHandler.createEvent(analyst,
                                 form.EventName.data,
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

        # redirect to the right page after creating the form
        return redirect(url_for("EventView", event=eventHandler.getEvent()))

    return render_template('CreateEvent.html', form=form)


@app.route('/EventView', methods=['GET', 'POST'])
def EventView():
    global analyst
    global notEvent
    events = eventHandler.getEvent()
    if events != None:
        event = events
    else:
        event = None
    # if notEvent:
    #     event = None

    leads = []
    nonLeads = []
    list = eventHandler.getEventFromDatabase().getEventTeam()
    for ana in list:
        for a in analystHandler.getAllAnalyst():
            if ana == a.getInitial() and a.getRole() == Role.LEAD:
                leads.append(ana)

            if ana == a.getInitial() and a.getRole() != Role.LEAD:
                nonLeads.append(ana)

    # get lists of analysts initials to display in event view
    leadList = []
    for ana in analystHandler.getAllAnalyst():

        if ana.getRole() == Role.LEAD:
            leadList.append(ana.getInitial())

    nonleadList = []
    for ana in analystHandler.getAllAnalyst():
        if ana.getRole() != Role.LEAD:
            nonleadList.append(ana.getInitial())

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveEvent' in request.form:
        # event.setArchiveStatus(True)
        # db.updateEvent(analyst, event)
        # delete event and its systems, tasks, etc since well deal only with one event at a time
        for subtask in subtaskHandler.getAllsubTask():
            subtask.setArchiveStatus(True)
        for task in taskHandler.getAllTask():
            task.setArchiveStatus(True)
        for system in systemHandler.getAllSystems():
            system.setArchiveStatus(True)

        event.setArchiveStatus(True)
        return redirect(url_for('SetupContentView'))

    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=eventHandler.getEventFromDatabase(), leadList=leads,
                           nonleadList=nonLeads)


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

        eventHandler.updateEvent(analyst, event)
        return redirect(url_for("EventView"))

    return render_template('EditEvent.html', event=event, form=form)  # pass parameter to populate with placeholders


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

        systemHandler.appendSystem(analyst,
                                   form.systemName.data,
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

        return redirect(url_for("Systems"))

    return render_template('CreateSystem.html', form=form)


@app.route('/SystemView/<system>', methods=['GET', 'POST'])
def SystemView(system):
    systemHandler.loadSystems()
    sys = systemHandler.getSystem(ObjectId(system))

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveSystem' in request.form:
        sys.setArchiveStatus(True)
        systemHandler.updateSystem(sys, analyst)
        return redirect(url_for('Systems'))
    return render_template('SystemView.html', system=sys)


@app.route('/EditSystem/<system>', methods=['GET', 'POST'])
def EditSystem(system):
    # systemHandler.loadSystems()
    sys = systemHandler.getSystem(ObjectId(system))

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

        systemHandler.updateSystem(sys, analyst)
        return redirect(url_for("SystemView", system=sys.getId()))

    return render_template('EditSystem.html', form=form, system=sys)


@app.route('/Systems')
def Systems():
    # get list of systems for this event and pass them as parameter (currently returning all systems in db)
    systemHandler.loadSystems()
    systemList = []
    for system in systemHandler.getAllSystems():
        if system.getArchiveStatus() == False:
            systemList.append(system)

    return render_template('Systems.html', systemList=systemList)


# function to archive a system from event and db
@app.route('/Systems/<system>', methods=['GET', 'POST'])
def ArchiveSystem(system):
    sys = systemHandler.getSystem(ObjectId(system))
    sys.setArchiveStatus(True)
    systemHandler.updateSystem(sys, analyst)

    return redirect(url_for('Systems'))


# function to restore a system from event and db
@app.route('/ArchiveContentView/<system>', methods=['GET', 'POST'])
def RestoreSystem(system):
    sys = systemHandler.getSystem(ObjectId(system))
    sys.setArchiveStatus(False)
    systemHandler.updateSystem(sys, analyst)

    return redirect(url_for('ArchiveContentView'))


@app.route('/CreateTask', methods=['GET', 'POST'])
def CreateTask():
    systemHandler.loadSystems()
    taskHandler.loadTask()
    # pass these lists as arguments to populate select fields with data from the db
    form = CreateTaskForm(tasks=taskHandler.getAllTask(), analysts=analystHandler.getAllAnalyst(),
                          collaborators=analystHandler.getAllAnalyst(), systems=systemHandler.getAllSystems())

    if 'createTask' in request.form:
        taskHandler.appendTask(analyst,
                               form.taskName.data,
                               form.taskDescription.data,
                               form.taskPriority.data,
                               form.taskProgress.data,
                               form.taskDueDate.data.strftime('%m/%d/%Y'),
                               form.associationToTask.data,
                               form.taskAnalystAssignment.data,
                               form.taskCollaboratorAssignment.data,
                               False,
                               form.associationToSystem.data,
                               form.taskAttachment.data)

        return redirect(url_for("Tasks"))

    return render_template('CreateTask.html', form=form)


@app.route('/TaskView/<task>', methods=['GET', 'POST'])
def TaskView(task):
    taskHandler.loadTask()
    task1 = taskHandler.getTask(ObjectId(task))
    # display names of associated tasks instead of the id numbers stored in db
    # if we dont store the unique id number we might get repeated tasks/analysts if they have the same name...
    taskName = []
    for task0 in task1.getAssociationToTask():
        for t in taskHandler.getAllTask():
            if ObjectId(task0) == t.getId():
                taskName.append(t.getTitle())

    systemHandler.loadSystems()
    if task1.getAssociationToSystem():
        systemParent = ObjectId(task1.getAssociationToSystem()[0])
        systemName = systemHandler.getSystem(ObjectId(task1.getAssociationToSystem()[0])).getName()
    else:
        systemParent = ""
        systemName = ""

    # print(os.path.abspath(task1.getAttachment()))

    # check if archive task button has been pressed, if so, set it to be archived and redirect
    if 'ArchiveTask' in request.form:
        task1.setArchiveStatus(True)
        taskHandler.updateTask(task1, analyst)
        return redirect(url_for('Tasks'))

    if 'DemoteTask' in request.form:
        subtaskHandler.appendSubtask(analyst,
                                     task1.getTitle(),
                                     task1.getDescription(),
                                     task1.getProgress(),
                                     task1.getDueDate(),
                                     [],
                                     task1.getAnalystAssigment(),
                                     task1.getCollaboratorAssignment(),
                                     False,
                                     task1.getAttachment())
        task1.setArchiveStatus(True)
        return redirect(url_for('Tasks'))

    return render_template('TaskView.html', task=task1, taskName=taskName, systemParent=systemParent,
                           systemName=systemName)


@app.route('/DemoteTask/<task>', methods=['GET', 'POST'])
def DemoteTask(task):
    taskHandler.loadTask()
    task1 = taskHandler.getTask(ObjectId(task))

    subtaskHandler.appendSubtask(analyst,
                                 task1.getTitle(),
                                 task1.getDescription(),
                                 task1.getProgress(),
                                 task1.getDueDate(),
                                 [],
                                 task1.getAnalystAssigment(),
                                 task1.getCollaboratorAssignment(),
                                 False,
                                 task1.getAttachment())

    task1.setArchiveStatus(True)
    return redirect(url_for('Tasks'))


@app.route('/EditTask/<task>', methods=['GET', 'POST'])
def EditTask(task):
    taskHandler.loadTask()
    systemHandler.loadSystems()
    task1 = taskHandler.getTask(ObjectId(task))
    form = EditTaskForm()

    form.associationToTask.choices = [(c.getId(), c.getTitle()) for c in taskHandler.getAllTask()]
    form.taskAnalystAssignment.choices = [(c.getInitial(), c.getInitial()) for c in analystHandler.getAllAnalyst()]
    form.taskCollaboratorAssignment.choices = [(c.getInitial(), c.getInitial()) for c in analystHandler.getAllAnalyst()]
    form.associationToSystem.choices = [(system.getId(), system.getName()) for system in systemHandler.getAllSystems()]

    # populate the form with the data of the task to edit
    if request.method == 'GET':
        form.taskName.data = task1.getTitle()
        form.taskDescription.data = task1.getDescription()
        form.taskPriority.data = task1.getPriority()
        form.taskProgress.data = task1.getProgress()
        form.taskDueDate.data = datetime.strptime(task1.getDueDate(), '%m/%d/%Y')
        # i dont know how to edit the attachments
        # form.taskAttachment.data = task1.getAttachment()
        form.associationToTask.data = task1.getAssociationToTask()
        form.taskAnalystAssignment.data = task1.getAnalystAssigment()
        form.taskCollaboratorAssignment.data = task1.getCollaboratorAssignment()
        form.associationToSystem.data = task1.getAssociationToSystem()[0]

    if 'editTask' in request.form:
        task1.setTitle(form.taskName.data)
        task1.setDescription(form.taskDescription.data)
        task1.setPriority(form.taskPriority.data)
        task1.setProgress(form.taskProgress.data)
        task1.setDueDate(form.taskDueDate.data.strftime('%m/%d/%Y'))
        # task1.appendAttachment(form.taskAttachment.data)
        task1.setAssociationToTask(form.associationToTask.data)
        task1.setAnalystAssigment(form.taskAnalystAssignment.data)
        task1.setCollaboratorAssignment(form.taskCollaboratorAssignment.data)
        task1.setAssociationToSystem(form.associationToSystem.data)

        taskHandler.updateTask(task1, analyst)
        return redirect(url_for("TaskView", task=task1.getId()))

    return render_template('EditTask.html', form=form, task=task1)


@app.route('/Tasks')
def Tasks():
    # get list of systems for this event and pass them as parameter (currently returning all systems in db)
    taskHandler.loadTask()
    tasksList = []
    for task in taskHandler.getAllTask():
        if task.getArchiveStatus() == False:
            tasksList.append(task)
    return render_template('Tasks.html', tasksList=tasksList)


# function to archive a system from event and db
@app.route('/Tasks/<task>', methods=['GET', 'POST'])
def ArchiveTask(task):
    taskHandler.loadTask()
    tsk = taskHandler.getTask(ObjectId(task))
    tsk.setArchiveStatus(True)
    taskHandler.updateTask(tsk, analyst)
    return redirect(url_for('Tasks'))


@app.route('/RestoreTask/<task>', methods=['GET', 'POST'])
def RestoreTask(task):
    taskHandler.loadTask()
    tsk = taskHandler.getTask(ObjectId(task))
    tsk.setArchiveStatus(False)
    taskHandler.updateTask(tsk, analyst)

    return redirect(url_for('ArchiveContentView'))


@app.route('/CreateSubTask', methods=['GET', 'POST'])
def CreateSubTask():
    taskHandler.loadTask()
    form = CreateSubtaskForm(tasks=taskHandler.getAllTask(), analysts=analystHandler.getAllAnalyst(),
                             collaborators=analystHandler.getAllAnalyst())

    if 'createSubtask' in request.form:
        subtaskHandler.appendSubtask(analyst,
                                     form.subTaskName.data,
                                     form.subTaskDescription.data,
                                     Progress.getMember(form.subTaskProgress.data),
                                     form.subTaskDueDate.data.strftime('%m/%d/%Y'),
                                     form.associationTask.data,
                                     form.subTaskAnalystAssignment.data,
                                     form.subTaskCollaboratorAssignment.data,
                                     False,
                                     form.subTaskAttachment.data)
        return redirect(url_for("Subtasks"))

    return render_template('CreateSubTask.html', form=form)


@app.route('/EditSubTask/<subtask>', methods=['GET', 'POST'])
def EditSubTask(subtask):
    taskHandler.loadTask()
    subT = subtaskHandler.getSubtask(ObjectId(subtask))
    form = EditSubtaskForm()
    form.associationTask.choices = [(c.getId(), c.getTitle()) for c in taskHandler.getAllTask()]
    form.subTaskAnalystAssignment.choices = [(c.getInitial(), c.getInitial()) for c in analystHandler.getAllAnalyst()]
    form.subTaskCollaboratorAssignment.choices = [(c.getInitial(), c.getInitial()) for c in
                                                  analystHandler.getAllAnalyst()]

    # populate the form with the data of the system to edit
    if request.method == 'GET':
        form.subTaskName.data = subT.getTitle()
        form.subTaskDescription.data = subT.getDescription()
        form.subTaskProgress.data = subT.getProgress()
        form.subTaskDueDate.data = datetime.strptime(subT.getDueDate(), '%m/%d/%Y')
        # form.subTaskAttachment.data = subT.getAttachment()
        # form.associationTask.data = subT.getAssociationToTask()
        form.subTaskAnalystAssignment.data = subT.getAnalystAssigment()
        form.subTaskCollaboratorAssignment.data = subT.getCollaboratorAssignment()

    if 'editSubtask' in request.form:
        subT.setTitle(form.subTaskName.data)
        subT.setDescription(form.subTaskDescription.data)
        subT.setProgress(form.subTaskProgress.data)
        subT.setDueDate(form.subTaskDueDate.data.strftime('%m/%d/%Y'))
        # subT.setAttachment(form.subTaskAttachment.data)
        # subT.setAssociationToTask(form.associationTask.data)
        subT.setAnalystAssigment(form.subTaskAnalystAssignment.data)
        subT.setCollaboratorAssignment(form.subTaskCollaboratorAssignment.data)

        subtaskHandler.updateSubtask(subT, analyst)
        return redirect(url_for("SubTaskView", subtask=subT.getId()))

    return render_template('EditSubTask.html', form=form, subtask=subT)


@app.route('/SubTaskView/<subtask>', methods=['GET', 'POST'])
def SubTaskView(subtask):
    # subtaskHandler.loadSubtask()
    taskHandler.loadTask()
    subT = subtaskHandler.getSubtask(ObjectId(subtask))

    if subT.getAssociationToTask():
        taskParent = ObjectId(subT.getAssociationToTask()[0])
        taskName = taskHandler.getTask(ObjectId(subT.getAssociationToTask()[0])).getTitle()
    else:
        taskParent = ""
        taskName = ""

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveSubtask' in request.form:
        subT.setArchiveStatus(True)
        subtaskHandler.updateSubtask(subT, analyst)

        return redirect(url_for('Subtasks'))
    if 'PromoteToTask' in request.form:
        taskHandler.appendTask(analyst,
                               subT.getTitle(),
                               subT.getDescription(),
                               Priority.MEDIUM.value,
                               subT.getProgress(),
                               subT.getDueDate(),
                               subT.getAssociationToTask(),
                               subT.getAnalystAssigment(),
                               subT.getCollaboratorAssignment(),
                               False,
                               None,
                               subT.getAttachment())
        subT.setArchiveStatus(True)
        return redirect(url_for('Tasks'))

    return render_template('SubTaskView.html', subtask=subT, taskParent=taskParent, taskName=taskName)


@app.route('/PromoteToTask/<subtask>', methods=['GET', 'POST'])
def PromoteToTask(subtask):
    subT = subtaskHandler.getSubtask(ObjectId(subtask))
    taskHandler.appendTask(analyst,
                           subT.getTitle(),
                           subT.getDescription(),
                           Priority.MEDIUM.value,
                           subT.getProgress(),
                           subT.getDueDate(),
                           subT.getAssociationToTask(),
                           subT.getAnalystAssigment(),
                           subT.getCollaboratorAssignment(),
                           False,
                           None,
                           subT.getAttachment())

    subT.setArchiveStatus(True)
    return redirect(url_for('Subtasks'))


@app.route('/Subtasks')
def Subtasks():
    # subtaskHandler.loadSubtask()
    subTasksList = []
    for subtask in subtaskHandler.getAllsubTask():
        if subtask.getArchiveStatus() == False:
            subTasksList.append(subtask)

    return render_template('Subtasks.html', subTasksList=subTasksList)


# function to archive a system from event and db
@app.route('/Subtasks/<subtask>', methods=['GET', 'POST'])
def ArchiveSubtask(subtask):
    subtaskHandler.loadSubtask()
    subT = subtaskHandler.getSubtask(ObjectId(subtask))
    subT.setArchiveStatus(True)
    subtaskHandler.updateSubtask(subT, analyst)

    return redirect(url_for('Subtasks'))


@app.route('/RestoreSubtask/<subtask>', methods=['GET', 'POST'])
def RestoreSubtask(subtask):
    subT = subtaskHandler.getSubtask(ObjectId(subtask))
    subT.setArchiveStatus(False)
    subtaskHandler.updateSubtask(subT, analyst)
    return redirect(url_for('ArchiveContentView'))


@app.route('/CreateFinding', methods=['GET', 'POST'])
def CreateFinding():
    taskHandler.loadTask()
    form = CreateFindingForm(findings=findingHandler.getAllFindings(), analysts=analystHandler.getAllAnalyst(),
                             collaborators=analystHandler.getAllAnalyst(), tasks=taskHandler.getAllTask())
    if 'createFinding' in request.form:
        # if I just pass form.findingPosture.data we would get the same result, so what is the diff?
        # print(Posture.getMember(form.findingPosture.data))
        # cast this to enum type
        findingHandler.appendFinding(analyst,
                                     form.findingHostName.data,
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
                                     form.findingCollaboratorAssignment.data,
                                     form.associationTask.data)
        return redirect(url_for("FindingsView"))

    return render_template('CreateFinding.html', form=form)


@app.route('/FindingsView')
def FindingsView():
    findingHandler.loadFindings()
    findingsList = []
    for finding in findingHandler.getAllFindings():
        if finding.getArchiveStatus() == False:
            findingsList.append(finding)
    return render_template('FindingsView.html', findingsList=findingsList)


@app.route('/FindingView/<finding>', methods=['GET', 'POST'])
def FindingView(finding):
    taskHandler.loadTask()
    findingHandler.loadFindings()
    find = findingHandler.getFinding(ObjectId(finding))
    # display names of associated findings
    findingsName = []
    for finding in find.getAssociationTo():
        for t in findingHandler.getAllFindings():
            if ObjectId(finding) == t.getid():
                findingsName.append(t.getHostName())

    if find.getAssociatedTask():
        taskParent = ObjectId(find.getAssociatedTask()[0])
        taskName = taskHandler.getTask(taskParent).getTitle()
    else:
        taskParent = ""
        taskName = ""

    findingsAnalysts = []
    for analys in find.getAnalystAssigned():
        for t in analystHandler.getAllAnalyst():
            if ObjectId(analys) == t.getId():
                findingsAnalysts.append(t.getInitial())
    findingsAnalystsC = []
    for analys in find.getCollaboratorsAssigned():
        for t in analystHandler.getAllAnalyst():
            if ObjectId(analys) == t.getId():
                findingsAnalystsC.append(t.getInitial())

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveFinding' in request.form:
        find.setArchiveStatus(True)
        findingHandler.updateFinding(find, analyst)
        return redirect(url_for('FindingsView'))

    return render_template('FindingView.html', finding=find, findingsName=findingsName,taskParent=taskParent,taskName=taskName,findingsAnalysts=findingsAnalysts,findingsAnalystsC=findingsAnalystsC)



@app.route('/EditFinding/<finding>', methods=['GET', 'POST'])
def EditFinding(finding):
    findingHandler.loadFindings()
    find = findingHandler.getFinding(ObjectId(finding))

    form = EditFindingForm()
    form.associationToFinding.choices = [(c.getid(), c.getHostName()) for c in findingHandler.getAllFindings()]
    form.findingAnalystAssignment.choices = [(c.getId(), c.getInitial()) for c in analystHandler.getAllAnalyst()]
    form.findingCollaboratorAssignment.choices = [(c.getId(), c.getInitial()) for c in analystHandler.getAllAnalyst()]
    form.associationTask.choices = [(task.getId(), task.getTitle()) for task in taskHandler.getAllTask()]

    # populate the form with the data of the system to edit
    if request.method == 'GET':
        form.findingHostName.data = find.getHostName()
        form.findingIPPort.data = find.getIpPort()
        form.findingDescription.data = find.getDescription()
        form.findingLongDescription.data = find.getLongDescription()
        form.findingStatus.data = find.getStatus()
        form.findingType.data = find.getType()
        form.findingClassification.data = find.getClassification()
        form.associationToFinding.data = find.getAssociationTo()
        # form.findingEvidence.data = find.getEvidence()
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
        form.associationTask.data = find.getAssociatedTask()[0]

    if 'editFinding' in request.form:
        find.setHostName(form.findingHostName.data)
        find.setIpPort(form.findingIPPort.data)
        find.setDescription(form.findingDescription.data)
        find.setLongDescription(form.findingLongDescription.data)
        find.setStatus(form.findingStatus.data)
        find.setType(form.findingType.data)
        find.setClassification(form.findingClassification.data)
        find.setAssociationTo(form.associationToFinding.data)
        # find.setEvidence(form.findingEvidence.data)
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
        find.setAssociatedTask(form.associationTask.data)

        findingHandler.updateFinding(find,analyst)
        return redirect(url_for("FindingView", finding=find.getid()))
    return render_template('EditFinding.html', form=form, finding=find)


# function to archive a system from event and db
@app.route('/ArchiveFinding/<finding>', methods=['GET', 'POST'])
def ArchiveFinding(finding):
    find = findingHandler.getFinding(ObjectId(finding))
    find.setArchiveStatus(True)
    findingHandler.updateFinding(find, analyst)
    return redirect(url_for('FindingsView'))


@app.route('/RestoreFinding/<finding>', methods=['GET', 'POST'])
def RestoreFinding(finding):
    find = findingHandler.getFinding(ObjectId(finding))
    find.setArchiveStatus(False)
    findingHandler.updateFinding(find, analyst)
    return redirect(url_for('ArchiveContentView'))


@app.route('/GenerateReport')
def GenerateReport():
    return render_template('GenerateReport.html')


@app.route('/ArchiveContentView')
def ArchiveContentView():
    systemHandler.loadSystems()
    taskHandler.loadTask()
    # subtaskHandler.loadSubtask()
    findingHandler.loadFindings()
    archivedSystemList = []
    for archivedsystem in systemHandler.getAllSystems():
        if archivedsystem.getArchiveStatus() == True:
            archivedSystemList.append(archivedsystem)
    archivedTasksList = []
    for archivedTask in taskHandler.getAllTask():
        if archivedTask.getArchiveStatus() == True:
            archivedTasksList.append(archivedTask)
    archivedSubtasksList = []
    for archivedSubtask in subtaskHandler.getAllsubTask():
        if archivedSubtask.getArchiveStatus() == True:
            archivedSubtasksList.append(archivedSubtask)

    archivedFindingsList = []
    for archivedFinding in findingHandler.getAllFindings():
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
    findingHandler.loadFindings()

    print("RiskMatrixReport")
    findingsList = []
    for finding in findingHandler.getAllFindings():
        if finding.getArchiveStatus() == False:
            findingsList.append(finding)

    # Code to generate RiskMatrixReport
    createRiskMatrixReport(findingsList, event)

    return render_template('FindingsView.html', findingsList=findingsList)


@app.route('/ERBReport')
def ERBReport():
    findingHandler.loadFindings()

    findingsList = []
    for finding in findingHandler.getAllFindings():
        if finding.getArchiveStatus() == False:
            findingsList.append(finding)

    systemsList = []
    for system in systemHandler.getAllSystems():
        if finding.getArchiveStatus() == False:
            systemsList.append(system)

    # generate ERB report
    generateERB(event, findingsList, systemsList)

    return render_template('FindingsView.html', findingsList=findingsList)


@app.route('/FinalTechnicalReport')
def FinalTechnicalReport():
    print("FinalTechnicalReport")
    findingHandler.loadFindings()
    findingsList = []
    for finding in findingHandler.getAllFindings():
        if finding.getArchiveStatus() == False:
            findingsList.append(finding)

    generateFinalTecReport(event, findingsList)

    return render_template('FindingsView.html', findingsList=findingsList)


@app.route('/AnalystProgressSummaryContentView/<initials>', methods=['GET', 'POST'])
def AnalystProgressSummaryContentView(initials):
    for analyst in analystHandler.getAllAnalyst():
        if analyst.getInitial() == initials:
            a = analyst

    findingsList = []
    for finding in findingHandler.getAllFindings():
        for aanalyst in finding.getAnalystAssigned():
            if a.getInitial() == aanalyst:
                findingsList.append(finding)

    tasksList = []
    for task in taskHandler.getAllTask():
        for aanalyst in task.getAnalystAssigment():
            if a.getInitial() == aanalyst:
                tasksList.append(task)

    subTasksList = []
    for subtask in subtaskHandler.getAllsubTask():
        for aanalyst in subtask.getAnalystAssigment():
            if a.getInitial() == aanalyst:
                subTasksList.append(subtask)

    return render_template('AnalystProgressSummaryContentView.html', findingsList=findingsList, tasksList=tasksList,
                           subTasksList=subTasksList)


if __name__ == '__main__':
    app.run(debug=True)  # runs the application
