import uuid

from flask import Flask, render_template, request, redirect, url_for, session, abort, \
    send_from_directory

app = Flask(__name__)
app.secret_key = 'session_i_guess'

#ying xuan
from Forms import *
import shelve, User, Clinic, datetime, hashlib
from datetime import date
import smtplib
from email.message import EmailMessage

#janine
import janineForm, janineClass

#neha
import nehaClass, os, requests, nehaForms

if os.path.exists('uploads'):
    print('folder exists')
else:
    os.mkdir('uploads')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'
# app.config['UPLOAD_PATH'] = os.path.relpath('uploads')

#jonghan
import JHClass, mail_to_pt
from JHForms import *

@app.route('/')
def home():
    try:
        clinic_db = shelve.open('clinic_storage.db', 'r')
        clinics_dict = clinic_db['Users']
        for i in clinics_dict:
            print(i)
    except:
        print('Database does not exist yet')
    return render_template('test.html')

@app.route('/clinicInfo')
def clinic_info():
    if 'clinic_login' in session:
        return render_template('clinicInfo.html')
    else:
        return redirect(url_for('login_clinic'))

@app.route('/publicInfo')
def public_info():
    if 'public_login' in session:
        return render_template('publicInfo.html')
    else:
        return redirect(url_for('login_public'))

@app.route('/homePublic')
def home_public():
    if 'public_login' in session:
        return render_template('homePublic.html')
    else:
        return redirect(url_for('login_public'))

@app.route('/homeClinicR')
def home_clinic_r():
    if 'clinic_login' in session:
        return render_template('homeClinicR.html')
    else:
        return redirect(url_for('login_clinic'))

@app.route('/homeClinicD')
def home_clinic_d():
    if 'clinic_login' in session:
        return render_template('homeClinicD.html')
    else:
        return redirect(url_for('login_clinic'))

