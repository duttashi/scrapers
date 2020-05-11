# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:53:14 2020

@author: Ashish
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

val = 10
jobs = []
with requests.Session() as session:
    page_number = 1
    url = 'https://www.indeed.com.my/data-scientist-jobs'
    while True:
        # print("Processing page: #{page_number}; url: {url}".format(page_number=page_number, url = url))
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # check if there is next page, break if not
        next_link = soup.find("span", class_="pn")
        print(next_link)
        if next_link is None:
            break
        else:
            val1 = val * page_number
            next_url = urljoin(url, "jobs?q=data+scientist&start=", val1)
            # print("next link: ", next_link)
            print("Processing page: #{page_number}; url: {url}".format(page_number=page_number
                                                                       , url=next_url))
            # get the page
            page_data = requests.get(next_url)
            # create soup
            page_text = soup(page_data.text, "html.parser")
            
            results = page_text.find_all("div", attrs={"data-tn-component": "organicJob"})
            for result in results:
                job_title = result.find_all(name="a", attrs={"data-tn-element": "jobTitle"})
                jobs.append(job_title["title"])
                    
            
            # # find and store job titles
            # for div in page_text.find_all(name="div", attrs={"data-tn-component": "organicJob"}):
            #      for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            #          jobs.append(a["title"])

            page_number += 1
            val *= page_number
    print("Done.")