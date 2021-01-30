from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import datetime as dt
import logging
from tkinter import *
from tkinter import messagebox
import sys
import os
import threading
from tsetmc import Time

"""
This program can be initial multiple bots together but if only we open new program for it
like we click on the "robot.py" and open two terminal and in which we type our username & password
and the bot will do the algorithm

ALGORITHM: 
    1 - start buying/selling from start time to the end time
    2 - when we bought/sold the stock the bot should break out or goto other stock
    3 - we must make sure that as the bot buys/sells the stock doesn't buy/sell it again
    
"""


# For .exe file
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Using logging module to see what error did we encountered
logging.basicConfig(filename='robot.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


def clear():
    stock_price_entry.delete(0, END)
    stock_quantity_entry.delete(0, END)
    cost_label.configure(text="0")


def clear_all():
    stock_price_entry.delete(0, END)
    stock_quantity_entry.delete(0, END)


def buy():
    global username, password, stock, stock_price, stock_quantity, start_time, end_time, trade_type
    username = user_entry.get()
    password = password_entry.get()
    stock = stock_entry.get()
    stock_price = stock_price_entry.get()
    stock_quantity = stock_quantity_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    trade_type = 'b'

    if username == '' or password == '' or stock == '' or stock_price == '' or stock_quantity == '' or start_time == '' \
            or end_time == '':
        messagebox.showerror(title="Empty form field", message="لطقا همه فیلد هارا پر کنید")

    else:

        try:
            start_time = dt.datetime.strptime(start_time_entry.get(), "%H:%M:%S")
            end_time = dt.datetime.strptime(end_time_entry.get(), "%H:%M:%S")
            time_bool = True
        except ValueError:
            time_bool = False
            messagebox.showerror(title="Time Format",
                                 message="لطفا زمان را به صورت 24 ساعت وارد کنید و به فرمت\n 01:23 وارد کنید")

        try:
            if stock_price != '' and stock_quantity != '' and int(stock_price) % 10 == 0 and time_bool:
                total_price = int(stock_price_entry.get()) * int(stock_quantity_entry.get())
                text = "{:,}".format(total_price) + " ريال "
                cost_label.configure(text=text)
        except ValueError:
            messagebox.showerror(title="Number Failure", message="لطفا قیمت و تعداد را با عدد وارد کنید")

        buy_message = messagebox.askokcancel(title="Price Check", message=f"از خرید خود به مبلغ {text} اطمینان دارید؟")
        if buy_message == True:
            clear_all()
            threading.Thread(target=call).start()


def sell():
    global username, password, stock, stock_price, stock_quantity, start_time, end_time, trade_type
    username = user_entry.get()
    password = password_entry.get()
    stock = stock_entry.get()
    stock_price = stock_price_entry.get()
    stock_quantity = stock_quantity_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    trade_type = 's'

    if username == '' or password == '' or stock == '' or stock_price == '' or stock_quantity == '' or start_time == '' \
            or end_time == '':
        messagebox.showerror(title="Empty form field", message="لطقا همه فیلد هارا پر کنید")

    else:
        start_time = dt.datetime.strptime(start_time_entry.get(), "%H:%M:%S")
        end_time = dt.datetime.strptime(end_time_entry.get(), "%H:%M:%S")

        if stock_price != '' and stock_quantity != '' and int(stock_price) % 10 == 0:
            total_price = int(stock_price_entry.get()) * int(stock_quantity_entry.get())
            text = "{:,}".format(total_price) + " ريال "
            cost_label.configure(text=text)

        sell_message = messagebox.askokcancel(title="Price Check", message=f"از فروش خود به مبلغ {text} اطمینان دارید؟")
        if sell_message == True:
            clear_all()
            threading.Thread(target=call).start()


def ui():
    root = Tk()
    root.title("Stock Bot")
    root.resizable(False, False)
    root.iconbitmap(resource_path('bot.ico'))
    root.geometry('400x400')
    user_label = Label(root, text="username", font=("Helvatica", 10), fg='red')
    user_label.grid(row=1, column=1, padx=50, pady=15)

    global user_entry
    user_entry = Entry(root)
    user_entry.grid(row=1, column=2)

    password_label = Label(root, text="password", font=("Helvatica", 10), fg='red')
    password_label.grid(row=2, column=1)

    global password_entry
    password_entry = Entry(root)
    password_entry.grid(row=2, column=2, padx=70)

    stock_label = Label(root, text="نماد سهم", font=("Helvatica", 10))
    stock_label.grid(row=3, column=1, pady=10)

    global stock_entry
    stock_entry = Entry(root)
    stock_entry.grid(row=3, column=2, padx=70)

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

    guid = Label(root, text="زمان را به صورت 23:23:23 وارد کنید", font=("Helvatica", 10, 'bold'), fg="red")
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

    global cost_label
    cost_label = Label(root, text="0")
    cost_label.grid(row=9, column=2)

    cost_label_text = Label(root, text="قیمت کل خرید/فروش", fg='red')
    cost_label_text.grid(row=9, column=1)

    buy_btn = Button(root, text='خرید', bg='green', font=("Helvatica", 10), fg='black', command=buy, width=5)
    buy_btn.grid(row=10, column=1, pady=10)

    sell_btn = Button(root, text='فروش', bg='red', font=("Helvatica", 10), fg='black', command=sell, width=5)
    sell_btn.grid(row=10, column=2)

    root.mainloop()


# This function checks that our current time is in the our start time and our end time
def time(start, end, current):
    start = start.strftime("%H:%M:%S")
    end = end.strftime("%H:%M:%S")
    if (start >= current) and (current <= end) and (start < end):
        return True
    return False


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
        call()

    try:
        # Passing through the junk pages
        driver.find_element_by_xpath('//*[@id="intro-mask"]/div[1]/div[13]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="intro-skip"]').click()
        sleep(0.5)
        driver.find_element_by_xpath('//*[@id="siteVersionContainer"]/div/div[1]/span[2]').click()

    except ElementNotInteractableException:
        logging.info("Slow Internet Connection -> couldn't load the main page")
        driver.quit()
        call()

    except NoSuchElementException:
        logging.info("Wrong Password or username")
        driver.quit()
        messagebox.showwarning(title="CAPTCHA", message="Please enter the CAPTCHA next time")
        # length -= 12
        call()


def stock_search():
    try:
        # for loop use for sth else here
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
        call()


def trade():
    # website is automatically set to buy option so we just
    # need to define sell option
    sell = driver.find_element_by_xpath('//*[@id="sendorder-container"]/div[1]/div[2]/div')
    if trade_type == 's':
        sell.click()
        sleep(1)

    sleep(3)

    # passing quantity
    driver.find_element_by_xpath('//*[@id="send_order_txtCount"]').send_keys(stock_quantity)
    sleep(1)

    # passing price
    driver.find_element_by_xpath('//*[@id="send_order_txtPrice"]').send_keys(stock_price)

    robot_trade()


# **** main function which do the trade ***
def robot_trade():
    # How many times to click on buy/sell button
    length = (end_time - start_time).seconds

    now_time = Time()
    # time to wait until time occurs
    length_wait = (start_time - now_time.__str__()).seconds

    sleep(length_wait - 2)
    for _ in range(length):
        # sell or buy button ** which the path is the same **
        sleep(0.3)
        driver.find_element_by_xpath('//*[@id="send_order_btnSendOrder"]').click()

        # press the final button
        sleep(0.3)
        driver.find_element_by_xpath('//*[@id="sendorder_ModalConfirm_btnSendOrder"]').click()

    driver.quit()
    messagebox.showinfo(title="success", message="Trade completed")


def start_trading():
    global driver

    # In order to disable notification we use "webdriver.ChrimeOption" to pass the options we want to use
    chrome_options = webdriver.ChromeOptions()
    # disable chrome notification command
    prefs = {"profile.default_content_setting_values.notifications": 2}
    # passing the argument to our chrome driver
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-ssl-errors=yes')

    # path to web driver location on PC TODO:make it dynamic

    PATH = resource_path("chromedriver.exe")
    # starting driver
    driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)

    log_in()  # Initializing the login function
    stock_search()  # Initializing the stock search function


# call the trade function
def call():
    # because in stock market price is from 10x
    if int(stock_price) % 10 != 0:
        messagebox.showerror(title="Price Error",
                             message="Your price should be from 10x please Enter again the price ...")
        clear()
    # we can't order buy under 5,000,000 RIALS
    elif (int(stock_price) * int(stock_quantity) < 5000000) and (trade_type == "b"):
        messagebox.showerror(title="Underprice", message="You can't buy less than 5,000,000 ريال")
        clear()
    else:
        # current time
        current_time = Time().__str__().strftime("%H:%M:%S")

        # check if our current time is in the our start and end time
        if time(start_time, end_time, current_time):
            print("Bot started ... ")
            start_trading()
        else:
            messagebox.showerror(title="TIME Error",
                                 message="Please Enter the time correctly")
            logging.error("Current time is NOT in time period")


if __name__ == '__main__':
    # Calling the main function to start all the functions
    ui()
