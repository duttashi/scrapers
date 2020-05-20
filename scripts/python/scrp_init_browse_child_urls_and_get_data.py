from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

full_urls=[]
gym_data=[]
gym_hours=[]
base_url = "https://www.planetfitness.com/sitemap"
session = requests.Session()
response = session.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

tds = soup.find_all('td', {'class': 'club-title'})
links = [td.find('a')['href'] for td in tds]
keywords = ['gyms']

# construct full urls and store in a list
init_url = "https://www.planetfitness.com/"
for link in links:
    next_url = urljoin(init_url, link)
    full_urls.append(next_url)
    # print(next_url)

# now browse to each url in list and get the data and save to list
for link in full_urls:
    page_data = session.get(link)
    # create soup
    soup = BeautifulSoup(page_data.content, "html.parser")
    street_addr = soup.find('p', class_="address")
    addr_dict = {p['itemprop']: p.text for p in street_addr.findAll('span')}
    print(addr_dict)
    gym_data.append(addr_dict)
    
    gym_hrs_data = soup.find('div', class_="columns small-12 medium-6")
    gym_hrs = {p: p.text for p in gym_hrs_data.findAll('p')}
    #print(gym_hrs)
    gym_hours.append(gym_hrs)
    
    

# print(gym_data)
    