#!/usr/bin/env python
# coding: utf-8

# Using the `twint` library for twitter data scraping

# In[1]:


# install the library 
# pip3 install twint
# load the library
import twint


# In[2]:


# Set up TWINT config
c = twint.Config()
c.Search("KTM")


# In[3]:


# Run
twint.run.Search(c)


# In[ ]:




