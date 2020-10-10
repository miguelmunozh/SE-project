from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, IPAddress, Optional
from wtforms.fields.html5 import DateField


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
                            choices=[('COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT',
                                      'Cooperative Vulnerability Penetration Assessment(CVPA)'),
                                     ('COOPERATIVE_VULNERABILITY_INVESTIGATION',
                                      'Cooperative Vulnerability Investigation (CVI)'),
                                     ('VERIFICATION_OF_FIXES', 'Verification of Fixes (VOF)')],
                            validators=[DataRequired()])
    OrganizationName = StringField('Organization Name', validators=[DataRequired()])
    CustomerName = StringField('Customer name', validators=[DataRequired()])
    AssessmentDate = DateField('Assessment date', validators=[DataRequired()])
    DeclassificationDate = DateField('Declassification date', validators=[DataRequired()])
    SCTG = StringField('Security Classification Title Guide', validators=[DataRequired()])
    EventClassification = SelectField('Event Classification',
                                      choices=[('TOP_SECRET', 'Top secret'),
                                               ('SECRET', 'Secret'),
                                               ('CONFIDENTIAL', 'Confidential'),
                                               ('CLASSIFIED', 'Classified'),
                                               ('UNCLASSIFIED', 'Unclassified')], validators=[DataRequired()])
    # For event team in event class
    EventLeadAnalysts = StringField('Event Lead Analysts')
    EventAnalysts = StringField('Event Analysts')

    EventClassifiedBy = StringField('Classified by', validators=[DataRequired()])
    EventDerivedFrom = StringField('Derived from', validators=[DataRequired()])


class EditEventForm(FlaskForm):
    EditEventName = StringField('Event Name')
    EditEventDescription = StringField('Event Description')
    EditEventVersion = StringField('Event Version', validators=[DataRequired()])
    EditEventType = SelectField('Event Type',
                                choices=[('COOPERATIVE_VULNERABILITY_PENETRATION_ASSESSMENT',
                                          'Cooperative Vulnerability Penetration Assessment(CVPA)'),
                                         ('COOPERATIVE_VULNERABILITY_INVESTIGATION',
                                          'Cooperative Vulnerability Investigation (CVI)'),
                                         ('VERIFICATION_OF_FIXES', 'Verification of Fixes (VOF)')],
                                validators=[DataRequired()])
    EditEventOrganizationName = StringField('Organization Name')
    EditEventCustomerName = StringField('Customer name')
    EditEventAssessmentDate = DateField('Assessment date')
    EditEventDeclassificationDate = DateField('Declassification date')
    EditEventSCTG = StringField('Security Classification Title Guide')
    EditEventClassification = SelectField('Event Classification',
                                          choices=[('TOP_SECRET', 'Top secret'),
                                                   ('SECRET', 'Secret'),
                                                   ('CONFIDENTIAL', 'Confidential'),
                                                   ('CLASSIFIED', 'Classified'),
                                                   ('UNCLASSIFIED', 'Unclassified')])
    EditEventClassifiedBy = StringField('Classified by')
    EditEventDerivedFrom = StringField('Derived from')


class CreateAnalystForm(FlaskForm):
    CreateAnalystFName = StringField('Analyst First Name', validators=[DataRequired()])
    CreateAnalystLName = StringField('Analyst Last Name')
    CreateAnalystInitials = StringField('Initials', validators=[DataRequired()])
    CreateAnalystRole = SelectField('Analyst role',
                                    choices=[('analyst', 'Non-lead Analyst'),
                                             ('lead', 'Lead Analyst'),
                                             ('collaborator', 'Collaborator')], validators=[DataRequired()])
