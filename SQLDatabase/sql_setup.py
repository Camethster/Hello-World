# %%
import sqlite3 
import tkinter as tk


def setup():
    connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE PRODUCT(
                PRODUCT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                NAME TEXT NOT NULL, 
                PART_NUM TEXT NOT NULL,
                WEIGHT REAL,
                HEIGHT REAL,
                LENGTH REAL,
                WIDTH REAL,
                CARB_APR REAL,
                IMAGE_ID REAL
                );''')
    cursor.execute('''CREATE TABLE WAREHOUSE(
        WAREHOUSE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME TEXT NOT NULL,
        UPS_GROUND REAL,
        FEDEX_GROUD REAL,
        FIRST_CLASS REAL,
        PRIORITY REAL,
        SECOND_DAY REAL,
        OVERNIGHT REAL,
        OVERSIZED REAL,
        LTL REAL,
        ADDRESS_ID REAL
    );''')
    cursor.execute('''CREATE TABLE warehouse_has_product(
        WAREHOUSE_HAS_PRODUCT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        WAREHOUSE_ID INT FORIEGN KEY NOT NULL,
        PRODUCT_ID INT FORIEGN KEY NOT NULL,
        PT_NUM TEXT NOT NULL,
        COST REAL,
        QUANTITY REAL,
        SHIP_COST REAL,
        STATE REAL
        );''')
    connection.commit()
    connection.close()

def cleanup():
    connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE PRODUCT ;''')
    cursor.execute('''DROP TABLE WAREHOUSE;''')
    cursor.execute('''DROP TABLE WAREHOUSE_HAS_PRODUCT;''')
    connection.commit()
    connection.close()

def view(table):
    window = tk.Tk()

    connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM {};'''.format(table))
    iterate = 0
    headers = list(map(lambda x: x[0], cursor.description))
    for col in headers:
        label = tk.Label(master=window,text = col,width=10,anchor=tk.NW)
        label.grid(row=0,column=iterate)
        iterate += 1
    iterate = 0
    for col in cursor.fetchone():
        label = tk.Label(master=window,text = col,width=10,anchor=tk.NW)
        label.grid(row=1,column=iterate)
        iterate +=1

    window.mainloop()
    connection.commit()
    connection.close()

def verify(window,col,values,table):
    try:
        connection = sqlite3.connect('Snake_Riv.db')
        cursor = connection.cursor()
        col_form = sql_str_form(col)
        val_list = list()
        val_list.append("NULL")
        for x in values:
            val_list.append(x.get())
        val_form = sql_str_form(val_list)
        print(val_form + col_form)
        cursor.execute('''INSERT INTO {} ({}) VALUES({});'''.format(table,col_form,val_form))
        connection.commit()
        connection.close()
    except sqlite3.OperationalError as e:
        tk.Message(window,text=e).grid(row=3,column=0)
        return False
    tk.Message(window,text="Success").grid(row=3,column=0)
    return True


def add(table):
    add_win = tk.Tk()

    connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT  * FROM ({});'''.format(table))
    iterate = 0
    head_frm = tk.Frame(add_win)
    headers = list(map(lambda x: x[0], cursor.description))
    for col in headers:
        label = tk.Label(head_frm,text = col,width=10,anchor=tk.NW)
        label.grid(row=0,column=iterate)
        iterate += 1
    
    rows = []
    for x in range(1,len(headers)):
        rows.append(tk.Entry(width=10,master=head_frm))
        rows[(x-1)].grid(row=1,column=x)   
    sub_btn= tk.Button(head_frm,
    justify=tk.LEFT,
    text="submit",
    width=10,
    command= lambda : verify(head_frm,headers,rows,table))
    sub_btn.grid(row=2,column=0)
    head_frm.grid(row=0)
    add_win.mainloop()
    connection.commit()
    connection.close()


def ui():
    root = tk.Tk() 
    view_btn  = tk.Button(root,text='View', width = 10,command=lambda:  view("PRODUCT"))
    add_btn  = tk.Button(root,text='Add', width = 10,command=lambda: add("PRODUCT"))
    view_btn.pack()
    add_btn.pack()
    root.mainloop()

def sql_str_form(a_list):
    val_form = ""
    for x in a_list:
        try:
            int(x)
            val_form = val_form + x + ", "
        except:
            val_form = val_form + '\'' + x + '\'' + ", "
    return val_form[:-2]
def main():
    """connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT PRODUCT_ID FROM PRODUCT''')
    cursor.execute('''INSERT INTO PRODUCT VALUES (1,'CAM','123')''',)
    print(cursor.fetchall())"""
    ui()

    

if __name__ == "__main__":
    main()


# %%
