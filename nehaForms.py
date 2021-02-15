from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators,FileField,BooleanField, FloatField
from wtforms.fields.html5 import DateField,EmailField,TimeField,IntegerField
import shelve
from datetime import date

def list_of_clinics():
    clinics_list = ['']
    list_of_clinics.clinic_id_list = ['']
    try:
        clinic_db = shelve.open('clinic_storage.db', 'r')
        users_dict = clinic_db['Users']
    except:
        print('No database created yet')
        users_dict = {}
    else:
        clinic_db.close()
    for clinic_id in users_dict:
        clinics_list.append(users_dict[clinic_id].get_name())
        list_of_clinics.clinic_id_list.append(clinic_id)
    print(clinics_list)
    return clinics_list

def list_of_clinics_bylocation():
    clinic_location_dict = {}
    try:
        clinic_db = shelve.open('clinic_storage.db', 'r')
        users_dict = clinic_db['Users']
    except:
        print('No database created yet')
        users_dict = {}
    locations = ['Ang Mo Kio', 'Bedok', 'Bishan', 'Braddell', 'Buangkok', 'Bugis', 'Canberra', 'Changi', 'Chinatown', 'Clementi', 'Harbourfront', 'Hougang', 'Jurong', 'Khatib', 'Kovan', 'Marina', 'Orchard', 'Pasir Ris', 'Punggol', 'Sembawang', 'Sengkang', 'Tampines', 'Woodlands', 'Yio Chu Kang', 'Yishun']
    for i in locations:
        clinics_list = ['']
        list_of_clinics_bylocation.clinic_id_list = ['']
        value = [clinics_list, list_of_clinics_bylocation.clinic_id_list]
        clinic_location_dict[i] = [value]
        for clinic_id in users_dict:
            location = users_dict[clinic_id].get_area()
            if location == i:
                clinics_list.append(users_dict[clinic_id].get_name())
                list_of_clinics_bylocation.clinic_id_list.append(clinic_id)
                value = [clinics_list, list_of_clinics_bylocation.clinic_id_list]
                clinic_location_dict[location] = value
        # print(clinics_list)
    clinic_db.close()
    input_location = input('Location: ')
    return(clinic_location_dict[input_location][0])
    # clinic_db.close()
    # return clinics_list

class CreateUserForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.Length(min=9,max=9), validators.DataRequired()])
    email= EmailField('Email',[validators.Length(min=1, max=150), validators.DataRequired()])
    phone= StringField('Contact Number',[validators.Length(min=8,max=8), validators.DataRequired()])
    purpose = SelectField('Purpose', [validators.DataRequired()], choices=[('',''),('M', 'Medical Test/Examination'), ('D', 'Doctor Consultation'), ('C', 'Collection of Documents')], default='')
    date_of_arrival=DateField('Date', format='%Y-%m-%d')
    message = TextAreaField('Message (elaborate on condition or any symptoms)', [validators.Optional()])
    time= TimeField('Time',[validators.DataRequired()])
    clinic = SelectField('Choose Clinic', [validators.DataRequired()], choices=list_of_clinics(), default='')

    def validate_date_of_arrival(form, field):
        today_date = date.today()
        if field.data < today_date:
            raise validators.ValidationError("Appointment date must not be earlier than today's date.")


class UpdateAndCancel(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    nric = StringField('NRIC', [validators.Length(min=9,max=9), validators.DataRequired()])
    email= EmailField('Email',[validators.Length(min=1, max=150), validators.DataRequired()])
    phone= StringField('Contact Number',[validators.Length(min=8,max=8), validators.DataRequired()])
    purpose = SelectField('Purpose', [validators.DataRequired()], choices=[('M', 'Medical Test/Examination'), ('D', 'Doctor Consultation'), ('C', 'Collection of Documents')], default='')
    date_of_arrival=DateField('Date', format='%Y-%m-%d')
    message = TextAreaField('Message (elaborate on condition or any symptoms)', [validators.Optional()])
    time= TimeField('Time',[validators.DataRequired()])
    clinic = SelectField('Choose Clinic', [validators.DataRequired()], choices=list_of_clinics(), default='')

    def validate_date_of_arrival(form, field):
        today_date = date.today()
        if field.data < today_date:
            raise validators.ValidationError("Appointment date must not be earlier than today's date.")

class update_items(Form):
    quantities = IntegerField('Enter Quantity',[validators.DataRequired()])
    qty=StringField('Enter Quantity',[validators.optional()])
    price=IntegerField('',[validators.DataRequired()])
    pricing=StringField('Total Price',[validators.optional()])

class CreateShoppingItems(Form):
    quantity = IntegerField('Enter Product Quantity',[validators.DataRequired(),validators.NumberRange(min=1,max=1000)])
    product_name = SelectField('Select Product', [validators.DataRequired()], choices=[('Paracetamol','Paracetamol'),('Aspirin', 'Aspirin'), ('Antiseptic Cream', 'Antiseptic Cream'), ('Strepsils', 'Strepsils'),('Zyrtec-R', 'Zyrtec-R'),('Bandages', 'Bandages')], default='')
    product_description=TextAreaField('Enter Product Description',[validators.Length(min=8,max=150), validators.DataRequired()])
    price=FloatField('Enter Product Price',[validators.DataRequired()])

if __name__ == '__main__':
    x = list_of_clinics_bylocation()
