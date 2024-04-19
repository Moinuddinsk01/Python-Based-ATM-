class Receiver:
    def __init__(self, acc_no, name):
        self.__acc_no = acc_no
        self.__name = name 
    def getAccNo(self):
        return self.__acc_no
    def getAccHolderName(self):
        return self.__name
        

class UserForLogin:
    def __init__(self, acc_no, pin):
        self.__acc_no = acc_no
        self.__pin = pin 
    def getAccNo(self):
        return self.__acc_no
    def getPin(self):
        return self.__pin
        
        
class User:
    def __init__(self, acc_no, acc_holder, pin):
        self.__acc_no = acc_no
        self.__acc_holder = acc_holder
        self.__pin = pin
    def getAccNo(self):
        return self.__acc_no
    def getAccHolderName(self):
        return self.__acc_holder
    def getPin(self):
        return self.__pin
    def setBalance(self, balance=0):
        self.__balance = balance
    def getBalance(self):
        return self.__balance


    
