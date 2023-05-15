# https://github.com/sdabhi23/bsedata/blob/master/bsedata/indices.py
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
}


def indices(category):
    cat = {
        "market_cap/broad": "1,2",
        "sector_and_industry": "2,2",
        "thematics": "3,2",
        "strategy": "4,2",
        "sustainability": "5,2",
        "volatility": "6,1",
        "composite": "7,1",
        "government": "8,1",
        "corporate": "9,1",
        "money_market": "10,1"
    }
    try:
        ddl_category = cat[category]
    except KeyError:
        print('''
### Invalid category ###
Use one of the categories mentioned below:

market_cap/broad
sector_and_industry
thematics
strategy
sustainability
volatility
composite
government
corporate
money_market
        ''')
        return
    baseurl = '''https://m.bseindia.com/IndicesView_New.aspx'''
    res = requests.get(baseurl, headers=headers)
    c = res.content
    soup = bs(c, "lxml")
    options = {
        '__EVENTTARGET': 'ddl_Category',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATEGENERATOR': '162C96CD',
        'UcHeaderMenu1$txtGetQuote': '',
        '__EVENTVALIDATION': '',
        '__VIEWSTATE': ''
    }
    for input in soup("input"):
        try:
            if(input['type'] == "hidden"):
                if(input['id'] == '__VIEWSTATE'):
                    options['__VIEWSTATE'] = input['value']
                elif(input['id'] == '__EVENTVALIDATION'):
                    options['__EVENTVALIDATION'] = input['value']
        except KeyError:
            continue
    options['ddl_Category'] = ddl_category
    res = requests.post(url=baseurl, data=options, headers=headers)
    c = res.content
    soup = bs(c, "lxml")
    index_list = []
    for td in soup('td'):
        try:
            if(td['class'][0] == 'TTRow_left'):
                index = {}
                index['currentValue'] = td.next_sibling.string.strip()
                index['change'] = td.next_sibling.next_sibling.string.strip()
                index['pChange'] = td.next_sibling.next_sibling.next_sibling.string.strip()
                index['scripFlag'] = td.a['href'].strip().split('=')[1]
                index['name'] = td.a.string.strip().replace(';', '')
                index_list.append(index)
        except KeyError:
            continue
    results = {}
    for span in soup("span", id="inddate"):
        results['updatedOn'] = span.string[6:].split('|')[0].strip()
    results['indices'] = index_list
    return results

stock_indexes = indices(category="money_market")
print(stock_indexes)