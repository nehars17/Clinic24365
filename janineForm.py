from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField

class MedicalConditionAllergy(Form):
    type = RadioField('Type: ', [validators.DataRequired()], choices=[('Allergy', 'Allergy'), ('Medical Condition', 'Medical Condition')])
    mca = StringField('Allergy/Medical Condition:: ', [validators.DataRequired()])
    description = TextAreaField('Description: ', [validators.Optional()])

class CreatePrescriptionForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.length(min=9, max=9), validators.DataRequired()])
    clinic = StringField('Clinic Name', [validators.DataRequired()])
    medication = TextAreaField('Medication', [validators.DataRequired()], )
    symptoms = TextAreaField('Symptoms', [validators.DataRequired()])
    instructions = TextAreaField('Instructions', [validators.DataRequired()])
    sideEffects = TextAreaField('Side Effects', [validators.DataRequired()])

class CreateReferral(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.Length(min=9, max=9), validators.DataRequired()])
    reason = TextAreaField('Reason for Referral', [validators.DataRequired()])
    organisation = TextAreaField('Hospital/Specialist Center Referred To', [validators.DataRequired()])
    date = DateField('Referral issued on', format='%Y-%m-%d')

class CreateMedCert(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.Length(min=9, max=9), validators.DataRequired()])
    startDate = DateField('Start of MC', [validators.DataRequired()])
    endDate = DateField('End of MC', [validators.DataRequired()])

