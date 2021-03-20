# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 18:26:21 2021

@author: Ashish
"""

import requests
from bs4 import BeautifulSoup
import csv
import re

base_url = "https://www.flipkart.com/search?q=mobiles&page="

def get_urls(): 
    csv_file = open("flipkart_data.csv", "a")
    writer = csv.writer(csv_file)

    writer.writerow(
        ['Product_name', 'Price', 'Rating', 'Product-url'])

    for page in range(1, 510):

        page = base_url + str(page)

        response = requests.get(page).text

        soup = BeautifulSoup(response, 'lxml')

        for product_urls in soup.find_all('a', href=True, attrs={'class': '_1fQZEK'}):
            
            #name
            try:
                name = product_urls.find('div', attrs={'class': '_4rR01T'}).text
            except Exception as e:
                name = "NA"

            #price
            try:
                price = product_urls.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).text
                price = re.split("\₹", price)
                price = price[-1]
            except Exception as e:
                price = "NA"

            #rating
            try:
                rating = product_urls.find('div', attrs={'class': '_3LWZlK'}).text
            except Exception as e:
                rating = "NA"
            #item_url
            try:
                item_url = soup.find('a', class_="_1fQZEK", target="_blank")['href']
                item_url = " https://www.flipkart.com" + item_url
                item_url = re.split("\&", item_url)
                item_url = item_url[0]
            except Exception as e:
                item_url = "NA"

            print(f'Product name is {name}')
            print(f'Product price is {price}')
            print(f'Product rating is {rating}')
            print(f'Product url is {item_url}')


            writer.writerow(
                [name, price, rating, item_url])

get_urls()