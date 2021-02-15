from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField, RadioField, IntegerField
from wtforms.fields.html5 import EmailField, TelField, TimeField, DateField
from datetime import date

# def validate_nric(form, field):
#     value = field.data
#     if value[0].upper() != 'S' and value[0].upper() != 'T' and value[0].upper() != 'G':
#         raise validators.ValidationError('NRIC must be S or T or G')
#     if value[1:8].isnumeric() != True:
#         raise validators.ValidationError('NRIC middle must be digits')
#     if value[-1].isalpha() != True:
#         raise validators.ValidationError('NRIC end must be an alphabet')
#     x=(int(value[1])*2+int(value[2])*7+int(value[3])*6+int(value[4])*5+int(value[5])*4+int(value[6])*3+int(value[7])*2+4)%11
#     if value[-1] == "J" or value[-1]=="j":
#         y=0
#     elif value[-1]== "Z" or value[-1]=="z":
#         y=1
#     elif value[-1]== "I" or value[-1]=="i":
#         y=2
#     elif value[-1] =="H" or value[-1]=="h":
#         y=3
#     elif value[-1] =="G" or value[-1]=="g":
#         y=4
#     elif value[-1] =="F" or value[-1]=="f":
#         y=5
#     elif value[-1] =="E" or value[-1]=="e":
#         y=6
#     elif value[-1] =="D" or value[-1]=="d":
#         y=7
#     elif value[-1] =="C" or value[-1]=="c":
#         y=8
#     elif value[-1] =="B" or value[-1]=="b":
#         y=9
#     elif value[-1] =="A" or value[-1]=="a":
#         y=10
#     if x != y:
#         raise validators.ValidationError('Invalid NRIC')


def validate_tel(form, field):
    value = field.data
    if value.isnumeric() == False or (value[0] != '9' and value[0] != '8' and value[0] != '6'):
        raise validators.ValidationError('Incorrect contact number format')

