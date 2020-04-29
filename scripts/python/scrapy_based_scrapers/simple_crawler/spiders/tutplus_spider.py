# Load the required libraries
# reference: http://blog.siliconstraits.vn/building-web-crawler-scrapy/
# To execute this spider, change the spider name in settings.py and in scrapy configuration file in Pycharm IDE
# Learnings: You can create as many spiders as you want in one project
# TODO activity: Find out how to execute multiple spiders from one scrapy project

import scrapy
from scrapy.spiders import Spider
from simple_crawler.items import simple_crawlerItem
from scrapy.http import Request  # Request class enables us to recursively crawl a page.


class tutplus_spider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["code.tutsplus.com"]
    start_urls = ["http://code.tutsplus.com/"]


def parse(self, response):
    titles = response.xpath('//a[contains(@class, "posts__post-title")]/h1/text()').extract()
    for title in titles:
        item = simple_crawlerItem()
        item["title"] = title
        yield item