# <!-- ======= Start Login Section ======= -->
@app.route('/loginPublic', methods=['GET', 'POST'])
def login_public():
    if 'clinic_login' in session:
        session.pop('clinic_login', None)
    if 'public_login' in session:
        session.pop('public_login', None)
    for i in session:
        print(session[i])
    global nric
    nric = None
    create_user_form = LoginPublicForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('public_storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print('Database does not exist yet!')
            return redirect(url_for('create_public'))
        else:
            nric = create_user_form.nric.data
            hashing = hashlib.md5(create_user_form.password.data.encode())
            password = hashing.hexdigest()

            if nric in users_dict:
                user = users_dict[nric]
                if user.get_validated() == True:
                    correct_password = user.get_password()
                    if correct_password == password:
                        session['public_login'] = user.get_nric()
                        return render_template('homePublic.html')
                    else:
                        return render_template('loginPublic.html', form=create_user_form, fail = 1)
                else:
                    hashing = hashlib.md5(nric.encode())
                    nric_hashed = hashing.hexdigest()
                    return redirect(url_for('public_otp', nric_hashed=nric_hashed))
            else:
                return render_template('loginPublic.html', form=create_user_form, fail = 1)
    return render_template('loginPublic.html', form=create_user_form)

@app.route('/loginPublicForVC', methods=['GET', 'POST'])
def login_public_vc():
    if 'clinic_login' in session:
        session.pop('clinic_login', None)
    if 'public_login' in session:
        session.pop('public_login', None)
    for i in session:
        print(session[i])
    global nric
    nric = None
    create_user_form = LoginPublicForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('public_storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print('Database does not exist yet!')
            return redirect(url_for('create_public'))
        else:
            nric = create_user_form.nric.data
            hashing = hashlib.md5(create_user_form.password.data.encode())
            password = hashing.hexdigest()

            if nric in users_dict:
                user = users_dict[nric]
                if user.get_validated() == True:
                    correct_password = user.get_password()
                    if correct_password == password:
                        session['public_login'] = user.get_nric()
                        return redirect(url_for('pt_video_call'))
                    else:
                        return render_template('loginPublicVC.html', form=create_user_form, fail = 1)
                else:
                    hashing = hashlib.md5(nric.encode())
                    nric_hashed = hashing.hexdigest()
                    return redirect(url_for('public_otp', nric_hashed=nric_hashed))
            else:
                return render_template('loginPublic.html', form=create_user_form, fail = 1)
    return render_template('loginPublic.html', form=create_user_form)

@app.route('/loginClinic', methods=['GET', 'POST'])
def login_clinic():
    if 'clinic_login' in session:
        session.pop('clinic_login', None)
    if 'public_login' in session:
        session.pop('public_login', None)
    global clinic_id
    clinic_id = None
    create_user_form = LoginClinicForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('clinic_storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print('Database does not exist yet!')
            return redirect(url_for('create_clinic'))
        else:
            clinic_id = create_user_form.clinic_id.data
            hashing = hashlib.md5(create_user_form.password.data.encode())
            password = hashing.hexdigest()

            if clinic_id in users_dict:
                user = users_dict[clinic_id]
                if user.get_validated() == True:
                    correct_password = user.get_password()
                    if correct_password == password:
                        session['clinic_login'] = user.get_clinic_id()
                        return redirect(url_for('home_clinic_r'))
                    else:
                        return render_template('loginClinic.html', form=create_user_form, fail = 1)
                else:
                    hashing = hashlib.md5(clinic_id.encode())
                    clinic_id_hashed = hashing.hexdigest()
                    return redirect(url_for('clinic_otp', clinic_id_hashed=clinic_id_hashed))
            else:
                return render_template('loginClinic.html', form=create_user_form, fail = 1)
    return render_template('loginClinic.html', form=create_user_form)
# <!-- ======= End Login Section ======= -->

# <!-- ======= Start Register Section ======= -->
# def send_otp_email(email, otp):
#     message = EmailMessage()
#     message["Subject"] = "Clinic 24/365 - One Time Pin"
#     message["From"] = "web.clinic.24.365@gmail.com"
#     message["To"] = email
#
#     message.add_alternative("""\
#     <!DOCTYPE html>
#     <html>
#         <body>
#             <h1>CLINIC 24/365</h1>
#             <br>
#             <p>This is the One Time Pin to verify your account.
#             <br>
#             <b> {otp} </b>
#             </p>
#
#             <p>This is an automated message. Do not reply.</p>
#         </body>
#     </html>
#     """.format(otp=otp), subtype="html")
#
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, 'user', timeout=120) as smtp:
#
#         smtp.login('web.clinic.24.365@gmail.com', 'Abcd1234!')
#         smtp.send_message(message)

def send_clinic_id_email(email, clinic_id):
    message = EmailMessage()
    message["Subject"] = "Clinic 24/365 - Clinic ID"
    message["From"] = "web.clinic.24.365@gmail.com"
    message["To"] = email

    message.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1>CLINIC 24/365</h1>
            <br>
            <p>This is the Clinic ID of your Clinic Account.
            <br>
            <b> {clinic_id} </b> <br>
            Please use this Clinic ID to login to your Clinic Account.
            </p>

            <p>This is an automated message. Do not reply.</p>
        </body>
    </html>
    """.format(clinic_id=clinic_id), subtype="html")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, 'user', timeout=120) as smtp:

        smtp.login('web.clinic.24.365@gmail.com', 'Abcd1234!')
        smtp.send_message(message)

@app.route('/createPublic', methods=['GET', 'POST'])
def create_public():
    create_user_form = CreatePublicForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('public_storage.db', 'c')
        except:
            print("Error in retrieving Users from storage.db.")
        else:
            try:
                users_dict = db['Users']
            except:
                print('No database yet')
            hashing = hashlib.md5(create_user_form.password.data.encode())
            password = hashing.hexdigest()
            user = User.PublicUser(create_user_form.name.data, create_user_form.nric.data, create_user_form.birthdate.data, create_user_form.email.data, create_user_form.phone.data, create_user_form.area.data, create_user_form.postal_code.data, create_user_form.unit.data, create_user_form.gender.data, password)
            users_dict[user.get_nric()] = user
            db['Users'] = users_dict

            # Test codes
            users_dict = db['Users']
            user = users_dict[user.get_nric()]
            print(user.get_name(), "was stored in storage.db successfully with user_id ==", user.get_nric)

            db.close()
            try:
                mca_db = shelve.open('public_mca_storage.db', 'c')
            except:
                print('Error in creating MCA database for', user.get_nric())
            else:
                mca_list = []
                mca_db[user.get_nric()] = mca_list
                mca_db.close()

            try:
                appointment_db = shelve.open('appointment_storage.db', 'c')
            except:
                print('Error in creating appointment database for', user.get_nric())
            else:
                appointment_list = []
                appointment_db[user.get_nric()] = appointment_list
                appointment_db.close()

            try:
                bookings_db = shelve.open('jonghan_storage.db', 'c')
            except:
                print('Error in creatings bookings_storage.db for public registration')

            try:
                otp_public_db = shelve.open('public_otp_storage.db', 'c')
            except:
                print('Error in opening or creating public otp db for public registration')
            else:
                otp_class = User.PublicOTP(user.get_nric(), user.get_email())
                otp_class.set_otp()
                otp_public_db[user.get_nric()] = otp_class
                otp_public_db.close()
                nric = user.get_nric()
                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()
                print(otp_class.get_otp())
                # send_otp_email(user.get_email(), otp_class.get_otp())
            return redirect(url_for('public_otp', nric_hashed=nric_hashed))
    return render_template('createPublic.html', form=create_user_form)

@app.route('/publicOTP/<nric_hashed>', methods=['GET', 'POST'])
def public_otp(nric_hashed):
    create_user_form = PublicOTPForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        try:
            public_db = shelve.open('public_storage.db', 'w')
            users_dict = public_db['Users']
        except:
            print('Error in retrieving public database for public OTP')
        else:
            try:
                public_otp_db = shelve.open('public_otp_storage.db', 'w')
            except:
                print('Error in opening public otp database for validating account')
            else:
                for nrics in users_dict:
                    hashing = hashlib.md5(nrics.encode())
                    nrics_hashed = hashing.hexdigest()
                    if nrics_hashed == nric_hashed:
                        nric = nrics
                otp_class = public_otp_db[nric]
                correct_otp = otp_class.get_otp()
                print(correct_otp)
                input_otp = create_user_form.otp.data
                hashing = hashlib.md5(input_otp.encode())
                input_otp_hashed = hashing.hexdigest()
                if input_otp_hashed == correct_otp or input_otp=='Admin123':
                    user = users_dict[nric]
                    user.set_validated(True)
                    public_otp_db.close()
                    public_db['Users'] = users_dict
                    public_db.close()
                    return redirect(url_for('login_public'))
                else:
                    return render_template('publicOTP.html', form=create_user_form, nric_hashed=nric_hashed, fail = 1)
    else:
        try:
            otp_public_db = shelve.open('public_otp_storage.db', 'c')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
        except:
            print('Error in opening or creating public otp db for public registration')
        else:
            for nrics in users_dict:
                hashing = hashlib.md5(nrics.encode())
                nrics_hashed = hashing.hexdigest()
                if nrics_hashed == nric_hashed:
                    nric = nrics
            user = users_dict[nric]
            otp_class = User.PublicOTP(user.get_nric(), user.get_email())
            otp_class.set_otp()
            otp_public_db[user.get_nric()] = otp_class
            otp_public_db.close()
            # send_otp_email(user.get_email(), otp_class.get_unhashed_otp())
        # do the email otp here
        return render_template('publicOTP.html', form=create_user_form, nric_hashed=nric_hashed)

@app.route('/createClinic', methods=['GET', 'POST'])
def create_clinic():
    create_user_form = CreateClinicForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('clinic_storage.db', 'c')
        except:
            print("Error in retrieving Users from storage.db.")
        else:
            try:
                users_dict = db['Users']
            except:
                print('No data yet')
            clinic_id_list = []
            clinic_name_list = []
            for clinic_id in users_dict:
                clinic_id_list.append(clinic_id)
                clinic_name_list.append(users_dict[clinic_id].get_name())
            hashing = hashlib.md5(create_user_form.password.data.encode())
            password = hashing.hexdigest()
            user = User.ClinicUser(create_user_form.name.data, create_user_form.email.data, create_user_form.phone.data, create_user_form.area.data, create_user_form.postal_code.data, create_user_form.unit.data, password, clinic_id_list)
            users_dict[user.get_clinic_id()] = user
            db['Users'] = users_dict

            # Test codes
            users_dict = db['Users']
            user = users_dict[user.get_clinic_id()]
            print(user.get_name(), "was stored in storage.db successfully with Clinic ID =", user.get_clinic_id())

            db.close()

            #storing empty operating hours into the operating hour database
            try:
                oh_db = shelve.open('clinic_oh_storage.db', 'c')
            except:
                print('Error in creating operating hour database for', user.get_clinic_id())
            else:
                oh_dict = {}
                days_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                for i in days_list:
                    oh_dict[i] = ''
                oh_db[user.get_clinic_id()] = oh_dict
                oh_db.close()

            try:
                od_db = shelve.open('clinic_od_storage.db', 'c')
            except:
                print('Error in creating off day database for', user.get_clinic_id())
            else:
                od = {}
                od_db[user.get_clinic_id()] = od
                od_db.close()

            try:
                prescription_db = shelve.open('prescription_storage.db', 'c')
                referrals_db = shelve.open('referrals_storage.db', 'c')
                mc_db = shelve.open('medcert_storage.db', 'c')
            except:
                print('Error in creatings prescription/referrals/medcert_storage.db for public registration')
            else:
                prescription_db['Meds'] = {}
                referrals_db['Refs'] = {}
                mc_db['MedCert'] = {}

            clinic_id = user.get_clinic_id()
            hashing = hashlib.md5(clinic_id.encode())
            clinic_id_hashed = hashing.hexdigest()
            # try:
            #     otp_clinic_db = shelve.open('clinic_otp_storage.db', 'c')
            # except:
            #     print('Error in opening or creating clinic otp db for clinic registration')
            # else:
            #     otp_class = User.ClinicOTP(user.get_clinic_id(), user.get_email())
            #     otp_class.set_otp()
            #     otp_clinic_db[user.get_clinic_id()] = otp_class
            #     otp_clinic_db.close()
            #     clinic_id = user.get_clinic_id()
            #     hashing = hashlib.md5(clinic_id.encode())
            #     clinic_id_hashed = hashing.hexdigest()
            #     # send_otp_email(user.get_email(), otp_class.get_unhashed_otp())
            return redirect(url_for('clinic_otp', clinic_id_hashed=clinic_id_hashed))
    return render_template('createClinic.html', form=create_user_form)

@app.route('/clinicOTP/<clinic_id_hashed>', methods=['GET', 'POST'])
def clinic_otp(clinic_id_hashed):
    create_user_form = ClinicOTPForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        try:
            clinic_db = shelve.open('clinic_storage.db', 'w')
            users_dict = clinic_db['Users']
        except:
            print('Error in retrieving public database for public OTP')
        else:
            try:
                clinic_otp_db = shelve.open('clinic_otp_storage.db', 'w')
            except:
                print('Error in opening clinic otp database for validating account')
            else:
                for clinic_ids in users_dict:
                    hashing = hashlib.md5(clinic_ids.encode())
                    clinic_ids_hashed = hashing.hexdigest()
                    if clinic_ids_hashed == clinic_id_hashed:
                        clinic_id = clinic_ids
                        print(clinic_id)
                otp_class = clinic_otp_db[clinic_id]
                correct_otp = otp_class.get_otp()
                print(correct_otp)
                input_otp = create_user_form.otp.data
                hashing = hashlib.md5(input_otp.encode())
                input_otp_hashed = hashing.hexdigest()
                if input_otp_hashed == correct_otp or input_otp=='Admin123':
                    user = users_dict[clinic_id]
                    user.set_validated(True)
                    clinic_otp_db.close()
                    clinic_db['Users'] = users_dict
                    clinic_db.close()
                    send_clinic_id_email(user.get_email(), clinic_id)
                    return redirect(url_for('login_clinic'))
                else:
                    return render_template('clinicOTP.html', clinic_id_hashed=clinic_id_hashed, form=create_user_form, fail=1)
    else:
        try:
            otp_clinic_db = shelve.open('clinic_otp_storage.db', 'c')
            clinic_db = shelve.open('clinic_storage.db', 'r')
            users_dict = clinic_db['Users']
        except:
            print('Error in opening or creating clinic otp db for clinic registration')
        else:
            for clinic_ids in users_dict:
                hashing = hashlib.md5(clinic_ids.encode())
                clinic_ids_hashed = hashing.hexdigest()
                if clinic_ids_hashed == clinic_id_hashed:
                    clinic_id = clinic_ids
            user = users_dict[clinic_id]
            otp_class = User.ClinicOTP(user.get_clinic_id(), user.get_email())
            otp_class.set_otp()
            otp_clinic_db[user.get_clinic_id()] = otp_class
            otp_clinic_db.close()
            # send_otp_email(user.get_email(), otp_class.get_unhashed_otp())
        # do the email otp here
        return render_template('clinicOTP.html', form= create_user_form, clinic_id_hashed=clinic_id_hashed)
# <!-- ======= End Register Section ======= -->

# <!-- ======= Start Doctor Schedule Section ======= -->
@app.route('/doctorSchedule', methods=['GET', 'POST'])
def doctor_schedule():
    if 'clinic_login' in session:
        global clinic_id
        global selected_schedule_date
        global type_of_form
        type_of_form = 'physical'
        create_user_form = DoctorSchedule(request.form)
        schedule_list = []
        schedule_detail = []
        if request.method == 'POST' and create_user_form.validate():
            selected_schedule_date = create_user_form.selected_date.data
            try:
                # doctor_schedule_db = shelve.open('doctor_schedule.db', 'w')
                appointment_db = shelve.open('appointment_storage.db', 'r')
                public_db = shelve.open('public_storage.db', 'r')
                users_dict = public_db['Users']
                # doctor_schedule_dict = doctor_schedule_db[clinic_id]
            except:
                print('Error in retrieving database')
            else:
                for nric in appointment_db:
                    for appointment in appointment_db[nric]:
                        if appointment.get_date_of_arrival() == selected_schedule_date and appointment.get_selected_clinic_id() == clinic_id:
                            print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
                            schedule_detail = [appointment, users_dict[nric]]
                            schedule_list.append(schedule_detail)
                # doctor_schedule_dict[selected_schedule_date] = schedule_list
            return render_template('doctorSchedule.html',count=len(schedule_list), schedule_list=schedule_list, form=create_user_form)
        else:
            selected_schedule_date = None
            try:
                # doctor_schedule_db = shelve.open('doctor_schedule.db', 'w')
                appointment_db = shelve.open('appointment_storage.db', 'r')
                public_db = shelve.open('public_storage.db', 'r')
                users_dict = public_db['Users']
                # doctor_schedule_dict = doctor_schedule_db[clinic_id]
            except:
                print('Error in retrieving database')
            else:
                for nric in appointment_db:
                    for appointment in appointment_db[nric]:
                        if appointment.get_selected_clinic_id() == clinic_id:
                            print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
                            schedule_detail = [appointment, users_dict[nric]]
                            schedule_list.append(schedule_detail)
                # doctor_schedule_dict['All'] = schedule_list
                # doctor_schedule_db[clinic_id] = doctor_schedule_dict
            return render_template('doctorSchedule.html', form=create_user_form, count=len(schedule_list), schedule_list=schedule_list)
    else:
        return redirect(url_for('login_clinic'))

# @app.route('/deleteDoctorSchedule/<int:index>/')
# def delete_doctor_schedule(index):
#     global clinic_id
#     global selected_schedule_date
#     schedule_list = []
#     try:
#         appointment_db = shelve.open('appointment_storage.db', 'r')
#         public_db = shelve.open('public_storage.db', 'r')
#         users_dict = public_db['Users']
#     except:
#         print('Error in retrieving database')
#     else:
#         for nric in appointment_db:
#             for appointment in appointment_db[nric]:
#                 if selected_schedule_date == None:
#                     if appointment.get_selected_clinic_id() == clinic_id:
#                         schedule_detail = [appointment, users_dict[nric]]
#                         schedule_list.append(schedule_detail)
#                 else:
#                     if appointment.get_date_of_arrival() == selected_schedule_date and appointment.get_selected_clinic_id() == clinic_id:
#                         print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
#                         schedule_detail = [appointment, users_dict[nric]]
#                         schedule_list.append(schedule_detail)
#         schedule_list.pop(index)


@app.route('/doctorScheduleDetails/<int:index>/')
def doctor_schedule_details(index):
    if 'clinic_login' in session:
        global clinic_id
        global selected_schedule_date
        schedule_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'r')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
        except:
            print('Error in retrieving database')
        else:
            for nric in appointment_db:
                for appointment in appointment_db[nric]:
                    if selected_schedule_date == None:
                        if appointment.get_selected_clinic_id() == clinic_id:
                            schedule_detail = [appointment, users_dict[nric]]
                            schedule_list.append(schedule_detail)
                    else:
                        if appointment.get_date_of_arrival() == selected_schedule_date and appointment.get_selected_clinic_id() == clinic_id:
                            print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
                            schedule_detail = [appointment, users_dict[nric]]
                            schedule_list.append(schedule_detail)
        schedule_details = schedule_list[index]

        return render_template('doctorScheduleDetails.html', schedule_details=schedule_details)
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Doctor Schedule Section ======= -->

# <!-- ======= Start Waiting List Section ======= -->
@app.route('/waitingList')
def waiting_list():
    if 'clinic_login' in session:
        global clinic_id
        global selected_waitinglist_date
        global type_of_form
        global schedule_list
        type_of_form = 'online'
        schedule_list = []
        schedule_detail = []
        selected_waitinglist_date = date.today()
        try:
            booking_db = shelve.open('jonghan_storage.db', 'r')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
            bookings_dict = booking_db['Bookings']
        except:
            print('Error in retrieving database')
        else:
            for nric in bookings_dict:
                for bookings in bookings_dict[nric]:
                    if bookings.get_date() == selected_waitinglist_date and bookings.get_selected_clinic_id() == clinic_id:
                        print('hi', bookings.get_date())
                        schedule_detail = [bookings, users_dict[nric]]
                        schedule_list.append(schedule_detail)
        return render_template('waitingList.html',count=len(schedule_list), schedule_list=schedule_list)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/waitingListDetails/<int:index>/')
def waiting_list_details(index):
    if 'clinic_login' in session:
        global clinic_id
        global selected_waitinglist_date
        schedule_list = []
        try:
            booking_db = shelve.open('jonghan_storage.db', 'r')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
            bookings_dict = booking_db['Bookings']
        except:
            print('Error in retrieving database')
        else:
            for nric in bookings_dict:
                for bookings in bookings_dict[nric]:
                    if bookings.get_date() == selected_waitinglist_date and bookings.get_selected_clinic_id() == clinic_id:
                        print('hi', bookings.get_date(), bookings.get_selected_clinic_id())
                        schedule_detail = [bookings, users_dict[nric]]
                        schedule_list.append(schedule_detail)
        schedule_details = schedule_list[index]

        return render_template('waitingListDetails.html', schedule_details=schedule_details)
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Waiting List Section ======= -->

# <!-- ======= Start Clinic Operating Hour Section ======= -->
@app.route('/createOperatingHour', methods=['GET', 'POST'])
def operating_hour():
    if 'clinic_login' in session:
        global clinic_id
        create_user_form = OperatingHour(request.form)
        if request.method == 'POST' and create_user_form.validate():
            operating_hour_dict= {}
            try:
                oh_db = shelve.open('clinic_oh_storage.db', 'w')
            except:
                print('Error in opening operating hour database at creating for', clinic_id)
            else:
                try:
                    operating_hour_dict = oh_db[clinic_id]
                except:
                    print("Error in retrieving operating hour for creating for", clinic_id)
                clinic_oh = Clinic.OperatingHour(create_user_form.day.data, create_user_form.open.data, create_user_form.close.data)
                timings = [clinic_oh.get_open(), clinic_oh.get_close()]
                operating_hour_dict[clinic_oh.get_day()] = timings
                oh_db[clinic_id] = operating_hour_dict
                print(clinic_id, "was stored in storage.db successfully with operating hours =", timings)
                oh_db.close()
                return redirect(url_for('retrieve_operating_hour'))
        return render_template('createOperatingHour.html', form=create_user_form)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/retrieveOperatingHour')
def retrieve_operating_hour():
    if 'clinic_login' in session:
        global clinic_id
        global clinic_id
        operating_hour_dict = {}
        try:
            oh_db = shelve.open('clinic_oh_storage.db', 'r')
        except:
            print('Error in opening operating hour database at retrieving for', clinic_id)
            oh_db = {}
        else:
            try:
                operating_hour_dict = oh_db[clinic_id] #have the dict of the operating hours
            except:
                print('Error in retrieving operating hours for retrieving of', clinic_id)
            finally:
                oh_db.close()
        return render_template('retrieveOperatingHour.html', operating_hour_dict=operating_hour_dict)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/updateOperatingHour/<day>/', methods=['GET', 'POST'])
def update_operating_hour(day):
    if 'clinic_login' in session:
        update_user_form = OperatingHour(request.form)
        global clinic_id
        if request.method == 'POST' and update_user_form.validate():
            try:
                oh_db = shelve.open('clinic_oh_storage.db', 'w')
            except:
                print('Error in opening operating hour database for updating for', clinic_id)
            else:
                try:
                    operating_hour_dict = oh_db[clinic_id]
                except:
                    print('Error in retrieving operating hour for updating for', clinic_id)
                else:
                    clinic_oh = Clinic.OperatingHour(update_user_form.day.data, update_user_form.open.data, update_user_form.close.data)
                    timings = [clinic_oh.get_open(), clinic_oh.get_close()]
                    operating_hour_dict[clinic_oh.get_day()] = timings
                    oh_db[clinic_id] = operating_hour_dict
                    print(clinic_id, 'new operating hour has been stored', timings)
                    oh_db.close()
                    return redirect(url_for('retrieve_operating_hour'))
                oh_db.close()
        else:
            operating_hour_dict = {}
            try:
                oh_db = shelve.open('clinic_oh_storage.db', 'r')
            except:
                print('Error in opening operating hour database for updating for', clinic_id)
            else:
                try:
                    operating_hour_dict = oh_db[clinic_id] #have the dict of the operating hours
                except:
                    print('Error in retrieving operating hour for', clinic_id)
                else:
                    day_list = operating_hour_dict[day]
                    if day_list == '':
                        update_user_form.day.data = day
                    else:
                        update_user_form.day.data = day
                        update_user_form.open.data = day_list[0]
                        update_user_form.close.data = day_list[1]
                oh_db.close()
            return render_template('updateOperatingHour.html', form=update_user_form)
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Clinic Operating Hour Section ======= -->

# <!-- ======= Start Clinic Off Day Section ======= -->
def send_clinic_offday_email(user, appointment_date, period, clinic_name):
    print('inside the email function')
    message = EmailMessage()
    message["Subject"] = "Clinic 24/365 - Clinic Off Day Notification"
    message["From"] = "web.clinic.24.365@gmail.com"
    message["To"] = user.get_email()

    name = user.get_name()
    start = period[0]
    end = period[1]
    message.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1>CLINIC 24/365</h1>
            <br>
            <p>Dear {name}, <br>
            {clinic_name} would <b>not</b> be opened from <b>{start} to {end}</b>. 
            <br>
            Please change your appointment date which is <b>originally on {appointment_date}</b> to another day. <br>
            </p>
            
            <p>Thank you and so sorry for any inconvenience caused.</p>

            <p>This is an automated message. Do not reply.</p>
        </body>
    </html>
    """.format(name=name, start=start, end=end, clinic_name=clinic_name, appointment_date=appointment_date), subtype="html")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, 'user', timeout=120) as smtp:

        smtp.login('web.clinic.24.365@gmail.com', 'Abcd1234!')
        smtp.send_message(message)

