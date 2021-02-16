from tkinter import *
import os
import sys
from selenium import webdriver
from time import sleep
from tkinter import messagebox
from data import StockData
from tkinter import ttk
import threading
import datetime as dt

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def refresh():
    root.destroy()
    ui()

def order(_type):
    username = var_user.get()
    stock = var.get()
    price = stock_price_entry.get()
    quantity = stock_quantity_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    trade_type = _type

    save_record = StockData('record')
    save_record.save_information(username=username, name=stock, quantity=quantity, 
                                stock_price=price, trade_type=trade_type, trade_date=dt.datetime.today().strftime("%Y-%m-%d"),
                                trade_time=dt.datetime.today().strftime("%H:%M:%S")  ,start_time=start_time, end_time=end_time)
    
    stock_price_entry.delete(0, END)
    stock_quantity_entry.delete(0, END)
    start_time_entry.delete(0, END)
    end_time_entry.delete(0, END)
    


# For stock
def add(name, description, place=None, window=None, change_password=False):
    if window == "S" or window == "M":
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
                    stock_des_entry.delete(0, END)
                    stock_name_entry.delete(0, END)
                    messagebox.showinfo(title="Stock Add", message="اطلاعات سهم ذخیره شد")
            else:
                if place == "E":
                    messagebox.showinfo(title="Add to Stocks", message="You need to at least enter a name for your stock")
                _refresh = False
        else:
            messagebox.showinfo(title="Same Stock", message="این اطلاعت سهم موجود است")
            if place == "E":
                stock_name_entry.delete(0, END)
                stock_des_entry.delete(0, END)
                
    elif window == "U":                                  
        user = user_name_entry.get()
        pswd = user_pas_entry.get()

        user_check = StockData("user")
        users_list = [s[0] for s in user_check.show()]

        if user not in users_list and user != "" and pswd != "":
            user_save = StockData("user")
            user_save.save_information(username=user, password=pswd)
            messagebox.showinfo(title="Success", message="کاربر با موفقیت افزوده شد")
            refresh()
        
        elif (user in users_list or change_password) and pswd != "" and user != "":
            want_to_change = messagebox.askokcancel(title="Update Info", message=f"آیا میخواهید اطلاعات مربوط به {user} را تغییر دهید؟")
            if want_to_change:
                user_qs = StockData("user")
                pk = user_qs.show_single_query(username=user)[0][2]

                update_user_qs = StockData("user")
                update_user_qs.update(username=user, password=pswd, pk=pk)
                messagebox.showinfo(title="Success", message="اطلاعات کاربر با موفقیت تغییر یافت")
                refresh()


# For stock
def delete(window):
    if window == "S":
        name = stock_name_entry.get()
        _stock = StockData("stock")
        text = _stock.show_single_query(name=name)[0][0]
        try:
            yes_no =  messagebox.askokcancel(title="Delete Alert", message=f"آیا از حذف {text} مطمئن هستید؟")

            if yes_no:
                # Remove from database
                _stock.delete(name=name)
                messagebox.showinfo(title="Success", message="سهم با موفقیت حذف شد")
                refresh()
        except TypeError:
            print("Primary key didn't specefied")
   
    elif window == "U":
        user = user_name_entry.get()
        pswd_check = user_pas_entry.get()
        _user = StockData("user")
        text = _user.show_single_query(username=user)
        try:
            yes_no =  messagebox.askokcancel(title="Delete Alert", message=f"آیا از حذف کاربر {text[0][0]} مطمئن هستید؟")

            if yes_no:
                # Remove from database
                if pswd_check == text[0][1]:
                    _user.delete(username=user)
                    messagebox.showinfo(title="Success", message="کاربر با موفقیت حذف شد")
                    root.destroy()
                    ui()
                else:
                    messagebox.showerror(title="Password Error", message="رمز درست وارد نشده است")    
        except TypeError:
            print("Primary key didn't specefied")
        except IndexError:
            messagebox.showerror(title="Empty fields", message="لطفا فیلد هارا پرکنید")

# For stock
def update():
    name = stock_name_entry.get()
    description = stock_des_entry.get()
    stock_data = StockData('stock')
    pk = stock_data.show_single_query(name=name_stock)[0][2]
    stock_data.update(name=name, description=description, pk=pk)
    master.destroy()
    stock_window()
    messagebox.showinfo(title="Change Success", message="تغییرات با موفقیت اعمال شد")
    root.destroy()
    ui()

