# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:23:53 2020

This script enhances the `scrp_init_write_pandas_dataframe_to_mysql.py`
by modularising the code. It further enhances the code by writing the
scraped data to database.

@author: Ashish
"""

# library calls
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import sqlalchemy
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

# Define global variables
# connect to server
mysql_engine = sqlalchemy.create_engine(
    'mysql://root:ashoo@localhost/db_practise')

# modularise the code


def count_job_pages(pageURL):
    session = requests.Session()
    response = session.get(pageURL)
    soup = BeautifulSoup(response.content, "lxml")
    search_count = soup.find("div", id="searchCountPages")
    search_count = str(search_count)
    res = [int(i) for i in search_count.split() if i.isdigit()]
    # get the second number
    res = res[1]
    return res


def get_multiple_webpage_data(page_url, page_count):
    val = 2
    # initialise empty lists
    company_list = []
    rating_list = []
    company_location_list = []
    advertpost_date_list = []
    jobpos_title_list = []
    counter = 1
    with requests.Session() as session:
        page_number = 1
        while (counter <= page_count):
            response = session.get(page_url)
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
                # rel_url = "jobs?q=data+analyst+internship&l=" + str(val1)
                next_url = urljoin(page_url, rel_url)
                print("Processing page: #{page_number}; url: {url}".format(
                    page_number=page_number, url=next_url)
                    )
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
                jobpos = soup.find_all("a", class_=["jobtitle turnstileLink visited", "jobtitle turnstileLink"])
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
                    dict([(k, pd.Series(v)) for k, v in data.items()])
                    )
                jobs_df.reset_index(drop=True)
            counter += 1
    # print(jobs_df)
    # write dataframe to csv
    jobs_df.to_csv("../../data/jobs_df.csv", sep=',')
    print("Done.")
    return jobs_df


# create table in mysql database
def create_table_in_database(mysql_engine):
    # create database instance
    # myconxn = mysql_engine.raw_connection()
    myconxn = mysql_engine.connect()
    # check if table exists then drop it
    myconxn.execute("drop table if exists jobs")
    # check if table does not exist then create one
    myconxn.execute("create table jobs(sno int(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY,company_name varchar(30), company_rating float(3), job_loc varchar(30), advert_postdate varchar(30),job_title varchar(30))")
    print("Table created")


def write_to_database(jobs_df):
    # write pandas dataframe to database
    jobs_df.to_sql(name='jobs', con=mysql_engine, if_exists='replace')
    print("Dataframe sucessfully written to database")


def read_from_database(jobs_df):
    # read data from database
    print("Now reading from the database....")
    with mysql_engine.connect() as connection:
        result = connection.execute("select `*` from jobs")
        for row in result:
            print(row)


# invoke defined functions
if __name__ == '__main__':
    myurl = 'https://www.indeed.com.my/data-scientist-jobs'
    # myurl = "https://www.indeed.com.my/jobs?q=data+analyst&l="
    # myurl = "https://www.indeed.com.my/jobs?q=data+analyst+internship&l="
    page_count = count_job_pages(myurl)
    print(page_count)
    jobs_data = get_multiple_webpage_data(myurl, page_count)
    # print(jobs_data)
    create_table_in_database(mysql_engine)
    write_to_database(jobs_data)
    read_from_database(jobs_data)
