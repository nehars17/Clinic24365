import random, string, hashlib


class PublicUser:
    def __init__(self, name, nric, birthdate, email, phone, area, postal_code, unit, gender, password):
        self.__name = name
        self.__nric = nric
        self.__birthdate = birthdate
        self.__email = email
        self.__phone = phone
        self.__area = area
        self.__postal_code = postal_code
        self.__unit = unit
        self.__gender = gender
        self.__password = password
        self.__validated = False
        # self.set_password(password, cfm_password)
        # self.set_nric(nric)
        # self.set_phone(phone)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_nric(self, nric):
        if nric[0].isalpha and nric[-1].isalpha and nric[1:-1].isnumeric:
            self.__nric = nric.upper()
        else:
            self.__nric = 'Invalid'

    def get_nric(self):
        return self.__nric

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def get_birthdate(self):
        return self.__birthdate

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_phone(self, phone):
        self.__phone = phone

    def get_phone(self):
        return self.__phone

    def set_area(self, area):
        self.__area = area

    def get_area(self):
        return self.__area

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def get_postal_code(self):
        return self.__postal_code

    def set_unit(self, unit):
        self.__unit = unit

    def get_unit(self):
        return self.__unit

    def set_gender(self, gender):
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def set_validated(self, validated):
        self.__validated = validated

    def get_validated(self):
        return self.__validated

    # def set_cfm_password(self, cfm_password):
    #     self.__cfm_password = cfm_password
    # def get_cfm_password(self):
    #     return self.__cfm_password


class ClinicUser:
    def __init__(self, name, email, phone, area, postal_code, unit, password, id_list):
        self.__name = name
        self.__area = area
        self.__postal_code = postal_code
        self.__unit = unit
        self.__email = email
        self.__phone = phone
        self.__password = password
        self.__clinic_id = ''
        self.__validated = False
        # self.set_password(password, cfm_password)
        # self.set_phone(phone)
        self.set_clinic_id(id_list)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_area(self, area):
        self.__area = area

    def get_area(self):
        return self.__area

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def get_postal_code(self):
        return self.__postal_code

    def set_unit(self, unit):
        self.__unit = unit

    def get_unit(self):
        return self.__unit

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_phone(self, phone):
        self.__phone = phone
        # if phone[0] == '8' or phone[0] == '9' or phone == '6':
        #     self.__phone = phone
        # else:
        #     self.__phone = 'Invalid'

    def get_phone(self):
        return self.__phone

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    # def set_cfm_password(self, cfm_password):
    #     self.__cfm_password = cfm_password
    # def get_cfm_password(self):
    #     return self.__cfm_password

    def set_clinic_id(self, id_list):
        digits = string.digits
        letters = string.ascii_letters
        id = ''
        while len(id) != 6:
            for i in range(1):
                id += random.choice(letters)
            for i in range(1):
                id += random.choice(digits)
        if id in id_list:
            self.set_clinic_id()
        else:
            self.__clinic_id = id

    def get_clinic_id(self):
        return self.__clinic_id

    def set_validated(self, validated):
        self.__validated = validated

    def get_validated(self):
        return self.__validated


# class OTP:
#     def __init__(self):
#         self.__otp = ''
#         self.set_otp()
#
#     def set_otp(self):
#         otp = ''
#         digits = string.digits
#         while len(otp) != 6:
#             otp += digits
#         self.__otp = otp
#     def get_otp(self):
#         return self.__otp

import smtplib
from email.message import EmailMessage

def send_otp_email(email, otp):
    message = EmailMessage()
    message["Subject"] = "Clinic 24/365 - One Time Pin"
    message["From"] = "web.clinic.24.365@gmail.com"
    message["To"] = email

    message.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1>CLINIC 24/365</h1>
            <br>
            <p>This is the One Time Pin to verify your account.
            <br>
            <b> {otp} </b>
            </p>

            <p>This is an automated message. Do not reply.</p>
        </body>
    </html>
    """.format(otp=otp), subtype="html")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, 'user', timeout=120) as smtp:

        smtp.login('web.clinic.24.365@gmail.com', 'Abcd1234!')
        smtp.send_message(message)

class PublicOTP:
    def __init__(self, nric, email):
        self.__nric = nric
        self.__email = email
        self.__otp = ''
        # self.set_otp()

    def set_nric(self, nric):
        self.__nric = nric

    def get_nric(self):
        return self.__nric

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_otp(self):
        otp = ''
        digits = string.digits
        while len(otp) != 6:
            otp += random.choice(digits)
        self.send_email(self.get_email(), otp)
        hashing = hashlib.md5(otp.encode())
        otp_hashed = hashing.hexdigest()
        self.__otp = otp_hashed

    def get_otp(self):
        return self.__otp

    def send_email(self, email, otp):
        send_otp_email(email, otp)

    # def set_unhashed_otp(self, otp):
    #     self.__unhashed_otp = otp
    #
    # def get_unhashed_otp(self):
    #     return self.__unhashed_otp


class ClinicOTP:
    def __init__(self, clinic_id, email):
        self.__clinic_id = clinic_id
        self.__email = email
        self.__otp = ''
        # self.__unhashed_otp = ''
        # self.set_otp()

    def set_clinic_id(self, clinic_id):
        self.__clinic_id = clinic_id

    def get_clinic_id(self):
        return self.__clinic_id

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_otp(self):
        otp = ''
        digits = string.digits
        while len(otp) != 6:
            otp += random.choice(digits)
        self.send_email(self.get_email(), otp)
        hashing = hashlib.md5(otp.encode())
        otp_hashed = hashing.hexdigest()
        self.__otp = otp_hashed

    def get_otp(self):
        return self.__otp

    def send_email(self, email, otp):
        send_otp_email(email, otp)

    # def set_unhashed_otp(self, otp):
    #     self.__unhashed_otp = otp
    #
    # def get_unhashed_otp(self):
    #     return self.__unhashed_otp


if __name__ == '__main__':
    # name = input('Name: ')
    # nric = input('Nric: ')
    # address = input('address: ')
    # email = input('email: ')
    # phone = input('phone: ')
    # gender = input('gender: ')
    # password = input('password: ')
    # cfm_password = input('confirm password: ')
    # p = PublicUser(name, nric, email, phone, gender, password, cfm_password)
    # c = ClinicUser(name, address, email, phone, password, cfm_password)
    # print(p.get_password(), p.get_nric(), c.get_clinic_id(), p.get_phone())
    clinic_id = input('Clinic ID: ')
    print('1')
    cotp = ClinicOTP(clinic_id)
    print('2')
    print(cotp.get_otp())
