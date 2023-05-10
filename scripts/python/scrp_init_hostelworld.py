# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 09:25:57 2021

@author: Ashish
"""
# import required libraries
from selenium.webdriver.chrome.options import Options

def set_browser_options(self):
    chrome_options = Options()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
    })
   
    return

def invoke_driver():
    driver = webdriver.Chrome("c:/users/ashoo/documents/playground_python/chromedriver.exe",options = chrome_options)
    
