from tkinter import *
import os
import sys
from selenium import webdriver
from time import sleep
from tkinter import messagebox
from data import StockData

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def add():
    name = stock_name_entry.get()
    description = stock_des_entry.get()
    if name != "":
        # insert into database
        stock = StockData()
        stock.save_stock(name, description)
        # Clear the fields
        stock_name_entry.delete(0, END)
        stock_des_entry.delete(0, END)
    else:
        messagebox.showinfo(title="Add to Stocks", message="You need to at least enter a name for your stock")

        
def show():
    stock = StockData()
    stocks = stock.show()
    show_label = Label(master, text="")
    show_label.grid(row=1, column=1)
    stock_show = ""
    for s in stocks:
        stock_show += str(s[2]) + " | " + s[1] + " | " + s[0] + "\n"

    show_label.config(text=stock_show)

def delete():
    pk = stock_name_entry.get()
    stock = StockData()
    text = stock.show_single_query(pk)
    try:
        yes_no =  messagebox.askokcancel(title="Delete Alert", message="Do you want to delete " 
                                                                        + str(text[0][0]))

        if yes_no:
            # Remove from database
            stock.delete(pk)
            stock_name_entry.delete(0, END)
    except TypeError:
        print("Primary key didn't specefied")

def update():
    name = stock_name_entry.get()
    description = stock_des_entry.get()
    stock = StockData()
    stock.update(name, description, pk_up)
    master.destroy()
    stock_window()
    messagebox.showinfo(title="Change Success", message="تغییرات با موفقیت اعمال شد")

def edit():
    master.title("Update stock info")
    stock_label.config(text="ویرایش اطلاعات سهم", fg="green")
    submit_btn.destroy()
    show_btn.destroy()
    del_btn.destroy()
    edit_btn.destroy()

    global pk_up
    pk_up = stock_name_entry.get()
    stock_name_entry.delete(0, END)
    stock = StockData()
    stocks = stock.show_single_query(pk_up)
    try:
        stock_name_entry.insert(0, stocks[0][0])
        stock_des_entry.insert(0, stocks[0][1])
    except TypeError:
        print("Primary key didn't specefied")    

    edit_btn_1 = Button(stock_label, text='ثبت ویرایش', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=update)
    edit_btn_1.grid(row=2, column=1, pady=10, padx=(0, 300))


def stock_window():
    global master
    master = Toplevel(root)
    master.title("Add a Stock")
    master.iconbitmap(resource_path('bot.ico'))
    master.geometry('400x180')
    
    global stock_label
    stock_label = LabelFrame(master, text="اضافه کردن سهم", width=100)
    stock_label.grid(row=0, column=1, padx=30, ipady=8, ipadx=5)

    stock_name_label = Label(stock_label, text="نام سهم", font=("Helvatica", 12))
    stock_name_label.grid(row=0, column=0, pady=10, padx=(10, 0))

    stock_des_label = Label(stock_label, text="توضیحات", font=("Helvatica", 12))
    stock_des_label.grid(row=1, column=0, padx=(10, 0))

    global stock_name_entry
    stock_name_entry = Entry(stock_label)
    stock_name_entry.grid(row=0, column=1, padx=70)

    global stock_des_entry
    stock_des_entry = Entry(stock_label)
    stock_des_entry.grid(row=1, column=1, padx=70)

    global submit_btn, show_btn, del_btn, edit_btn
    submit_btn = Button(stock_label, text='افزودن', bg='orange', font=("Helvatica", 10, 'bold'), fg='black', command=add, width=5)
    submit_btn.grid(row=2, column=1, pady=5, padx=(100, 0))

    show_btn = Button(stock_label, text='نمایش', bg='green', font=("Helvatica", 10, 'bold'), fg='black', command=show, width=5)
    show_btn.grid(row=2, column=1, pady=5, padx=(100, 120))

    del_btn = Button(stock_label, text='حذف', bg='red', font=("Helvatica", 10, 'bold'), fg='black', command=delete, width=5)
    del_btn.grid(row=2, column=1, pady=5, padx=(40, 200))

    edit_btn = Button(stock_label, text='ویرایش', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=edit, width=5)
    edit_btn.grid(row=2, column=1, pady=10, padx=(0, 300))