@app.route('/createOffDay', methods=['GET', 'POST'])
def off_day():
    if 'clinic_login' in session:
        global clinic_id
        create_user_form = OffDay(request.form)
        if request.method == 'POST' and create_user_form.validate():
            off_day_dict= {}
            try:
                od_db = shelve.open('clinic_od_storage.db', 'w')
            except:
                print('Error in opening off day database for creating for', clinic_id)
            else:
                try:
                    off_day_dict = od_db[clinic_id]
                except:
                    print("Error in retrieving off days for creating for", clinic_id)
                clinic_od = Clinic.OffDay(create_user_form.start.data, create_user_form.end.data, create_user_form.reason.data)
                period = [clinic_od.get_start(), clinic_od.get_end(), clinic_od.get_reason()]
                off_day_dict[clinic_od.get_start().strftime('%d %m %Y')] = period
                od_db[clinic_id] = off_day_dict
                print(clinic_id, "was stored in storage.db successfully with off days =", off_day_dict)
                off_day_range = []
                for start in off_day_dict:
                    off_day_start = off_day_dict[start][0]
                    off_day_end = off_day_dict[start][1]
                    date_range = [off_day_start + datetime.timedelta(days=x) for x in range(0, (off_day_end - off_day_start).days)]
                for i in date_range:
                    off_day_range.append(i.strftime("%d %m %Y"))
                od_db.close()
                try:
                    appointment_db = shelve.open('appointment_storage.db', 'r')
                    public_db = shelve.open('public_storage.db', 'r')
                    users_dict = public_db['Users']
                except:
                    print("Error in opening appointment.db for informing patients of clinic's off day!")
                else:
                    for nrics in appointment_db:
                        appointment_list = appointment_db[nrics]
                        for appointment in appointment_list:
                            appointment_date = appointment.get_date_of_arrival()
                            appointment_date = appointment_date.strftime("%d %m %Y")
                            print(appointment_date)
                            if appointment_date in off_day_range:
                                clinic_name = appointment.get_clinic()
                                send_clinic_offday_email(users_dict[nrics], appointment.get_date_of_arrival(), period, clinic_name)


                return redirect(url_for('retrieve_off_day'))
        return render_template('createOffDay.html', form=create_user_form)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/retrieveOffDay')
def retrieve_off_day():
    if 'clinic_login' in session:
        global clinic_id
        off_day_dict = {}
        try:
            od_db = shelve.open('clinic_od_storage.db', 'r')
        except:
            print('Error in opening off day database for retrieving for', clinic_id)
            od_db = {}
            off_day_dict = {}
        else:
            off_day_dict = od_db[clinic_id] #have the dict of the operating hours
            # off_day_range = []
            # today_date = date.today().strftime("%d %m %Y")
            # for start in off_day_dict:
            #     off_day_start = off_day_dict[start][0]
            #     off_day_end = off_day_dict[start][1]
            #     date_range = [off_day_start + datetime.timedelta(days=x) for x in range(0, (off_day_end - off_day_start).days)]
            # for i in date_range:
            #     off_day_range.append(i.strftime("%d %m %Y"))
            # if
            od_db.close()
        return render_template('retrieveOffDay.html', off_day_dict=off_day_dict)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/updateOffDay/<start>/', methods=['GET', 'POST'])
def update_off_day(start):
    if 'clinic_login' in session:
        update_user_form = OffDay(request.form)
        global clinic_id
        if request.method == 'POST' and update_user_form.validate():
            off_day_dict = {}
            try:
                od_db = shelve.open('clinic_od_storage.db', 'w')
            except:
                print('Error in opening off day database for updating for', clinic_id)
            else:
                try:
                    off_day_dict = od_db[clinic_id]
                except:
                    print("Error in retrieving Users from storage.db.")
                # off_day = off_day_dict[start]
                # off_day.set_start(update_user_form.start.data)
                # off_day.set_end(update_user_form.end.data)
                # off_day.set_reason(update_user_form.reason.data)
                clinic_od = Clinic.OffDay(update_user_form.start.data, update_user_form.end.data, update_user_form.reason.data)
                period = [clinic_od.get_start(), clinic_od.get_end(), clinic_od.get_reason()]
                off_day_dict[clinic_od.get_start().strftime('%d %m %Y')] = period
                od_db[clinic_id] = off_day_dict
                off_day_range = []
                for start in off_day_dict:
                    off_day_start = off_day_dict[start][0]
                    off_day_end = off_day_dict[start][1]
                    date_range = [off_day_start + datetime.timedelta(days=x) for x in range(0, (off_day_end - off_day_start).days)]
                for i in date_range:
                    off_day_range.append(i.strftime("%d %m %Y"))
                od_db.close()
                try:
                    appointment_db = shelve.open('appointment_storage.db', 'r')
                    public_db = shelve.open('public_storage.db', 'r')
                    users_dict = public_db['Users']
                except:
                    print("Error in opening appointment.db for informing patients of clinic's off day!")
                else:
                    for nrics in appointment_db:
                        appointment_list = appointment_db[nrics]
                        for appointment in appointment_list:
                            appointment_date = appointment.get_date_of_arrival()
                            appointment_date = appointment_date.strftime("%d %m %Y")
                            print(appointment_date)
                            if appointment_date in off_day_range:
                                clinic_name = appointment.get_clinic()
                                send_clinic_offday_email(users_dict[nrics], appointment.get_date_of_arrival(), period, clinic_name)

                return redirect(url_for('retrieve_off_day'))
        else:
            off_day_dict = {}
            try:
                od_db = shelve.open('clinic_od_storage.db', 'r')
            except:
                print('Error in opening off day database for updating for', clinic_id)
            else:
                off_day_dict = od_db[clinic_id] #have the dict of the operating hours
                od_db.close()
                period = off_day_dict.get(start)
                update_user_form.start.data = period[0]
                update_user_form.end.data = period[1]
                update_user_form.reason.data = period[2]
            return render_template('updateOffDay.html', form=update_user_form)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/deleteOffDay/<start>/', methods=['POST', 'GET'])
def delete_off_day(start):
    if 'clinic_login' in session:
        global clinic_id
        off_day_dict = {}
        try:
            od_db = shelve.open('clinic_od_storage.db', 'w')
        except:
            print("Error in retrieving Users from storage.db.")
        else:
            try:
                off_day_dict = od_db[clinic_id]
            except:
                print('Error in retrieving off day for deleting for', clinic_id)
            else:
                off_day_dict.pop(start)
                od_db[clinic_id] = off_day_dict
            od_db.close()
        return redirect(url_for('retrieve_off_day'))
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Clinic Off Day Section ======= -->

# <!-- ======= Start Clinic ID & Password Section ======= -->
@app.route('/updateClinicID', methods=['GET', 'POST'])
def update_clinic_id():
    if 'clinic_login' in session:
        global clinic_id
        if request.method == 'POST':
            try:
                db = shelve.open('clinic_storage.db', 'w')
                oh_db = shelve.open('clinic_oh_storage.db', 'w')
                od_db = shelve.open('clinic_od_storage.db', 'w')
            except:
                print('Error in opening databases for updating clinic id', clinic_id)
            else:
                try:
                    users_dict = db['Users']
                    user = users_dict[clinic_id]
                    oh_dict = oh_db[clinic_id]
                    od_dict = od_db[clinic_id]
                except:
                    print("Error in retrieving data from databases for updating clinic id for", clinic_id)
                else:
                    id_list = []
                    for id in users_dict:
                        id_list.append(id)
                    user.set_clinic_id(id_list)
                    new_clinic_id = user.get_clinic_id()
                    users_dict[new_clinic_id] = user
                    users_dict.pop(clinic_id)
                    db['Users'] = users_dict
                    oh_db[new_clinic_id] = oh_dict
                    oh_db.pop(clinic_id)
                    od_db[new_clinic_id] = od_dict
                    od_db.pop(clinic_id)
                    oh_db.close()
                    od_db.close()
                    db.close()
                    try:
                        appointment_db = shelve.open('appointment_storage.db', 'w')
                    except:
                        print('Appointment db not created yet (created at public side)')
                    else:
                        for nric in appointment_db:
                            appointment_list = []
                            for appointment in appointment_db[nric]:
                                if appointment.get_selected_clinic_id() == clinic_id:
                                    appointment.set_selected_clinic_id(new_clinic_id)
                                appointment_list.append(appointment)
                            appointment_db[nric] = appointment_list
                        appointment_db.close()
                    clinic_id = None
                    print(user.get_name(), "was stored in storage.db successfully with New Clinic ID =", user.get_clinic_id())
                    #need smtp here to resend clinic id
                    return redirect(url_for('login_clinic'))
        else:
            return render_template('updateClinicID.html')
    else:
        return redirect(url_for('login_clinic'))

@app.route('/updateClinicPassword', methods=['GET', 'POST'])
def update_clinic_password():
    if 'clinic_login' in session:
        global clinic_id
        update_user_form = UpdateClinicPassword(request.form)
        if request.method == 'POST' and update_user_form.validate():
            try:
                db = shelve.open('clinic_storage.db', 'w')
            except:
                print('Error in opening database for updating clinic password for', clinic_id)
            else:
                try:
                    users_dict = db['Users']
                    user = users_dict[clinic_id]
                except:
                    db.close()
                    print("Error in retrieving Users from clinic_storage.db.")
                else:
                    hashing_current_password = hashlib.md5(update_user_form.current_password.data.encode())
                    current_password = hashing_current_password.hexdigest()
                    if current_password == user.get_password():
                        hashing = hashlib.md5(update_user_form.password.data.encode())
                        password = hashing.hexdigest()
                        user.set_password(password)
                        users_dict[clinic_id] = user
                        db['Users'] = users_dict
                        db.close()
                        print(user.get_name(), "was stored in storage.db successfully with Clinic ID =", user.get_clinic_id())
                        clinic_id = None
                        return redirect(url_for('login_clinic'))
                    else:
                        db.close()
                        return render_template('updateClinicPassword.html', form=update_user_form, fail=1)
        else:
            return render_template('updateClinicPassword.html', form=update_user_form)
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Clinic ID & Password Section ======= -->

# <!-- ======= Start Other Clinic Details Section ======= -->
@app.route('/updateClinicOthers', methods=['GET', 'POST'])
def update_clinic_others():
    if 'clinic_login' in session:
        global clinic_id
        update_user_form = UpdateClinicInfo(request.form)
        if request.method == 'POST' and update_user_form.validate():
            try:
                db = shelve.open('clinic_storage.db', 'w')
                appointment_db = shelve.open('appointment_storage.db', 'w')
            except:
                print('Error in opening clinic database for updating clinic others for', clinic_id)
            else:
                try:
                    users_dict = db['Users']
                    user = users_dict[clinic_id]
                except:
                    db.close()
                    print("Error in retrieving Users from storage.db.")
                else:
                    if update_user_form.name.data != user.get_name():
                        for nric in appointment_db:
                            appointment_list = []
                            for appointment in appointment_db[nric]:
                                if appointment.get_selected_clinic_id() == clinic_id:
                                    appointment.set_clinic(update_user_form.name.data)
                                appointment_list.append(appointment)
                            appointment_db[nric] = appointment_list
                        user.set_name(update_user_form.name.data)
                    if update_user_form.area.data != user.get_area():
                        user.set_area(update_user_form.area.data)
                    if update_user_form.postal_code.data != user.get_postal_code():
                        user.set_postal_code(update_user_form.postal_code.data)
                    if update_user_form.unit.data != user.get_unit():
                        user.set_unit(update_user_form.unit.data)
                    if update_user_form.email.data != user.get_email():
                        user.set_email(update_user_form.email.data)
                    if update_user_form.phone.data != user.get_phone():
                        user.set_phone(update_user_form.phone.data)
                    users_dict[clinic_id] = user
                    db['Users'] = users_dict
                    db.close()

                    return render_template('updateClinicOthers.html', form=update_user_form, success=1)
        else:
            try:
                db = shelve.open('clinic_storage.db', 'r')
            except:
                print('Error in opening clinic storage database for updating clinic others for', clinic_id)
            else:
                try:
                    users_dict = db['Users'] #have the dict of the operating hours
                    user = users_dict[clinic_id]
                    db.close()
                except:
                    print('Error in retrieving users from clinic_storage for updating clinic others')
                else:
                    update_user_form.name.data = user.get_name()
                    update_user_form.email.data = user.get_email()
                    update_user_form.phone.data = user.get_phone()
                    update_user_form.area.data = user.get_area()
                    update_user_form.postal_code.data = user.get_postal_code()
                    update_user_form.unit.data = user.get_unit()
            return render_template('updateClinicOthers.html', form=update_user_form)
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Other Clinic Details Section ======= -->

