#!/usr/bin/env python
# coding: utf-8

# Aim:
# 
# To develop a scraper that can scrape the following contents from multiple pages of a website.
# 
# Objective: 
# 
# 1. Scrape the paper title, author list, publication date, abstract and download the full paper.
# 
# 2. To scrape content from multiple pages and write scraped content to disc.
# 
# Website to scrape the data from: http://www.mecs-press.org/ijmecs/v11n2.html

# In[2]:


# load the required libraries
import requests
from bs4 import BeautifulSoup


# In[1]:


pgUrl = "http://www.mecs-press.org/ijmecs/v11n2.html"


# In[5]:


# define function to extract page
def get_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


# In[6]:


# get data
def get_article_name(url):
    soup = get_page(url)
    try:
        title = soup.find(h3="tit")
        print("SUCCESS")

    except AttributeError:
        print("ERROR")
    return(title)


# In[7]:


# call the scraper function
print(get_article_name(pgUrl))

