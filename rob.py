from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

PATH = r"E:\IDMs\chromedriver.exe"  # path to webdriver location on PC

# TODO: make usernames & passwords dynamic
username = '0780885651'
password = 'Hossein1374'

trade_type = str(input(f"Do you want to sell or buy ? [s, b]? "))
quantity = int(input(f"How much you wanna buy from : "))
price = int(input(f"In what price of : "))

# In order to disable notification we use "webdriver.ChrimeOption" to pass the options we want to use
chrome_options = webdriver.ChromeOptions()

# disable chrome notification command
prefs = {"profile.default_content_setting_values.notifications": 2}

# passing the argument to our chrome driver
chrome_options.add_experimental_option("prefs", prefs)

# starting driver
driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)


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

    sleep(5)   # CAPTCHA time delay TODO: find better time limit if exists one

    # clicking on log-in button
    driver.find_element_by_xpath('//*[@id="submit_btn"]').click()

    driver.switch_to.window(window_before)


def stock_search():
    stocks = ['ثامید1', 'شستا1']

    # Passing through the junk pages
    sleep(4)
    driver.find_element_by_xpath('//*[@id="intro-mask"]/div[1]/div[13]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="intro-skip"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="siteVersionContainer"]/div/div[1]/span[2]').click()
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


if __name__ == '__main__':
    log_in()
    stock_search()








