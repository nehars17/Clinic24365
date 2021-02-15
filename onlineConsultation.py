import shelve

class OnlineConsultation:
    queue_count = 0

    def __init__(self, fullname, location, clinic, symptoms, notes, timing, nric, date):
        self.__user_id = ""
        self.__fullname = fullname
        self.__location = location
        self.__clinic = clinic
        self.__symptoms = symptoms
        self.__notes = notes
        self.__timing = timing
        self.__nric = nric
        self.__date = date
        self.__queue_num = OnlineConsultation.queue_count
        self.__has_credit = False
        self.__has_booked = False

    def get_user_id(self):
        return self.__user_id

    def get_fullname(self):
        return self.__fullname

    def get_location(self):
        return self.__location

    def get_clinic(self):
        return self.__clinic

    def get_symptoms(self):
        return self.__symptoms

    def get_notes(self):
        return self.__notes

    def get_timing(self):
        return self.__timing

    def get_date(self):
        return self.__date

    def get_queue_num(self):
        return self.__queue_num

    def get_has_credit(self):
        return self.__has_credit

    def get_has_booked(self):
        return self.__has_booked

    def get_nric(self):
        return self.__nric


    # Setter methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def set_location(self, location):
        self.__location = location

    def set_clinic(self, clinic):
        self.__clinic = clinic

    def set_symptoms(self, symptoms):
        self.__symptoms = symptoms

    def set_notes(self, notes):
        self.__notes = notes

    def set_timing(self, timing):
        self.__timing = timing

    def set_date(self, date):
        self.__date = date

    def set_queue_num(self, queue_num):
        self.__queue_num = queue_num

    def set_has_credit(self, has_credit):
        self.__has_credit = has_credit

    def set_has_booked(self, has_booked):
        self.__has_booked = has_booked

    def set_nric(self, nric):
        self.__nric = nric

if __name__ == "__main__":
    db = shelve.open('storage.db', 'r')
    bookings = db["Bookings"]
    print(bookings["T1234567E"].get_date())
