# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:00:19 2020

@author: Ashish
Reference: https://stackoverflow.com/questions/24598648/searching-google-with-selenium-and-python
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('http://www.google.com')

search = browser.find_element_by_name('q')
search.send_keys("lenovo laptop for sale")
search.send_keys(Keys.RETURN) # hit return after you enter search text
time.sleep(5) # sleep for 5 seconds so you can see the results

# grab all results on page
grab_urls=[]

# browser.quit()

