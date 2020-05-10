#!/usr/bin/env python
# coding: utf-8

# #### Objective: To learn web data scraping using BeautifulSoup, requests and lxml
# 
# This notebook is following the book, "Web scraping with python: collecting data from the modern web" by Ryan Mitchell, 1st edition.

# In[ ]:


# check installed packages
# Reference: https://stackoverflow.com/questions/12939975/how-to-list-all-installed-packages-and-their-versions-in-python
# Type conda list in command promt

# install packages for web scraping
import sys
get_ipython().system('conda install --yes --prefix {sys.prefix} requests')


# In[1]:


from urllib.request import urlopen
html = urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())


# In[4]:


# running beautiful soup
from bs4 import BeautifulSoup as bs
html = urlopen("http://www.pythonscraping.com/pages/page1.html")
bsObj = bs(html.read())
print(bsObj.h1)


# In[1]:


import requests


# In[2]:


url="https://github.com/duttashi/"


# In[3]:


page = requests.get(url)


# In[4]:


page


# In[5]:


# response code 200 means page was downloaded
page.text


# In[6]:


# Stepping Through a Page with Beautiful Soup
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.text, "html.parser")


# In[7]:


print(soup.prettify())


# #### Finding Instances of a Tag
# We can extract a single tag from a page by using Beautiful Soup’s `find_all` method. This will return all instances of a given tag within a document.
# 

# In[8]:


soup.find_all('p')


# We can target specific classes and IDs by using the `find_all()` method and passing the class and ID strings as arguments. In Beautiful Soup we will assign the string for the class to the keyword argument `class_`

# In[12]:


soup.find_all(class_="repo js-repo")


# In[13]:


soup.find_all("span" ,class_="repo js-repo")


# Now let's try to automate the scraping process by asking the user for the webpage and then extract stuff out off it.

# In[3]:


from bs4 import BeautifulSoup

import requests

url = input("Enter a website to extract the URL's from: ")

r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)

for link in soup.find_all('a'):
    print(link.get('href'))


# Great! how about we put all these scraped links into a list and then loop through each item in the list to visit the page?

# In[10]:


pages= [] # empty list

print ("List is empty now", pages)

for link in soup.find_all('a'):
    url = link.get('href')
    pages.append(url)
    print(url)

# print list dimensions
print("\n\tThe number of items in the list are: ", len(pages))


# Note: The list `pages` contains several irrelevant items like `#`, tags like `/feeds`, `/questions`, `/help`, `None`. So the questions is how to remove all the non-url items from this list?

# #### Scraping twitter data
# Required library: tweepy

# In[1]:


# load the required libraries
import tweepy


# In[8]:


# Read the twitter credential file
creds_file="twitter_creds.txt"

with open(creds_file,'r') as f:
   
    mylist=[line.rstrip('\n') for line in f]

#print (mylist)


consumer_key = mylist[0] # The first element of the list
consumer_secret = mylist[1] # The second element of the list
#print("ckey: "+consumer_key, "\ncs: "+consumer_secret)
access_token= mylist[2] # The third element of the list
access_token_secret = mylist[3] # The last element of the list


# In[9]:


# Reference: https://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html#auth-tutorial

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Now, lets print the tweets from my home timeline

# In[10]:


public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)


# In[4]:


from tweepy import Cursor
from twitter_client import get_twitter_client
if __name__ == '__main__':
    client = get_twitter_client()
    for status in Cursor(client.home_timeline).items(10):
        # Process a single status
        print(status.text)


# In[5]:


# Get the User object for twitter...
user = api.get_user('twitter')


# In[8]:


# collect tweets on UnitedAirlines
for tweet in tweepy.Cursor(api.search,q="#unitedAIRLINES",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)


# Alright, so now lets write this data to a csv file

# In[9]:


import csv


# In[10]:


# Open/Create a file to append data
csvFile = open('ua.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
for tweet in tweepy.Cursor(api.search,q="#unitedAIRLINES",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


# In[11]:


# Another example
# Open/Create a file to append data
csvFile = open('kohli.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
for tweet in tweepy.Cursor(api.search,q="#kohli",count=100,
                           lang="en",
                           since="2015-01-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


# In[6]:


# collect tweets on #MRT, #KTM, #monorail
for tweet in tweepy.Cursor(api.search,q="#KTM",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)


# In[7]:


# collect tweets on #MRT, #KTM, #monorail
for tweet in tweepy.Cursor(api.search,q="#MRT",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)


# In[8]:


# collect tweets on #monorail
for tweet in tweepy.Cursor(api.search,q="#monorail",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)


# In[18]:


# collect tweets on #MRT, #KTM, #monorail in bahasa melayu
# for more language codes, refer to https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
for tweet in tweepy.Cursor(api.search,q="#KTM",count=100,
                           lang="en", 
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text)


# In[ ]:




