#!/usr/bin/env python
# coding: utf-8

# Objective: Parsing web links at different depths

# import the required libraries
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# the website to scrape
link = "https://www.courts.com.sg/sitemap"

# create beatiful soup object
res = requests.get(link)
soup = BeautifulSoup(res.text, "lxml")

# write the program logic
# CAUTION: Executing the given logic will traverse the entire website and can take more than 2 minutes to complete.
for item in soup.select(".nav-dropdown li a"):
    if "#" in item.get("href"):continue  #kick out invalid links
    newlink = urljoin(link,item.get("href"))
    req = requests.get(newlink)
    sauce = BeautifulSoup(req.text,"lxml")
    for elem in sauce.select(".product-item-info .product-item-link"):
        print(elem.get_text(strip=True))

# As we can see from the above logic, there is no way to limit the `crawling-depth`. For instance, in `R`, the library `Rcrawler` provides 'MaxDepth' so the crawler will go within a certain number of links from the homepage within that domain.
# `Rcrawler(Website = "https://stackoverflow.com/", no_cores = 4, no_conn = 4, ExtractCSSPat = c("div"), ****MaxDepth=5****)`
# 
# So the obvious question is, "how to limit the crawling depth when using Beautiful Soup?".

# Answer: There is no function in BeautifulSoup because BeautifulSoup is not crawler.
# It only parses string with HTML so you could search in HTML.
# 
# There is no function in requests because requests is no crawler too.
# It only reads data from server so you could use it with BeautifulSoup or similar.
# 
# If you use BeautifulSoup and request then you have to do all on your own - you have to build crawling system from scratch.
# 
# `Scrapy` is a real crawler (or rather framework to build spiders and crawl network).
# And it has option `DEPTH_LIMIT`

