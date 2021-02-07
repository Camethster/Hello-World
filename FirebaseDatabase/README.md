# Overview
I created this to teach myself about cloud database and python application integration. As modifications come, I hope to use it personally as a CRM.

This software was written to make simple changes to a cloud database.  It includes changing customer data, creating new customers, deleting old ones, find specific ones, and displaying all customers.



[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

Using Google Firebase's Realtime Database, I provided quick and constant feedback to my app that updates instantaneously.

I used a simple structure for my first time. It goes as follows

```
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
```

# Development Environment

The following tools used in this exercise are:
- Visual Studio Code
- [Google Firebase's Realtime Database](https://console.firebase.google.com)

The coding language used is [Python](https://www.python.org/) with the help of the following libraries:

- firebase_admin
- tabulate


# Useful Websites

{Make a list of websites that you found helpful in this project}
* [firebase_admin Documentation](https://firebase.google.com/docs/reference/admin/python)
* [Tabulate Documenation](https://pypi.org/project/tabulate/)
* [Dictionary Usage](https://developers.google.com/edu/python/dict-files)
* [Stack Overflow](https://stackoverflow.com/)

# Future Work

* Add more specific search options
* Another table for product
* Specific Case Handling