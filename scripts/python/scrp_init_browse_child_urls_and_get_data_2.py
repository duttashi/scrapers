# -*- coding: utf-8 -*-
"""
Created on Thu May  6 23:00:59 2021
Source: https://stackoverflow.com/questions/67311882/trouble-scraping-all-the-books-from-a-section-without-hardcoding-payload
@author: Ashish
"""

import json
import re

import requests
from bs4 import BeautifulSoup


# The chunk is how many carousel items are going to be requested for;
# this can vary from 4 - 10 items, as on the web-page.
# Also, the other list is used as the indexes key in the payload.
def get_idx_and_indexes(carousel_ids: list, chunk: int = 5) -> iter:
    for index in range(0, len(carousel_ids), chunk):
        tmp = carousel_ids[index:index + chunk]
        yield tmp, [carousel_ids.index(item) for item in tmp]


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36",
}

product_url = 'https://www.amazon.de/Rust-Programming-Language-Covers-2018/dp/1718500440/'
# Getting the product HTML as it carries all the carousel data items 
with requests.Session() as session:
    r = session.get("https://www.amazon.com", headers=headers)
    page = session.get(product_url, headers=headers)

# This is where the carousel data sits along with all the items needed to make
# the following requests e.g. items, acp-params, linkparameters, marketplaceid etc.
initial_soup = BeautifulSoup(
    re.search(r"<!--CardsClient-->(.*)<input", page.text).group(1),
    "lxml",
).find_all("div")

# Preparing all the details for subsequent requests to carousel_endpoint
item_ids = json.loads(initial_soup[3]["data-a-carousel-options"])["ajax"]["id_list"]
payload = {
    "aAjaxStrategy": "promise",
    "aCarouselOptions": initial_soup[3]["data-a-carousel-options"],
    "aDisplayStrategy": "swap",
    "aTransitionStrategy": "swap",
    "faceoutkataname": "GeneralFaceout",
    "faceoutspecs": "{}",
    "individuals": "0",
    "language": "en-US",
    "linkparameters": initial_soup[0]["data-acp-tracking"],
    "marketplaceid": initial_soup[3]["data-marketplaceid"],
    "name": "p13n-sc-shoveler_hgm4oj1hneo",  # this changes by can be ignored
    "offset": "6",
    "reftagprefix": "pd_sim",
}

headers.update(
    {
        "x-amz-acp-params": initial_soup[0]["data-acp-params"],
        "x-requested-with": "XMLHttpRequest",
    }
)

# looping through the carousel data and performing requests
carousel_endpoint = " https://www.amazon.com/acp/p13n-desktop-carousel/funjjvdbohwkuezi/getCarouselItems"
for ids, indexes in get_idx_and_indexes(item_ids):
    payload["ids"] = ids
    payload["indexes"] = indexes
    # The actual carousel data
    response = session.post(carousel_endpoint, json=payload, headers=headers)
    carousel = BeautifulSoup(response.text, "lxml").find_all("a")
    print("\n".join(a.getText() for a in carousel))