# For stock
def edit():
    
    def backward():
        master.destroy()
        stock_window()
    global name_stock
    name_stock = stock_name_entry.get()
    stock_data = StockData("stock")
    s_name = stock_data.show_single_query(name=name_stock)
    
    if s_name != []: 
        master.title("Update stock info")
        stock_label.config(text="ویرایش اطلاعات سهم", fg="green")
        submit_btn.destroy()
        del_btn.destroy()
        edit_btn.destroy()

        _stocks = stock_data.show_single_query(name=name_stock)
        try:
            if _stocks[0][1] != None:
                stock_des_entry.insert(0, _stocks[0][1])
        except TypeError:
            print("Primary key didn't specefied")    

        edit_btn_1 = Button(stock_label, text='ثبت ویرایش', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=update)
        edit_btn_1.grid(row=2, column=1, pady=10, padx=(0, 300))

        edit_btn_2 = Button(stock_label, text='برگشت', bg='red', font=("Helvatica", 10, 'bold'), fg='black', command=backward)
        edit_btn_2.grid(row=2, column=1, pady=10)
    else:
        messagebox.showerror(title="Database Error", message="This query is empty")

# For stock
def stock_window():
    def put_in(*args):
        stock_name = stock_name_combo.get()
        stock_init_des = StockData("stock")
        des = stock_init_des.show_single_query(name=stock_name)
        if des[0][1] != None:
            stock_des_entry.delete(0, END)
            stock_des_entry.insert(0, des[0][1])
        else:
            stock_des_entry.delete(0, END)
        stock_name_entry.delete(0, END)
        stock_name_entry.insert(0, stock_name)
    
    global master
    master = Toplevel(root)
    master.resizable(False, False)
    master.title("Add a Stock")
    master.iconbitmap(resource_path('bot.ico'))
    master.geometry('530x160')
    
    global stock_label
    stock_label = LabelFrame(master, text="اضافه کردن سهم", width=100)
    stock_label.grid(row=0, column=1, padx=30, ipady=8, ipadx=5)

    stock_name_label = Label(stock_label, text="نام سهم", font=("Helvatica", 12))
    stock_name_label.grid(row=0, column=0, pady=10, padx=(10, 0))

    stock_des_label = Label(stock_label, text="توضیحات", font=("Helvatica", 12))
    stock_des_label.grid(row=1, column=0, padx=(10, 0))

    global stock_name_combo
    stock_name_combo = StringVar()
    stock_name_combo.set("سهم را انتخاب کنید")
    stock_drop = ttk.Combobox(stock_label, textvariable=stock_name_combo, values=STOCKS, width=17, height=6)
    stock_drop.grid(row=0, column=1, padx=(280, 0))
    stock_drop.current()
    stock_drop.bind("<<ComboboxSelected>>", put_in)

    global stock_name_entry
    stock_name_entry = Entry(stock_label)
    stock_name_entry.grid(row=0, column=1, padx=70)

    global stock_des_entry
    stock_des_entry = Entry(stock_label)
    stock_des_entry.grid(row=1, column=1, padx=70)

    global submit_btn, show_btn, del_btn, edit_btn
    submit_btn = Button(stock_label, text='افزودن', bg='orange', font=("Helvatica", 10, 'bold'), fg='black', command=lambda: add(stock_name_entry.get(), stock_des_entry.get(), place="E", window="S"), width=5)
    submit_btn.grid(row=2, column=1, pady=5, padx=(100, 0))

    del_btn = Button(stock_label, text='حذف', bg='red', font=("Helvatica", 10, 'bold'), fg='black', command=lambda: delete("S"), width=5)
    del_btn.grid(row=2, column=1, pady=5, padx=(40, 140))

    edit_btn = Button(stock_label, text='ویرایش', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=edit, width=5)
    edit_btn.grid(row=2, column=1, pady=10, padx=(0, 300))


