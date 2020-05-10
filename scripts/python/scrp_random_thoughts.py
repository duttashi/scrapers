#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#### References

https://www.seleniumhq.org/docs/03_webdriver.jsp#chapter03-reference
https://sites.google.com/a/chromium.org/chromedriver/downloads
https://pypi.org/project/selenium/
https://selenium-python.readthedocs.io/getting-started.html#simple-usage


# In[2]:


# A basic selenium based program
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


# In[3]:


# Create a new instance of the Firefox driver
browser = webdriver.Chrome('C:/Windows/chromedriver.exe')


# In[6]:


# go to the google home page
browser.get("http://www.google.com")

# the page is ajaxy so the title is originally this:
print browser.title

# find the element that's name attribute is q (the google search box)
inputElement = browser.find_element_by_name("q")

# type in the search
inputElement.send_keys("cheese!")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(browser, 10).until(EC.title_contains("cheese!"))

    # You should see "cheese! - Google Search"
    print(browser.title)

finally:
    browser.quit()


# In[4]:


# URL and Request code for BeautifulSoup

url_filter_bc = 'https://www.backcountry.com/msr-miniworks-ex-ceramic-water-filter?skid=CAS0479-CE-ONSI&ti=U2VhcmNoIFJlc3VsdHM6bXNyOjE6MTE6bXNy'
res_filter_bc = requests.get(url_filter_bc, headers = {'User-agent' : 'notbot'})


# Function that scrapes the reivews

def scrape_bc(request, website):
    newlist = []
    soup = BeautifulSoup(request.content, 'lxml')
    newsoup = soup.find('div', {'id': 'the-wall'})
    reviews = newsoup.find('section', {'id': 'wall-content'})

    for row in reviews.find_all('section', {'class': 'upc-single user-content-review review'}):
        newdict = {}
        newdict['review']  = row.find('p', {'class': 'user-content__body description'}).text
        newdict['title']   = row.find('h3', {'class': 'user-content__title upc-title'}).text
        newdict['website'] = website

        newlist.append(newdict)

    df = pd.DataFrame(newlist)
    return df


# function that uses Selenium and combines that with the scraper function to output a pandas Dataframe

def full_bc(url, website):
    driver = connect_to_page(url, headless=False)
    request = requests.get(url, headers = {'User-agent' : 'notbot'})
    time.sleep(5)
    full_df = pd.DataFrame()
    while True:
        try:
            loadMoreButton = driver.find_element_by_xpath("//a[@class='btn js-load-more-btn btn-secondary pdp-wall__load-more-btn']")
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(2)
        except:
            print('Done Loading More')

#             full_json = driver.page_source
            temp_df = pd.DataFrame()
            temp_df = scrape_bc(request, website)

            full_df = pd.concat([full_df, temp_df], ignore_index = True)

            time.sleep(7)
            driver.quit()
            break

    return  full_df 


# In[10]:


import requests
from bs4 import BeautifulSoup

url = "http://www.bloomberg.com/quote/SPX:IND"
raw_html = requests.get(url)

# get in BeautifulSoup format
processed_html = BeautifulSoup(raw_html.content, "html.parser")
# print('processed_html = ', processed_html)
# tag = processed_html.find_all("div", class_= "headline__07dbac92")
#tag = processed_html.find_all("div", class_= "block_uuid")
tag = processed_html.find_all("div")
print('Tag = ', tag)


# In[ ]:




