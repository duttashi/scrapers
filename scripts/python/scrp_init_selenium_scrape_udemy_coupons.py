# -*- coding: utf-8 -*-
"""
Created on Mon May 25 09:11:53 2020

@author: Ashish
"""


from bs4 import BeautifulSoup
from selenium import webdriver


coupon_title=[] #List to store coupon title
coupon_date=[] #List to store coupon date
coupon_url=[] #List to store coupon url

driver = webdriver.Chrome(executable_path = r'C:/Users/Ashoo/Documents/playground_python/chromedriver.exe')
driver.get("https://udemycoupons.me/")
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
soup.prettify()
search_coupon = soup.find_all('div',{'class':'td_module_1 td_module_wrap td-animation-stack'})

for coupon in search_coupon:
    coupon_title = coupon.find('h3',{'class':'entry-title td-module-title'}).text
    coupon_date = coupon.find('span',{'class':'td-post-date'}).text
    coupon_url = coupon.find('a').get('href')
    print(coupon_title, coupon_date, coupon_url)
    # data = dict({'coupon name': coupon_title,
    #              'coupon date': coupon_date,
    #              'coupon url':coupon_url
    #              })
    # # create dataframe
    # products_df = pd.DataFrame(
    #     dict([(k, pd.Series(v)) for k, v in data.items()])
    #     )
    # products_df.to_csv('../../data/coupon_data.csv', sep=",")
