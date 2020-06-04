# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:09:38 2020
# SO response posted at https://stackoverflow.com/questions/62165635/how-to-scrape-data-from-flexbox-element-container-with-python-and-beautiful-soup/62167578#62167578
@author: Ashish
"""


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep

# create object for chrome options
chrome_options = Options()
base_url = 'https://www.pse.com/outage/outage-map'

chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('user-data-dir=C:\\Users\\Ashoo\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
    })
# invoke the webdriver
browser = webdriver.Chrome(executable_path = r'C:/Users/Ashoo/Documents/playground_python/chromedriver.exe',
                          options = chrome_options)
browser.get(base_url)
delay = 5 #secods

while True:
    try:
        WebDriverWait(browser, delay)
        #print ("Page is ready")
        sleep(5)
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        #print(html)
        soup = BeautifulSoup(html, "html.parser")
        for item_n in soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-4 listView-container'):
            for item_n_text in item_n.find_all(name="span"):
                print(item_n_text.text)
            print('-' * 80)
    except TimeoutException:
        print ("Loading took too much time!-Try again")
# close the automated browser
browser.close()