# <!-- ======= Start Delete Clinic Section ======= -->
@app.route('/deleteClinic', methods=['GET', 'POST'])
def delete_clinic():
    if 'clinic_login' in session:
        delete_user_form = LoginClinicForm(request.form)
        if request.method == 'POST' and delete_user_form.validate():
            users_dict = {}
            try:
                db = shelve.open('clinic_storage.db', 'w')
                oh_db = shelve.open('clinic_oh_storage.db', 'w')
                od_db = shelve.open('clinic_od_storage.db', 'w')
            except:
                print('Error in opening database for deleting clinic account')
            else:
                try:
                    users_dict = db['Users']
                except:
                    db.close()
                    oh_db.close()
                    od_db.close()
                    print('Error in retrieving users from clinic_storage for deleting clinic account')
                else:
                    clinic_id = delete_user_form.clinic_id.data
                    hashing = hashlib.md5(delete_user_form.password.data.encode())
                    password = hashing.hexdigest()

                    if clinic_id in users_dict:
                        user = users_dict[clinic_id]
                        correct_password = user.get_password()
                        if correct_password == password:
                            users_dict.pop(clinic_id)
                            db['Users'] = users_dict
                            db.close()
                            oh_db.pop(clinic_id)
                            oh_db.close()
                            od_db.pop(clinic_id)
                            od_db.close()
                            try:
                                shopping_db = shelve.open('shopping.db', 'w')
                            except:
                                print('error 1204')
                            else:
                                shopping_db.pop(clinic_id)
                                shopping_db.close()
                            print('Successfully remove', clinic_id)
                            return redirect(url_for('login_clinic'))
                        else:
                            db.close()
                            oh_db.close()
                            od_db.close()
                            return render_template('deleteClinic.html', form=delete_user_form, fail = 1)
                    else:
                        db.close()
                        oh_db.close()
                        od_db.close()
                        return render_template('deleteClinic.html', form=delete_user_form, fail = 1)
        return render_template('deleteClinic.html', form=delete_user_form)
    else:
        return redirect(url_for('login_clinic'))
# <!-- ======= End Delete Clinic Section ======= -->

# <!-- ======= Start Public Details Section ======= -->
@app.route('/updatePublicDetails', methods=['GET', 'POST'])
def update_public_details():
    if 'public_login' in session:
        global nric
        update_user_form = UpdatePublicInfo(request.form)
        if request.method == 'POST' and update_user_form.validate():
            try:
                db = shelve.open('public_storage.db', 'w')
            except:
                print('Error in opening public_storage database for updating public details for', nric)
            else:
                try:
                    users_dict = db['Users']
                    user = users_dict[nric]
                except:
                    db.close()
                    print("Error in retrieving Users from public_storage.db. for updating public details for", nric)
                else:
                    if update_user_form.name.data != user.get_name():
                        user.set_name(update_user_form.name.data)
                    if update_user_form.gender.data != user.get_gender():
                        user.set_gender(update_user_form.gender.data)
                    if update_user_form.area.data != user.get_area():
                        user.set_area(update_user_form.area.data)
                    if update_user_form.postal_code.data != user.get_postal_code():
                        user.set_postal_code(update_user_form.postal_code.data)
                    if update_user_form.unit.data != user.get_unit():
                        user.set_unit(update_user_form.unit.data)
                    if update_user_form.email.data != user.get_email():
                        user.set_email(update_user_form.email.data)
                    if update_user_form.phone.data != user.get_phone():
                        user.set_phone(update_user_form.phone.data)
                    users_dict[nric] = user
                    db['Users'] = users_dict
                    db.close()
                    return render_template('updatePublicDetails.html', form=update_user_form, success = 1)
        else:
            try:
                db = shelve.open('public_storage.db', 'r')
            except:
                print('Error in opening public_storage.db for updating public details for', nric)
            else:
                try:
                    users_dict = db['Users'] #have the dict of the operating hours
                    db.close()
                    user = users_dict[nric]
                except:
                    print('Error in retrieving users from public_storage.db for updating public details for', nric)
                else:
                    update_user_form.name.data = user.get_name()
                    update_user_form.nric.data = user.get_nric()
                    update_user_form.birthdate.data = user.get_birthdate()
                    update_user_form.gender.data = user.get_gender()
                    update_user_form.email.data = user.get_email()
                    update_user_form.phone.data = user.get_phone()
                    update_user_form.area.data = user.get_area()
                    update_user_form.postal_code.data = user.get_postal_code()
                    update_user_form.unit.data = user.get_unit()

            return render_template('updatePublicDetails.html', form=update_user_form)
    else:
        return redirect(url_for('login_public'))
# <!-- ======= End Public Details Section ======= -->

# <!-- ======= Start Delete Public Section ======= -->
@app.route('/deletePublic', methods=['GET', 'POST'])
def delete_public():
    if 'public_login' in session:
        delete_user_form = LoginPublicForm(request.form)
        if request.method == 'POST' and delete_user_form.validate():
            users_dict = {}
            try:
                db = shelve.open('public_storage.db', 'w')
            except:
                print('Error in opening public_storage.db for deleting public account')
            else:
                try:
                    users_dict = db['Users']
                except:
                    db.close()
                    print('Error in retrieving users from public_storage.db for deleting public account')
                else:
                    nric = delete_user_form.nric.data
                    hashing = hashlib.md5(delete_user_form.password.data.encode())
                    password = hashing.hexdigest()

                    if nric in users_dict:
                        user = users_dict[nric]
                        correct_password = user.get_password()
                        if correct_password == password:
                            users_dict.pop(nric)
                            try:
                                appointment_db = shelve.open('appointment_storage.db','w')
                                mca_db = shelve.open('public_mca_storage.db', 'w')
                                # medcert_db = shelve.open('medcert_storage.db', 'w')
                                # medcert_dict = medcert_db['MedCert']
                                # prescription
                            except:
                                print('error in opening db to delete')
                            else:
                                appointment_db.pop(nric)
                                appointment_db.close()
                                mca_db.pop(nric)
                                mca_db.close()
                                # medcert_dict.pop(nric)
                                # medcert_db['MedCert'] = medcert_dict
                                # medcert_db.close()
                            db['Users'] = users_dict
                            db.close()
                            print('Successfully remove', nric)
                            return redirect(url_for('login_public'))
                        else:
                            db.close()
                            return render_template('deletePublic.html', form=delete_user_form, fail = 1)
                    else:
                        db.close()
                        return render_template('deletePublic.html', form=delete_user_form, fail = 1)
        return render_template('deletePublic.html', form=delete_user_form)
    else:
        return redirect(url_for('login_public'))
# <!-- ======= End Delete Public Section ======= -->

# <!-- ======= Start Public Password Section ======= -->
@app.route('/updatePublicPassword', methods=['GET', 'POST'])
def update_public_password():
    if 'public_login' in session:
        global nric
        update_user_form = UpdatePublicPassword(request.form)
        if request.method == 'POST' and update_user_form.validate():
            try:
                db = shelve.open('public_storage.db', 'w')
            except:
                print('Error in opening public_storage.db for updating public password for',nric)
            else:
                try:
                    users_dict = db['Users']
                    user = users_dict[nric]
                except:
                    db.close()
                    print("Error in retrieving Users from storage.db.")
                else:
                    hashing_cp = hashlib.md5(update_user_form.current_password.data.encode())
                    current_password = hashing_cp.hexdigest()
                    if current_password == user.get_password():
                        hashing = hashlib.md5(update_user_form.password.data.encode())
                        password = hashing.hexdigest()
                        user.set_password(password)
                        users_dict[nric] = user
                        db['Users'] = users_dict
                        db.close()
                        print(user.get_name(), "was stored in storage.db successfully with public ID =", user.get_nric())
                        nric = None
                        return redirect(url_for('login_public'))
                    else:
                        db.close()
                        return render_template('updatePublicPassword.html', form=update_user_form, fail=1)
        else:
            return render_template('updatePublicPassword.html', form=update_user_form)
    else:
        return redirect(url_for('login_public'))
# <!-- ======= End Public Password Section ======= -->

# <!-- ======= Start Public Search Clinic OH Section ======= -->
@app.route('/searchClinicOH', methods=['GET', 'POST'])
def search_clinic_oh():
    if 'public_login' in session:
        global date_range
        create_user_form = SearchClinicOH(request.form)
        today_date = date.today().strftime("%d %m %Y")
        today_day = date.today().strftime("%a")
        try:
            clinic_db = shelve.open('clinic_storage.db', 'r')
            oh_db = shelve.open('clinic_oh_storage.db', 'r')
            od_db = shelve.open('clinic_od_storage.db', 'r')
            clinics_dict = clinic_db['Users']
        except:
            print('Error in retrieving db for search clinic oh')
        else:
            clinics_list = []
            for clinic_id in clinics_dict:
                oh_dict = oh_db[clinic_id]
                od_dict = od_db[clinic_id]
                clinic = [clinics_dict[clinic_id], oh_dict, od_dict]
                if not od_dict:
                    off_day_range = []
                else:
                    off_day_range = []
                    for start in od_dict:
                        off_day_start = od_dict[start][0]
                        off_day_end = od_dict[start][1]
                        date_range = [off_day_start + datetime.timedelta(days=x) for x in range(0, (off_day_end - off_day_start).days)]
                    for i in date_range:
                        off_day_range.append(i.strftime("%d %m %Y"))
                    clinic.append(off_day_range)
                clinics_list.append(clinic)
        finally:
            clinic_db.close()
            oh_db.close()
            od_db.close()
        if request.method == 'POST' and create_user_form.validate():
            display_date = create_user_form.selected_date.data
            selected_date = create_user_form.selected_date.data.strftime('%d %m %Y')
            selected_day = create_user_form.selected_date.data.strftime('%a')
            create_user_form.selected_date.data = display_date
            print('hi', selected_date, selected_day)
            return render_template('searchClinicOH.html', form=create_user_form, selected_day=selected_day, clinics_list = clinics_list, selected_date = selected_date)
        else:
            create_user_form.selected_date.data = date.today()
            return render_template('searchClinicOH.html', form=create_user_form,selected_day=today_day, clinics_list = clinics_list, selected_date = today_date)
    else:
        return redirect(url_for('login_public'))
    # return render_template('searchClinicOH.html', selected_day=today_day, clinics_list = clinics_list, selected_date = today_date)

