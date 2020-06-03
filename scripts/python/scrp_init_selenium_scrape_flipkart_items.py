# -*- coding: utf-8 -*-
"""
Created on Sun May 24 21:14:00 2020

@author: Ashoo
"""


from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
driver = webdriver.Chrome(executable_path = r'C:\Users\Ashoo\Downloads\software\chromedriver_win32\chromedriver.exe')
driver.get("https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&amp;amp;amp;uniq")
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
    name=a.find('div', attrs={'class':'_3wU53n'})
    price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
    rating=a.find('div', attrs={'class':'hGSR34'})
    products.append(name.text)
    prices.append(price.text)
    ratings.append(rating.text)
    data = dict({'Product Name': products,
                 'Price': prices,
                 'Rating':ratings
                 })
    # create dataframe
    products_df = pd.DataFrame(
        dict([(k, pd.Series(v)) for k, v in data.items()])
        )
    products_df.to_csv('products.csv', sep=",")
