from tkinter import *
import os
import sys
from selenium import webdriver
from time import sleep
from tkinter import messagebox
from data import StockData
from tkinter import ttk

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def add(name, description, place=None):
    check = StockData("stock")
    list_stock = check.show()

    names_list = [s[0] for s in list_stock]
    
    if name not in names_list:
        if name != "":
            # insert into database
            stock = StockData("stock")
            stock.save_information(name=name, description=description)
            # Clear the fields
            if place == "E":
                stock_name_entry.delete(0, END)
                stock_des_entry.delete(0, END)
        else:
            messagebox.showinfo(title="Add to Stocks", message="You need to at least enter a name for your stock")
            refresh = False
    else:
        messagebox.showinfo(title="Same Stock", message="این اطلاعت سهم موجود است")
        if place == "E":
            stock_name_entry.delete(0, END)
            stock_des_entry.delete(0, END)
        
        
def show_qs():
    stock = StockData("stock")
    stocks = stock.show()
    
    # Getting the number of queries
    global stocks_qs_count 
    stocks_qs_count = len(stocks)
    
    show_label = Label(master, text="")
    show_label.grid(row=1, column=1)
    stock_show = ""
    for s in stocks:
        stock_show += s[0] + "\n"

    show_label.config(text=stock_show)

def delete():
    name = stock_name_entry.get()
    _stock = StockData("stock")
    text = _stock.show_single_query(name=name)[0][0]
    print(text)
    try:
        yes_no =  messagebox.askokcancel(title="Delete Alert", message="Do you want to delete " 
                                                                        + str(text))

        if yes_no:
            # Remove from database
            _stock.delete(name=name)
            stock_name_entry.delete(0, END)
            messagebox.showinfo(title="Success", message="سهم با موفقیت حذف شد")
    except TypeError:
        print("Primary key didn't specefied")

def update():
    name = stock_name_entry.get()
    description = stock_des_entry.get()
    
    stock_data.update(name=name, description=description)
    master.destroy()
    stock_window()
    messagebox.showinfo(title="Change Success", message="تغییرات با موفقیت اعمال شد")

def edit():
    name_stock = stock_name_entry.get()
    global stock_data
    stock_data = StockData("stock")
    s_name = stock_data.show_single_query(name=name_stock)

    if s_name != []: 
        master.title("Update stock info")
        stock_label.config(text="ویرایش اطلاعات سهم", fg="green")
        submit_btn.destroy()
        show_btn.destroy()
        del_btn.destroy()
        edit_btn.destroy()

        stock_name_entry.delete(0, END)
        _stocks = stock_data.show_single_query(name=name_stock)
        try:
            stock_name_entry.insert(0, _stocks[0][0])
            if _stocks[0][1] != None:
                stock_des_entry.insert(0, _stocks[0][1])
        except TypeError:
            print("Primary key didn't specefied")    

        edit_btn_1 = Button(stock_label, text='ثبت ویرایش', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=update)
        edit_btn_1.grid(row=2, column=1, pady=10, padx=(0, 300))
    else:
        messagebox.showerror(title="Database Error", message="This query is empty")

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
    submit_btn = Button(stock_label, text='افزودن', bg='orange', font=("Helvatica", 10, 'bold'), fg='black', command=lambda: add(stock_name_entry.get(), stock_des_entry.get(), place="E"), width=5)
    submit_btn.grid(row=2, column=1, pady=5, padx=(100, 0))

    show_btn = Button(stock_label, text='نمایش', bg='green', font=("Helvatica", 10, 'bold'), fg='black', command=show_qs, width=5)
    show_btn.grid(row=2, column=1, pady=5, padx=(100, 120))

    del_btn = Button(stock_label, text='حذف', bg='red', font=("Helvatica", 10, 'bold'), fg='black', command=delete, width=5)
    del_btn.grid(row=2, column=1, pady=5, padx=(40, 200))

    edit_btn = Button(stock_label, text='ویرایش', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=edit, width=5)
    edit_btn.grid(row=2, column=1, pady=10, padx=(0, 300))


def short_form(val):
    width=16
    selected_value = var.get()
    var.set(selected_value[:width] + ("" if len(selected_value) <= width else "..."))
    selected_value = str(selected_value).split(" | ")[0]

