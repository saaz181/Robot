from selenium import webdriver
import datetime as dt

"""
This class return TIME from http://www.tsetmc.com/Loader.aspx?ParTree=15 website
in order to use it as our time option in bot
"""


class Time(object):
    PATH = 'chromedriver.exe'

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")  # make chrome browser hidden
        self.chrome_options.add_argument('--ignore-certificate-errors')  # disable chrome security alerts
        self.chrome_options.add_argument('--allow-insecure-localhost')  # allow 'chromedriver' to run on localhost
        self.chrome_options.add_argument('--ignore-ssl-errors=yes')  # disable SSL security of chrome browser

        self.driver = webdriver.Chrome(executable_path=self.PATH, options=self.chrome_options)
        self.driver.get("http://www.tsetmc.com/Loader.aspx?ParTree=15")

    def __str__(self):
        clock = self.driver.find_element_by_class_name('RealServerTime')
        self.current_time = dt.datetime.strptime(clock.text, "%H:%M:%S")
        self.driver.quit()
        return self.current_time
