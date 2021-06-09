# -*- coding: utf-8 -*-
"""
Created on Wed May 12 13:32:23 2021
data source: domain.com.au 
Objective: scrape data on properties for rent in Adelaide
@author: Ashish
"""

import requests
from bs4 import BeautifulSoup
# from lxml import html

base_url = "https://www.domain.com.au/rent/adelaide-sa-5000/?page="

response = requests.get(base_url).text
soup = BeautifulSoup(response, 'lxml')

# root = html.fromstring(response.content)
# result_list = []
# price = response.xpath('//div[@class="css-qrqvvg"]')[0].strip()

# print (price)

for page in range(1, 3):
    page = base_url + str(page)
    response = requests.get(page).text
    soup = BeautifulSoup(response, 'lxml')
    for advert_text in soup.find_all('div', attrs={'class': 'css-9hd67m'}):
        # print(advert_text)
        try:
            price = soup.find('p', attrs={'class': 'css-mgq8yx'}).text
            print(price)
        except Exception as e:
            price = "NA"