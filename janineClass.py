from User import *

class PatientCondition:
    def __init__(self, type, mca, descriptions):
        self.__type = type
        self.__mca = mca
        self.__descriptions = descriptions

    def set_type(self, type):
        self.__type = type
    def get_type(self):
        return self.__type

    def set_mca(self, mca):
        self.__mca = mca
    def get_mca(self):
        return self.__mca

    def set_descriptions(self, descriptions):
        self.__descriptions = descriptions
    def get_descriptions(self):
        return self.__descriptions

class Referrals():
    def __init__(self, nric, name, reason, organisation, date):
        self.__nric = nric
        self.__name = name
        self.__reason = reason
        self.__organisation = organisation
        self.__date = date

    def set_reason(self, reason):
        self.__reason = reason

    def get_reason(self):
        return self.__reason

    def set_organisation(self, organisation):
        self.__organisation = organisation

    def get_organisation(self):
        return self.__organisation

    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name

    def set_nric(self,nric):
        self.__nric=nric

    def get_nric(self):
        return self.__nric

    def set_date(self, date):
        self.__date = date

    def get_date(self):
        return self.__date

class MedicalCertificate():
    def __init__(self, nric, name, startDate, endDate):
        self.__nric = nric
        self.__name = name
        self.__startDate = startDate
        self.__endDate = endDate

    def set_startDate(self, startDate):
        self.__startDate = startDate

    def get_startDate(self):
        return self.__startDate

    def set_endDate(self, endDate):
        self.__endDate = endDate

    def get_endDate(self):
        return self.__endDate

    def set_nric(self,nric):
        self.__nric=nric

    def get_nric(self):
        return self.__nric

    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name


class UserMeds:
    count_id = 0
    def __init__(self, nric, name, clinic, symptoms, medication, instructions, sideEffects):
        UserMeds.count_id += 1
        self.__nric = nric
        self.__name = name
        self.__clinic = clinic
        self.__symptoms = symptoms
        self.__medication = medication
        self.__instructions = instructions
        self.__sideEffects = sideEffects

    def set_nric(self, nric):
        self.__nric = nric

    def get_nric(self):
        return self.__nric

    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name

    def set_clinic(self, clinic):
        self.__clinic = clinic

    def get_clinic(self):
        return self.__clinic

    def set_symptoms(self, symptoms):
        self.__symptoms = symptoms

    def get_symptoms(self):
        return self.__symptoms

    def set_medication(self, medication):
        self.__medication = medication

    def get_medication(self):
        return self.__medication

    def set_instructions(self, instructions):
        self.__instructions = instructions

    def get_instructions(self):
        return self.__instructions

    def set_sideEffects(self, sideEffects):
        self.__sideEffects = sideEffects

    def get_sideEffects(self):
        return self.__sideEffects
