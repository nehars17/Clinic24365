class Patient:
    nric = ''
    count_id=0
    def __init__(self,purpose,clinic,date_of_arrival,time,message, selected_clinic_id):
        Patient.nric = ''
        Patient.count_id+=1
        self.__user_id=Patient.count_id
        self.__nric = Patient.nric
        self.__purpose = purpose
        self.__date_of_arrival=date_of_arrival
        self.__time=time
        self.__message=message
        self.__clinic=clinic
        self.__selected_clinic_id = selected_clinic_id

    def get_user_id(self):
        return self.__user_id
    def get_purpose(self):
        return self.__purpose
    def get_nric(self):
        return self.__nric

    def get_clinic(self):
        return self.__clinic

    def get_date_of_arrival(self):
        return self.__date_of_arrival

    def get_time(self):
        return self.__time

    def get_message(self):
        return self.__message

    def set_clinic(self,clinic):
        self.__clinic=clinic

    def set_purpose(self, purpose):
        self.__purpose = purpose

    def set_nric(self, nric):
        self.__nric = nric

    def set_time(self, time):
        self.__time = time


    def set_date_of_arrival(self, date_of_arrival):
        self.__date_of_arrival = date_of_arrival

    def set_message(self, message):
        self.__message = message

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_selected_clinic_id(self, selected_clinic_id):
        self.__selected_clinic_id = selected_clinic_id
    def get_selected_clinic_id(self):
        return self.__selected_clinic_id

class ShoppingCart():
    count_id=0
    def __init__(self,image_location,quantity,product_name,product_description,price):
        ShoppingCart.count_id+=1
        self.__product_id = ShoppingCart.count_id
        self.__image_location=image_location
        self.__quantity=quantity
        self.__product_name=product_name
        self.__product_description=product_description
        self.__price=price
        self.__cart_total=0

    def set_product_id(self,product_id):
        self.__product_id= product_id

    def set_cart_total(self,cart_total):
        self.__cart_total= cart_total


    def set_image_location(self,image_location):
        self.__image_location=image_location

    def set_quantity(self,quantity):
        self.__quantity=quantity

    def set_product_name(self,product_name):
        self.__product_name = product_name

    def set_product_description(self, product_description):
        self.__product_description=product_description

    def set_price(self, price):
        self.__price = price

    def get_image_location(self):
        return self.__image_location

    def get_quantity(self):
        return self.__quantity

    def get_product_name(self):
        return self.__product_name

    def get_price(self):
        return self.__price

    def get_product_description(self):
        return self.__product_description

    def get_product_id(self):
        return self.__product_id

    def get_cart_total(self):
        return self.__cart_total

