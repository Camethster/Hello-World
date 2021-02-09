# %%
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from tabulate import tabulate
  
def intialize():
    #Intialize the database
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred,
                                    {"databaseURL" : "https://customerdata-39ba5-default-rtdb.firebaseio.com",
                                    "databaseAuthVariableOverride": None},
                                name = "right")
    return

def get_connected():
    # Get previous app settings
    app = firebase_admin.get_app("right")
    # Return database reference
    return db.reference("/",app)

def action():
    # User interface with some case handling
    choice = 0
    print("What would you like to do?: ")
    while (choice == 0):
        try:
            print("1) Add Customer")
            print("2) Change Customer")
            print("3) Remove Customer")
            print("4) Find Customer")
            print("5) Display Customers")
            print("6) Quit")
            choice = int(input())
        except:
            print("Use the numbers listed please.")
        if(choice > 6):
            print("Use the numbers listed please.")
            choice = 0
    return choice

def add_customer(db,fname,lname,address,city,state,zip_code,phone_number,status):
    # Get last customer name
    
    last_cust = db.child("Customer").order_by_key().limit_to_last(1).get()
    last_key = last_cust.keys()
    s = "%s" % last_key
    new_index = "customer" + str(int(s.split("customer")[1].split("'")[0])+1)
    #Adds a new customer
    db.child("Customer").update({
        new_index : 
        {
            "First_Name"  :  fname ,
            "Last_Name"  : lname ,
            "Street_Address" : address ,
            "City" : city ,
            "State" : state ,
            "Zip_Code" : zip_code ,
            "Phone_Number"  : phone_number ,
            "Status" : status,
        }
    })

def update_customer(db,name):
    #finds the customer and returns parent and child in tuple
    customer = find_customer(db,name)
    changing = True
    while changing == True:
        change = str.replace(input("What would you like to change?: ")," ","_")
        avalue = input("To what value?")
        db.child("Customer").child(customer[0]).update(
            {
                change : avalue
            }
        )

        if input("Anymore changes on this Customer(y/n)? ") ==  "Y": 
            changing = True 
        else: 
            changing = False

def delete_customer(db,name):
    customer = find_customer(db,name)
    db.child("Customer").child(customer[0]).delete()

def find_customer(db,name):
    #Finds customer using their first name
    customer = db.child("Customer").get().items()
    for child in customer:
        values = child[1]
        if values["First_Name"] == name:
            print("First Name: %(First_Name)s" %values)
            print("Last Name: %(Last_Name)s" %values)
            print("Street Address: %(Street_Address)s" %values)
            print("City: %(City)s" %values)
            print("State: %(State)s" %values)
            print("Zip Code: %(Zip_Code)s" %values)
            print("Phone Number: %(Phone_Number)s" %values)
            print("Status: %(Status)s" %values)
            return child
    print("Customer not found.")
    return


def display_customers(db):
    customer = db.child("Customer").get().values()
    print(tabulate(customer))


def main():
    try:
    #Set up if not set up already 
        intialize()
        db = get_connected()
    except ValueError:
        pass

    #establish connection
    db = get_connected()

    
    #UI
    done = False
    while not done:
        choice = action()
        if choice == 1:
            # Choice 1 add customer with exception handling
            print("Press esc for any null values")
            fname = input("What is the First Name? ")
            lname = input("Last Name? ")
            address = input("Street Address? ")
            city = input ("City? ")
            state = input("State? ")
            while True:
                try:
                    zip_code = int(input("Zip Code(xxxxx)? "))
                    phone_number = int(input("Phone Number(xxxxxxxxxx)?"))
                    break
                except ValueError:
                    print("Please input a number for Zip and Phone Number")
            status =  input("Status? ") 
            add_customer(db,fname,lname,address,city,state,zip_code,phone_number,status)
        elif(choice == 2):
            name = input("Which customer do you want to update? ")
            update_customer(db, name)
        elif(choice == 3):
            name = input("Which customer do you want to delete? ")
            delete_customer(db,name)
        elif(choice == 4):
            name = input("Which customer do you want to find? ")
            find_customer(db, name)
        elif(choice == 5):
            display_customers(db)    
        elif choice == 6:
            done = True 


if __name__ == "__main__":
    main()


    # %%
