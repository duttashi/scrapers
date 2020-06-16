# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:51:24 2020
Aim: To scrape sensex index data from bombay stock exchange website
Challenge #1: get values from dropdown list, select a value and click on submit button
Challege #2: Once submit button is clicked, it will the show table data. Scrape this data  

@author: Ashish
"""
# load required libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# create object for chrome options
chrome_options = Options()
# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
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
print(browser.title)
delay = 3 # seconds
browser.get("https://www.bseindia.com/Indices/IndexArchiveData.html")
try:
    
    #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ddlIndex')))
    print ("Page is ready!")
    # find the xpath of the sensus Index drop downlist
    dropdown = browser.find_element_by_xpath('//*[@id="ddlIndex"]')
    selector = Select(dropdown)

    options = selector.options
    for index in range(1, len(options)-1):
        print(options[index].text)
except TimeoutException:
    print ("Loading took too much time!")


# search_btn = driver.find_element_by_xpath('//*[@class="btn btn-default"]')
# search_btn.click()

# close the browser window
browser.close()


