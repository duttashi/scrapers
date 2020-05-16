# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:53:14 2020

@author: Ashish
Other websites for crawling: https://companies.naukri.com/ibm-jobs/data-scientist-jobs
https://www.naukri.com/data-scientist-jobs?k=data%20scientist
"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy

val = 2
job_list = []  # initialise an empty list
company_list = []
rating_list = []
company_location_list = []
advertpost_date_list = []
jobpos_title_list = []

counter = 1
pages_to_scrape = 1

url = 'https://www.indeed.com.my/data-scientist-jobs'
session = requests.Session()
response = session.get(url)
soup = BeautifulSoup(response.content, "lxml")
search_count = soup.find("div", id="searchCountPages")
search_count = str(search_count)
res = [int(i) for i in search_count.split() if i.isdigit()]
# get the second number
res = res[1]
# res = 5


with requests.Session() as session:
    page_number = 1
    url = 'https://www.indeed.com.my/data-scientist-jobs'
    counter = 1
    while (counter <= res):
        response = session.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        # check if there is next page, break if not
        next_link = soup.find("span", class_="pn")
        # print(next_link)
        if next_link is None:
            break
        else:
            val1 = val * page_number
            # Note: when joining/concatenating a string to an integer,
            # then coerce the integer to string as given below
            rel_url = "jobs?q=data+scientist&start=" + str(val1)
            # next_url = urljoin(url, "jobs?q=data+scientist&start=", val1)
            next_url = urljoin(url, rel_url)
            # print("next link: ", next_link)
            print("Processing page: #{page_number}; url: {url}".format(
                page_number=page_number, url=next_url))
            # get the page
            page_data = requests.get(next_url)

            # create soup
            soup = BeautifulSoup(page_data.content, "lxml")
            company_name = soup.find_all('span', class_="company")
            company_rating = soup.find_all("span", class_="ratingsContent")
            company_loc = soup.find_all(
                "span", class_="location accessible-contrast-color-location")
            advert_post_date = soup.find_all("span", class_="date")
            # searching for multiple attribute values
            jobpos = soup.find_all("a", class_=["jobtitle turnstileLink visited", 
                                                "jobtitle turnstileLink"
                                                ]
                                   )
            # append results to list
            for company in company_name:
                company_list.append(company.text)
            for rate in company_rating:
                rating_list.append(rate.text)
            for loc in company_loc:
                company_location_list.append(loc.text)
            for postDate in advert_post_date:
                advertpost_date_list.append(postDate.text)
            for jobTitle in jobpos:
                jobpos_title_list.append(jobTitle.text)

            page_number += 1
            # Reference: See this So post: https://stackoverflow.com/questions/19736080/creating-dataframe-from-a-dictionary-where-entries-have-different-lengths
            data = dict({"CompanyName": company_list,
                         "CompanyRating": rating_list,
                         "JobLocation": company_location_list,
                         "AdvertPostDate": advertpost_date_list,
                         "JobTitle": jobpos_title_list})
            # create dataframe
            jobs_df = pd.DataFrame(
                dict([(k, pd.Series(v)) for k, v in data.items()]
                     )
                )
            jobs_df.reset_index(drop=True)
        counter += 1

print(jobs_df)
# write dataframe to csv
jobs_df.to_csv("../../data/jobs_df.csv", sep=',')
print("Done.")

# write the scraped data to database
# engine = sqlalchemy.create_engine('mysql://user:password@server') # connect to server
# reference: See this https://docs.sqlalchemy.org/en/13/core/engines.html to create database url
mysql_engine = sqlalchemy.create_engine('mysql://root:ashoo@localhost/db_practise') # connect to server

jobs_df.to_sql(name='jobs', con=mysql_engine, if_exists='replace')

# How to use the mysql engine in python? See this reference:
with mysql_engine.connect() as connection:
    result = connection.execute("select `*` from jobs")
    for row in result:
        print(row)
