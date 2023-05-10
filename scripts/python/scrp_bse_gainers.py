# reference: https://github.com/sdabhi23/bsedata

from bs4 import BeautifulSoup as bs
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
}


def getGainers():
    baseurl = '''https://m.bseindia.com'''
    res = requests.get(baseurl, headers=headers)
    c = res.content
    soup = bs(c, "lxml")
    for tag in soup("div"):
        try:
            if(tag['id'] == 'divGainers'):
                resSoup = tag
                break
        except KeyError:
            continue
    children = list(resSoup.table.contents)
    children = children[1:]
    gainers = []
    for tr in children:
        td = tr.contents
        gainer = {
            "securityID": str(td[0].a.string),
            "scripCode": str(tr.td.a["href"].split("=")[1]),
            "LTP": str(td[1].string),
            "change": str(td[2].string),
            "pChange": str(td[3].string)
        }
        gainers.append(gainer)
    return gainers

def getLosers():
    baseurl = '''https://m.bseindia.com'''
    res = requests.get(baseurl, headers=headers)
    c = res.content
    soup = bs(c, "lxml")
    for tag in soup("div"):
        try:
            if(tag['id'] == 'divLosers'):
                resSoup = tag
                break
        except KeyError:
            continue
    children = list(resSoup.table.contents)
    children = children[1:]
    losers = []
    for tr in children:
        td = tr.contents
        loser = {
            "securityID": str(td[0].a.string),
            "scripCode": str(tr.td.a["href"].split("=")[1]),
            "LTP": str(td[1].string),
            "change": str(td[2].string),
            "pChange": str(td[3].string)
        }
        losers.append(loser)
    return losers


gainers = getGainers()
print(gainers)
losers = getLosers()
print(losers)