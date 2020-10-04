from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from database.analyst import Analyst, Role
from database.databaseHandler import DatabaseHandler
from database.event import Event, EventType, EventClassification
from forms import *

# creates the flask app
app = Flask(__name__)
Bootstrap(app)
# needed for flask-wtf
app.config['SECRET_KEY'] = 'encrypted'

# get instance of db
db = DatabaseHandler()
events = db.getAllEvents()

print(len(events))
event = events[0]


@app.route('/', methods=['GET', 'POST'])
def SetupContentView():
    # main page, login page
    # return a html page at the directory specified by the app.rout above
    return render_template('SetupContentView.html')


@app.route('/EventView', methods=['GET', 'POST'])
def EventView():
    # pass event as parameter to use the event variable in the EventView.html
    return render_template('EventView.html', event=event)


@app.route('/EditEvent', methods=['GET', 'POST'])
def EditEvent():
    return render_template('EditEvent.html')


@app.route('/CreateEvent', methods=['GET', 'POST'])
def CreateEvent():
    # create a form from the forms.py file (need to import the file)
    form = CreateEventForm()

    # check if the submit button has been pressed, if so create an event obj
    if request.method == 'POST':
        # the date returns none
        w = form.DeclassificationDate.data
        print(w)
        # uncomment to create an event object in your local db
        # newEvent = Event(form.EventName.data,
        #              form.EventDescription.data,
        #              form.EventType.data,
        #              "1.0",
        #              form.AssessmentDate.data,
        #              form.SCTG.data,
        #              form.OrganizationName.data,
        #              form.EventClassification.data,
        #              form.DeclassificationDate.data,
        #              form.CustomerName.data,
        #              False,
        #              form.EventAnalysts.data)
        # db.updateEvent(newEvent)
        # if the button with name attribute's value 'create' is pressed, then redirect to the right page
        if 'create' in request.form:
            return redirect(url_for("EventView"))

    return render_template('CreateEvent.html', form=form)


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
