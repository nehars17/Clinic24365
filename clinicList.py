import shelve

class clinicList:
    def __init__(self, location, clinic):
        self.__location = location
        self.__clinic = clinic

    def get_location(self):
        return self.__location

    def get_clinic(self):
        return self.__clinic

    def set_location(self, location):
        self.__location = location

    def set_clinic(self, clinic):
        self.__clinic = clinic


def checkandenter(clinic):
    global clinics
    if clinic.get_location() not in clinics:
        clinics[clinic.get_location()] = [clinic.get_clinic()]
    else:
        for i in clinics:
            for a in clinics[i]:
                if clinic.get_clinic() == a:
                    return
            if clinic.get_location() == i:
                clinics[i].append(clinic.get_clinic())

if __name__ == "__main__":
    clinics = {}
    db = shelve.open('storage.db', 'c')

    try:
        clinics = db["ClinicList"]
    except:
        print("Error locating file")

    clinic = clinicList("AMK", "Lim Clinic")
    checkandenter(clinic)

    clinic = clinicList("AMK", "Fast Clinic")
    checkandenter(clinic)

    clinic = clinicList("Bedok", "ABC Clinic")
    checkandenter(clinic)

    clinic = clinicList("Bishan", "JD Clinic")
    checkandenter(clinic)

    db['ClinicList'] = clinics
    db.close()

    db = shelve.open('storage.db', 'r')
    clinicsListed = db['ClinicList']
    db.close()

    print(clinicsListed)
