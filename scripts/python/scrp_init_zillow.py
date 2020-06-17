# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 22:27:16 2020

@author: Ashish
"""


import json
import requests
from bs4 import BeautifulSoup

link = "https://www.zillow.com/homes/40223_rb/"

res = requests.get(link,headers={"User-Agent":"Mozilla/5.0"})
soup = BeautifulSoup(res.text,"lxml")
for homes in soup.select("script[type='application/ld+json']"):
    home_url = json.loads(homes.get_text(strip=True))['url']
    print(home_url)