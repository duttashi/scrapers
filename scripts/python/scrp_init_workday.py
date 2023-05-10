import requests

headers = { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json,application/xml'}

r = requests.get('https://wd1.myworkdaysite.com/en-US/recruiting/upenn/careers-at-penn', headers=headers)
# links = ['https://wd1.myworkdaysite.com' + i['title']['commandLink'] for i in r.json()['body']['children'][0]['children'][0]['listItems']]
# print(links)