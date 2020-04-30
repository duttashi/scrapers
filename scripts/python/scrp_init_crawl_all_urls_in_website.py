# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:29:04 2020

@author: Ashoo
"""

from bs4 import BeautifulSoup as bs
import urllib.request, urllib.error

base_url = ("http://www.jict.uum.edu.my/index.php/previous-issues/169-journal-of-information-and-communication-technology-jict-vol19no1jan2020")
# page = requests.get(base_url)
# Query the website and return the html to the variable 'page'


try:
    page = urllib.request.urlopen(base_url)
except urllib.error.HTTPError as e:
    # Return code error (e.g. 404, 501, ...)
    # ...
    print('HTTPError: {}'.format(e.code))
except urllib.error.URLError as e:
    # Not an HTTP-specific error (e.g. connection refused)
    # ...
    print('URLError: {}'.format(e.reason))

# Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = bs(page, features="lxml")
# print(list(soup.children))

# Use function “prettify” to look at nested structure of HTML page
# print(soup.prettify())

# get_links= soup.find_all('div')[0].get_text()
# get_links = soup.select("div span a")
# print(get_links)
all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))
