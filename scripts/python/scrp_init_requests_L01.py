# load required libraries
import requests
from bs4 import BeautifulSoup as bs
# define the webpage address to access
URL = 'https://en.wikipedia.org/wiki/Main_Page'

response = requests.get(URL)

if(response.status_code == 200):
    print("Success, able to connect to page")
    # show the page content
    #print(response.content)
    #print(response.headers)
    data = response.text
    soup = bs(response.text, 'html.parser')
    #print(data)
    search_results = soup.find_all('li')
    print(search_results)
    print(len(search_results))
elif (response.status_code == 400):
    print("Failed: unable to access the page")
