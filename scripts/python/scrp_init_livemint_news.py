import requests
from bs4 import BeautifulSoup as bs

URL = 'https://www.livemint.com/mutual-fund/page-2'

req = requests.get(URL)
soup = bs(req.text, 'html.parser')

titles = soup.find_all('h2', attrs={'class':'headline'})

print(titles)