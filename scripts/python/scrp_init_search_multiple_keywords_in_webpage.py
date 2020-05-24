# -*- coding: utf-8 -*-
"""
Created on Sun May 24 12:54:46 2020

@author: Ashoo
"""


import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.meridianenergy.co.nz')
soup = BeautifulSoup(page.content, 'html.parser')
keywords_to_find = ['sustainable', 'renewable', 'electric cars']
results = soup.find_all(string=lambda text: text and any (x in text for x in keywords_to_find))
print(results)  