# -*- coding: utf-8 -*-
"""
Created on Sat May 23 11:30:54 2020

@author: Ashish
"""
# load required libraries
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# set the chromedriver/firefox drive path variable
path_to_chromedriver = '/Users/Ashoo/Miniconda3/chromedriver' # change path as needed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery");
chrome_options.add_argument("--start-maximized")
browser_obj = webdriver.Chrome(executable_path = path_to_chromedriver,
                               options=chrome_options)
browser_obj.delete_all_cookies()
browser_obj.set_window_size(800,800)
browser_obj.set_window_position(0,0)
print ('arguments done')
headers = {
        'authority': 'www.totalwine.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'referer': 'https://www.totalwine.com/beer/united-states/c/001304',
        'accept-language': 'en-US,en;q=0.9',
    }

# soup = 

# create browser object
browser_obj.get('https://www.google.com/')

# find google search textbox
google_search_box = browser_obj.find_element_by_name('q')
# type a search string in google search box
google_search_box.send_keys("covid19 news")
# simulate pressing the emnter key on keyboard
google_search_box.send_keys(Keys.RETURN)
# find the xpath for google search button
# find search results
search_results = browser_obj.find_element_by_xpath('//div[@class="r"]')
# create emoty list to store search result text
for i in search_results:
    print(i.text)
search_res=[]
print(search_results.text)

# create soup

# keep the browser open for 10 seconds
time.sleep(10)
# close the browser
browser_obj.close()
