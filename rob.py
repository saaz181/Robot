from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import datetime as dt
from itertools import cycle
import logging

logging.basicConfig(filename='robot.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: make GUI
# TODO: make usernames & passwords dynamic
username = ''
password = ''


def time(start, end, current):
    if (current >= start) and (current <= end):
        return True
    return False


def waiting_dot():
    n_points = 10
    points_l = ['.' * i + ' ' * (n_points - i) + '\r' for i in range(n_points)]
    count = 0
    for points in cycle(points_l):
        print(points, end='')
        sleep(0.0000001)
        count += 1
        if count == 100:
            break


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

    # Passing username
    driver.find_element_by_xpath('//*[@id="Username"]').send_keys(username)
    sleep(1)
    # Passing password
    driver.find_element_by_xpath('//*[@id="Password"]').send_keys(password)

    try:
        sleep(5)   # CAPTCHA time delay TODO: find better time limit if exists one

        # clicking on log-in button
        driver.find_element_by_xpath('//*[@id="submit_btn"]').click()

        driver.switch_to.window(window_before)

        # Passing through the junk pages
        sleep(4)
        driver.find_element_by_xpath('//*[@id="intro-mask"]/div[1]/div[13]').click()
    except NoSuchElementException as e:
        logging.error("Captcha didn't entered")
        print(e.msg)
        driver.quit()
        call()

    sleep(1)
    driver.find_element_by_xpath('//*[@id="intro-skip"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="siteVersionContainer"]/div/div[1]/span[2]').click()


def stock_search():
    stocks = ['ثامید1', 'شستا1']

    count = 0
    try:
        for stock in stocks:
            _search = driver.find_element_by_xpath('//*[@id="stockAutocomplete-container-sendorder"]')
            search_icon = _search.find_element_by_css_selector('#btnSearchStockAutoComplete > span')
            if count > 0:
                search_icon.click()
                sleep(2)

            # search for stock
            search = driver.find_element_by_xpath("//input[@placeholder='جستجوی سهم']")
            if count == 0:
                search.click()

            search.send_keys(stock)
            sleep(1)
            search.send_keys(Keys.ARROW_DOWN)
            search.send_keys(Keys.RETURN)

            trade()
            count += 1

    except ElementNotInteractableException as e:
        print(e.msg)
        # driver.quit()


def trade():
    # website is automatically set to buy option so we just
    # need to define sell option
    sell = driver.find_element_by_xpath('//*[@id="sendorder-container"]/div[1]/div[2]/div')
    if trade_type == 's':
        sell.click()
        sleep(1)

    sleep(3)
    # passing quantity
    driver.find_element_by_xpath('//*[@id="send_order_txtCount"]').send_keys(quantity)
    sleep(1)
    # passing price
    driver.find_element_by_xpath('//*[@id="send_order_txtPrice"]').send_keys(price)
    # sell or buy button
    sleep(1)
    driver.find_element_by_xpath('//*[@id="send_order_btnSendOrder"]').click()

    sleep(1)
    driver.find_element_by_xpath('//*[@id="sendorder_ModalConfirm_btnCancel"]').click()


def start_trading():
    global driver
    # In order to disable notification we use "webdriver.ChrimeOption" to pass the options we want to use
    chrome_options = webdriver.ChromeOptions()
    # disable chrome notification command
    prefs = {"profile.default_content_setting_values.notifications": 2}
    # passing the argument to our chrome driver
    chrome_options.add_experimental_option("prefs", prefs)

    PATH = r"E:\IDMs\chromedriver.exe"  # path to webdriver location on PC
    # starting driver
    driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)

    log_in()
    stock_search()


def call():
    global trade_type, quantity, price
    trade_type = str(input(f"Do you want to sell or buy [s, b]? "))
    buy_sell = "buy"
    if trade_type == 's' or trade_type == 'S':
        buy_sell = "sell"
    quantity = int(input(f"How many you wanna {buy_sell}: "))
    price = int(input("In what price: "))

    if price % 10 != 0:
        print("Your price should be from 10x please Enter again the price ...")
        call()
    elif (price * quantity < 5000000) and (trade_type == "b"):
        print("You can't buy less than 5,000,000 ريال")
        call()
    else:

        time_correct_format = True
        while time_correct_format:
            try:
                # getting start time
                start_time = dt.datetime.strptime(input("Enter your start time in HH:MM format: "), "%H:%M").strftime("%H:%M")
                # getting end time
                end_time = dt.datetime.strptime(input("Enter your end time in HH:MM format: "), "%H:%M").strftime("%H:%M")
                time_correct_format = False
            except ValueError:
                print("You need to enter the time in correct format")

        # current time
        current_time = dt.datetime.now().time().strftime("%H:%M")

        print("Bot is starting ")
        waiting_dot()

        # start threading for multiple users
        if time(start_time, end_time, current_time):
            start_trading()
        else:
            print("In your time period this action can't be done\nplease Specify other time period\n")


if __name__ == '__main__':
    call()
