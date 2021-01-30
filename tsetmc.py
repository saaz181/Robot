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
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=self.PATH, options=self.chrome_options)
        self.driver.get("http://www.tsetmc.com/Loader.aspx?ParTree=15")

    def __str__(self):
        clock = self.driver.find_element_by_class_name('RealServerTime')
        self.current_time = dt.datetime.strptime(clock.text, "%H:%M:%S")
        self.driver.quit()
        return self.current_time
