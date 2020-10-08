from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flaskProject.database.analyst import Analyst, Role
from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.database.event import Event, EventType, EventClassification

# creates the flask app
app = Flask(__name__)
Bootstrap(app)

# get instance of db
db = DatabaseHandler()
events = db.getAllEvents()
# event that is passed as parameters to display info in eventView.html
# the ideal is to select the last element in the list, since it would
# be the last event created, the rest would be archived
event = events[0]

analysts = db.getAllAnalyst()
analyst = analysts[0]


@app.route('/', methods=['GET', 'POST'])
def SetupContentView():
    # main page, login page
    # return a html page at the directory specified by the app.rout above

    # get analyst data and create object, store it in db
    return render_template('SetupContentView.html')


@app.route('/EventView', methods=['POST'])
def EventView():
    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=event)


@app.route('/EditEvent', methods=['GET', 'POST'])
def EditEvent():
    # get the values of the fields from the editEvent.html form
    if request.method == 'POST':
        # for all of the fields of the actual event, get the value and then set it (--IS NOT WORKING--)
        eventName = request.form['eventName']
        eventDescription = request.form['eventDescription']

        event.setName(eventName)
        event.setDescription(eventDescription)

    return render_template('EditEvent.html')


@app.route('/CreateEvent', methods=['GET', 'POST'])
def CreateEvent():
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
    app.run()  # runs the application