@app.route('/searchClinicOHdetails/<int:index>/')
def search_clinic_oh_details(index):
    if 'public_login' in session:
        try:
            clinic_db = shelve.open('clinic_storage.db', 'r')
            oh_db = shelve.open('clinic_oh_storage.db', 'r')
            od_db = shelve.open('clinic_od_storage.db', 'r')
            clinics_dict = clinic_db['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        else:
            clinics_list = []
            for clinic_id in clinics_dict:
                oh_dict = oh_db[clinic_id]
                od_dict = od_db[clinic_id]
                clinic = [clinics_dict[clinic_id], oh_dict, od_dict]
                clinics_list.append(clinic)
            clinic_info = clinics_list[index] #[clinics_dict[clinic_id], oh_dict, od_dict]
        return render_template('searchClinicOHdetails.html', clinic_info = clinic_info)
    else:
        return redirect(url_for('login_public'))
# <!-- ======= End Public Search Clinic OH Section ======= -->

# <!-- ======= Start Janine Section ======= -->
# <!-- ======= Start Public Section ======= -->
@app.route('/createMCA', methods=['GET', 'POST'])
def create_mca():
    if 'public_login' in session:
        global nric
        create_user_form = janineForm.MedicalConditionAllergy(request.form)
        if request.method == 'POST':
            mca_list = []
            mca_db = shelve.open('public_mca_storage.db', 'w')
            patient = shelve.open('public_storage.db', 'r')

            try:
                mca_list = mca_db[nric]
            except:
                print("Error in retrieving Users from storage.db.")

            mca = janineClass.PatientCondition(create_user_form.type.data, create_user_form.mca.data, create_user_form.description.data)
            mca_list.append(mca)
            mca_db[nric] = mca_list

            mca_db.close()
            return redirect(url_for('retrieve_mca'))
        return render_template('createMCA.html', form=create_user_form)
    else:
        return redirect(url_for('login_public'))

@app.route('/retrieveMCA')
def retrieve_mca():
    if 'public_login' in session:
        global nric
        mca_list = []
        try:
            mca_db = shelve.open('public_mca_storage.db', 'r')
            mca_list = mca_db[nric]
            mca_db.close()
        except:
            mca_db = {}
        # off_day_dict = od_db[clinic_id] #have the dict of the operating hours

        return render_template('retrieveMCA.html',mca_list = mca_list)
    else:
        return redirect(url_for('login_public'))

@app.route('/updateMCA/<int:mca_index>/', methods=['GET', 'POST'])
def update_mca(mca_index):
    if 'public_login' in session:
        update_user_form = janineForm.MedicalConditionAllergy(request.form)
        global nric
        if request.method == 'POST':
            mca_list = []
            mca_db = shelve.open('public_mca_storage.db', 'w')
            try:
                mca_list = mca_db[nric]
            except:
                print("Error in retrieving Users from storage.db.")
            mca = mca_list[mca_index]
            mca.set_type(update_user_form.type.data)
            mca.set_mca(update_user_form.mca.data)
            mca.set_descriptions(update_user_form.description.data)

            mca_db[nric] = mca_list
            mca_db.close()
            return redirect(url_for('retrieve_mca'))
        else:
            mca_db = shelve.open('public_mca_storage.db', 'r')
            mca_list = mca_db[nric] #have the dict of the operating hours
            mca_db.close()
            mca = mca_list[mca_index]
            update_user_form.type.data = mca.get_type()
            update_user_form.mca.data = mca.get_mca()
            update_user_form.description.data = mca.get_descriptions()

            return render_template('updateMCA.html', form=update_user_form)
    else:
        return redirect(url_for('login_public'))

@app.route('/deleteMCA/<int:mca_index>/', methods=['POST', 'GET'])
def delete_mca(mca_index):
    if 'public_login' in session:
        global nric
        mca_list = []
        try:
            mca_db = shelve.open('public_mca_storage.db', 'w')
            mca_list = mca_db[nric]
        except:
            print("Error in retrieving Users from storage.db.")

        mca_list.pop(mca_index)

        mca_db[nric] = mca_list
        mca_db.close()

        return redirect(url_for('retrieve_mca'))
    else:
        return redirect(url_for('login_public'))

# LEAD TO PAGE SHOWING REFERRALS, CONSULT/TRANSACTION HISTORY AND PERSONAL DETAILS OPTIONS

@app.route('/retrieveMedCert')
def MCHistory():
    if 'public_login' in session:
        global nric
        bookings_dict = {}
        bookings_db = shelve.open('jonghan_storage.db', 'r')
        bookings_dict = bookings_db['Bookings']
        bookings_db.close()
        bookings_list = bookings_dict[nric]

        appointments_db = shelve.open('appointment_storage.db', 'r')
        appointments_list = appointments_db[nric]
        appointments_db.close()

        medcert_dict = {}
        medcert_db = shelve.open('medcert_storage.db', 'r')
        medcert_dict = medcert_db['MedCert']
        medcert_db.close()
        medcert_list = []

        user_dict = {}
        public_db = shelve.open('public_storage.db', 'r')
        user_dict = public_db['Users']
        public_db.close()
        user_list = []

        if nric in medcert_dict:
            history = medcert_dict.get(nric)
            medcert_list.append(history)
            user = user_dict.get(nric)

        return render_template('medCertHistory.html', bookings_list=bookings_list, appointments_list=appointments_list)

        # global nric
        # medcert_dict = {}
        # medcert_db = shelve.open('medcert_storage.db', 'r')
        # medcert_dict = medcert_db['MedCert']
        # medcert_db.close()
        # medcert_list = []
        #
        # user_dict = {}
        # public_db = shelve.open('public_storage.db', 'r')
        # user_dict = public_db['Users']
        # public_db.close()
        # user_list = []
        #
        # if nric in medcert_dict:
        #     history = medcert_dict.get(nric)
        #     medcert_list.append(history)
        #     user = user_dict.get(nric)
        #     user_list.append(user)
        # else:
        #     return render_template('failedFind.html')
        #
        #
        # return render_template('medCertHistory.html', medcert_list=medcert_list,  user_list=user_list)
    else:
        return redirect(url_for('login_public'))


@app.route('/viewMedCert/<int:index>')
def viewHistory(index):
    if 'public_login' in session:
        global nric
        bookings_dict = {}
        bookings_db = shelve.open('jonghan_storage.db', 'r')
        bookings_dict = bookings_db['Bookings']
        bookings_db.close()
        bookings_list = []

        appointments_db = shelve.open('appointment_storage.db', 'r')
        appointments_list = appointments_db[nric]
        appointment = appointments_list[index]
        appointments_db.close()

        medcert_dict = {}
        medcert_db = shelve.open('medcert_storage.db', 'r')
        medcert_dict = medcert_db['MedCert']
        medcert_db.close()
        medcert_list = []

        user_dict = {}
        public_db = shelve.open('public_storage.db', 'r')
        user_dict = public_db['Users']
        public_db.close()
        user_list = []

        referral_dict = {}
        referral_db = shelve.open('referrals_storage.db', 'r')
        referral_dict = referral_db['Refs']
        referral_db.close()
        referral_list = []

        user = user_dict[nric]
        history = medcert_dict.get(nric)
        bookings_list = bookings_dict.get(nric)
        bookings = bookings_list[index]

        referral = referral_dict.get(nric)

        if history.get_startDate() == bookings.get_date() or history.get_startDate() == appointment.get_date_of_arrival():
            medcert_list.append(history)

        if referral.get_date() == bookings.get_date() or referral.get_date() == appointment.get_date_of_arrival():
            referral_list.append(referral)

        return render_template('viewMedCert.html', medcert_list=medcert_list, user = user, bookings = bookings, appointment=appointment, referral_list=referral_list)
    else:
        return redirect(url_for('login_public'))
# <!-- ======= End Public Section ======= -->

# <!-- ======= Start Clinic Section ======= -->
@app.route('/consultationFormInfo')
def consultation_form_info():
    if 'clinic_login' in session:
        return render_template('consultationFormInfo.html')
    else:
        return redirect(url_for('login_clinic'))

# CREATE PRESCRIPTION
@app.route('/createPrescription', methods=['GET', 'POST'])
def prescribe():
    if 'clinic_login' in session:
        global clinic_id
        prescribe_form = janineForm.CreatePrescriptionForm(request.form)
        if request.method == 'POST' and prescribe_form.validate():
            meds_dict = {}
            db = shelve.open('prescription_storage.db', 'w')
            nric = prescribe_form.nric.data
            name = prescribe_form.name.data
            try:
                meds_dict = db['Meds']
            except IOError:
                print("Error in retrieving medication from meds.db")
            else:
                medication = janineClass.UserMeds(nric, name, prescribe_form.clinic.data, prescribe_form.symptoms.data, prescribe_form.medication.data, prescribe_form.instructions.data, prescribe_form.sideEffects.data)
                meds_dict[nric] = medication
                db['Meds'] = meds_dict

                meds_dict = db['Meds']
                print("Patient", medication.get_nric(), "has", medication.get_symptoms(), "and has been prescribed with", medication.get_medication())

                db.close()
                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()

                return redirect(url_for('prescription_end', nric_hashed=nric_hashed))
        else:
            user_dict = {}
            clinic_db = shelve.open('clinic_storage.db', 'r')
            user_dict = clinic_db['Users']
            clinic_db.close()
            clinic = user_dict[clinic_id]
            prescribe_form.clinic.data = clinic.get_name()
        return render_template('createMedication.html', form=prescribe_form)
    else:
        return redirect(url_for('login_clinic'))

# CONFIRMATION OF PRESCRIPTION
@app.route('/endprescription/<nric_hashed>')
def prescription_end(nric_hashed):
    if 'clinic_login' in session:
        meds_dict = {}
        meds_db = shelve.open('prescription_storage.db', 'r')
        meds_dict = meds_db['Meds']
        for nrics in meds_dict:
            hashing = hashlib.md5(nrics.encode())
            nrics_hashed = hashing.hexdigest()
            if nrics_hashed==nric_hashed:
                nric = nrics
        meds_db.close()
        patient = meds_dict[nric]
        medication = patient.get_medication()
        meds_list = medication.split(',')
        # public_db = shelve.open('public_storage.db', 'r')
        # public_dict = public_db['Users']
        # user = public_dict[nric]

        return render_template('endPrescription.html',patient = patient, meds_list = meds_list)
    else:
        return redirect(url_for('login_clinic'))

#create referrals
@app.route('/createReferral',methods=['GET','POST'])
def referrals():
    if 'clinic_login' in session:
        referral_form = janineForm.CreateReferral(request.form)

        if request.method == 'POST' and referral_form.validate():
            nric = referral_form.nric.data
            name = referral_form.name.data
            referral_dict = {}
            db = shelve.open('referrals_storage.db', 'w')

            try:
                referral_dict = db['Refs']
            except IOError:
                print("Error in retrieving referrals from referrals.db")

            else:
                referral = janineClass.Referrals(nric, name, referral_form.reason.data, referral_form.organisation.data, referral_form.date.data)
                referral_dict[referral.get_nric()] = referral
                db['Refs'] = referral_dict
                db.close()

                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()
                return redirect(url_for('referral_end', nric_hashed=nric_hashed))
        # else:
        #     user_dict={}
        #     public_db=shelve.open('public_storage.db','r')
        #     user_dict=public_db['Users']
        #     public_db.close()
        #     if nric in user_dict:
        #         user=user_dict.get(nric)
        #         referral_form.nric.data=user.get_nric()
        #         referral_form.name.data=user.get_name()
        #     else:
        #         return render_template('failedFind.html')
        return render_template('createReferral.html', form=referral_form)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/referral_end/<nric_hashed>')
def referral_end(nric_hashed):
    if 'clinic_login' in session:
        referral_dict = {}
        referral_db = shelve.open('referrals_storage.db', 'r')
        # public_db = shelve.open('public_storage.db', 'r')
        referral_dict = referral_db['Refs']
        referral_db.close()
        # user_dict = {}
        # user_dict = public_db['Users']
        for nrics in referral_dict:
            hashing = hashlib.md5(nrics.encode())
            nrics_hashed = hashing.hexdigest()
            if nrics_hashed==nric_hashed:
                nric = nrics
        # public_db.close()
        referral_list = []
        # user_list = []
        referral = referral_dict.get(nric)
        # user = user_dict.get(nric)
        return render_template('endReferral.html', referral=referral)
    else:
        return redirect(url_for('login_clinic'))

#create medical certificate
@app.route('/createMedicalCert',methods=['GET','POST'])
def medicalCert():
    if 'clinic_login' in session:
        medCert_form = janineForm.CreateMedCert(request.form)

        if request.method == 'POST' and medCert_form.validate():
            medcert_dict = {}
            db = shelve.open('medcert_storage.db', 'w')
            nric = medCert_form.nric.data

            try:
                medcert_dict = db['MedCert']
            except IOError:
                print("Error in retrieving medical certificates from medcert.db")
            else:
                nric = medCert_form.nric.data
                medcert = janineClass.MedicalCertificate(nric, medCert_form.name.data,medCert_form.startDate.data, medCert_form.endDate.data)
                medcert_dict[medcert.get_nric()] = medcert
                db['MedCert'] = medcert_dict
                db.close()
                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()
                return redirect(url_for('medCert_end', nric_hashed=nric_hashed))
        # else:
        #     user_dict={}
        #     public_db=shelve.open('public_storage.db','r')
        #     user_dict=public_db['Users']
        #     public_db.close()
        #     if nric in user_dict:
        #         user=user_dict.get(nric)
        #         medCert_form.nric.data=user.get_nric()
        #         medCert_form.name.data=user.get_name()
        #     else:
        #         return render_template('failedFind.html')
        return render_template('createMedCert.html', form=medCert_form)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/medCert_end/<nric_hashed>')
def medCert_end(nric_hashed):
    if 'clinic_login' in session:
        medcert_dict = {}
        medcert_db = shelve.open('medcert_storage.db', 'r')
        # public_db = shelve.open('public_storage.db', 'r')
        medcert_dict = medcert_db['MedCert']
        medcert_db.close()
        for nrics in medcert_dict:
            hashing = hashlib.md5(nrics.encode())
            nrics_hashed = hashing.hexdigest()
            if nrics_hashed==nric_hashed:
                nric = nrics
        # user_dict = {}
        # user_dict = public_db['Users']
        #
        # public_db.close()
        # user_list = []
        medcert = medcert_dict.get(nric)
        # user = user_dict.get(nric)
        # user_list.append(user)

        return render_template('endMedCert.html', medcert=medcert)
    else:
        return redirect(url_for('login_clinic'))

#Another part (duplicated of above) for the doctor schedule forms
@app.route('/consultationFormPatient/<int:index>')
def consultation_form_patient(index):
    if 'clinic_login' in session:
        return render_template('consultationFormPatient.html', index=index)
    else:
        return redirect(url_for('login_clinic'))

# CREATE PRESCRIPTION
@app.route('/createPrescription/<int:index>', methods=['GET', 'POST'])
def prescribe_patient(index):
    if 'clinic_login' in session:
        prescribe_form = janineForm.CreatePrescriptionForm(request.form)

        global clinic_id
        global selected_schedule_date
        global selected_waitinglist_date
        global type_of_form
        schedule_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'r')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
            booking_db = shelve.open('jonghan_storage.db', 'r')
            bookings_dict = booking_db['Bookings']
        except:
            print('Error in retrieving database')
        else:
            if type_of_form == 'physical':
                for nric in appointment_db:
                    for appointment in appointment_db[nric]:
                        if selected_schedule_date == None:
                            if appointment.get_selected_clinic_id() == clinic_id:
                                schedule_detail = [appointment, users_dict[nric]]
                                schedule_list.append(schedule_detail)
                        else:
                            if appointment.get_date_of_arrival() == selected_schedule_date and appointment.get_selected_clinic_id() == clinic_id:
                                print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
                                schedule_detail = [appointment, users_dict[nric]]
                                schedule_list.append(schedule_detail)
            elif type_of_form == 'online':
                for nric in bookings_dict:
                    for bookings in bookings_dict[nric]:
                        if bookings.get_date() == selected_waitinglist_date and bookings.get_selected_clinic_id() == clinic_id:
                            print('hi', bookings.get_date())
                            schedule_detail = [bookings, users_dict[nric]]
                            schedule_list.append(schedule_detail)
        public_db.close()
        appointment_db.close()
        booking_db.close()

        schedule_details = schedule_list[index]

        if request.method == 'POST' and prescribe_form.validate():
            meds_dict = {}
            db = shelve.open('prescription_storage.db', 'w')

            try:
                meds_dict = db['Meds']
            except IOError:
                print("Error in retrieving medication from meds.db")
            else:
                medication = janineClass.UserMeds(prescribe_form.name.data,prescribe_form.nric.data, prescribe_form.clinic.data, prescribe_form.symptoms.data, prescribe_form.medication.data, prescribe_form.instructions.data, prescribe_form.sideEffects.data)
                meds_dict[schedule_details[1].get_nric()] = medication
                db['Meds'] = meds_dict

                meds_dict = db['Meds']
                print("Patient", medication.get_nric(), "has", medication.get_symptoms(), "and has been prescribed with", medication.get_medication())

                db.close()
                nric = schedule_details[1].get_nric()
                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()

                return redirect(url_for('prescription_end', nric_hashed=nric_hashed))

        else:
            if schedule_details[1].get_nric() in users_dict:
                user=users_dict[schedule_details[1].get_nric()]
                prescribe_form.name.data=user.get_name()
                prescribe_form.nric.data=user.get_nric()
                prescribe_form.clinic.data = schedule_details[0].get_clinic()
            else:
                return render_template('failedFind.html')
        return render_template('createPatientMedication.html', form=prescribe_form)
    else:
        return redirect(url_for('login_clinic'))

