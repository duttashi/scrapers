# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 12:27:24 2021

@author: Ashish
"""

import requests
from bs4 import BeautifulSoup
response = requests.get(
	url="https://www.reddit.com/",)
print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')
links = soup.findAll('a')
for link in links:
    print(link['href'])
    

