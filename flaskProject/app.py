from datetime import datetime, date
from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
<<<<<<< HEAD
from flaskProject.database.analyst import Analyst, Role
from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.database.event import Event, EventType, EventClassification
=======
from database.analyst import Analyst, Role
from database.databaseHandler import DatabaseHandler
from database.event import Event, EventType, EventClassification
from forms import *
>>>>>>> 8125c4e0bab99e25fd5d7b45909f1f3077dedb06

# creates the flask app
app = Flask(__name__)
Bootstrap(app)
# needed for flask-wtf
app.config['SECRET_KEY'] = 'encrypted'

# get instance of db
db = DatabaseHandler()


@app.route('/', methods=['GET', 'POST'])
def SetupContentView():
    # checks if the submit btn has been pressed
    if request.method == 'POST':
        # prints the value of the html field with the name attribute set to 'initials'
        print(request.form['initials'])
    # return a html page at the directory specified by the app.rout above
    return render_template('SetupContentView.html')


@app.route('/EventView', methods=['GET', 'POST'])
def EventView():
    events = db.getAllEvents()
    # make sure that events[0] is the last event added,so that in case you create another event that last event shows up
    # in the event view
    events.reverse()
    event = events[0]
    
    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=event)


@app.route('/EditEvent', methods=['GET', 'POST'])
def EditEvent():
    return render_template('EditEvent.html')


@app.route('/CreateEvent', methods=['GET', 'POST'])
def CreateEvent():
<<<<<<< HEAD
    # if the create button is pressed create a new object with the info entered by the user
    # if request.method == 'POST':
    # create an event object. which is stored in the database
    # creating the object here causes a bad request error in the browser, why? where do i create the object?
    #    event = Event(request.form['eventName'],
    #                  request.form['eventDescription'],
    #                  EventType.VERIFICATION_OF_FIXES.value,
    #                  "1.0",
    #                  request.form['eventDateStart'],
    #                  request.form['eventSCTG'],
    #                  request.form['eventOrgName'],
    #                  request.form['eventClassification'].value,
    #                  request.form['eventDateEnd'],
    #                  request.form['eventCustomerName'],
    #                  False,
    #                  request.form['eventNonLead'])

    return render_template('CreateEvent.html')
=======
    # create a form from the forms.py file (need to import the file)
    form = CreateEventForm()

    # check if the create event button has been pressed, if so create an event obj
    if 'create' in request.form:
        newEvent = Event(form.EventName.data,
                         form.EventDescription.data,
                         form.EventType.data,
                         1.0,
                         form.AssessmentDate.data.strftime('%m/%d/%Y'),
                         form.SCTG.data,
                         form.OrganizationName.data,
                         form.EventClassification.data,
                         form.DeclassificationDate.data.strftime('%m/%d/%Y'),
                         form.CustomerName.data,
                         False,
                         form.EventAnalysts.data)
        db.updateEvent(newEvent)
        # redirect to the right page after creating the form
        return redirect(url_for("EventView"))

    return render_template('CreateEvent.html', form=form)
>>>>>>> 8125c4e0bab99e25fd5d7b45909f1f3077dedb06


@app.route('/CreateSystem')
def CreateSystem():
    return render_template('CreateSystem.html')


@app.route('/EditSystem')
def EditSystem():
    return render_template('EditSystem.html')


@app.route('/SystemView')
def SystemView():
    return render_template('SystemView.html')


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
    return render_template('Systems.html')


if __name__ == '__main__':
    app.run(debug=True)  # runs the application
