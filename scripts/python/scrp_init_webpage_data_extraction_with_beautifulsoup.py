#!/usr/bin/env python
# coding: utf-8

# ### Idea
# 
# The idea is to prompt the user for a website name and then extract the data from that page.

# In[8]:


# required libraries
from bs4 import BeautifulSoup as soup
import urllib.request
from nltk.corpus import stopwords


# In[2]:


# initialise the variables
train_data=[]
test_data=[]


# In[6]:


# Prompting the user for webpage to crawl
url_to_parse=input("Enter the url to open: ")
#myhtml=urllib.urlopen(url_to_parse).read()
myhtml = urllib.request.urlopen(url_to_parse)


# In[7]:


# Stripping the html tags and removing the encoding
currySoup=soup(myhtml,from_encoding="utf-8")


# In[9]:


# Searching for text content. Note..You will have to know the html tag where the content is placed
content=currySoup.find("p")
# creating a list of all the sentences found in the web page
word_list = ["".join(x.findAll(text=True)) for x in content.findAllNext("p")]


# In[11]:


print(word_list)


# In[12]:


# Filtering the words on basis of stopwords
#filtered_words = [word for word in word_list if word not in stopset]
#train_data=filtered_words
#test_data=filtered_words


# In[ ]:




