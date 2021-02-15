from wtforms import Form, StringField, TextAreaField, validators
from wtforms.fields.html5 import DateField

class CreateReferral(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.Length(min=9, max=9), validators.DataRequired()])
    reason = TextAreaField('Reason for Referral', [validators.DataRequired()])
    organisation = TextAreaField('Hospital/Specialist Center Referred To', [validators.DataRequired()])
    date = DateField('Referral issued on', format='%Y-%m-%d')