def record_history():
    new = Toplevel(root)
    new.title("RECORDS OF ORDERS")    
    new.geometry("1000x400")
    new.resizable(False, False)
    new.iconbitmap(resource_path('bot.ico'))

    style = ttk.Style()
    # style.theme_use("clam")
    # configure our treeview color
    style.configure("Treeview", 
                    background="white", 
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white")
    style.map("Treeview", 
                background=[("selected", "#4d4d4d")])
 
    record_tree_frame = Frame(new)
    record_tree_frame.grid(row=0, column=1, pady=10)
    
    record_scroll = Scrollbar(record_tree_frame)
    record_scroll.pack(side=RIGHT, fill=Y)

    record_tree = ttk.Treeview(record_tree_frame, yscrollcommand=record_scroll.set)
    record_tree.pack(fill='both')

    # Define our columns
    record_scroll.config(command=record_tree.yview)
    record_tree['columns'] = ('username', "stock's name", 'quantity', "stock's price", 'trade-type', 
                                'trade-date', 'trade-time','start-time', 'end-time')

    # Format our columns
    record_tree.column("#0", width=60, minwidth=10, anchor=W)
    record_tree.column("username", width=120, minwidth=80, anchor=CENTER)                            
    record_tree.column("stock's name", width=80, minwidth=80, anchor=CENTER)                            
    record_tree.column("quantity", width=80, minwidth=30, anchor=CENTER)
    record_tree.column("stock's price", width=80, minwidth=30, anchor=CENTER)
    record_tree.column("trade-type", width=80, minwidth=10, anchor=CENTER)
    record_tree.column("trade-date", width=120, minwidth=20, anchor=CENTER)
    record_tree.column("trade-time", width=120, minwidth=20, anchor=CENTER)
    record_tree.column("start-time", width=120, minwidth=20, anchor=CENTER)
    record_tree.column("end-time", width=120, minwidth=20, anchor=CENTER)

    # Create Heading
    record_tree.heading("#0", text="ID", anchor=CENTER)
    record_tree.heading("username", text="username", anchor=CENTER)
    record_tree.heading("stock's name", text="نام سهم", anchor=CENTER)
    record_tree.heading("quantity", text="تعداد", anchor=CENTER)
    record_tree.heading("stock's price", text="قیمت", anchor=CENTER)
    record_tree.heading("trade-type", text="نوع معامله", anchor=CENTER)
    record_tree.heading("trade-date", text="تاریخ معامله", anchor=CENTER)
    record_tree.heading("trade-time", text="زمان سفارش", anchor=CENTER)
    record_tree.heading("start-time", text="زمان شروع", anchor=CENTER)
    record_tree.heading("end-time", text="زمان پایان", anchor=CENTER)

    trade_type = {"B": "خرید", 
                  "S": "فروش"}

    record_tree.tag_configure("buy", background="#00cc00")
    record_tree.tag_configure("sell", background="#ff4d4d")

    count = 0
    records = StockData('record')
    for record in records.show():
        if record[4] == 'B':
            color_type = "buy",
        else:
            color_type = "sell"

        record_tree.insert(parent="", index="end", iid=count, text=record[9], values=(record[0], record[1], record[2], 
                                                                                        record[3], trade_type[record[4]],
                                                                                        record[5], record[6], record[7], 
                                                                                        record[8]),
                                                                                        tags=(color_type,))
        count += 1                                                                            

        def remove_many(event):
            x = record_tree.selection()
            _x = [int(record_tree.item(i)['text']) for i in x]
            for pk in _x:
                delete_record = StockData('record')
                delete_record.delete(pk=pk)

            for _record in x:
                record_tree.delete(_record)

        def up():
            rows = record_tree.selection()
            for row in rows:
                record_tree.move(row, record_tree.parent(row), record_tree.index(row)-1)

        def down():
            rows = record_tree.selection()
            for row in reversed(rows):
                record_tree.move(row, record_tree.parent(row), record_tree.index(row)+1)


        remove_button = Button(new, text="حذف", bg='#ff0000', fg="black", font=("Helvatica", 13), command=lambda: remove_many(0), width=20)
        remove_button.grid(row=3, column=1)
        record_tree.bind("<Delete>", remove_many)

        move_up = Button(new, text="\U0001F815", font=10, command=up)
        move_up.grid(row=3, column=1, padx=(300, 0))        

        move_down = Button(new, text="\U0001F817", font=10, command=down)
        move_down.grid(row=3, column=1, padx=(0, 300))        


# for main window
def save_info():
    user = str(var_user.get())
    pswd = password_entry.get()
    
    stock = str(var.get())
    check_user = StockData("user")
    
    list_users = check_user.show()
    users_list = [s[0] for s in list_users]

    global _refresh
    _refresh = True
    
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
                user_update.update(username=user, password=pswd, pk=check_user_name[0][2])
                messagebox.showinfo(title="Success", message="اطلاعات با موفقیت تغییر یافت")

        else:
            messagebox.showinfo(title="Same user", message="این نام کاربری قبلا ذخیره شده است")
            _refresh = False
    
    if stock != " ":
        add(stock, description=None, window="M")
    
    password_entry.delete(0, END)
    var_user.set('')
    var.set('')
    if _refresh:
        refresh()

# for main window
def auto_complete(*args):
    user_name = str(var_user.get())
    users = StockData("user")
    related_password = users.show_single_query(username=user_name)[0][1]
    password_entry.delete(0, END)
    password_entry.insert(0, related_password)

# hide the password in main window and user window
def hide(place):
    if place == "M":
        password_entry.config(show=bullet)
        show_password_btn.config(text="show", command=lambda: show(place))
    # we can use else instead of elif    
    elif place == "U":
        user_pas_entry.config(show=bullet)
        show_password.config(text="show", command=lambda: show(place))

# show the password in main window and user window
def show(place):
    if password_entry.get() != "" and place == "M":
        password_entry.config(show="")
        show_password_btn.config(text="hide", command=lambda: hide(place))
    # we can use else instead of elif        
    elif place == "U":
        user_pas_entry.config(show="")
        show_password.config(text="hide", command=lambda: hide(place))

# user profile window
def user_profile():
    def put_in(*args):
        user_name = user_name_combo.get()
        user_init = StockData("user")
        user_data = user_init.show_single_query(username=user_name)
        
        user_name_entry.delete(0, END)
        user_name_entry.insert(0, user_name)

        user_pas_entry.delete(0, END)
        user_pas_entry.insert(0, user_data[0][1])
        
    
    main = Toplevel(root)
    main.title("User Profile")
    main.iconbitmap(resource_path('bot.ico'))
    main.geometry("560x220")

    global user_label
    user_label = LabelFrame(main, text="تغییر نام کاربری", width=100)
    user_label.grid(row=0, column=1, padx=30, ipady=8, ipadx=5)

    user_name_emoji = Label(user_label, text="\U0001F464", font=("Helvatica", 50, "bold"), bg="grey", fg="white")
    user_name_emoji.grid(row=0, column=0, pady=10, padx=(10, 0))

    stock_name_label = Label(user_label, text="username", font=("Helvatica", 10, "italic"), fg="red")
    stock_name_label.grid(row=0, column=1, pady=10, padx=(10, 0))

    stock_des_label = Label(user_label, text="password", font=("Helvatica", 10, "italic"), fg="red")
    stock_des_label.grid(row=1, column=1, padx=(10, 0))

    global user_name_combo
    user_name_combo = StringVar()
    user_name_combo.set(" Choose ...")
    user_drop = ttk.Combobox(user_label, textvariable=user_name_combo, values=user_info, width=17, height=6)
    user_drop.grid(row=0, column=2, padx=(200, 0))
    user_drop.current()
    user_drop.bind("<<ComboboxSelected>>", put_in)

    global user_name_entry
    user_name_entry = Entry(user_label, justify=CENTER)
    user_name_entry.grid(row=0, column=2, padx=(0, 90))

    global user_pas_entry
    user_pas_entry = Entry(user_label, justify=CENTER, show=bullet)
    user_pas_entry.grid(row=1, column=2, padx=(0, 90))

    global show_password
    show_password = Button(user_label, text="show", relief=SUNKEN, bd=0, fg="blue", command=lambda: show("U"))
    show_password.grid(row=1, column=2, padx=(100, 0))

    
    add_btn = Button(user_label, text='افزودن', bg='orange', font=("Helvatica", 10, 'bold'), fg='black', command=lambda: add(user_name_entry.get(), user_pas_entry.get(), window="U"), width=5)
    add_btn.grid(row=2, column=2, pady=5, padx=(100, 0))

    delete_btn = Button(user_label, text='حذف', bg='red', font=("Helvatica", 10, 'bold'), fg='black', command=lambda: delete("U"), width=5)
    delete_btn.grid(row=2, column=2, pady=5, padx=(40, 140))

    edit_pswd_btn = Button(user_label, text='ویرایش رمز', bg='yellow', font=("Helvatica", 10, 'bold'), fg='black', command=lambda: add(user_name_entry.get(), user_pas_entry.get(), window="U", change_password=True), width=8)
    edit_pswd_btn.grid(row=2, column=2, pady=10, padx=(0, 300))

   
# main window of application
def ui():
    global root
    root = Tk()
    root.title("Stock Bot")
    root.resizable(False, False)
    root.iconbitmap(resource_path('bot.ico'))
    root.geometry('440x450')
    user_label = Label(root, text="username", font=("Helvatica", 10), fg='red')
    user_label.grid(row=0, column=0, padx=50, pady=15)

    global var_user, user_info
    var_user = StringVar()
    _users = StockData('user')
    user_info = [s[0] for s in _users.show()]    

    user_entry = ttk.Combobox(root, width=17, textvariable=var_user, values=user_info, height=5)
    user_entry.grid(row=0, column=1)
    user_entry.current()
    user_entry.bind("<<ComboboxSelected>>", auto_complete)


    password_label = Label(root, text="password", font=("Helvatica", 10), fg='red')
    password_label.grid(row=1, column=0)

    global password_entry, bullet
    bullet = "\u2022"
    password_entry = Entry(root, show=bullet, justify=CENTER)
    password_entry.grid(row=1, column=1, padx=70)

    global show_password_btn 
    show_password_btn = Button(root, text="show", relief=SUNKEN, bd=0, fg="blue", command=lambda: show('M'))
    show_password_btn.grid(row=1, column=1, padx=(0, 200))

    stock_label_1 = Label(root, text="نماد سهم", font=("Helvatica", 10))
    stock_label_1.grid(row=2, column=0, pady=10)

    
    global var, STOCKS
    _stocks = StockData("stock")
    STOCKS = [s[0] for s in _stocks.show()]
    var = StringVar()
    var.set("")
    stock_drop = ttk.Combobox(root, textvariable=var, values=STOCKS, width=17, height=6)
    stock_drop.grid(row=2, column=1)
    stock_drop.current()
    
    
    stock_description = Button(root, text='edit', font=("Helvatica", 10), fg='green', relief=SUNKEN,command=stock_window, bd=0, cursor="hand2")
    stock_description.grid(row=2, column=1, padx=(0, 200))

    stock_price_label = Label(root, text="قیمت سهم (ريال)", font=("Helvatica", 10))
    stock_price_label.grid(row=3, column=0, pady=10)

    global stock_price_entry
    stock_price_entry = Entry(root, justify=CENTER)
    stock_price_entry.grid(row=3, column=1, padx=70)

    stock_quantity_label = Label(root, text="تعداد", font=("Helvatica", 10))
    stock_quantity_label.grid(row=4, column=0, pady=10)

    global stock_quantity_entry
    stock_quantity_entry = Entry(root, justify=CENTER)
    stock_quantity_entry.grid(row=4, column=1, padx=70)

    guid = Label(root, text="زمان را به صورت 01:10:03 وارد کنید", font=("Helvatica", 10, 'bold'), fg="red")
    guid.grid(row=5, column=0)

    start_time_label = Label(root, text="ساعت شروع", font=("Helvatica", 10))
    start_time_label.grid(row=6, column=0, pady=10)

    global start_time_entry
    start_time_entry = Entry(root, justify=CENTER)
    start_time_entry.grid(row=6, column=1, padx=70)

    end_time_label = Label(root, text="ساعت پایان", font=("Helvatica", 10))
    end_time_label.grid(row=7, column=0, pady=10)

    global end_time_entry
    end_time_entry = Entry(root, justify=CENTER)
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

    buy_btn = Button(root, text='خرید', bg='green', font=("Helvatica", 10), fg='black', command=lambda: order('B'), width=5)
    buy_btn.grid(row=10, column=0, pady=10)

    sell_btn = Button(root, text='فروش', bg='red', font=("Helvatica", 10), fg='black', command=lambda: order('S'), width=5)
    sell_btn.grid(row=10, column=1)

    save_btn = Button(root, text='ذخیره اطلاعات', bg='grey', font=("Helvatica", 10), fg='black', command=save_info, width=10)
    save_btn.grid(row=10, column=1, padx=(0, 250))

    menubar = Menu(root)
    
    _file = Menu(menubar, tearoff=0)
    _file.add_command(label="Refresh           \U0001F504", command=refresh)
    _file.add_command(label="Save info        \U0001F4BE", command=save_info)
    _file.add_command(label="Records          \U0000241E", command=record_history)
    _file.add_separator()
    _file.add_command(label="Exit                 \U0000274C", command=lambda: root.destroy())
    menubar.add_cascade(label="File", menu=_file)

    tab = Menu(menubar, tearoff=0)
    tab.add_command(label="ویرایش نام کاربری   \U0001F464", command=lambda: threading.Thread(target=user_profile).start())
    tab.add_command(label="ویرایش سهم    \U0001F58A", command=lambda: threading.Thread(target=stock_window).start())
    menubar.add_cascade(label="Edit", menu=tab)
    
    root.config(menu=menubar)
    root.mainloop()

ui()
