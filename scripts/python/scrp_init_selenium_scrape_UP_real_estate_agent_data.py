# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:09:00 2020

@author: Ashish
"""
# Objective: Scrape the Uttar Pradesh Real Estate website https://www.up-rera.in/agents
# Aim # get UP real estate agent's table data on this page https://www.up-rera.in/agents & write to dataframe'

# load required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# create empty list to hold data
restate_data = []

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
driver.get("https://www.up-rera.in/agents")
print(driver.title)

# create beautifulsoup object
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

for tdata in soup.find_all('table',class_='table table-bordered table-striped'):
    if(tdata in soup.find('span')):
        #print(tdata.text)
    #print(tdata.text)
    #//table[@class="table table-bordered table-striped"]//span will give all data
        restate_data.append(tdata.text.strip())
driver.close()
print(restate_data)
