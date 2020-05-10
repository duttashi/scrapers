#!/usr/bin/env python
# coding: utf-8

# Objectives:
# 
# 1. Scrape a book - http://www.gutenberg.org/files/10150/10150-h/10150-h.htm
#     
# 2. Text cleaning
# 
# 3. Create a Bag of Words - https://medium.freecodecamp.org/an-introduction-to-bag-of-words-and-how-to-code-it-in-python-for-nlp-282e87a9da04
# 
# Alternative approach
# 
# https://stackoverflow.com/questions/15507172/how-to-get-bag-of-words-from-textual-data

# ##### Part 1: Data extraction from html page

# In[1]:


# load the required libraries
import requests
from bs4 import BeautifulSoup
import re


# In[2]:


#page = requests.get('http://www.gutenberg.org/files/10150/10150-h/10150-h.htm')
page = requests.get('http://www.gutenberg.org/files/345/345-h/345-h.htm')


# In[6]:


if(page.status_code==200):
    print(page.text)
else:
    print("\n Error: Page could not be read")


# In[23]:


soup = BeautifulSoup(page.text, 'html.parser')


# The novel text is encolsed in the `p` tag.

# Step 2: Get rid of the boilerplate Gutenberg license text so it doesn't mess up the analysis

# In[24]:


text = soup.get_text()
print(text)


# In[25]:


# Text preprocessing
def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    clean = re.compile('margin-top: text-align p .c text-indent font-family .errata')
    return re.sub(clean, '', text)


# In[26]:


text1 = remove_html_tags(text)


# In[27]:


print(text1)


# In[ ]:




