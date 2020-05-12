# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:53:14 2020

@author: Ashish
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
import pandas as pd

val = 2
job_list = [] # initialise an empty list
company_list = []
rating_list = []
counter = 2

with requests.Session() as session:
    page_number = 1
    url = 'https://www.indeed.com.my/data-scientist-jobs'
    counter = 1
    while (counter<3):
        # print("Processing page: #{page_number}; url: {url}".format(page_number=page_number, url = url))
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
            print("Processing page: #{page_number}; url: {url}".format(page_number=page_number
                                                                       , url=next_url))
            # get the page
            page_data = requests.get(next_url)
            # create soup
            soup = BeautifulSoup(page_data.content, "lxml")
            # page_text = soup.get_text()
            
            # page_text = soup(page_data, "html.parser")
            # print(page_text) # the page text is printing
            # results = soup.find_all("div", attrs={"data-tn-component": "organicJob"})
            # company_name = soup.find_all('a', class_ = "turnstileLink")
            company_name = soup.find_all('span', class_ = "company")
            company_rating = soup.find_all("span", class_ = "ratingsContent")
            # print(results)
            for company in company_name:
                company_list.append(company.text)
            
            for rate in company_rating:
                rating_list.append(rate.text)
                # result.next_sibling
            
            # res = soup.find_all('span', class_ = "jobtitle turnstileLink visited")
            # print(res)
            # for result in res:
            #     job_list.append(result)
                
                
                
            # results = soup.find_all("h2", _class="title")
            # print(results)
            # for result in results:
            #     # check print statement
            #     # print("job title is: ", result)
            #     company_name = result.find_all("span", class_= "company")
            #     job_title = result.find_all("a", class_= "jobtitle turnstileLink visited")
            #     print("company name: ", company_name, " job title: ", job_title)
            #     # append result to list
            #     company_list.append(company_name)
            #     job_list.append(job_title)
                
                    
            
            # find and store job titles
            # for div in page_text.find_all(name="div", attrs={"data-tn-component": "organicJob"}):
            #      for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            #          jobs.append(a["title"])

            page_number += 1
            # # val *= page_number
            # # write jobs list to disk for checking
            # fh = open('myfile.csv', 'w+')
            # fh.write(data)
            # fh.close()
            
            # create a dictionary becuse some columns dont have values
            data = dict({"Company name": company_list, 
                                   "Company rating":rating_list})
            
            # create dataframe
            jobs_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))
            jobs_df.reset_index(drop=True)
        counter+=1
    
print(jobs_df)
# write dataframe to csv
jobs_df.to_csv("../../data/jobs_df.csv", sep=',')


print("Done.")