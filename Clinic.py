from User import ClinicUser

class OperatingHour:
    def __init__(self, day, open, close):
        self.__day = day
        self.__open = open
        self.__close = close
        self.set_open(open)
        self.set_close(close)
        # self.__break_start = break_start
        # self.__break_end = break_end

    def set_day(self, day):
        self.__day = day
    def get_day(self):
        return self.__day

    def set_open(self, open):
        self.__open = open
    def get_open(self):
        return self.__open

    def set_close(self, close):
        self.__close = close
    def get_close(self):
        return self.__close

    # def set_break_start(self, bstart):
    #     self.__break_start = bstart
    # def get_break_start(self):
    #     return self.__break_start
    #
    # def set_break_end(self, bend):
    #     self.__break_end = bend
    # def get_break_end(self):
    #     return self.__break_end

class OffDay:
    # count_id = 0
    def __init__(self, start, end, reason):
        # OffDay.count_id +=1
        # self.__id = OffDay.count_id
        self.__start = start
        self.__end = end
        self.__reason = reason

    def set_id(self, id):
        self.__id = id
    def get_id(self):
        return self.__id

    def set_start(self, start):
        self.__start = start
    def get_start(self):
        return self.__start

    def set_end(self, end):
        self.__end = end
    def get_end(self):
        return self.__end

    def set_reason(self, reason):
        self.__reason = reason
    def get_reason(self):
        return self.__reason
