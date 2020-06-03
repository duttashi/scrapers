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
from urllib.parse import urljoin
import requests
import csv

# create empty list to hold data
phone_urls = []
phone_urls_cmplt =[]

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
#print(driver.title)

# create beautifulsoup object
content = driver.page_source
#print(content)
soup = BeautifulSoup(content, 'html.parser')
# get the urls        
for pdata in soup.find_all("a"):
    
    if(pdata.parent.name=="td"):
        href = pdata['href']
        print(href)
        # add the urls to list
        phone_urls.append(href)
#print(phone_urls)
        
# Create complete urls from the phone_urls list
base_url = "https://www.gsmarena.com/"
# join the base_url with the phone_urls
for url in phone_urls:
    complete_url = urljoin(base_url, url)
    #print(complete_url)
    phone_urls_cmplt.append(complete_url)
# Iterate over the list having complete urls and browse the webpage
# to get the necessary data

phone_brand =[]
phone_brand_urls = []

for url in phone_urls_cmplt:
    # get the page
     page_data = requests.get(url)
     # create soup
     soup = BeautifulSoup(page_data.content, "lxml")
     for pname in soup.find_all('div', class_="makers"):
         for pdata in pname.findChildren('span'):
             phone_brand.append(pdata.text)
             #print(pdata)
     for phurl in soup.find_all('table'):
         for ptbldata in phurl.findChildren('td'):
             for purl in phurl.findChildren('href'):
                 print(purl)
         # for phurl in pname.find_all('a'):
         #     for purl in phurl.findChildren('href'):
         #         print(purl)
         #         complete_url = urljoin(base_url,purl)
         #         print(complete_url)
         #         phone_brand_urls.append(complete_url.text)
                 # if(purl=="zte-phones-62.php"):
                 #      break
                 #  else:
                 #      continue
      # for span_text in soup.findChildren('span'):
      #     print(span_text)
            
     #phone_name = soup.find_all('div', class_="makers")
# write data to file
with open('phone_brand_data.csv', mode="w", newline='\n') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(phone_brand)

with open('phone_brand_urldata.csv', mode="w", newline='\n') as myfile1:
     wr = csv.writer(myfile1, quoting=csv.QUOTE_ALL)
     wr.writerow(phone_brand_urls)
     

#print(phone_urls_cmplt)
myfile.close()
myfile1.close()
driver.close()
#print(phone_data)


