#!/usr/bin/env python
# coding: utf-8

# Objective: To collect the date, title, and content from the newspaper (the new york times)
# 
# Website to scrape: https://www.nytimes.com/
# 
# Search string: `security`
# 
# Published articles date range: `Jan 01 2018` till `May 27 2019` 

# In[1]:


# load required libraries
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[6]:


# create base
base = "https://www.nytimes.com"
browser = webdriver.Chrome('C:/Windows/chromedriver.exe')
wait = WebDriverWait(browser, 10)
browser.get('https://www.nytimes.com/search?endDate=20190527&query=security&sort=newest&startDate=20180101')


# In[7]:


# Build logic
while True:
    try:
        time.sleep(1)
    show_more = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button"][contains(.,"Show More")]')))
        show_more.click()
    except Exception as e:
            print(e)
            break

soup = BeautifulSoup(browser.page_source,'lxml')
search_results = soup.find('ol', {'data-testid':'search-results'})
for a in search_results.find_all('a', href=True):
    page_url = "https://www.nytimes.com" + a['href']
    print(page_url)
    page = requests.get(page_url)
    page_soup = BeautifulSoup(page.content,'lxml')
    page_soup_div = page_soup.find_all("div", {"class":"StoryBodyCompanionColumn"})
    for p_content in page_soup_div:
        print(p_content.text)


# Reference: This question was originally asked on [SO](https://stackoverflow.com/questions/56334695/how-to-scrape-newspaper-articles-from-website-using-selenium-and-beautifulsoup-i)

# In[ ]:




