# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:20:00 2020
Objective: Browse US schools website, scrape required data and write to disc
@author: Ashish
"""
# import required libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import csv
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

# Declare global variables
# driver = webdriver.Chrome()
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(executable_path = r'C:/Users/Ashoo/Documents/playground_python/chromedriver.exe',
                          options = chrome_options)
dataPath = r'C:\Users\Ashoo\Documents\playground_python\scrapers\data\us_schools_data.csv'
# Program Logic

# open the browser
driver.get("https://web3.ncaa.org/hsportal/exec/hsAction")

# find the webpage elements and save to variable
state_drop = driver.find_element_by_id("state")
state = Select(state_drop)
state.select_by_visible_text("New Jersey")

driver.find_element_by_id("city").send_keys("Galloway")
driver.find_element_by_id("name").send_keys("Absegami High School")
driver.find_element_by_class_name("forms_input_button").send_keys(Keys.RETURN)
driver.find_element_by_id("hsSelectRadio_1").click()

#scraping the caption of the tables
all_sub_head = driver.find_elements_by_class_name("tableSubHeaderForWsrDetail") 

#scraping all the headers of the tables
all_headers = driver.find_elements_by_class_name("tableHeaderForWsrDetail")

#filtering the desired headers
required_headers = all_headers[5:]

#scraoing all the table data
all_contents = driver.find_elements_by_class_name("tdTinyFontForWsrDetail")

#filtering the desired tabla data
required_contents = all_contents[45:]

# write scrape data to file
lstdata = [e.text for e in required_contents]

with open(dataPath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(lstdata)

print("Data written to disc. GoodBye!")
driver.close()
