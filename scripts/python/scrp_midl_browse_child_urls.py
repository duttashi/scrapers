# -*- coding: utf-8 -*-
"""
Created on Wed May 13 08:17:19 2020
This script enhances the `scrp_init_browse_child_urls` by modularising the code

@author: Ashish
"""

# library calls


from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import pandas as pd

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

# invoke defined functions

myurl = 'https://www.indeed.com.my/data-scientist-jobs'
# myurl = "https://www.indeed.com.my/jobs?q=data+analyst&l="
# myurl = "https://www.indeed.com.my/jobs?q=data+analyst+internship&l="
page_count = count_job_pages(myurl)
print(page_count)
jobs_data = get_multiple_webpage_data(myurl, page_count)
print(jobs_data)
