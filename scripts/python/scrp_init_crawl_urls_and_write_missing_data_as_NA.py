# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:36:02 2020

@author: Ashish
"""

from selenium import webdriver
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep

data = []

final_list = [
    'https://www.hostelworld.com/pwa/hosteldetails.php/Itaca-Hostel/Barcelona/1279?from=2020-11-21&to=2020-11-22&guests=1',
    'https://www.hostelworld.com/pwa/hosteldetails.php/Be-Ramblas-Hostel/Barcelona/435?from=2020-11-27&to=2020-11-28&guests=1'
]

# load your driver only once to save time
# driver = selenium.webdriver.Chrome()
# driver = webdriver.Chrome(ChromeDriverManager().install())
# create object for chrome options
chrome_options = Options()
# base_url = 'https://shopee.com.my/shop/13377506/search?page=0&sortBy=sales'

# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('user-data-dir=C:\\Users\\Ashoo\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
    })
driver = webdriver.Chrome("c:/tmp/chromedriver.exe",options = chrome_options)

for url in final_list:
    data.append({})

    # cache the HTML code to the filesystem
    # generate a filename from the URL where all non-alphanumeric characters (e.g. :/) are replaced with underscores _
    filename = ''.join([s if s.isalnum() else '_' for s in url])
    if not os.path.isfile(filename):
        driver.get(url)
        
        # better use selenium's wait functions here  
        time.sleep(random.randint(10, 20))
        source = driver.page_source
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(source)
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    soup = BeautifulSoup(source, 'html.parser')

    review = soup.find_all(class_='reviews')[-1]
    
    try:
        price = soup.find_all('span', attrs={'class':'price'})[-1] 
    except:
        price = soup.find_all('span', attrs={'class':'price'})

    data[-1]['name'] = soup.find_all(class_=['title-2'])[0].text.strip()
    
    rating_labels = soup.find_all(class_=['rating-label body-3'])
    rating_scores = soup.find_all(class_=['rating-score body-3'])
    assert len(rating_labels) == len(rating_scores)
    for label, score in zip(rating_labels, rating_scores):
        data[-1][label.text.strip()] = score.text.strip()
    
    data[-1]['price'] = price.text.strip()
    data[-1]['review'] = review.text.strip()
    data.append(data[0].copy())
    del(data[-1]['Staff'])
    data[-1]['name'] = 'Incomplete Hostel'
    df = pd.DataFrame(data)
    print(df)  
    
