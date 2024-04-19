from user import * #user module which contains types of users
from atm import * #atm module which is virtual ATM and has datase
import time
import random


print("===============WELCOME TO ATM===============")
time.sleep(1)
print()
print()

def generate_account_number(): #generating 12 digit accout number
    number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    return number

def start(): # this is the start of the project 
    check = input("""Choose the option 
        1. Login
        2. New user
        3. Exit
      """)
    # user can choose these options, each does their operations
    if check == "1":
        login()
    elif check == "2":
        register()
    elif check == "3":
        exit(0)
    else:
        print("Choose the correct option",end="")
        for i in range(5):
            print(".",end="")
            time.sleep(1)
        print()
        start()


atm = ATM() # atm instance as ATM machine

def balanceCheck(obj): #this function used for checking balance, written seperately because this block is used 4-5 times
    balance = atm.checkBalance(obj)
    print(obj.getAccHolderName()+'(xxxxxxxx'+obj.getAccNo()[-4:]+'),',"your available balance is",balance)
    time.sleep(1)
    print("Thank your for using ATM")
    time.sleep(1)
    start()

def chooseFunctionality(obj): #after logging in successfully, user can do these functionalities
    check = input("""What do you want to do ?
        1. Withdraw
        2. Deposit
        3. Pin change
        4. Balance check
        5. Mini statement
        6. Transfer money
        7. Exit
    """)
    #user can do these 7 functionalities, if user chooses other than these options user will be suggested to choose among these options
    if check == "1":
        check_amount = input("""......Quick withdrawal.....
     Select the amount 
         1. 100
         2. 500
         3. 1000
         4. 5000
         5. 10000
         6. Other
                     """)
        #With Quick withdrawal we can reduce user's efforts
        if check_amount == "1":
            amount = 100 
        elif check_amount == "2":
            amount = 500 
        elif check_amount == "3":
            amount = 1000 
        elif check_amount == "4":
            amount = 5000
        elif check_amount == "5":
            amount = 10000 
        elif check_amount == "6":
            amount = int(input("Enter the amount: "))
        else:
            print("Choose the option properly...")
            time.sleep(1)
            start()
        res = atm.withdraw(obj, amount) # calls withdraw function of atm 
        if res == 3:
            print("Rs"+str(amount), "has been debited from xxxxxxxx"+obj.getAccNo()[-4:])
            checkBal = input("Do you want to check the available balance? Yes/No: ")
            if checkBal.lower() == "yes":
                balanceCheck(obj)
            else:
                start()
        elif res == 1: # if res return 1 means that the ATM doesn't have enough money and user reported that
            print("Thank you for reporting....")
            time.sleep(1)
            print("You can use the ATM now.")
            time.sleep(1)
            start()
        else:
            start()
            
    elif check == "2": #if it is 2 users chose to deposit
        amount = int(input("Enter the amount: "))
        atm.deposit(obj, amount)
        time.sleep(1)
        print("Rs"+str(amount), "has been credited successfully into xxxxxxxx"+obj.getAccNo()[-4:])
        checkBal = input("Do you want to check the available balance? Yes/No: ")
        if checkBal.lower() == "yes":
            balanceCheck(obj)
        else:
            start()
    elif check == "3": #chaning the pin 
        newPin = input("Set your 4 digit new pin: ")
        while newPin == obj.getPin(): #new pin must not be same as old
            print("New pin can't be same as old pin...!")
            newPin = input("Set your 4 digit new pin: ")
        atm.pinchange(obj, newPin)
        time.sleep(1)
        print(obj.getAccHolderName()+'(xxxxxxxx'+obj.getAccNo()[-4:]+'),', "your pin has been changed.")
        time.sleep(1)
        start()
    elif check == "4":
        balanceCheck(obj) #checking balance
    elif check == "5": # when it is 5, will get Ministatement of last 10 transactions
        atm.getMinistatement(obj)
        time.sleep(1)
        start()
    elif check == "6": # money transfer to other customer
        acc_no = input("Enter the account number of the receiver: ")
        acc_holder = input("Enter the name of the receiver: ")
        recv = Receiver(acc_no, acc_holder)
        res = atm.moneyTransfer(obj, recv)
        if res == 1:
            checkBal = input("Do you want to check the available balance? Yes/No: ")
            if checkBal.lower() == "yes":
                balanceCheck(obj)
            else:
                start()
        else:
            start()
    elif check == "7":
        exit1()
    else:
        print("Select the option properly.....!")
        chooseFunctionality(obj)
    

def login(): #this function is used for logging in 
    acc_no = input("Enter your account number: ")
    time.sleep(1)
    pin = input("Enter your pin: ")
    objFor = UserForLogin(acc_no,pin)
    if(atm.isCustomer(objFor.getAccNo())):
        if(atm.checkPin(objFor)):
            name = atm.getNameOfCustomer(objFor.getAccNo(), objFor.getPin())
            obj = User(objFor.getAccNo(), name, objFor.getPin())
            print('Hello', obj.getAccHolderName()+",")
            chooseFunctionality(obj)
        else:
            print("Wrong PIN....!")
            start()
    else:
        print("you are not a customer. Do register...!")
        start() 
        
    
def register(): # this function is used for registering
    name = input("Enter your name: ")
    time.sleep(1)
    acc_no = generate_account_number()
    while atm.isCustomer(acc_no): # assigns a unique account number
        acc_no = generate_account_number()
    print(acc_no,",this is your Account number.")
    time.sleep(1)
    pin = input("Set your 4 digit pin: ")
    time.sleep(1)
    depcheck = input("Do you want you deposit cash now? Yes?No")
    if(depcheck.lower()=='yes'):
        balance = int(input("Enter the cash: "))
    else:
        balance = 0
    obj = User(acc_no, name, pin)
    obj.setBalance(balance)
    atm.addCustomer(obj)
    start()
def exit1():
    start()
    
    
    
start() # staring the program


