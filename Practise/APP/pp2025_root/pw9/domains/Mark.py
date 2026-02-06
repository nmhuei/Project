import math

class Mark:
    def __init__(self, cid, sid, mark, credit):
        self.__cid = cid
        self.__sid = sid
        self.__mark = math.floor(mark * 10) / 10
        self.__credit = credit

    def get_cid(self):
        return self.__cid

    def get_sid(self):
        return self.__sid

    def get_mark(self):
        return self.__mark
    
    def get_credit(self):
        return self.__credit

    def set_cid(self, cid):
        self.__cid = cid

    def set_sid(self, sid):
        self.__sid = sid

    def set_mark(self, mark):
        self.__mark = math.floor(mark * 10) / 10
        
    def set_credit(self, credit):
        self.__credit = credit

