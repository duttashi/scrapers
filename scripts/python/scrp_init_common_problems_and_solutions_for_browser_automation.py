#!/usr/bin/env python
# coding: utf-8

# #### Common problem's and solutions for broswer automation

# ##### Problem

# In[3]:


url = 'https://www.mouthshut.com/product-reviews/ICICI-Lombard-Auto-Insurance-reviews-925641018'.format
driver = webdriver.Chrome
driver.get(url(1))


# In[1]:


import webbrowser
webbrowser.open('http://www.google.com')


# In[1]:


from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
driver.get("http://google.com/")
print ("Headless Firefox Initialized")
#driver.quit()


# In[1]:


from selenium import webdriver
browser = webdriver.Firefox()


# ##### Solution

# To solve the above problems, ensure the following are in order;
# 
# 1. The `geckodriver.exe` or the `chromedriver.exe` files are the same version as the Chrome or Firefox versions.
# 
# 2. The `geckodriver.exe` or the `chromedriver.exe` files have full permissions. In windows environment, right click on the file, choose properties-> security.
# 
# 3. The `geckodriver.exe` or the `chromedriver.exe` files are in a folder like, `c:\tmp\`
#     
# 4. The `geckodriver.exe` or the `chromedriver.exe` files are specified in the `System Path`.
# 
# 5. The `geckodriver.exe` or the `chromedriver.exe` files when used in code, then they should be written as, `C:/tmp/chromedriver.exe`

# In[1]:


from selenium import webdriver
#driver = webdriver.Firefox(executable_path='C:\tmp\geckodriver.exe')
driver = webdriver.Chrome(executable_path='C:/tmp/chromedriver.exe')
driver.get('http://inventwithpython.com')

