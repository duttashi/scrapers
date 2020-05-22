# -*- coding: utf-8 -*-
"""
Created on Fri May 22 16:40:38 2020

@author: Ashoo
"""


from google import google
from bs4 import BeautifulSoup
from selenium import webdriver
import collections

class bsetools() :

    def __init__(self):
        #Constructor for this class.
        self.board = "BSE"
        self.bse_website = "https://www.bseindia.com/"

    def __get_bse_link(self, search_quote) :
        #Appending share price BSE to get a specific search result
        google_term = search_quote + " share price BSE"
        search_results = google.search(google_term)
        for result in search_results:
            if "bseindia" in result.link:
                return result.link, True

        #If there is a wrong search term or could not find bseindia link
        return "NA", False

    def get_BSE_index(self):
        #browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        #Set headless chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # start chrome browser
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(self.bse_website)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        Sensex = collections.namedtuple('Sensex', ['bse_index', 'diff'])
        Sensex.bse_index =  soup.find('div', class_='newsensexvalue').text.strip()
        #As the new website gives lot of unnecessary information, we just strip it and take the first part
        Sensex.diff =  soup.find('div', class_='newsensextext2').text.strip().split('\n')[0]
        #Check if index returned is float, replacing commas with empty space so that it is easy to convert into float and check
        #if isinstance(float(Sensex.bse_index.replace(',', '')), float) :
        if Sensex.bse_index:
            return Sensex

        return "Cannot find index now"

    def __get_price_from_bse(self, bse_link) :
        i = 0
        quote = None
        #Attempt searching the quote for 5 times
        while(quote is None or i < 4) :
            #browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
            options = webdriver.ChromeOptions()
            options.add_argument('headless')

            # start chrome browser
            browser = webdriver.Chrome(chrome_options=options)
            browser.get(bse_link)
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            #Get current price of share
            quote = soup.find('strong', id='idcrval')
            i = i + 1
        #Remove all tags and html class information and capture only value
        quote = quote.text.strip()
        diff_than_yesterday = soup.find('span', class_ ='sensexbluetext')
        #Check if number which we have captured is float
        if isinstance(float(quote), float) :
            return quote, diff_than_yesterday.text.strip()

        return "Cannot find price", ""

    def get_quote(self, company_name) :
        bse_link, flag = self.__get_bse_link(company_name)
        if flag :
            share_price = self.__get_price_from_bse(bse_link)
            return share_price
        else :
            #Return relevant error message and empty bse index link in case there is no bse_link found
           return "No relevant share price found for " + company_name