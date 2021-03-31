# %%
import sqlite3 
import tkinter as tk


def setup():
    connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE PRODUCT(
                PRODUCT_ID INT PRIMARY KEY NOT NULL,
                WAREHOUSE_HAS_PRODUCT INT FORIEGN KEY NOT NULL,
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
        WAREHOUSE_ID INT PRIMARY KEY NOT NULL,
        WAREHOUSE_HAS_PRODUCT INT FORIEGN KEY NOT NULL,
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
        WAREHOUSE_HAS_PRODUCT_ID INT PRIMARY KEY NOT NULL,
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

def view():
    window = tk.Tk()

    connection = sqlite3.connect('Snake_Riv.db')
    cursor = connection.cursor()
    cursor.execute('''PRAGMA table_info(PRODUCT);''')
    print(cursor.fetchall())
    
    label = tk.Label(width = 20, text = cursor.fetchall()[1])
    label.pack()
    window.mainloop()

def ui():
    root = tk.Tk() 
    click_ent = tk.Entry()
    click_ent.focus_set()
    ok_btn  = tk.Button(text='OK', width = 10,command=view)
    ok_btn.pack()
    mainloop()

def main():
    cleanup()
    setup()
    ui()

if __name__ == "__main__":
    main()


# %%