def save_info():
    user = str(var_user.get())
    pswd = password_entry.get()
    
    stock = str(var.get())
    check_user = StockData("user")
    
    list_users = check_user.show()
    users_list = [s[0] for s in list_users]
    pswds_list = [s[1] for s in list_users]
    global refresh
    refresh = True
    if user not in users_list and user != "" and pswd != "":
        user_create = StockData('user')
        user_create.save_information(username=user, password=pswd)

    elif user in users_list:
        user_check = StockData('user')
        check_user_name = user_check.show_single_query(username=user)
        if check_user_name[0][0] != user or check_user_name[0][1] != pswd:
            change = messagebox.askokcancel(title="Change Info", message=f"میخواهید اطلاعات مربوط به {user} را تغییر دهید؟ ")
            if change:
                user_update = StockData('user')
                user_update.update(username=user, password=pswd)
                messagebox.showinfo(title="Success", message="اطلاعات با موفقیت تغییر یافت")

        else:
            messagebox.showinfo(title="Same user", message="این نام کاربری قبلا ذخیره شده است")
            refresh = False
    print(stock)
    if stock != " ":
        add(stock, description=None)
    
    password_entry.delete(0, END)
    var_user.set('')
    var.set('')
    if refresh:
        root.destroy()
        ui()

def auto_complete(*args):
    user_name = str(var_user.get())
    users = StockData("user")
    related_password = users.show_single_query(username=user_name)[0][1]
    password_entry.delete(0, END)
    password_entry.insert(0, related_password)


def hide():
    password_entry.config(show="*")
    show_password_btn.config(text="show password", command=show)

def show():
    if password_entry.get() != "":
        password_entry.config(show="")
        show_password_btn.config(text="hide password", command=hide)
    

def ui():
    _stocks = StockData("stock")
    STOCKS = [s[0] for s in _stocks.show()]

    _users = StockData('user')
    user_info = [s[0] for s in _users.show()]


    global root
    root = Tk()
    root.title("Stock Bot")
    root.resizable(False, False)
    root.iconbitmap(resource_path('bot.ico'))
    root.geometry('440x450')
    user_label = Label(root, text="username", font=("Helvatica", 10), fg='red')
    user_label.grid(row=0, column=0, padx=50, pady=15)

    global var_user
    var_user = StringVar()

    user_entry = ttk.Combobox(root, width=17, textvariable=var_user, values=user_info, height=5)
    user_entry.grid(row=0, column=1)
    user_entry.current()
    user_entry.bind("<<ComboboxSelected>>", auto_complete)


    password_label = Label(root, text="password", font=("Helvatica", 10), fg='red')
    password_label.grid(row=1, column=0)

    global password_entry
    password_entry = Entry(root, show="*")
    password_entry.grid(row=1, column=1, padx=70)

    global show_password_btn 
    show_password_btn = Button(root, text="show password", relief=SUNKEN, bd=0, fg="blue", command=show)
    show_password_btn.grid(row=1, column=1, padx=(0, 250))

    stock_label_1 = Label(root, text="نماد سهم", font=("Helvatica", 10))
    stock_label_1.grid(row=2, column=0, pady=10)

    global var
    var = StringVar()
    var.set(" ")
    global stock_drop
    stock_drop = ttk.Combobox(root, textvariable=var, values=STOCKS, width=17, height=8)
    stock_drop.grid(row=2, column=1)
    stock_drop.current()
    
    
    stock_description = Button(root, text='Edit', font=("Helvatica", 10), fg='green', relief=SUNKEN,command=stock_window, bd=0, cursor="hand2")
    stock_description.grid(row=2, column=1, padx=(0, 200))

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

    delay_between_order_label = Label(root, text="فاصله بین  هر سفارش (میلی ثانیه)", fg="red")
    delay_between_order_label.grid(row=8, column=0, pady=10)

    global delay_between_order
    delay_between_order = Spinbox(root, from_=300, to=1000, justify=CENTER, width=10)
    delay_between_order.grid(row=8, column=1, pady=10)

    global cost_label
    cost_label = Label(root, text="0")
    cost_label.grid(row=9, column=1)

    cost_label_text = Label(root, text="قیمت کل خرید/فروش", fg='red')
    cost_label_text.grid(row=9, column=0)

    buy_btn = Button(root, text='خرید', bg='green', font=("Helvatica", 10), fg='black', command=lambda: order('b'), width=5)
    buy_btn.grid(row=10, column=0, pady=10)

    sell_btn = Button(root, text='فروش', bg='red', font=("Helvatica", 10), fg='black', command=lambda: order('s'), width=5)
    sell_btn.grid(row=10, column=1)

    save_btn = Button(root, text='ذخیره اطلاعات', bg='grey', font=("Helvatica", 10), fg='black', command=save_info, width=10)
    save_btn.grid(row=10, column=1, padx=(0, 250))

    root.mainloop()

ui()
