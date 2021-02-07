# %%
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import pandas as pd
import json
from tabulate import tabulate
  
def intialize():
    # should get intialize the database
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred,
                                    {"databaseURL" : "https://customerdata-39ba5-default-rtdb.firebaseio.com",
                                    "databaseAuthVariableOverride": None},
                                name = "right")
    return

def get_connected():
    # should pull up previous app 
    app = firebase_admin.get_app("right")
    # Return client  
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
            print("5) Quit")
            choice = int(input())
        except:
            print("Use the numbers listed please.")
        if(choice > 5):
            print("Use the numbers listed please.")
            choice = 0
    return choice

def set_base(db):
    # if the database hasn't been intialized set up the structure
    db.set(
       {
            "Customer" :
            {
                "customer1" :
                {
                    "First_Name"  :  "" ,
                    "Last_Name"  : "" ,
                    "Street_Address" : "" ,
                    "City" : "" ,
                    "State" : "" ,
                    "Zip_Code" : "" ,
                    "Phone_Number"  : "" ,
                    "Status" : "",
                }
            }
        }
    )

def add_customer(db,fname,lname,address,city,state,zip_code,phone_number,status):
    # Get last customer name
    
    last_cust = db.order_by_key().limit_to_last(1).get()
    last_key = last_cust['Customer'].keys()
    s = "%s" % last_key
    new_index = "customer" + str(int(s.split("customer")[1].split("'")[0])+1)
    
    #map_values
    db.child("Customer").set({
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

def update_customer(db,customer):
    find_customer(db,name)

def find_customer(db,name):
    customer = db.child("Customer").equal_to(name).get()
    print() 


def main():
    try:
    #Set up if not set up already 
        intialize()
        db = get_connected()
        set_base(db)
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
        
        elif(choice == 4):
            
        elif choice == 5:
            done = True 


if __name__ == "__main__":
    main()


    # %%