def validate_password_strength(form, field):
    value = field.data
    uppercase = 0
    lowercase = 0
    numbers = 0
    special_char = 0
    special_char_list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', "\\", ']', '^', '_', '`', '{', '|', '}', '~']
    for i in value:
        if i.isupper() == True:
            uppercase += 1
        elif i.islower() == True:
            lowercase += 1
        elif i.isnumeric() == True:
            numbers += 1
        elif i in special_char_list:
            special_char += 1
    # print(uppercase, lowercase, numbers, special_char)
    # print(value)
    if uppercase == 0 or lowercase == 0 or numbers == 0 or special_char == 0:
        raise validators.ValidationError('Password must contain a mix of uppercase and lowercase letters, numbers and special characters')
    # if lowercase == 0:
    #     raise validators.ValidationError('Password must contain lowercase letters')
    # if numbers == 0:
    #     raise validators.ValidationError('Password must contain numbers')
    # if special_char == 0:
    #     raise validators.ValidationError('Password must contain special characters')

def validate_postal_code(form, field):
    value = field.data
    print(value)
    if len(value) != 6:
        raise validators.ValidationError('Invalid Postal Code! Must be 6 digits!')
    elif value.isnumeric() == False:
        raise validators.ValidationError('Invalid Postal Code! Must be 6 digits!')


class CreatePublicForm(Form):
    name = StringField('Full Name as in NRIC:', [validators.Length(min=1, max=150), validators.DataRequired()])
    area = SelectField('Area/Nearest MRT: ', [validators.DataRequired()], choices=['', 'Ang Mo Kio', 'Bedok', 'Bishan', 'Braddell', 'Buangkok', 'Bugis', 'Canberra', 'Changi', 'Chinatown', 'Clementi', 'Harbourfront', 'Hougang', 'Jurong', 'Khatib', 'Kovan', 'Marina', 'Orchard', 'Pasir Ris', 'Punggol', 'Sembawang', 'Sengkang', 'Tampines', 'Woodlands', 'Yio Chu Kang', 'Yishun'], default='')
    # street = StringField('Street Name: ', [validators.DataRequired()])
    # block = IntegerField('Block Number: ', [validators.DataRequired()])
    postal_code = StringField('Postal Code: ', [validate_postal_code, validators.DataRequired()])
    unit = StringField('Unit Number: ', [validators.DataRequired()])
    nric = StringField('NRIC:', [validators.Length(min=9, max=9), validators.DataRequired()])
    birthdate = DateField('Birth Date:', [validators.DataRequired()])
    email = EmailField('Email Address:', [validators.Length(min=6, max=150), validators.DataRequired()])
    phone = StringField('Contact Number:', [validators.Length(min=8, max=8), validators.DataRequired(), validate_tel])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match'), validate_password_strength])
    cfm_password = PasswordField('Confirm Password:', [validators.Length(min=8, max=15), validators.DataRequired()])

class CreateClinicForm(Form):
    name = StringField('Clinic Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    area = SelectField('Area/Nearest MRT: ', [validators.DataRequired()], choices=['', 'Ang Mo Kio', 'Bedok', 'Bishan', 'Braddell', 'Buangkok', 'Bugis', 'Canberra', 'Changi', 'Chinatown', 'Clementi', 'Harbourfront', 'Hougang', 'Jurong', 'Khatib', 'Kovan', 'Marina', 'Orchard', 'Pasir Ris', 'Punggol', 'Sembawang', 'Sengkang', 'Tampines', 'Woodlands', 'Yio Chu Kang', 'Yishun'], default='')
    # street = StringField('Street Name: ', [validators.DataRequired()])
    # block = IntegerField('Block Number: ', [validators.DataRequired()])
    postal_code = StringField('Postal Code: ', [validate_postal_code, validators.DataRequired()])
    unit = StringField('Unit Number: ', [validators.DataRequired()])
    email = EmailField('Email Address:', [validators.Length(min=6, max=150), validators.DataRequired()])
    phone = StringField('Contact Number:', [validators.Length(min=8, max=8), validators.DataRequired(), validate_tel])
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match'), validate_password_strength])
    cfm_password = PasswordField('Confirm Password:', [validators.Length(min=8, max=15), validators.DataRequired()])

class LoginPublicForm(Form):
    nric = StringField('NRIC:', [validators.Length(min=9, max=9), validators.DataRequired()])
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.DataRequired()])

class LoginClinicForm(Form):
    clinic_id = StringField('Clinic ID:', [validators.Length(min=6, max=6), validators.DataRequired()])
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.DataRequired()])

class OperatingHour(Form):
    day = SelectField('Day: ', [validators.DataRequired()], choices=[('', 'Select'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], default='')
    open = TimeField('Opening Time:', [validators.Optional()])
    close = TimeField('Closing Time:', [validators.Optional()])
    # break_start = TimeField('Break Start Time:', [validators.Optional()])
    # break_end = TimeField('Break End Time:', [validators.Optional()])

class OffDay(Form):
    start = DateField('Start of off day(s):', [validators.DataRequired()])
    end = DateField('End of off day(s):', [validators.DataRequired()])
    reason = TextAreaField('Reason/Message: ', [validators.Optional()])
    def validate_end(form, field):
        if field.data < form.start.data:
            raise validators.ValidationError("End date must not be earlier than start date.")
    def validate_start(form, field):
        today_date = date.today()
        if field.data < today_date:
            raise validators.ValidationError("Start date must not be earlier than today's date.")

class IdPassword(Form):
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.Optional()])
    cfm_password = PasswordField('Confirm Password:', [validators.Length(min=8, max=15), validators.Optional()])

class UpdateClinicInfo(Form):
    name = StringField('Clinic Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    area = SelectField('Area/Nearest MRT: ', [validators.DataRequired()], choices=['', 'Ang Mo Kio', 'Bedok', 'Bishan', 'Braddell', 'Buangkok', 'Bugis', 'Canberra', 'Changi', 'Chinatown', 'Clementi', 'Harbourfront', 'Hougang', 'Jurong', 'Khatib', 'Kovan', 'Marina', 'Orchard', 'Pasir Ris', 'Punggol', 'Sembawang', 'Sengkang', 'Tampines', 'Woodlands', 'Yio Chu Kang', 'Yishun'], default='')
    # street = StringField('Street Name: ', [validators.DataRequired()])
    # block = IntegerField('Block Number: ', [validators.DataRequired()])
    postal_code = StringField('Postal Code: ', [validate_postal_code, validators.DataRequired()])
    unit = StringField('Unit Number: ', [validators.DataRequired()])
    email = EmailField('Email Address:', [validators.Length(min=6, max=150), validators.DataRequired()])
    phone = TelField('Phone Number:', [validators.Length(min=8, max=8), validators.DataRequired(), validate_tel])

class UpdatePublicInfo(Form):
    name = StringField('Full Name as in NRIC:', [validators.Length(min=1, max=150), validators.DataRequired()])
    area = SelectField('Area/Nearest MRT: ', [validators.DataRequired()], choices=['', 'Ang Mo Kio', 'Bedok', 'Bishan', 'Braddell', 'Buangkok', 'Bugis', 'Canberra', 'Changi', 'Chinatown', 'Clementi', 'Harbourfront', 'Hougang', 'Jurong', 'Khatib', 'Kovan', 'Marina', 'Orchard', 'Pasir Ris', 'Punggol', 'Sembawang', 'Sengkang', 'Tampines', 'Woodlands', 'Yio Chu Kang', 'Yishun'], default='')
    # street = StringField('Street Name: ', [validators.DataRequired()])
    # block = IntegerField('Block Number: ', [validators.DataRequired()])
    postal_code = StringField('Postal Code: ', [validate_postal_code, validators.DataRequired()])
    unit = StringField('Unit Number: ', [validators.DataRequired()])
    email = EmailField('Email Address:', [validators.Length(min=6, max=150), validators.DataRequired()])
    phone = TelField('Phone Number:', [validators.Length(min=8, max=8), validators.DataRequired(), validate_tel])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    nric = StringField('NRIC:', [validators.Length(min=9, max=9), validators.DataRequired()])
    birthdate = DateField('Birth Date:', [validators.DataRequired()])

class UpdateClinicPassword(Form):
    current_password = PasswordField('Current Password:', [validators.Length(min=8, max=15), validators.DataRequired()])
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match'), validate_password_strength])
    cfm_password = PasswordField('Confirm Password:', [validators.Length(min=8, max=15), validators.DataRequired()])

class UpdatePublicPassword(Form):
    current_password = PasswordField('Current Password:', [validators.Length(min=8, max=15), validators.DataRequired()])
    password = PasswordField('Password:', [validators.Length(min=8, max=15), validators.DataRequired(), validators.EqualTo('cfm_password', message='Passwords must match'), validate_password_strength])
    cfm_password = PasswordField('Confirm Password:', [validators.Length(min=8, max=15), validators.DataRequired()])

class SearchClinicOH(Form):
    selected_date = DateField('Select Date:', [validators.Optional()])

class WaitingListForm(Form):
    selected_date = DateField('Select Date:', [validators.Optional()])

class PublicOTPForm(Form):
    otp = StringField('OTP: ', [validators.DataRequired()])

class ClinicOTPForm(Form):
    otp = StringField('OTP: ', [validators.DataRequired()])

class DoctorSchedule(Form):
    selected_date = DateField('Select Date:', [validators.Optional()])
