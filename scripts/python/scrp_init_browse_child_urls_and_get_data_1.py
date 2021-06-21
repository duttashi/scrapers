# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 21:53:53 2021

@author: Ashish
"""

#Import the packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import pandas
#The first line import the Web Driver, and the second import Chrome Options
#-----------------------------------#

#Chrome Options
page_link =[]
all_link = []
content = []
name_job = []
name_company = []
name_location = []
salary = []
expiry = []
upload_date = []
position = []
career = []
skill = []
language_of_cv = []
detail_address = []
number_employees = []

chrome_options = Options()
chrome_options.add_argument ('--ignore-certificate-errors')
chrome_options.add_argument ("--igcognito")
chrome_options.add_argument ("--window-size=1920x1080")
chrome_options.add_argument ('--headless')
#-----------------------------------#

driver = webdriver.Chrome(options=chrome_options, executable_path="C:/Users/Ashoo/Documents/playground_python/chromedriver.exe")
 
 #Open url
url = 'https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam'
driver.get(url)
driver.maximize_window()
time.sleep(5)
page_source = driver.page_source
soup = BeautifulSoup(page_source,"html.parser")
dataPath = r'C:\Users\Ashoo\Documents\playground_python\scrapers\data\Vietnamworks.csv'

#get all links
block_job_list = soup.find_all("div",{"class":"col-12 col-lg-8 col-xl-8 p-0 wrap-new"})
for i in block_job_list:
    link = i.find("a")
    try:
        all_link.append("https://www.vietnamworks.com" + link.get("href"))
    except AttributeError:
        print("error")
        print(i)


# print("\n".join(all_link))
# print(len(all_link))

# print(block_job_list)

#send request to each link

for i in all_link:
    page = requests.get(i)
    soup = BeautifulSoup(page.content,"html.parser")
    name_job.append(soup.find("h1",{"class":"job-title"}).text.replace("\n","").strip())

    name_company.append(soup.find("div",{"class","company-name"}).text.replace("\n","").strip())

    name_location.append(soup.find("span",{"class":"company-location"}).text.replace("\n","").strip())

    salary.append(soup.find("span",{"class":"salary"}).text.replace("\n","").strip())

    expiry.append(soup.find("span",{"class":"expiry gray-light"}).text.replace("\n","").strip())

    information = soup.find_all("div",{"class":"row summary-item"})
    for k in information:
        content.append(k.find("span",{"class":"content"}).text.replace('\xa0','').replace('\n', '').replace('  ',"").strip())

    upload_date = content[0]
    position = content[1]
    career = content[2]
    skill = content[3]
    language_of_cv = content[4]
    detail_address = content[5]
    number_employees = content[6]


data = {
   "Name": name_job,
   "Company": name_company,
   "Locations": name_location,
   "Salary": salary,
   "Upload date": upload_date,
   "Job position": position,
   "Career": career,
   "Skill": skill,
   "Language of cv": language_of_cv,
   "Detail address": detail_address,
   "Number employees": number_employees,
}
df = pandas.DataFrame(data)
df.to_csv( dataPath, index = False)
print(df.head())