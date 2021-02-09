from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, NoSuchWindowException
import datetime as dt
import logging
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sys
import os
import threading
from data import StockData

"""
This program can be initial multiple bots together but if only we open new program for it
like we click on the "robot.py" and open two terminal and in which we type our username & password
and the bot will do the algorithm

ALGORITHM: 
    1 - start buying/selling from start time to the end time
    2 - when we bought/sold the stock the bot should break out or goto other stock
    3 - we must make sure that as the bot buys/sells the stock doesn't buy/sell it again
        (which in this program isn't necessary)
    
"""


# For .exe file "PyInstaller" module and finding files easily
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

# Using logging module to see what error did we encountered
logging.basicConfig(filename=resource_path('robot.log'), filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Clear price, quantity and total price
def clear():
    stock_price_entry.delete(0, END)
    stock_quantity_entry.delete(0, END)
    cost_label.configure(text="0")

# Clear price & quantity
def clear_all():
    stock_price_entry.delete(0, END)
    stock_quantity_entry.delete(0, END)

# our buy button "green one"
def order(type):
    global username, password, stock, stock_price, stock_quantity, start_time, end_time, delay, trade_type
    username = user_entry.get()  # username entry field string
    password = password_entry.get()  # password entry field string
    stock = stock_entry.get()  # stock entry field "don't need to change language" string
    stock_price = stock_price_entry.get()  # price of a stock entry field string
    stock_quantity = stock_quantity_entry.get()  # quantity of a stock entry field string
    start_time = start_time_entry.get()  # what time to start entry field string
    end_time = end_time_entry.get()  # what time to finish entry field string
    try:
        delay = int(delay_between_order.get())  # Delay between each order
    except ValueError:
        messagebox.showerror(title="Base 10 Error", message="لطفا اعداد را به صورت صحیح و غیر اعشاری وارد کنید")
    trade_type = type  # specifying the type of our trade which is BUY

    type_value = {"s": 'فروش', "b": "خرید"}

    if username == '' or password == '' or stock == '' or stock_price == ''\
            or stock_quantity == '' or start_time == '' or end_time == '':

        messagebox.showerror(title="Empty form field", message="لطقا همه فیلد هارا پر کنید")

    else:
        # time_bool variable is for checking if they enter time correctly
        # proceed variable is for not encounter the last message box
        proceed = True

        try:
            start_time = dt.datetime.strptime(start_time_entry.get(), "%H:%M:%S")  # parse into datetime format
            end_time = dt.datetime.strptime(end_time_entry.get(), "%H:%M:%S")  # parse into datetime format
            time_bool = True

        except ValueError:
            time_bool = False
            proceed = False
            messagebox.showerror(title="Time Format",
                                 message="لطفا زمان را به صورت 12 ساعته وارد کنید و به فرمت درست وارد کنید")

        text = ""
        try:
            if time_bool:
                if stock_price != '' and stock_quantity != '':
                    total_price = int(stock_price_entry.get()) * int(stock_quantity_entry.get())
                    text = "{:,}".format(total_price) + " ريال "
                    cost_label.configure(text=text)

                if int(stock_price) % 10 != 0:
                    pass_ten_base = messagebox.askyesno(title="Price Error",
                                                        message="قیمت باید مضربی از 10 باشد میخواهید ادامه دهید")
                    if pass_ten_base:
                            proceed = True

                # we can't order buy under 5,000,000 RIALS
                if (trade_type == "b"):
                    if (int(stock_price) * int(stock_quantity) < 5000000):
                        messagebox.showerror(title="Underprice", message="خرید کمتر از 5,000,000 ريال ممکن نیست")
                        clear()
                        proceed = False

        except ValueError:
            messagebox.showerror(title="Number Failure", message="لطفا قیمت و تعداد را با عدد وارد کنید")
            proceed = False

        if proceed:
            trade_message = messagebox.askokcancel(title="Price Check",
                                                   message=f"از {type_value[type]} خود به مبلغ {text} اطمینان دارید؟")
            if trade_message:  # check for our messagebox value
                clear_all()
                # running bot separately from our GUI
                threading.Thread(target=start_trading).start()


# ***** #
# hiding the password entry
def hide():
    password_entry.config(show="*")
    show_password_btn.config(text="show password", command=show)
# showing the password entry
def show():
    if password_entry.get() != "":
        password_entry.config(show="")
        show_password_btn.config(text="hide password", command=hide)
# ***** #

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



# saving the username and password and the stock's name into database
def save_info():
    user = user_entry.get() # getting username combo value
    pswd = password_entry.get()  # getting password combo value
    stock = str(stock_entry.get()) # getting stock combo value

    check_user = StockData("user")  # connect to database
    
    list_users = check_user.show()

    users_list = [s[0] for s in list_users]
    pswds_list = [s[1] for s in list_users]
    
    # check if user not already saved and password isn't empty
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
        
    add(stock, description=None)
    
    password_entry.delete(0, END)
    user_entry.set('')
    stock_entry.set('')

# will fill the password field with related username
def auto_complete(*args):
    user_name = str(user_entry.get())
    users = StockData("user")
    related_password = users.show_single_query(username=user_name)[0][1]
    password_entry.delete(0, END)
    password_entry.insert(0, related_password)


# our GUI function which runs separately from TRADEs functions
def ui():
    global root
    root = Tk()
    root.title("Stock Bot")
    root.resizable(False, False)
    root.iconbitmap(resource_path('bot.ico'))
    root.geometry('440x450')
    user_label = Label(root, text="username", font=("Helvatica", 10), fg='red')
    user_label.grid(row=1, column=1, padx=50, pady=15)

    _users = StockData('user')  # connecting to users table
    user_info = [s[0] for s in _users.show()]
    global user_entry
    user_entry = StringVar()

    username_combo = ttk.Combobox(root, width=17, textvariable=user_entry, values=user_info, height=5)
    username_combo.grid(row=0, column=1)
    username_combo.current()
    username_combo.bind("<<ComboboxSelected>>", auto_complete)
    username_combo.grid(row=1, column=2)

    password_label = Label(root, text="password", font=("Helvatica", 10), fg='red')
    password_label.grid(row=2, column=1)

    global password_entry
    password_entry = Entry(root, show="*")
    password_entry.grid(row=2, column=2, padx=70)

    global show_password_btn 
    show_password_btn = Button(root, text="show password", relief=SUNKEN, bd=0, fg="blue", command=show)
    show_password_btn.grid(row=2, column=2, padx=(0, 250))

    stock_label = Label(root, text="نماد سهم", font=("Helvatica", 10))
    stock_label.grid(row=3, column=1, pady=10)

    _stocks = StockData("stock")  # connecting to stocks table
    STOCKS = [s[0] for s in _stocks.show()]
    global stock_entry
    
    stock_entry = StringVar()
    stock_entry.set("")    
    stock_drop = ttk.Combobox(root, textvariable=stock_entry, values=STOCKS, width=17, height=8)
    stock_drop.grid(row=3, column=2)
    stock_drop.current()
    
    stock_description = Button(root, text='Edit', font=("Helvatica", 10), fg='green', relief=SUNKEN,command=stock_window, bd=0, cursor="hand2")
    stock_description.grid(row=3, column=2, padx=(0, 200))

    stock_price_label = Label(root, text="قیمت سهم (ريال)", font=("Helvatica", 10))
    stock_price_label.grid(row=4, column=1, pady=10)

    global stock_price_entry
    stock_price_entry = Entry(root)
    stock_price_entry.grid(row=4, column=2, padx=70)

    stock_quantity_label = Label(root, text="تعداد", font=("Helvatica", 10))
    stock_quantity_label.grid(row=5, column=1, pady=10)

    global stock_quantity_entry
    stock_quantity_entry = Entry(root)
    stock_quantity_entry.grid(row=5, column=2, padx=70)

    guid = Label(root, text="زمان را به صورت 01:10:03 وارد کنید", font=("Helvatica", 10, 'bold'), fg="red")
    guid.grid(row=6, column=1)

    start_time_label = Label(root, text="ساعت شروع", font=("Helvatica", 10))
    start_time_label.grid(row=7, column=1, pady=10)

    global start_time_entry
    start_time_entry = Entry(root)
    start_time_entry.grid(row=7, column=2, padx=70)

    end_time_label = Label(root, text="ساعت پایان", font=("Helvatica", 10))
    end_time_label.grid(row=8, column=1, pady=10)

    global end_time_entry
    end_time_entry = Entry(root)
    end_time_entry.grid(row=8, column=2, padx=70)

    delay_between_order_label = Label(root, text="فاصله بین  هر سفارش (میلی ثانیه)", fg="red")
    delay_between_order_label.grid(row=9, column=1, pady=10)

    global delay_between_order
    delay_between_order = Spinbox(root, from_=300, to=1000, justify=CENTER, width=10)
    delay_between_order.grid(row=9, column=2, pady=10)

    global cost_label
    cost_label = Label(root, text="0")
    cost_label.grid(row=10, column=2)

    cost_label_text = Label(root, text="قیمت کل خرید/فروش", fg='red')
    cost_label_text.grid(row=10, column=1)

    buy_btn = Button(root, text='خرید', bg='green', font=("Helvatica", 10), fg='black', command=lambda: order('b'), width=5)
    buy_btn.grid(row=11, column=1, pady=10)

    sell_btn = Button(root, text='فروش', bg='red', font=("Helvatica", 10), fg='black', command=lambda: order('s'), width=5)
    sell_btn.grid(row=11, column=2)

    save_btn = Button(root, text='ذخیره اطلاعات', bg='grey', font=("Helvatica", 10), fg='black', command=save_info, width=10)
    save_btn.grid(row=11, column=2, padx=(0, 250))


    root.mainloop()


def log_in():  # Function which handles the log-in stuff

    # Website which has login page
    driver.get('https://online.emofid.com/Login')

    window_before = driver.window_handles[0]

    # we need to go to other page to log-in so we need to click in another button
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div').click()

    # waiting for the other page to load up
    sleep(1)

    # we need to switch between windows
    window_after = driver.window_handles[1]

    # switching to page page
    driver.switch_to.window(window_after)

    try:
        # Passing username
        driver.find_element_by_xpath('//*[@id="Username"]').send_keys(username)
        sleep(1)
        # Passing password
        driver.find_element_by_xpath('//*[@id="Password"]').send_keys(password)

        # CAPTCHA time delay
        sleep(11)

        # clicking on log-in button
        driver.find_element_by_xpath('//*[@id="submit_btn"]').click()

        driver.switch_to.window(window_before)
        sleep(4)

    except NoSuchElementException:
        logging.error("Captcha didn't entered")
        driver.quit()
        start_trading()

    try:
        # Passing through the junk pages
        driver.find_element_by_xpath('//*[@id="intro-mask"]/div[1]/div[13]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="intro-skip"]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="siteVersionContainer"]/div/div[1]/span[2]').click()

    except ElementNotInteractableException:  # if there is slow internet connection, this error will occur
        logging.info("Slow Internet Connection -> couldn't load the main page")
        driver.quit()
        start_trading()

    except NoSuchElementException:  # if captcha doesn't enter, this exception will occur
        logging.info("Wrong Password or username")
        driver.quit()
        messagebox.showwarning(title="CAPTCHA", message="لطفا کد کپچا را وارد کنید!")
        start_trading()


def stock_search():
    try:
        # pressing search icon to enter our stock's name
        _search = driver.find_element_by_xpath('//*[@id="stockAutocomplete-container-sendorder"]')
        search_icon = _search.find_element_by_css_selector('#btnSearchStockAutoComplete > span')

        search_icon.click()
        sleep(1)

        # enter into our search field
        search = driver.find_element_by_xpath("//input[@placeholder='جستجوی سهم']")

        search.send_keys(stock)
        sleep(2)

        # Choosing our stock from dropdown box
        search.send_keys(Keys.ARROW_DOWN)
        search.send_keys(Keys.RETURN)

        trade()  # trade function

    except ElementNotInteractableException as e:
        logging.info(e.msg)
        driver.quit()
        start_trading()


def trade():
    # website is automatically set to buy option so we just need to define sell option
    sell = driver.find_element_by_xpath('//*[@id="sendorder-container"]/div[1]/div[2]/div')
    if trade_type == 's':
        sell.click()
        sleep(1)

    sleep(3)

    # How many times to click on buy/sell button
    length = (end_time - start_time).seconds + 10

    # Getting time from website we crawling
    now_time = driver.find_element_by_xpath(
        '/html/body/app-container/app-content/div/div/div/div[3]/div[2]/'
        'div/div/widget/div/div/div/div[2]/send-order/div/div[7]/div[2]/div[2]/clock')

    # Convert into 12h clock
    current_time = dt.datetime.strptime(now_time.text, "%H:%M:%S").strftime("%I:%M:%S")

    # time to wait until time occurs
    length_wait = (start_time - dt.datetime.strptime(current_time, "%H:%M:%S")).seconds

    # passing quantity
    driver.find_element_by_xpath('//*[@id="send_order_txtCount"]').send_keys(stock_quantity)
    sleep(1)
    # passing price
    driver.find_element_by_xpath('//*[@id="send_order_txtPrice"]').send_keys(stock_price)
    
    sleep(length_wait - 5)

    # Calling the main function of our program 'robot_trade'
    robot_trade(length)


# **** main function which do the trade ***
def robot_trade(trade_time):

    _quit = True
    # sell or buy button
    order_btn = driver.find_element_by_xpath('//*[@id="send_order_btnSendOrder"]')
    for _ in range(trade_time * 4):
        try:
            sleep(delay / 1000)  # delay time between each order
            # sell or buy button ** which the path is the same **
            order_btn.click()

        except AttributeError:
            messagebox.showinfo(title="Window closed", message="مرورگر توسط کاربر بسته شد")
            _quit = False

        except NoSuchWindowException:
            messagebox.showinfo(title="Window closed", message="مرورگر توسط کاربر بسته شد")
            _quit = False

        except:
                # Getting time from website we crawling
                now_time = driver.find_element_by_xpath(
                    '/html/body/app-container/app-content/div/div/div/div[3]/div[2]/div/div/'
                    'widget/div/div/div/div[2]/send-order/div/div[7]/div[2]/div[2]/clock')

                # Convert into 12h clock
                current_time = dt.datetime.strptime(now_time.text, "%H:%M:%S").strftime("%I:%M:%S")

                length = (end_time - dt.datetime.strptime(current_time, "%H:%M:%S")).seconds
                robot_trade(length)

    if _quit:
        driver.quit()
    messagebox.showinfo(title="success", message="Trade completed")

# *** end of our main function of program ***


def start_trading():
    global driver

    # In order to disable notification we use "webdriver.ChrimeOption" to pass the options we want to use
    chrome_options = webdriver.ChromeOptions()
    # disable chrome notification command
    prefs = {"profile.default_content_setting_values.notifications": 2}
    # passing the argument to our chrome driver
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--ignore-certificate-errors')  # disable chrome security alerts
    chrome_options.add_argument('--allow-insecure-localhost')  # allow 'chromedriver' to run on localhost
    chrome_options.add_argument('--ignore-ssl-errors=yes')  # disable SSL security of chrome browser

    PATH = resource_path("chromedriver.exe")
    # starting driver
    driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)
    print(delay / 1000)

    log_in()  # Initializing the login function
    stock_search()  # Initializing the stock search function


if __name__ == '__main__':
    # Calling the GUI function to start all the functions
    ui()
