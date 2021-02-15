import shelve

class addVisit:

    def __init__(self, fullname, nric, visit_date, charge_type, pri_diagnosis, cash, company, allergies, mc_day, mc_reason, mc_date, sec_diagnosis, referral, claim, copayment, remarks, drug_list, drug_price_list, drug_qty_list, drug_amt_list, clinic, total_fee, consult_fee, drug_name,  drug_price, drug_qty, drug_amt, total_drugs, keep_date):
        self.__clinic = "ABC Clinic"

        db = shelve.open('storage.db', 'c')
        visits = db['visits']
        for i in visits:
            if i == self.__clinic:
                visitNum = visits[self.__clinic]
            else:
                visits[self.__clinic] = 0
                visitNum = visits[self.__clinic]

        visitNum += 1

        visits[self.__clinic] = visitNum
        db['visits'] = visits
        db.close()

        self.__visit_num = "EV" + str(visitNum)

        self.__drug_name = drug_name
        self.__drug_price = drug_price
        self.__drug_qty = drug_qty
        self.__drug_amt = drug_amt

        self.__drug_list = drug_list
        self.__drug_price_list = drug_price_list
        self.__drug_qty_list = drug_qty_list
        self.__drug_amt_list = drug_amt_list

        self.__fullname = fullname
        self.__nric = nric
        self.__visit_date = visit_date.replace(' ', '-')
        self.__charge_type = charge_type
        self.__pri_diagnosis = pri_diagnosis
        self.__cash = cash
        self.__company = company
        self.__allergies = allergies
        self.__mc_day = mc_day
        self.__mc_reason = mc_reason
        self.__mc_date = mc_date
        self.__sec_diagnosis = sec_diagnosis
        self.__referral = referral
        self.__claim = claim
        self.__copayment = copayment
        self.__remarks = remarks
        self.__clinic = clinic
        self.__total_fee = total_fee
        self.__consult_fee = consult_fee
        self.__total_drugs = total_drugs
        self.__keep_date = keep_date

    def get_keep_date(self):
        return self.__keep_date

    def set_keep_date(self, keep_date):
        self.__keep_date = keep_date

    def get_total_drugs(self):
        return self.__total_drugs

    def set_total_drugs(self, total_drugs):
        self.__total_drugs = total_drugs

    def get_drug_name(self):
        return self.__drug_name

    def set_drug_name(self, drug_name):
        self.__drug_name = drug_name

    def get_drug_price(self):
        return self.__drug_price

    def set_drug_price(self, drug_price):
        self.__drug_price = drug_price

    def get_drug_qty(self):
        return self.__drug_qty

    def set_drug_qty(self, drug_qty):
        self.__drug_qty = drug_qty

    def get_drug_amt(self):
        return self.__drug_amt

    def set_drug_amt(self, drug_amt):
        self.__drug_amt = drug_amt


    def get_consult_fee(self):
        return self.__consult_fee

    def set_consult_fee(self, consult_fee):
        self.__consult_fee = consult_fee

    def get_visit_num(self):
        return self.__visit_num

    def set_visit_num(self, visit_num):
        self.__visit_num = visit_num


    def get_drug_list(self):
        return self.__drug_list

    def get_drug_price_list(self):
        return self.__drug_price_list

    def get_drug_qty_list(self):
        return self.__drug_qty_list

    def get_drug_amt_list(self):
        return self.__drug_amt_list

    def set_drug_list(self, drug_list):
        self.__drug_list = drug_list

    def set_drug_price_list(self, drug_price_list):
        self.__drug_price_list = drug_price_list

    def set_drug_qty_list(self, drug_qty_list):
        self.__drug_qty_list = drug_qty_list

    def set_drug_amt_list(self, drug_amt_list):
        self.__drug_amt_list = drug_amt_list


    def get_fullname(self):
        return self.__fullname

    def get_nric(self):
        return self.__nric

    def get_visit_date(self):
        return self.__visit_date

    def get_charge_type(self):
        return self.__charge_type

    def get_pri_diagnosis(self):
        return self.__pri_diagnosis

    def get_cash(self):
        return self.__cash

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def set_nric(self, nric):
        self.__nric = nric

    def set_visit_date(self, visit_date):
        self.__visit_date = visit_date

    def set_charge_type(self, charge_type):
        self.__charge_type = charge_type

    def set_pri_diagnosis(self, pri_diagnosis):
        self.__pri_diagnosis = pri_diagnosis

    def set_cash(self, cash):
        self.__cash = cash


    def get_company(self):
        return self.__company

    def get_allergies(self):
        return self.__allergies

    def get_mc_day(self):
        return self.__mc_day

    def get_mc_reason(self):
        return self.__mc_reason

    def get_mc_date(self):
        return self.__mc_date

    def get_sec_diagnosis(self):
        return self.__sec_diagnosis

    def get_referral(self):
        return self.__referral

    def get_claim(self):
        return self.__claim

    def get_copayment(self):
        return self.__copayment

    def get_remarks(self):
        return self.__remarks

    def set_company(self, company):
        self.__company = company

    def set_allergies(self, allergies):
        self.__allergies = allergies

    def set_mc_day(self, mc_day):
        self.__mc_day = mc_day

    def set_mc_reason(self, mc_reason):
        self.__mc_reason = mc_reason

    def set_mc_date(self, mc_date):
        self.__mc_date = mc_date

    def set_sec_diagnosis(self, sec_diagnosis):
        self.__sec_diagnosis = sec_diagnosis

    def set_referral(self, referral):
        self.__referral = referral

    def set_claim(self, claim):
        self.__claim = claim

    def set_copayment(self, copayment):
        self.__copayment = copayment

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def get_clinic(self):
        return self.__clinic

    def set_clinic(self, clinic):
        self.__clinic = clinic

    def get_total_fee(self):
        return self.__total_fee

    def set_total_fee(self, total_fee):
        self.__total_fee = total_fee

if __name__ == "__main__":
    string = "2021-01-12"
    newString = string[-2:] + "-" + string[5:7] + "-" + string[:4]
    print(newString)
    db = shelve.open('storage.db', 'c')
    db['visits'] = {'ABC Clinic': 0}
    visits = db['visits']

    print(visits)
    db.close()
