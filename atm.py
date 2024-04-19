import sqlite3 # for DB
from datetime import datetime #for taking trasaction done time

conn = sqlite3.connect('sql.db') #Connecting to DB if doesn't exit, creates new
cursor = conn.cursor() #making connection with DB
table1 = """ CREATE TABLE IF NOT EXISTS ATMDB (
            Account_Number VARCHAR(12) PRIMARY KEY,
            Account_Holder_Name TEXT NOT NULL,
            Pin VARCHAR(4) NOT NULL,
            Balance INTEGER NOT NULL
        ); """  #ATMDB is a table for storing user data such as customers to the Bank
table2 = """ CREATE TABLE IF NOT EXISTS TransactionDB (
            Account_Number VARCHAR(12) NOT NULL,
            Account_Holder_Name TEXT NOT NULL,
            Transaction_Type VARCHAR(12) NOT NULL,
            Sender_name TEXT, 
            Sender_Account_Number VARCHAR(12),
            Receiver_name TEXT,
            Receiver_Account_Number VARCHAR(12),
            Transaction_Date DATETIME NOT NULL,
            Available_Balance INTEGER NOT NULL
        ); """
cursor.execute(table1)
cursor.execute(table2)

#Adding dummy rows 
query = """INSERT INTO ATMDB(Account_Number, Account_Holder_Name, Pin, Balance) 
        VALUES(?,?,?,?)"""  
cursor.execute(query,("123456789012","Munna","9346",100000))
cursor.execute(query,("123456789013","Nunna","1234",10000))



