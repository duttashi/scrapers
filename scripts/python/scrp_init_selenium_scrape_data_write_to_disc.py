# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:20:00 2020
Objective: Browse US schools website, scrape required data and write to disc
@author: Ashish
"""
# import required libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import csv

# Declare global variables
driver = webdriver.Chrome()
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