def short_form(val):
    var.set("...")

    stock_name = val.split(" | ")[0]
    stock_entry.delete(0, END)
    stock_entry.insert(0, stock_name)
    
_stocks = StockData()
STOCKS = [s[0] + " | " + s[1] for s in _stocks.show()]


def ui():
    global root
    root = Tk()
    root.title("Stock Bot")
    root.resizable(False, False)
    root.iconbitmap(resource_path('bot.ico'))
    root.geometry('400x400')
    user_label = Label(root, text="username", font=("Helvatica", 10), fg='red')
    user_label.grid(row=0, column=0, padx=50, pady=15)

    global user_entry
    user_entry = Entry(root)
    user_entry.grid(row=0, column=1)

    password_label = Label(root, text="password", font=("Helvatica", 10), fg='red')
    password_label.grid(row=1, column=0)

    global password_entry
    password_entry = Entry(root)
    password_entry.grid(row=1, column=1, padx=70)

    stock_label_1 = Label(root, text="نماد سهم", font=("Helvatica", 10))
    stock_label_1.grid(row=2, column=0, pady=10)

    global stock_entry
    stock_entry = Entry(root, width=20)
    stock_entry.grid(row=2, column=1)

    global var
    var = StringVar()
   
    stock_drop = OptionMenu(root, var, *STOCKS, command=short_form)
    stock_drop.grid(row=2, column=1, padx=(100, 0))
    stock_drop.config(width=0, anchor='center')

    stock_description = Button(root, text='+', bg='green', font=("Helvatica", 8), fg='black', command=stock_window)
    stock_description.grid(row=2, column=1, padx=(0, 200), ipadx=5)

    stock_price_label = Label(root, text="قیمت سهم (ريال)", font=("Helvatica", 10))
    stock_price_label.grid(row=3, column=0, pady=10)

    global stock_price_entry
    stock_price_entry = Entry(root)
    stock_price_entry.grid(row=3, column=1, padx=70)

    stock_quantity_label = Label(root, text="تعداد", font=("Helvatica", 10))
    stock_quantity_label.grid(row=4, column=0, pady=10)

    global stock_quantity_entry
    stock_quantity_entry = Entry(root)
    stock_quantity_entry.grid(row=4, column=1, padx=70)

    guid = Label(root, text="زمان را به صورت 01:10:03 وارد کنید", font=("Helvatica", 10, 'bold'), fg="red")
    guid.grid(row=5, column=0)

    start_time_label = Label(root, text="ساعت شروع", font=("Helvatica", 10))
    start_time_label.grid(row=6, column=0, pady=10)

    global start_time_entry
    start_time_entry = Entry(root)
    start_time_entry.grid(row=6, column=1, padx=70)

    end_time_label = Label(root, text="ساعت پایان", font=("Helvatica", 10))
    end_time_label.grid(row=7, column=0, pady=10)

    global end_time_entry
    end_time_entry = Entry(root)
    end_time_entry.grid(row=7, column=1, padx=70)

    global cost_label
    cost_label = Label(root, text="0")
    cost_label.grid(row=8, column=1)

    cost_label_text = Label(root, text="قیمت کل خرید/فروش", fg='red')
    cost_label_text.grid(row=8, column=0)

    buy_btn = Button(root, text='خرید', bg='green', font=("Helvatica", 10), fg='black', command=lambda: order('b'), width=5)
    buy_btn.grid(row=9, column=0, pady=10)

    sell_btn = Button(root, text='فروش', bg='red', font=("Helvatica", 10), fg='black', command=lambda: order('s'), width=5)
    sell_btn.grid(row=9, column=1)

    root.mainloop()

ui()
