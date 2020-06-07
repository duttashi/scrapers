# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:14:24 2020

@author: Ashish
"""

# load required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

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
driver = webdriver.Chrome(executable_path = r'C:/Users/Ashoo/Documents/playground_python/chromedriver.exe',
                          options = chrome_options)
driver.get("http://rera.rajasthan.gov.in/ProjectSearch")
print(driver.title)
# find the search button xpath
search_btn = driver.find_element_by_xpath('//*[@id="btn_SearchProjectSubmit"]')
search_btn.click()
xpath_first_view =  '//*[@id="OuterProjectGrid"]/div[3]/div[2]/div/table/tbody/tr[1]/td[7]'
# wait for the element to ensure it is available
WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,xpath_first_view)))
time.sleep(1) # to ensure click is not very quick
view1_btn = driver.find_element_by_xpath(xpath_first_view).click()

