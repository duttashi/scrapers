# -*- coding: utf-8 -*-
"""
Created on Sat May 30 16:43:03 2020
Last modified: June 9th 2020 4:10 pm

@author: Ashish
"""
# Objective: Scrape the gsmarena website https://www.gsmarena.com/makers.php3
# Aim # browse to each phone brand and get all the phone data

import csv
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
# load required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# create empty list to hold data
phone_urls = []
phone_urls_cmplt = []
phone_brand_urls = []
phone_brand = []
phone_brand_urlcmplt = []
phone_brand_urlcmplt_data = []

# set working directory
os.chdir('C:/Users/Ashoo/Documents/playground_python/scrapers/')
# print(os.getcwd())

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
# driver = webdriver.Chrome(executable_path = r'C:/Users/Ashoo/Documents/playground_python/chromedriver.exe',  options = chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.gsmarena.com/makers.php3")
# print(driver.title)

# create beautifulsoup object
content = driver.page_source
# print(content)
soup = BeautifulSoup(content, 'html.parser')
# get the urls        
for pdata in soup.find_all("a"):

    if (pdata.parent.name == "td"):
        href = pdata['href']
        # print(href)
        # add the urls to list
        phone_urls.append(href)

# Create complete urls from the phone_urls list
base_url = "https://www.gsmarena.com/"
# join the base_url with the phone_urls
for url in phone_urls:
    complete_url = urljoin(base_url, url)
    # print(complete_url)
    phone_urls_cmplt.append(complete_url)
# Iterate over the list having complete urls and browse the webpage
# to get the necessary data


try:
    for url in phone_urls_cmplt:
        page_data = requests.get(url)
        # create soup
        soup = BeautifulSoup(page_data.content, "lxml")
        for pname in soup.find_all('div', class_="makers"):
            for pdata in pname.findChildren('span'):
                # append phone brand to list
                phone_brand.append(pdata.text)
                # print(pdata.text)
                # for pdata in pname.findChildren('href'):
                #     print(pdata.text)
except requests.exceptions.RequestException as e:
    print(e)
    pass

# get all phone brand urls for each phone in the phone url list
try:
    for url in phone_urls_cmplt:
        page_data = requests.get(url)
        # create soup
        soup = BeautifulSoup(page_data.content, "lxml")
        for pname in soup.find_all('div', class_="makers"):
            for pdata in pname.findChildren('a'):
                href = pdata['href']
                phone_brand_urls.append(href)
                # print(href.text)

except requests.exceptions.RequestException as e:
    print(e)
    pass

# Create complete urls from the phone brand urls list
base_url = "https://www.gsmarena.com/"
# join the base_url with the phone_urls
for url in phone_brand_urls:
    complete_url = urljoin(base_url, url)
    print(complete_url)
    phone_brand_urlcmplt.append(complete_url)

# get phone data from phone brand urls complete list
try:
    for url in phone_brand_urlcmplt:
        page_data = requests.get(url)
        # create soup
        soup = BeautifulSoup(page_data.content, "lxml")
        for pname in soup.find_all('table', class_="nfo"):
            phone_brand_urlcmplt_data.append(pname.text)
            print(pname)
except requests.exceptions.RequestException as e:
    print(e)
    pass

# write data to file
with open('data/phone_brand_data.csv', mode="w", newline='') as myfile:
    wr = csv.writer(myfile, delimiter='\n')
    wr.writerow(phone_brand)

with open('data/phone_brand_urldata.csv', mode="w", newline='') as myfile1:
    wr = csv.writer(myfile1, delimiter='\n')
    wr.writerow(phone_brand_urlcmplt_data)

# print(phone_urls_cmplt)
myfile.close()
# myfile1.close()
driver.close()
print("complete")
# print(phone_data)