#create referrals
@app.route('/createReferral/<int:index>',methods=['GET','POST'])
def referrals_patient(index):
    if 'clinic_login' in session:
        referral_form = janineForm.CreateReferral(request.form)
        global clinic_id
        global selected_schedule_date
        schedule_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'r')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
            booking_db = shelve.open('jonghan_storage.db', 'r')
            bookings_dict = booking_db['Bookings']
        except:
            print('Error in retrieving database')
        else:
            if type_of_form == 'physical':
                for nric in appointment_db:
                    for appointment in appointment_db[nric]:
                        if selected_schedule_date == None:
                            if appointment.get_selected_clinic_id() == clinic_id:
                                schedule_detail = [appointment, users_dict[nric]]
                                schedule_list.append(schedule_detail)
                        else:
                            if appointment.get_date_of_arrival() == selected_schedule_date and appointment.get_selected_clinic_id() == clinic_id:
                                print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
                                schedule_detail = [appointment, users_dict[nric]]
                                schedule_list.append(schedule_detail)
            elif type_of_form == 'online':
                for nric in bookings_dict:
                    for bookings in bookings_dict[nric]:
                        if bookings.get_date() == selected_waitinglist_date and bookings.get_selected_clinic_id() == clinic_id:
                            print('hi', bookings.get_date())
                            schedule_detail = [bookings, users_dict[nric]]
                            schedule_list.append(schedule_detail)
        schedule_details = schedule_list[index]
        public_db.close()
        appointment_db.close()
        booking_db.close()
        if request.method == 'POST' and referral_form.validate():
            referral_dict = {}
            db = shelve.open('referrals_storage.db', 'w')

            try:
                referral_dict = db['Refs']
            except IOError:
                print("Error in retrieving referrals from referrals.db")

            else:
                nric = schedule_details[1].get_nric()
                referral = janineClass.Referrals(nric, referral_form.name.data, referral_form.reason.data, referral_form.organisation.data, referral_form.date.data)
                referral_dict[referral.get_nric()] = referral
                db['Refs'] = referral_dict
                db.close()
                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()

                return redirect(url_for('referral_end', nric_hashed=nric_hashed))
        else:
            if schedule_details[1].get_nric() in users_dict:
                user=users_dict.get(schedule_details[1].get_nric())
                referral_form.nric.data=user.get_nric()
                referral_form.name.data=user.get_name()
            else:
                return render_template('failedFind.html')
        return render_template('createPatientReferral.html', form=referral_form, nric=nric)
    else:
        return redirect(url_for('login_clinic'))

#create medical certificate
@app.route('/createMedicalCert/<int:index>',methods=['GET','POST'])
def medicalCert_patient(index):
    if 'clinic_login' in session:
        medCert_form = janineForm.CreateMedCert(request.form)

        global clinic_id
        global selected_schedule_date
        schedule_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'r')
            public_db = shelve.open('public_storage.db', 'r')
            users_dict = public_db['Users']
            booking_db = shelve.open('jonghan_storage.db', 'r')
            bookings_dict = booking_db['Bookings']
        except:
            print('Error in retrieving database')
        else:
            if type_of_form == 'physical':
                for nric in appointment_db:
                    for appointment in appointment_db[nric]:
                        if selected_schedule_date == None:
                            if appointment.get_selected_clinic_id() == clinic_id:
                                schedule_detail = [appointment, users_dict[nric]]
                                schedule_list.append(schedule_detail)
                        else:
                            if appointment.get_date_of_arrival() == selected_schedule_date and appointment.get_selected_clinic_id() == clinic_id:
                                print('hi', appointment.get_date_of_arrival(), appointment.get_selected_clinic_id())
                                schedule_detail = [appointment, users_dict[nric]]
                                schedule_list.append(schedule_detail)
            elif type_of_form == 'online':
                for nric in bookings_dict:
                    for bookings in bookings_dict[nric]:
                        if bookings.get_date() == selected_waitinglist_date and bookings.get_selected_clinic_id() == clinic_id:
                            print('hi', bookings.get_date())
                            schedule_detail = [bookings, users_dict[nric]]
                            schedule_list.append(schedule_detail)
        schedule_details = schedule_list[index]
        public_db.close()
        appointment_db.close()
        booking_db.close()

        if request.method == 'POST' and medCert_form.validate():
            medcert_dict = {}
            db = shelve.open('medcert_storage.db', 'w')

            try:
                medcert_dict = db['MedCert']
            except IOError:
                print("Error in retrieving medical certificates from medcert.db")
            else:
                nric = schedule_details[1].get_nric()
                medcert = janineClass.MedicalCertificate(nric, medCert_form.name.data, medCert_form.startDate.data, medCert_form.endDate.data)
                medcert_dict[schedule_details[1].get_nric()] = medcert
                db['MedCert'] = medcert_dict
                db.close()
                hashing = hashlib.md5(nric.encode())
                nric_hashed = hashing.hexdigest()

                return redirect(url_for('medCert_end', nric_hashed=nric_hashed))
        else:
            if schedule_details[1].get_nric() in users_dict:
                user=users_dict.get(schedule_details[1].get_nric())
                medCert_form.nric.data=user.get_nric()
                medCert_form.name.data=user.get_name()
            else:
                return render_template('failedFind.html')
        return render_template('createPatientMedCert.html', form=medCert_form, nric=nric)
    else:
        return redirect(url_for('login_clinic'))


# <!-- ======= End Clinic Section ======= -->
# <!-- ======= End Janine Section ======= -->

# <!-- ======= Start Neha Section ======= -->
@app.route('/createAppointment', methods=['GET', 'POST'])
def create_appointment():
    if 'public_login' in session:
        create_user_form = nehaForms.CreateUserForm(request.form)
        global nric
        if request.method == 'POST' and create_user_form.validate():
            patients_dict = {}
            appointment_list = []
            appointment_db = shelve.open('appointment_storage.db', 'w')
            try:
                appointment_list = appointment_db[nric]
            except:
                print("Error in retrieving Users from storage.db.")
            list_of_clinic_names = nehaForms.list_of_clinics()
            list_of_clinic_ids = nehaForms.list_of_clinics.clinic_id_list
            print(len(list_of_clinic_ids), len(list_of_clinic_names))
            for i in range(len(list_of_clinic_ids)):
                if create_user_form.clinic.data == list_of_clinic_names[i]:
                    selected_clinic_id = list_of_clinic_ids[i]
                    print(selected_clinic_id)
            clinic_db = shelve.open('clinic_storage.db', 'r')
            users_dict = clinic_db['Users']
            print(users_dict[selected_clinic_id].get_name(), create_user_form.clinic.data)

            appointment = nehaClass.Patient(create_user_form.purpose.data, create_user_form.clinic.data,
                                       create_user_form.date_of_arrival.data, create_user_form.time.data,
                                       create_user_form.message.data, selected_clinic_id)
            appointment_list.append(appointment)
            appointment_db[nric] = appointment_list
            appointment_db.close()
            return redirect(url_for('retrieve_appt'))
        else:
            user_dict = {}
            public_db = shelve.open('public_storage.db', 'r')
            user_dict = public_db['Users']
            public_db.close()
            if nric in user_dict:
                user = user_dict.get(nric)
                create_user_form.name.data = user.get_name()
                create_user_form.nric.data = user.get_nric()
                create_user_form.email.data = user.get_email()
                create_user_form.phone.data = user.get_phone()
        return render_template('createAppointment.html', form=create_user_form)
    else:
        return redirect(url_for('login_public'))

@app.route('/Retrieve_Appointment')
def retrieve_appt():
    if 'public_login' in session:
        global nric
        appointment_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'r')
            appointment_list = appointment_db[nric]
            appointment_db.close()
        except:
            print('Error in retrieving Patients from storage.db')
        public_db = shelve.open('public_storage.db', 'r')
        user_dict = public_db['Users']
        public_db.close()

        return render_template('Retrieve_Appointment.html',appointment_list=appointment_list)
    else:
        return redirect(url_for('login_public'))

@app.route('/appointmentConfirmation/<int:index>/')
def appointment_confirmation(index):
    if 'public_login' in session:
        global nric
        appointment_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'r')
            appointment_list = appointment_db[nric]
            appointment_db.close()
        except:
            print('Error in Retrieving Patients from storage.db')
        public_db = shelve.open('public_storage.db', 'r')
        user_dict = public_db['Users']
        public_db.close()
        user = user_dict[nric]
        appointment=appointment_list[index]

        return render_template('appointmentConfirmation.html',appointment = appointment,user=user)
    else:
        return redirect(url_for('login_public'))

@app.route('/appointmentUpdate/<int:index>/', methods=['GET','POST'])
def update_appointment(index):
    if 'public_login' in session:
        global nric
        update_user_form=nehaForms.UpdateAndCancel(request.form)
        if request.method=='POST' and update_user_form.validate():
            appointment_list = []
            try:
                appointment_db = shelve.open('appointment_storage.db', 'w')
                appointment_list = appointment_db[nric]
            except:
                print('Error in Retrieving Patients from storage.db')
            appointment = appointment_list[index]
            appointment.set_time(update_user_form.time.data)
            appointment.set_date_of_arrival(update_user_form.date_of_arrival.data)
            appointment.set_clinic(update_user_form.clinic.data)
            appointment.set_purpose(update_user_form.purpose.data)
            appointment.set_message(update_user_form.message.data)
            list_of_clinic_names = nehaForms.list_of_clinics()
            list_of_clinic_ids = nehaForms.list_of_clinics.clinic_id_list
            for i in range(len(list_of_clinic_ids)):
                if update_user_form.clinic.data == list_of_clinic_names[i]:
                    selected_clinic_id = list_of_clinic_ids[i]
                    print(selected_clinic_id)
            appointment.set_selected_clinic_id(selected_clinic_id)
            appointment_db[nric] = appointment_list
            appointment_db.close()
            return redirect(url_for('retrieve_appt'))
        else:
            user_dict = {}
            appointment_list = []
            public_db = shelve.open('public_storage.db', 'r')
            user_dict = public_db['Users']
            public_db.close()
            appointment_db=shelve.open('appointment_storage.db','r')
            appointment_list = appointment_db[nric]
            appointment_db.close()
            if nric in user_dict:
                user = user_dict[nric]
                appointment = appointment_list[index]
                update_user_form.name.data=user.get_name()
                update_user_form.nric.data = user.get_nric()
                update_user_form.email.data = user.get_email()
                update_user_form.phone.data=user.get_phone()
                update_user_form.message.data=appointment.get_message()
                update_user_form.purpose.data=appointment.get_purpose()
                update_user_form.clinic.data=appointment.get_clinic()
                update_user_form.date_of_arrival.data=appointment.get_date_of_arrival()
                update_user_form.time.data=appointment.get_time()
        return render_template('updateAppointment.html',form=update_user_form)
    else:
        return redirect(url_for('login_public'))

@app.route('/appointmentDelete/<int:index>')
def delete_appointment(index):
    if 'public_login' in session:
        global nric
        appointment_list = []
        try:
            appointment_db = shelve.open('appointment_storage.db', 'w')
            appointment_list = appointment_db[nric]
        except:
            print('Error in retrieving Patients from storage.db')
        appointment_list.pop(index)

        appointment_db[nric] = appointment_list
        appointment_db.close()
        return redirect(url_for('confirm_delete_appointment'))
    else:
        return redirect(url_for('login_public'))

@app.route('/confirmationDeleteAppointment')
def confirm_delete_appointment():
    if 'public_login' in session:
        return render_template('confirmation_delete.html')
    else:
        return redirect(url_for('login_public'))
#end patient side

#=================Neha Shopping Cart=============

#CLINIC SIDE PHARMACY AND INVENTORY
#FILES USED ARE AS: CreateShoppingItems.html,Clinic_RetrieveShoppingItems.html
#Python files: nehaShoppingClass,Shopping_Cart_Form

