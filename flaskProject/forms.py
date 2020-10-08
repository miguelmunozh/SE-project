from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


# These forms are created using flask-wdt (need pip installation)
# each form creates the fields we need for the form, we still need the html file and each form is represented as a class
class CreateEventForm(FlaskForm):
    # field to input a string with the label of 'Event Name'
    EventName = StringField('Event Name')
    EventDescription = StringField('Event Description')

    EventType = SelectField('Event Type',
                            choices=[('COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT',
                                      'Cooperative Vulnerability Penetration Assessment(CVPA)'),
                                     ('COOPERATIVE_VULNERABILITY_INVESTIGATION',
                                      'Cooperative Vulnerability Investigation (CVI)'),
                                     ('VERIFICATION_OF_FIXES', 'Verification of Fixes (VOF)')])
    OrganizationName = StringField('Organization Name')
    CustomerName = StringField('Customer name')
    AssessmentDate = DateField('Assessment date')
    DeclassificationDate = DateField('Declassification date')
    SCTG = StringField('Security Classification Title Guide')
    EventClassification = SelectField('Event Classification',
                                      choices=[('TOP_SECRET', 'Top secret'),
                                               ('SECRET', 'Secret'),
                                               ('CONFIDENTIAL', 'Confidential'),
                                               ('CLASSIFIED', 'Classified'),
                                               ('UNCLASSIFIED', 'Unclassified')])
    EventLeadAnalysts = StringField('Event Lead Analysts', )
    EventAnalysts = StringField('Event Analysts')

    # these two should go only on the edit event form i think, and someothers that are in the edit event html file
    # Archive Status
    # version
