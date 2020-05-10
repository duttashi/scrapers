#!/usr/bin/env python
# coding: utf-8

# #### Introduction
# 
# The [requests](https://2.python-requests.org/en/master/) library is the de facto standard for making HTTP requests in Python. It abstracts the complexities of making requests behind a beautiful, simple API so that you can focus on interacting with services and consuming data in your application.
# 
# ##### Basic idea
# The idea is to initially establsh a connection with a webpage using `requests` and then use `beautifulsoup` library to read/parse the data contained within `html/xml` tags.

# ##### Getting started
# Let’s begin by installing the requests library. To do so, run the following command:
# 
# `$ pip install requests`

# ##### Task 1: How to make a GET request
# 
# A GET request means to establish connection with a website.

# In[11]:


# define the webpage address to access
URL = 'https://en.wikipedia.org/wiki/Main_Page'


# In[12]:


# call the library
import requests
requests.get(URL)


# ##### The Response
# 
# A Response is a powerful object for inspecting the results of the request. Let’s make that same request again, but this time store the return value in a variable so that you can get a closer look at its attributes and behaviors:

# In[13]:


response = requests.get('https://en.wikipedia.org/wiki/Main_Page')


# ##### Status codes
# 
# A `200` status means that your request was successful, whereas a `404 NOT FOUND` status means that the resource you were looking for was not found. There are many other [possible status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) as well to give you specific insights into what happened with your request.
# 
# By accessing `.status_code`, you can see the status code that the server returned:

# In[4]:


response.status_code


# Let's use this information to make decisions:

# In[5]:


if response.status_code == 200:
    print('Success!')
elif response.status_code == 404:
    print('Not Found.')


# ##### Alternative method: Raising an Exception rather than using the status code's
# 
# Let’s say you don’t want to check the response’s status code in an if statement. Instead, you want to raise an exception if the request was unsuccessful. You can do this `using .raise_for_status()`:

# In[6]:


import requests
from requests.exceptions import HTTPError

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


# ##### Content
# 
# The response of a GET request often has some valuable information, known as a `payload`, in the message body. Using the attributes and methods of Response, you can view the payload in a variety of different formats.
# 
# To see the response’s content in bytes, you use `.content`:

# In[14]:


response = requests.get(URL)
response.content


# While `.content` gives you access to the raw bytes of the response payload, you will often want to convert them into a string using a character encoding such as `UTF-8`. response will do that for you when you access `.text`:

# In[15]:


response = requests.get(URL)
response.text


# If you take a look at the response, you’ll see that it is actually serialized `JSON` content. To get a dictionary, you could take the `str` you retrieved from `.text` and deserialize it using `.json` like:

# In[16]:


response = requests.get(URL).json()
print(response)


# ##### Headers
# 
# The response headers can give you useful information, such as the content type of the response payload and a time limit on how long to cache the response. To view these headers, access `.headers`:

# In[17]:


response.headers


# `.headers` returns a dictionary-like object, allowing you to access header values by key. For example, to see the content type of the response payload, you can access `Content-Type`:

# In[18]:


response.headers['Content-Type']


# Note: The HTTP spec defines headers to be case-insensitive, which means we are able to access these headers without worrying about their capitalization:

# In[19]:


response.headers['content-type']


# ##### Customizing the `GET` request 
# 
# One common way to customize a `GET` request is to pass values through query string parameters in the URL. To do this using `get()`, you pass data to `params`. For example, you can use GitHub’s Search API to look for the requests library:

# In[39]:


# Search Google
response = requests.get(
    'https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwiX8JTRwKviAhXEQo8KHf5MDloQPAgH',
    params={'q': 'data+science+jobs+malaysia:python'},
)
if response.status_code == 200:
    print('Success!\n')
elif response.status_code == 404:
    print('Not Found.\n')


# ##### Authentication
# 
# Authentication helps a service understand who you are. Typically, you provide your credentials to a server by passing data through the Authorization header or a custom header defined by the service. All the request functions you’ve seen to this point provide a parameter called auth, which allows you to pass your credentials.
# 
# One example of an API that requires authentication is GitHub’s Authenticated User API. This endpoint provides information about the authenticated user’s profile. To make a request to the Authenticated User API, you can pass your GitHub username and password in a tuple to `get()`:

# In[24]:


from getpass import getpass
requests.get('https://api.github.com/user', auth=('username', getpass()))


# #### Next step: when connection with website is sucessful
# 
# ##### Now we will use BeautifulSoup to parse the data in HTML/XML

# In[27]:


from bs4 import BeautifulSoup


# In[28]:


soup = BeautifulSoup(response.text, 'html.parser')


# In[29]:


soup.title


# In[30]:


soup.title.text


# In[41]:


search_results = soup.find_all('h3')

print (type(search_results))
print (len(search_results))


# ##### References:
# 
# 1. https://realpython.com/python-requests/

# #### Example Problem #1: Scrape two separate charts and merge them into one
# 
# **Problem background**: Scrape the data for top grossing movies in 2019 from the BoxOffice [website](https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019). The data is contained in the two tables on this page. 
# 
# **Problem**: How to extract two tables on this [page]((https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019)) and merge them into a single table/data frame?

# **Solution**: scrape the tables using the correct `html` tags and `concat` them.

# In[4]:


# Load the required libraries
import requests # to establish connection
from bs4 import BeautifulSoup # to read and parse the html
import pandas as pd # for data frame


# In[2]:


# Establish connection
URL = "https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019"
data = requests.get(URL).text


# In[3]:


#parse url
soup = BeautifulSoup(data, "html.parser")


# In[5]:


#find the tables you want
table = soup.findAll("table")[1:]


# In[6]:


#read it into pandas
df = pd.read_html(str(table))


# In[7]:


#concat both the tables
df = pd.concat([df[0],df[1]])


# In[8]:


# Result
df.head(5)


# In[9]:


df.tail(5)


# In[ ]:


#### Example Problem #2: Scrape two separate charts and merge them into one

**Problem background**: Scrape the data for top grossing movies in 2019 from the BoxOffice [website](https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019). The data is contained in the two tables on this page. 

get_ipython().set_next_input('**Problem**: How to extract two tables on this [page]((https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-2019)) and merge them into a single table/data frame');get_ipython().run_line_magic('pinfo', 'frame')


# In[ ]:




