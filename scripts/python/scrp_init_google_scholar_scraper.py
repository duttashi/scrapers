#!/usr/bin/env python
# coding: utf-8

# ##### Scraping and parsing citation info from Google Scholar search results

# Reference: https://stackoverflow.com/questions/56220399/scraping-and-parsing-citation-info-from-google-scholar-search-results

# In[1]:


import requests
from bs4 import BeautifulSoup as bs


# In[2]:


queries = ['mixed data clustering','educational data mining']


# In[3]:


#with requests.Session() as s:
with requests.Session() as s:
    for query in queries:
        url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + query + '&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        r = s.get(url)
        soup = bs(r.content, 'lxml') # or 'html.parser'
        title = soup.select_one('h3.gs_rt a').text if soup.select_one('h3.gs_rt a') is not None else 'No title'
        link = soup.select_one('h3.gs_rt a')['href'] if title != 'No title' else 'No link'
        citations = soup.select_one('a:contains("Cited by")').text if soup.select_one('a:contains("Cited by")') is not None else 'No citation count'
        print(title, link, citations)


# In[7]:


url = 'https://scholar.google.com/scholar?q=' + query + '&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'

content = requests.get(url).text
page = bs(content, 'lxml')
results = []
for entry in page.find_all("div", attrs={"class": "gs_ri"}): #tag containing both h3 and citation
    results.append({"title": entry.h3.a.text, "url": entry.a['href'], "citation": entry.find("div", attrs={"class": "gs_rs"}).text})
print(results)


# In[ ]:




