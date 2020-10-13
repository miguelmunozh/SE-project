from datetime import datetime, date

from bson import ObjectId
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap
from database.analyst import Analyst, Role
from database.databaseHandler import DatabaseHandler
from database.event import Event, EventType, EventClassification
from database.system import System
from forms import *
from Helper import *

# creates the flask app
app = Flask(__name__)
Bootstrap(app)
# needed for flask-wtforms
app.config['SECRET_KEY'] = 'encrypted'

# get instance of db
db = DatabaseHandler()

# analyst to pass as parameter to the updateEvent function,(will be deleted when we can know which analyst entered
# the system)
analyst = Analyst("jonathan", "roman", "jr", ["jr", "sr"], Role.LEAD.value)


# event = None


@app.route('/', methods=['GET', 'POST'])
def SetupContentView():
    # global event
    # events = db.getAllEvents()

    form = SetupContentViewForm()
    # checks if the submit btn in SetupContentView page has been pressed
    if 'LogCreateEvent' in request.form:
        # check if there is an event that is not archived, if so we use that event through the entire app
        # redirect to the right page depending on the user selection
        if form.SUCVSelection.data == 'create':
            # for e in events:
            #     if not e.getArchiveStatus():
            #         e.setArchiveStatus(True)
            #         db.updateEvent(analyst, e)
            # archive the event then create one
            return redirect(url_for("CreateEvent"))

        elif form.SUCVSelection.data == 'sync':
            # for e in events:
            #     # if there is an none archived event, set the actual event to that event
            #     if not e.getArchiveStatus():
            #         event = e
            #
            # if event.getArchiveStatus() == True: # or if event is None?
            #     error = "There is no existing event in your local system"
            #     return render_template('SetupContentView.html', form=form, error=error)

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
    events.reverse()
    event = events[0]
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
    events.reverse()
    event = events[0]
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
    events = db.getAllEvents()
    events.reverse()
    event = events[0]
    # get list of systems for this event and pass them as parameter (currently returning all systems in db)
    systemList = []
    for system in db.getAllSystems():
        if system.getArchiveStatus() == False:
            systemList.append(system)

    # check if archive event button has been pressed, if so, set it to be archived and redirect to main page
    if 'ArchiveEvent' in request.form:
        event.setArchiveStatus(True)
        db.updateEvent(analyst, event)
        return redirect(url_for('SetupContentView'))

    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=event, db=db, systemList=systemList)


@app.route('/EditEvent', methods=['GET', 'POST'])
def EditEvent():
    events = db.getAllEvents()
    events.reverse()
    event = events[0]
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
    # create a form from the forms.py file (need to import the file)
    form = CreateEventForm()

    # check if the create event button has been pressed, if so create an event obj
    if 'createEvent' in request.form:
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
        return redirect(url_for("EventView"))

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

        # incomplete, need to store the lists as lists in the object
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

    # HOW TO RELATE THE SYSTEM TO KNOW FROM WHICH EVENT IT'S COMMING FROM
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
        return redirect(url_for('EventView'))

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
        form.EditSystemLocation.data = locations
        form.EditSystemRouter.data = routers
        form.EditSystemSwitch.data = switches
        form.EditSystemRoom.data = rooms
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


@app.route('/CreateTask')
def CreateTask():
    return render_template('CreateTask.html')


@app.route('/TaskView')
def TaskView():
    return render_template('TaskView.html')


@app.route('/EditTask')
def EditTask():
    return render_template('EditTask.html')


@app.route('/CreateSubTask')
def CreateSubTask():
    return render_template('CreateSubTask.html')


@app.route('/EditSubTask')
def EditSubTask():
    return render_template('EditSubTask.html')


@app.route('/SubTaskView')
def SubTaskView():
    return render_template('SubTaskView.html')


@app.route('/CreateFinding')
def CreateFinding():
    return render_template('CreateFinding.html')


@app.route('/FindingsView')
def FindingsView():
    return render_template('FindingsView.html')


@app.route('/FindingView')
def FindingView():
    return render_template('FindingView.html')


@app.route('/EditFinding')
def EditFinding():
    return render_template('EditFinding.html')


@app.route('/GenerateReport')
def GenerateReport():
    return render_template('GenerateReport.html')


@app.route('/ArchiveContentView')
def ArchiveContentView():
    return render_template('ArchiveContentView.html')


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


@app.route('/Tasks')
def Tasks():
    return render_template('Tasks.html')


@app.route('/Subtasks')
def Subtasks():
    return render_template('Subtasks.html')


@app.route('/EventTree')
def EventTree():
    return render_template('EventTree.html')


@app.route('/AnalystProgressSummaryContentView')
def AnalystProgressSummaryContentView():
    return render_template('AnalystProgressSummaryContentView.html')


@app.route('/Systems')
def Systems():
    # get list of systems for this event and pass them as parameter (currently returning all systems in db)
    systemList = []
    for system in db.getAllSystems():
        if system.getArchiveStatus() == False:
            systemList.append(system)

    return render_template('Systems.html', systemList=systemList)


# function to delete analyst initials from event and db
@app.route('/Systems/<system>', methods=['GET', 'POST'])
def ArchiveSystem(system):
    for s in db.getAllSystems():
        if s.getId() == ObjectId(system):
            s.setArchiveStatus(True)
            db.updateSystem(analyst, s)
            return redirect(url_for('Systems'))
    return redirect(url_for('Systems'))


if __name__ == '__main__':
    app.run(debug=True)  # runs the application