class ATM: #Class ATM which resembles real time ATM machine
    cash_in_atm = 100000 #intially our ATM is having 100000rs in it
    @classmethod
    def setAmount(cls): #This classmethod is used for refilling the cash in the atm when the atm doesn't have enough cash
        cls.cash_in_atm = 100000
        
    def getDB(self):
        res = cursor.execute("SELECT * FROM ATMDB")
        for row in res:
            print(row)
            
    def checkPin(self, obj): # checking pin for authorization
        query = "SELECT Pin FROM ATMDB WHERE Pin = ?"
        res = cursor.execute(query, (obj.getPin(),)).fetchall()
        return len(res)>0
        
    def getNameOfCustomer(self, acc_no, pin): #getting customer name for further things 
        query = 'SELECT Account_Holder_Name FROM ATMDB WHERE Account_Number = ? AND Pin = ?'
        res = cursor.execute(query, (acc_no,pin)).fetchall()
        return res[0][0]
    
    
    def isCustomer(self,acc_no): #checking whether the customer exits or not
        query = "SELECT * FROM ATMDB WHERE Account_Number = ?"
        res = cursor.execute(query, (acc_no,)).fetchall()
        return len(res)>0
        
    def addCustomer(self, obj): # adding new customer to the DB
        query = """INSERT INTO ATMDB(Account_Number, Account_Holder_Name, Pin, Balance) 
        VALUES(?,?,?,?)""" 
        cursor.execute(query,(obj.getAccNo(), obj.getAccHolderName(), obj.getPin(), obj.getBalance()))
        
    def checkBalance(self, obj): #used for getting the balance of particular user
        query = 'SELECT Balance FROM ATMDB WHERE Account_Number = ?'
        res = cursor.execute(query, (obj.getAccNo(),)).fetchall()
        return res[0][0]
        
    def deposit(self, obj, amount): #used for depositing money into ATM(i.e, ATMDB)
        query = 'UPDATE ATMDB SET Balance = Balance + ? WHERE Account_Number = ?'
        cursor.execute(query,(amount, obj.getAccNo()))
        #Adding transaction copy to the TransactionDB for further use
        query = '''INSERT INTO TransactionDB('Account_Number', 'Account_Holder_Name', 'Transaction_Type', 
        'Transaction_Date', 'Available_Balance') VALUES(?,?,?,?,?)'''
        cursor.execute(query, (obj.getAccNo(), obj.getAccHolderName(), "Rs"+str(amount)+" Credited", datetime.now(), self.checkBalance(obj)))
        
    def pinchange(self, obj, newPin): # used for changing the PIN
        query = 'UPDATE ATMDB SET Pin = ? WHERE Pin = ?'
        cursor.execute(query,(newPin, obj.getPin()))
        
    def withdraw(self, obj, amount): #used for withdrawal 
        if amount>ATM.cash_in_atm: #whenever the money in ATM is enough for withdrawal we can report to 
            print("Insufficient money in the atm.....!")
            check = input("Do you want to report? Yes/no: ")
            if check.lower() == "yes":
                ATM.setAmount()
                return 1
            else:
                return 2 
        if amount>self.checkBalance(obj): #Can't make withdrawal when we don't have enough money
            print("Insufficient balance. You don't enough amount in your account.")
            check = input("Do you want to see the balance? Yes/No: ")
            if check.lower() == "yes":
                balance = self.checkBalance(obj)
                print(obj.getAccHolderName()+'(xxxxxxxx'+obj.getAccNo()[-4:]+'),',"your available balance is",balance)
                return 2 
        query = "UPDATE ATMDB SET Balance = Balance - ? WHERE Account_Number = ?"
        cursor.execute(query, (amount, obj.getAccNo()))
        ATM.cash_in_atm -= amount
        #Adding transaction copy to the TransactionDB for further use
        query = ''' INSERT INTO TransactionDB(Account_Number, Account_Holder_Name, Transaction_Type,
        Transaction_Date, Available_Balance) VALUES(?,?,?,?,?)'''
        cursor.execute(query, (obj.getAccNo(), obj.getAccHolderName(), "Rs"+str(amount)+" Debited", datetime.now(), self.checkBalance(obj)))
        return 3
    
    def moneyTransfer(self, obj, recv): #using this we can transfer money to others
        res = cursor.execute('SELECT Account_Holder_Name FROM ATMDB WHERE Account_Number = ?', (recv.getAccNo(),)).fetchall()
        if self.isCustomer(recv.getAccNo()) and recv.getAccHolderName()==res[0][0]: #checking whether the receiver exits or not
            amount = int(input("Enter the amount that you want to transfer: "))
            if self.checkBalance(obj)<amount: #can't make transfer when we don't have enough money
                print("Insufficient balance. You don't enough amount in your account to transfer.")
                return 1
            #updating their balances after transfer
            q1 = 'UPDATE ATMDB SET Balance = Balance - ? WHERE Account_Number = ?'
            q2 = 'UPDATE ATMDB SET Balance = Balance + ? WHERE Account_Number = ?'
            cursor.execute(q1, (amount, obj.getAccNo()))
            cursor.execute(q2, (amount, recv.getAccNo()))
            #updating transaction copies to the Transaction DB
            q1 = '''INSERT INTO TransactionDB(Account_Number, Account_Holder_Name, Transaction_Type, Receiver_name, 
            Receiver_Account_Number, Transaction_Date, Available_Balance) VALUES(?,?,?,?,?,?,?)'''
            q2 = '''INSERT INTO TransactionDB(Account_Number, Account_Holder_Name, Transaction_Type, Sender_name, 
            Sender_Account_Number, Transaction_Date, Available_Balance) VALUES(?,?,?,?,?,?,?)'''
            cursor.execute(q1, (obj.getAccNo(), obj.getAccHolderName(), "Rs"+str(amount)+" Debited", recv.getAccHolderName(), recv.getAccNo(), datetime.now(), self.checkBalance(obj)))
            cursor.execute(q2, (recv.getAccNo(), recv.getAccHolderName(), "Rs"+str(amount)+" Credited", obj.getAccHolderName(), obj.getAccNo(), datetime.now(), self.checkBalance(recv)))
            print("Rs"+str(amount),"has been transferred from",obj.getAccHolderName()+"("+obj.getAccNo()[-4:]+") to",recv.getAccHolderName()+"("+recv.getAccNo()[-4:]+")")
            return 1
        else:
            print("Details, you have provided, doesn't exist. Check the details.")
            return 0
            
    def getMinistatement(self, obj): #used for getting mini statement of last 10 transactions
        query = ''' SELECT Account_Number, Account_Holder_Name, Transaction_Type,
        COALESCE(Sender_name, '') AS Sender_name, 
        COALESCE(Sender_Account_Number, '') AS Sender_Account_Number, 
        COALESCE(Receiver_name, '') AS Receiver_name,
        COALESCE(Receiver_Account_Number, '') AS Receiver_Account_Number,
        Transaction_Date, Available_Balance 
        FROM TransactionDB WHERE Account_Number = ? LIMIT 10
        '''
        res = cursor.execute(query, (obj.getAccNo(),)).fetchall()
        column = ['Account_Number', 'Account_Holder_Name', 'Transaction_Type', 'Sender_name', 'Sender_Account_Number', 'Receiver_name', 'Receiver_Account_Number', 'Transaction_Date', 'Available_Balance']
        max_widths = [max(len(str(row[i])) for row in [column] + res) for i in range(len(column))]
        header_line = ' | '.join(str(heading).ljust(max_widths[i]) for i, heading in enumerate(column))
        print(header_line)
        print('-' * len(header_line))
        for row in res:
            print(' | '.join(str(item).ljust(max_widths[i]) for i, item in enumerate(row)))



    
    

    
    
