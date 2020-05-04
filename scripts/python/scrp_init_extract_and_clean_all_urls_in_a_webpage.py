# -*- coding: utf-8 -*-
"""
Created on Sun May  3 22:15:04 2020

@author: Ashish

Objective: Given a webpage, extract and claen all URLs in it.
"""

from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, urlunparse, quote
import urllib.request

# pageURL = "https://www.pastemagazine.com/noisetrade/music/"
pageURL = "https://stackoverflow.com/questions/tagged/beautifulsoup"

dirty_urls, clean_urls = [], []  # initialise empty list to contain all urls
itemStr = ''


def get_all_page_urls(url):
    r = urllib.request.urlopen(url)
    soup = bs(r, "html.parser")
    # find all links in page
    plink = soup.find_all('a')
    for link in plink:
        alink = link.get('href')
        dirty_urls.append(alink)

    return dirty_urls


def clean_page_urls(urlist):

    # clean the urls
    for url in urlist:
        parts = urlparse(url)
        cleanURL = urlunparse(parts._replace(path=quote(parts.path)))
        clean_urls.append(cleanURL)

    return clean_urls


#  url = input('URL to crawl: ')
soup = get_all_page_urls(pageURL)
# print("Dirty urls in page",soup)

cleanURL = clean_page_urls(soup)
print("Clean URLS", cleanURL)