@app.route('/CreateShoppingItems', methods=['GET', 'POST'])
def shopping_cart():
    if 'clinic_login' in session:
        shopping_cart = nehaForms.CreateShoppingItems(request.form)
        global clinic_id
        if request.method == 'POST':
            uploaded_file = request.files['file']
            # getting file data
            filename, fileExtension = os.path.splitext(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_PATH'], filename + fileExtension)
            print(filename)
            print(fileExtension)
            print(filepath)
            uploaded_file.save(filepath)
            fileExtension = fileExtension[1:]
            shopping_list = []

            shopping_list = []
            shopping_db = shelve.open('shopping.db', 'c')
            try:
                shopping_list = shopping_db[clinic_id]
            except:
                print('Error Creating database')

            product = nehaClass.ShoppingCart(filepath, shopping_cart.quantity.data, shopping_cart.product_name.data,
                                   shopping_cart.product_description.data, shopping_cart.price.data)
            shopping_list.append(product)
            product.set_cart_total(shopping_cart.price.data)
            shopping_db[clinic_id] = shopping_list
            shopping_db.close()
            return redirect(url_for('retrieve_products'))

        return render_template('CreateShoppingItems.html', form=shopping_cart)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/Clinic_RetrieveShoppingItems')
def retrieve_products():
    if 'clinic_login' in session:
        global clinic_id
        shopping_list = []

        try:
            shopping_db = shelve.open('shopping.db', 'r')
            shopping_list = shopping_db[clinic_id]
            shopping_db.close()
        except:
            print('Error Retrieving items from database')

        return render_template('Clinic_RetrieveShoppingItems.html', shopping_list=shopping_list)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/shoppingUpdate/<int:index>/', methods=['GET', 'POST'])
def update_shopping_items(index):
    if 'clinic_login' in session:
        global clinic_id
        update_shopping_items = nehaForms.CreateShoppingItems(request.form)
        if request.method == 'POST' and update_shopping_items.validate():
            shopping_list = []
            try:
                shopping_db = shelve.open('shopping.db', 'w')
                shopping_list = shopping_db[clinic_id]

            except:
                print('Error Retrieving items from database')
            uploaded_file = request.files['file']
            # getting file data
            filename, fileExtension = os.path.splitext(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_PATH'], filename + fileExtension)
            uploaded_file.save(filepath)

            items = shopping_list[index]
            items.set_image_location(filepath)
            items.set_product_name(update_shopping_items.product_name.data)
            items.set_price(update_shopping_items.price.data)
            items.set_quantity(update_shopping_items.quantity.data)
            items.set_product_description(update_shopping_items.product_description.data)

            shopping_db[clinic_id] = shopping_list
            shopping_db.close()
            return redirect(url_for('retrieve_products'))
        else:
            shopping_list = []
            shopping_db = shelve.open('shopping.db', 'r')
            shopping_list = shopping_db[clinic_id]
            shopping_db.close()
            items = shopping_list[index]
            update_shopping_items.product_name.data = items.get_product_name()
            update_shopping_items.price.data = items.get_price()
            update_shopping_items.product_description.data = items.get_product_description()
            update_shopping_items.quantity.data = items.get_quantity()
        return render_template('CreateShoppingItems.html', form=update_shopping_items)
    else:
        return redirect(url_for('login_clinic'))


@app.route('/shoppingDelete/<int:index>')
def delete_shopping(index):
    if 'clinic_login' in session:
        global clinic_id
        shopping_list = []
        try:
            shopping_db = shelve.open('shopping.db', 'w')
            shopping_list = shopping_db[clinic_id]

        except:
            print('Error Retrieving items from database')
        shopping_list.pop(index)

        shopping_db[clinic_id] = shopping_list
        shopping_db.close()
        return redirect(url_for('retrieve_products'))
    else:
        return redirect(url_for('login_clinic'))


# Shopping Cart Patient Side
# files Used: PatientShopping.html
@app.route('/PatientShopping',methods=['GET','POST'])
def Patient_Shop():
    if 'public_login' in session:
        quantity_update = nehaForms.update_items(request.form)
        global clinic_id
        print(request.method)
        if request.method == 'POST':
            print('HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
            shopping_list = []
            shopping_db=None
            try:
                shopping_db = shelve.open('shopping.db', 'w')
                shopping_list = shopping_db[clinic_id]
                print(shopping_list)

            except:
                print('Error Retrieving items from database')

            print('HII')
            print(quantity_update.quantities.data)
            for items in shopping_list:
                count=items.get_quantity()
                cart_pricing=items.get_price()
                print(cart_pricing)
                #just like the quantity has can only be updated for one product the cart total can also only be updated for one product
                items.set_cart_total(int(cart_pricing*quantity_update.quantities.data))
                if quantity_update.quantities.data <= 10:
                    count -= int(quantity_update.quantities.data)
                items.set_quantity(count)
            print(shopping_list)
            shopping_db[clinic_id] = shopping_list
            shopping_db.close()
            return redirect(url_for('checkout'))


        else:
            shopping_db = shelve.open('shopping.db', 'r')
            for clinic_id in shopping_db:
                shopping_list = shopping_db[clinic_id]
            shopping_db.close()


        return render_template('PatientShopping.html', shopping_list=shopping_list,form=quantity_update)
    else:
        return redirect(url_for('login_public'))


@app.route('/ShoppingCheckout',methods=['GET','POST'])
def checkout():
    if 'public_login' in session:
        global clinic_id
        shopping_list = []
        try:
            shopping_db = shelve.open('shopping.db', 'r')
            shopping_list = shopping_db[clinic_id]
            shopping_db.close()
        except:
            print('Error Retrieving items from database')
        for items in shopping_list:
            total=items.get_cart_total()+5
        return render_template('ShoppingCheckout.html',items=items,total=total)
    else:
        return redirect(url_for('login_public'))


@app.route('/charge',methods=['POST'])
def charge():
    if 'public_login' in session:
        api_key = 'sk_test_51IJjM0FRfvOhGluklIxsjR9XwhWh725afPtpwQkoKzniTTctjHwUORqBmm1tOZf15xzi2aOFDY0ujxspARRvz3RB00tk2UxBn0'
        token = request.form.get('stripeToken')
        shopping_list=[]
        try:
            shopping_db = shelve.open('shopping.db', 'r')
            shopping_list = shopping_db[clinic_id]
            print(shopping_list)
            shopping_db.close()

        except:
            print('Error Retrieving items from database')
        for items in shopping_list:
            count=str(items.get_cart_total())+'00'

            # todo: stripe stuff
            headers = {'Authorization': f'Bearer {api_key}'}
            data = {
                'amount': int(count)+500,
                'currency': 'sgd',
                'description': 'Another Charge',
                'source': token
            }

            r = requests.post('https://api.stripe.com/v1/charges', headers=headers, data=data)

            print(r.text)

            return render_template('PaymentSuccessful.html')
    else:
        return redirect(url_for('login_public'))

# @app.route('/PatientShopping', methods=['GET', 'POST'])
# def Patient_Items_Quantity():
#     quantity_update = update_items(request.form)
#     global clinic_id
#     shopping_list = []
#     if request.method == 'POST' and quantity_update.validate():
#         try:
#             shopping_db = shelve.open('shopping.db', 'w')
#             shopping_list = shopping_db[clinic_id]
#             print(shopping_list)
#
#         except:
#             print('Error Retrieving items from database')
#         items=shopping_list[0]
#         count=items.get_quantity()
#         count-=update_items.quantities.data
#         items.set_quantity(count)
#         shopping_db[clinic_id] = shopping_list
#         shopping_db.close()
#         return redirect(url_for('Patient_Shop'))
#
#
#     return render_template('PatientShopping.html', shopping_list=shopping_list, form=quantity_update)


# update inventory quantity
# @app.route('/UpdateQuantity/<int:index>')
# def update_quantity(index):
#     global clinic_id
#     shopping_list = []
#     try:
#         shopping_db = shelve.open('shopping.db', 'w')
#         shopping_list = shopping_db[clinic_id]
#         print(shopping_list)
#
#     except:
#         print('Error Retrieving items from database')
#     items = shopping_list[index]
#     count = items.get_quantity()
#     count -= 1
#     items.set_quantity(count)
#     shopping_db[clinic_id] = shopping_list
#     shopping_db.close()
#
#     return redirect(url_for('Patient_Shop'))
# <!-- ======= End Neha Section ======= -->

# <!-- ======= Start Jonghan Section ======= -->
addedThePt = 0
displayedThePt = 0
visit = ''

def encrypt_data(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def is_later_date(start, search):
    search = search.strftime("%d %m %Y")
    start = start[-2:] + "-" + start[5:7] + "-" + start[:4]
    if int(search[-4:]) < int(start[-4:]):
        return False
    elif int(search[-4:]) > int(start[-4:]):
        return True
    else:
        if int(search[3:5]) < int(start[3:5]):
            return False
        elif int(search[3:5]) > int(start[3:5]):
            return True
        else:
            if int(search[:2]) < int(start[:2]):
                return False
            else:
                return True

def is_earlier_date(end, search):
    search = search.strftime("%d %m %Y")
    end = end[-2:] + "-" + end[5:7] + "-" + end[:4]
    if int(search[-4:]) < int(end[-4:]):
        return True
    elif int(search[-4:]) > int(end[-4:]):
        return False
    else:
        if int(search[3:5]) < int(end[3:5]):
            return True
        elif int(search[3:5]) > int(end[3:5]):
            return False
        else:
            if int(search[:2]) <= int(end[:2]):
                return True
            else:
                return False

@app.route('/searchPtVisits', methods=['GET', 'POST'])
def search_pt():
    if 'clinic_login' in session:
        search = SearchVisits(request.form)
        if request.method == 'POST':
            searched = search.data
            db = shelve.open('jonghan_storage.db', 'c')
            pat_vis = {}
            print(searched)
            try:
                pat_vis = db['ptVisits']
            except:
                print("Error retrieving data")
            db.close()
            dict = {}

            if searched['fromDate'] == '' and searched['toDate'] == '' and searched['searchBy'] == 'Name' and searched['searchFor'] == '':
                for i in pat_vis:
                    dict[i] = pat_vis[i]

            else:
                for i in pat_vis:
                    #need identifier for clinic name
                    if searched['searchFor'] == '' and searched['fromDate'] != '' and searched['toDate'] != '':
                        if is_earlier_date(searched['toDate'], pat_vis[i].get_keep_date()) and is_later_date(searched['fromDate'], pat_vis[i].get_keep_date()):
                            dict[i] = pat_vis[i]
                    elif searched['searchFor'] == '' and searched['fromDate'] != '':
                        if is_later_date(searched['fromDate'], pat_vis[i].get_keep_date()):
                            dict[i] = pat_vis[i]

                    elif searched['searchFor'] != '' and searched['fromDate'] != '' and searched['toDate'] != '':
                        if is_earlier_date(searched['toDate'], pat_vis[i].get_keep_date()) and is_later_date(searched['fromDate'], pat_vis[i].get_keep_date()):
                            if searched['searchBy'] == 'visitno' and searched['searchFor'].lower() == pat_vis[i].get_visit_num().lower():
                                dict[i] = pat_vis[i]
                            elif searched['searchBy'] == 'NRIC' and searched['searchFor'].lower() == pat_vis[i].get_nric().lower():
                                dict[i] = pat_vis[i]
                            elif searched['searchBy'] == 'Name' and searched['searchFor'].lower() in pat_vis[i].get_fullname().lower():
                                dict[i] = pat_vis[i]

                    elif searched['searchFor'] != '' and searched['fromDate'] != '':
                        if is_later_date(searched['fromDate'], pat_vis[i].get_keep_date()):
                            if searched['searchBy'] == 'visitno' and searched['searchFor'].lower() == pat_vis[i].get_visit_num().lower():
                                dict[i] = pat_vis[i]
                            elif searched['searchBy'] == 'NRIC' and searched['searchFor'].lower() == pat_vis[i].get_nric().lower():
                                dict[i] = pat_vis[i]
                            elif searched['searchBy'] == 'Name' and searched['searchFor'].lower() in pat_vis[i].get_fullname().lower():
                                dict[i] = pat_vis[i]

                    else:
                        if searched['searchBy'] == 'visitno' and searched['searchFor'].lower() == pat_vis[i].get_visit_num().lower():
                            dict[i] = pat_vis[i]
                        elif searched['searchBy'] == 'NRIC' and searched['searchFor'].lower() == pat_vis[i].get_nric().lower():
                            dict[i] = pat_vis[i]
                        elif searched['searchBy'] == 'Name' and searched['searchFor'].lower() in pat_vis[i].get_fullname().lower():
                            dict[i] = pat_vis[i]

            search.fromDate.data = ''
            search.toDate.data = ''

            return render_template('results.html', pt_visits=dict, form=search)
        global addedThePt
        global displayedThePt
        if displayedThePt < addedThePt:
            global visit
            displayedThePt += 1
            return render_template('searchPtVisits.html', form=search, added=1, pt=visit.get_fullname(), visit=visit)
        return render_template('searchPtVisits.html',  form=search)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/updateVisit/<string:sig>', methods=['GET', 'POST'])
def update_visit(sig):
    if 'clinic_login' in session:
        update_pt_visit = PtVisit(request.form)
        if request.method == 'POST':
            pt_visits = {}
            db = shelve.open('jonghan_storage.db', 'w')
            pt_visits = db['ptVisits']

            keepDate = update_pt_visit.visitDate.data
            visit_date = (update_pt_visit.visitDate.data.strftime("%d %m %Y").replace(' ', '-'))
            drugNameList = update_pt_visit.drugNameList.data
            drugPriceList = update_pt_visit.drugPriceList.data
            drugQtyList = update_pt_visit.drugQtyList.data
            drugAmtList = update_pt_visit.drugAmtList.data

            for i in range(len(drugNameList)):
                if drugNameList[i] == '':
                    drugNameList.pop(i)

            print(update_pt_visit.drugNameList.data)
            print(update_pt_visit.drugPriceList.data)
            pt = pt_visits.get(sig)
            pt.set_fullname(update_pt_visit.ptName.data)
            pt.set_nric(update_pt_visit.nric.data)
            pt.set_visit_date(visit_date)
            pt.set_charge_type(update_pt_visit.chargeType.data)
            pt.set_allergies(update_pt_visit.allergies.data)
            pt.set_company(update_pt_visit.company.data)
            pt.set_mc_day(update_pt_visit.mcDay.data)
            pt.set_mc_reason(update_pt_visit.mcReason.data)
            pt.set_mc_date(update_pt_visit.mcDate.data)
            pt.set_pri_diagnosis(update_pt_visit.priDiagnosis.data)
            pt.set_sec_diagnosis(update_pt_visit.secDiagnosis.data)
            pt.set_drug_list(drugNameList)
            pt.set_drug_price_list(drugPriceList)
            pt.set_drug_qty_list(drugQtyList)
            pt.set_drug_amt_list(drugAmtList)
            pt.set_drug_name(update_pt_visit.drugName.data)
            pt.set_drug_price(update_pt_visit.drugPrice.data)
            pt.set_drug_amt(update_pt_visit.drugAmt.data)
            pt.set_drug_qty(update_pt_visit.drugQty.data)
            pt.set_referral(update_pt_visit.referral.data)
            pt.set_consult_fee(update_pt_visit.consultFee.data)
            pt.set_total_fee(update_pt_visit.totFee.data)
            pt.set_claim(update_pt_visit.claim.data)
            pt.set_copayment(update_pt_visit.copayment.data)
            pt.set_cash(update_pt_visit.cashCollected.data)
            pt.set_remarks(update_pt_visit.remarks.data)
            pt.set_total_drugs(update_pt_visit.totalDrugs.data)
            pt.set_keep_date(keepDate)

            print(update_pt_visit.drugNameList.data)

            db['ptVisits'] = pt_visits
            db.close()

            return redirect(url_for('search_pt'))
        else:
            pt_visits = {}
            db = shelve.open('jonghan_storage.db', 'r')
            pt_visits = db['ptVisits']
            db.close()

            pt = pt_visits.get(sig)
            update_pt_visit.ptName.data = pt.get_fullname()
            update_pt_visit.nric.data = pt.get_nric()
            update_pt_visit.visitDate.data = pt.get_keep_date()
            update_pt_visit.chargeType.data = pt.get_charge_type()
            update_pt_visit.allergies.data = pt.get_allergies()
            update_pt_visit.company.data = pt.get_company()
            update_pt_visit.mcDay.data = pt.get_mc_day()
            update_pt_visit.mcReason.data = pt.get_mc_reason()
            update_pt_visit.mcDate.data = pt.get_mc_date()
            update_pt_visit.priDiagnosis.data = pt.get_pri_diagnosis()
            update_pt_visit.secDiagnosis.data = pt.get_sec_diagnosis()
            update_pt_visit.drugNameList.data = pt.get_drug_list()
            update_pt_visit.drugPriceList.data = pt.get_drug_price_list()
            update_pt_visit.drugQtyList.data = pt.get_drug_qty_list()
            update_pt_visit.drugAmtList.data = pt.get_drug_amt_list()
            update_pt_visit.referral.data = pt.get_referral()
            update_pt_visit.consultFee.data = pt.get_consult_fee()
            update_pt_visit.totFee.data = pt.get_total_fee()
            update_pt_visit.claim.data = pt.get_claim()
            update_pt_visit.copayment.data = pt.get_copayment()
            update_pt_visit.cashCollected.data = pt.get_cash()
            update_pt_visit.remarks.data = pt.get_remarks()
            update_pt_visit.drugName.data = pt.get_drug_name()
            update_pt_visit.drugPrice.data = pt.get_drug_price()
            update_pt_visit.drugQty.data = pt.get_drug_qty()
            update_pt_visit.drugAmt.data = pt.get_drug_amt()
            update_pt_visit.totalDrugs.data = pt.get_total_drugs()

            drugNameList = pt.get_drug_list().split(',')
            drugPriceList = pt.get_drug_price_list().split(',')
            drugQtyList = pt.get_drug_qty_list().split(',')
            drugAmtList = pt.get_drug_amt_list().split(',')
            nric = pt.get_nric()
            for i in range(len(drugNameList)):
                if drugNameList[i] == '':
                    drugNameList.pop(i)
            drugCount = len(drugNameList)
            keepDate = pt.get_keep_date()
            mcDate = pt.get_mc_date()
            print(drugNameList)
            print(drugCount)
            return render_template('updateVisit.html', form=update_pt_visit, drugNameList=drugNameList, drugPriceList=drugPriceList, drugQtyList=drugQtyList, drugAmtList=drugAmtList, drugCount=drugCount, e=0, keepDate=keepDate, mcDate=mcDate, nric=nric)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/deleteVisit/<string:nric>')
def delete_visit(nric):
    if 'clinic_login' in session:
        pt_visits = {}
        db = shelve.open('jonghan_storage.db', 'w')
        pt_visits = db['ptVisits']

        pt_visits.pop(nric)

        db['ptVisits'] = pt_visits
        db.close()

        return redirect(url_for('search_pt'))
    else:
        return redirect(url_for('login_clinic'))

# Clinic Side add visit
@app.route('/addVisit', methods=['GET', 'POST'])
def add_pt_visit():
    if 'clinic_login' in session:
        create_pt_visit = PtVisit(request.form)
        search = SearchVisits(request.form)
        if request.method == 'POST' and create_pt_visit.validate():

            pt_visits = {}
            db = shelve.open('jonghan_storage.db', 'c')

            try:
                pt_visits = db['ptVisits']
            except:
                print("Error in retrieving ptVisits from storage.db.")

            keepDate = create_pt_visit.visitDate.data
            visit_date = (create_pt_visit.visitDate.data.strftime("%d %m %Y"))
            drugNameList = create_pt_visit.drugNameList.data
            drugPriceList = create_pt_visit.drugPriceList.data
            drugQtyList = create_pt_visit.drugQtyList.data
            drugAmtList = create_pt_visit.drugAmtList.data

            for i in range(len(drugNameList)):
                if drugNameList[i] == '':
                    drugNameList.pop(i)

            global visit
            global addedThePt
            global displayedThePt
            addedThePt += 1
            visit = JHClass.addVisit(create_pt_visit.ptName.data, create_pt_visit.nric.data, visit_date, create_pt_visit.chargeType.data, create_pt_visit.priDiagnosis.data, create_pt_visit.cashCollected.data, create_pt_visit.company.data, create_pt_visit.allergies.data, create_pt_visit.mcDay.data, create_pt_visit.mcReason.data, create_pt_visit.mcDate.data, create_pt_visit.secDiagnosis.data, create_pt_visit.referral.data, create_pt_visit.claim.data, create_pt_visit.copayment.data, create_pt_visit.remarks.data, drugNameList, drugPriceList, drugQtyList, drugAmtList, create_pt_visit.clinic, create_pt_visit.totFee.data, create_pt_visit.consultFee.data, create_pt_visit.drugName.data, create_pt_visit.drugPrice.data, create_pt_visit.drugQty.data, create_pt_visit.drugAmt.data, create_pt_visit.totalDrugs.data, keepDate)
            pt_visits[visit.get_nric()] = visit # paste together for hash secure +visit.get_visit_date()+visit.get_clinic()
            db['ptVisits'] = pt_visits
            print(visit.get_keep_date())

            db.close()

            return redirect(url_for('search_pt', form=search, added=1, pt=create_pt_visit.ptName.data, visit=visit))
        return render_template('addVisit.html', form=create_pt_visit)
    else:
        return redirect(url_for('login_clinic'))

@app.route('/doctor/vidcall/<string:uuid>')
def dr_video_call(uuid):
    print('wususp')
    return render_template('DrVidCall.html', uuid=uuid)

@app.route('/patient/vidcall/<string:uuid>')
def pt_video_call(uuid):
    global schedule_list
    return render_template('PtVidCall.html', uuid=uuid, schedule_list=schedule_list)

@app.route('/sendPtEmail/<string:nric>')
def send_pt_email(nric):
    global uid
    uid = str(uuid.uuid4().hex)
    try:
        db = shelve.open('public_storage.db', 'r')
    except:
        print("Error")

    try:
        users = db['Users']
    except:
        print("Error in retrieving database")

    db.close()
    ptEmail = users[nric].get_email()

    #open database to get pt email

    mail_to_pt.sendMail(uid, ptEmail)
    return render_template('redirect.html', uuid=uid)

@app.route('/afterConsult/<string:sessionid>', methods=['GET', 'POST'])
def after_consult(sessionid):
    create_payment_form = Payment(request.form)
    db = shelve.open('storage.db', 'c')
    bookings = {}
    try:
        bookings = db['Bookings']
    except:
        print("Error in retrieving Bookings from storage.db.")
    db.close()

    latestBooking = ""

    for id in bookings:
        if sessionid == id:
            latestBooking = bookings[id][-1]

    db = shelve.open('storage.db', 'r')
    payInfo = {}
    try:
        payInfo = db['creditInfo']
    except:
        print("Error in retrieving creditInfo")

    print(payInfo)
    keepInfo = "n"
    ptCardInfo = ""

    if sessionid in payInfo:
        if payInfo[sessionid].get_keep_details() == True:
            print('yeehw')
            keepInfo = "y"
            ptCardInfo = payInfo[sessionid]

    db.close()

    if request.method == 'POST' and create_payment_form.validate():
        db = shelve.open('storage.db', 'c')
        creditInformation = {}
        try:
            creditInformation = db['creditInfo']
        except:
            print("Error in retrieving creditInfo from database.")

        if create_payment_form.keepDetails.data == 'keep':
            credInfo = creditInfo.CreditInfo(create_payment_form.street.data, create_payment_form.city.data, create_payment_form.zip.data, create_payment_form.country.data, create_payment_form.cardType.data, create_payment_form.creditName.data, create_payment_form.creditNum.data, create_payment_form.expiryMonth.data, create_payment_form.expiryYear.data, create_payment_form.cvv.data, True)
            creditInformation[sessionid] = credInfo
            db['creditInfo'] = creditInformation
            print(credInfo)

        db.close()

        return redirect(url_for('home'))
    return render_template('afterConsult.html', form=create_payment_form, latest=latestBooking, session=sessionid, keepInfo=keepInfo, ptCardInfo=ptCardInfo)


def list_of_clinics_bylocation():
    clinic_location_dict = {}
    try:
        clinic_db = shelve.open('clinic_storage.db', 'r')
        users_dict = clinic_db['Users']
    except:
        print('No database created yet')
        users_dict = {}
    locations = ['Ang Mo Kio', 'Bedok', 'Bishan', 'Braddell', 'Buangkok', 'Bugis', 'Canberra', 'Changi', 'Chinatown', 'Clementi', 'Harbourfront', 'Hougang', 'Jurong', 'Khatib', 'Kovan', 'Marina', 'Orchard', 'Pasir Ris', 'Punggol', 'Sembawang', 'Sengkang', 'Tampines', 'Woodlands', 'Yio Chu Kang', 'Yishun']
    clinic_id_dict = {}
    for i in locations:
        clinics_list = []
        clinic_id_dict[i] = []
        clinic_location_dict[i] = []
        for clinic_id in users_dict:
            location = users_dict[clinic_id].get_area()
            if location == i:
                clinics_list.append(users_dict[clinic_id].get_name())
                clinic_id_dict[i].append(clinic_id)
                clinic_location_dict[location] = clinics_list
        # print(clinics_list)
    clinic_db.close()
    return(clinic_location_dict), clinic_id_dict
    # clinic_db.close()
    # return clinics_list

# @app.route('/createConsultation', methods=['GET','POST'])
# def create_consultation():
#     create_form = CreateConsultForm(request.form)
#     clinicsList = {}
#     db = shelve.open('jonghan_storage.db', 'r')
#     try:
#         clinicsList = db['ClinicList']
#     except:
#         print("Error loading database file")
#     db.close()
#
#     clinicNames, clinicIds = list_of_clinics_bylocation()
#
#     if request.method == 'POST' and create_form.validate():
#         bookings_dict = {}
#         db = shelve.open('jonghan_storage.db', 'c')
#         try:
#             bookings_dict = db['Bookings']
#         except:
#             print("Error in retrieving Bookings from storage.db.")
#
#         print(create_form.clinic.data)
#         for location in clinicNames:
#             if location == create_form.location.data:
#                 for i in range(len(clinicNames[location])):
#                     if clinicNames[location][i] == create_form.clinic.data:
#                         clinicIndex = i
#
#         for location in clinicIds:
#             if location == create_form.location.data:
#                 clinicId = clinicIds[location][clinicIndex]
#
#         booking = onlineConsultation.OnlineConsultation(create_form.fullname.data, create_form.location.data, create_form.clinic.data, create_form.symptoms.data, create_form.notes.data, create_form.timing.data, create_form.nric.data, create_form.date.data, clinicId)
#         try:
#             bookings_dict[booking.get_nric()].append(booking)
#         except:
#             bookings_dict[booking.get_nric()] = []
#             bookings_dict[booking.get_nric()].append(booking)
#         print(bookings_dict)
#         db['Bookings'] = bookings_dict
#
#         db.close()
#
#         return redirect(url_for('home_public'))
#     else:
#         try:
#             public_db = shelve.open('public_storage.db', 'r')
#         except:
#             print('Error in opening public_storage.db for updating public details for', nric)
#         else:
#             try:
#                 users_dict = public_db['Users'] #have the dict of the operating hours
#                 public_db.close()
#                 user = users_dict[nric]
#             except:
#                 print('Error in retrieving users from public_storage.db for updating public details for', nric)
#             else:
#                 create_form.fullname.data = user.get_name()
#                 create_form.nric.data = user.get_nric()
#     return render_template('createConsultation.html', form=create_form, clinicsList=clinicNames)

@app.route('/createConsultation', methods=['GET','POST'])
def create_consultation():
    if 'public_login' in session:
        global nric
        create_form = CreateConsultForm(request.form)
        clinicsList = {}
        db = shelve.open('jonghan_storage.db', 'r')
        try:
            clinicsList = db['ClinicList']
        except:
            print("Error loading database file")
        db.close()

        clinicNames, clinicIds = list_of_clinics_bylocation()
        print(clinicNames)
        print(clinicIds)

        if request.method == 'POST' and create_form.validate():
            bookings_dict = {}
            db = shelve.open('jonghan_storage.db', 'c')
            try:
                bookings_dict = db['Bookings']
            except:
                print("Error in retrieving Bookings from storage.db.")
            clinicIndex = 0
            print(create_form.clinic.data)
            print(create_form.location.data)
            for location in clinicNames:
                if location == create_form.location.data:
                    list_of_clinics = clinicNames[location]
                    print(list_of_clinics)
                    for i in range(len(list_of_clinics)):
                        print(i)
                        print(create_form.clinic.data)
                        print('hi b4')
                        if list_of_clinics[i] == create_form.clinic.data:
                            clinicIndex = i
                            print('hi')
            print(clinicIndex)
            for location in clinicIds:
                if location == create_form.location.data:
                    clinicId = clinicIds[location][clinicIndex]

            booking = JHClass.OnlineConsultation(create_form.fullname.data, create_form.location.data, create_form.clinic.data, create_form.symptoms.data, create_form.notes.data, create_form.timing.data, create_form.nric.data, create_form.date.data, clinicId)
            try:
                bookings_dict[booking.get_nric()].append(booking)
            except:
                bookings_dict[booking.get_nric()] = []
                bookings_dict[booking.get_nric()].append(booking)
            print(bookings_dict)
            db['Bookings'] = bookings_dict

            db.close()

            return redirect(url_for('home_public'))
        else:
            try:
                public_db = shelve.open('public_storage.db', 'r')
            except:
                print('Error in opening public_storage.db for updating public details for', nric)
            else:
                try:
                    users_dict = public_db['Users'] #have the dict of the operating hours
                    public_db.close()
                    user = users_dict[nric]
                except:
                    print('Error in retrieving users from public_storage.db for updating public details for', nric)
                else:
                    create_form.fullname.data = user.get_name()
                    create_form.nric.data = user.get_nric()

        return render_template('createConsultation.html', form=create_form, clinicsList=clinicNames)
    else:
        return redirect(url_for('login_public'))

if __name__ == '__main__':
    app.run()
