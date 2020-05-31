# -*- coding: utf-8 -*-
"""
Created on Sat May 30 16:43:03 2020

@author: Ashish
"""
# Objective: Scrape the gsmarena website https://www.gsmarena.com/makers.php3
# Aim # browse to each phone brand and get all the phone data

# load required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# create empty list to hold data
phone_data = []

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
driver.get("https://www.gsmarena.com/makers.php3")
print(driver.title)

# create beautifulsoup object
content = driver.page_source
#print(content)
soup = BeautifulSoup(content, 'html.parser')
#print(soup.find_all('div',class_='st-text'))

# get data from within multiple tags
for pdata in soup.find_all("td"):
    if(pdata.parent.name=="tr"):
        print(pdata.text)
        
for pdata in soup.find_all("a"):
    if(pdata.parent.name=="td"):
        href = pdata['href']
        print(href)
        #print(pdata.text)
# TO DO: split the strig ito 3 parts, namely, phone brand name, count of phones, and word device
    #print(tdata.text)
    #//table[@class="table table-bordered table-striped"]//span will give all data
        phone_data.append(pdata.text.strip())
driver.close()
#print(phone_data)


