from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

# creates the flask app
app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def SetupContentView():
    # main page, login page
    # return a html page at the directory specified by the app.rout above
    return render_template('SetupContentView.html')


@app.route('/EventView')
def EventView():
    return render_template('EventView.html')


@app.route('/EditEvent')
def EditEvent():
    return render_template('EditEvent.html')


@app.route('/CreateEvent')
def CreateEvent():
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

if __name__ == '__main__':
    app.run()  # runs the application
