# Load the required libraries
# Python ver: 2.7
# Scrapy ver: 1.2.0
# Using CrawlSpider because of the function parse_page. If want to use function parse then use BaseSpider.
# see this SO post http://stackoverflow.com/questions/5264829/why-does-scrapy-throw-an-error-for-me-when-trying-to-spider-and-parse-a-site

import scrapy
from scrapy.http import Request
import csv
from scrapy.spiders import Rule
from scrapy.selector import Selector
from ..items import simple_crawlerItem
from scrapy.linkextractors import LinkExtractor

class ebay_spider(scrapy.Spider):
    name = "ebay_spider"
    allowed_domains = ["http://ebay.com.my/"]
    start_urls = ["http://deals.ebay.com.my/"]

    rules = [Rule(LinkExtractor(allow='page/*'), follow=True, callback='parse'), ]

    def parse(self, response):
        item = simple_crawlerItem()
        # Note / selects the specific tag text and // selects the specific tag text as well as its children tags
        descr = response.xpath("//div/div/div/a/span/text()").extract()
        price = response.xpath("//div/div/div//span[@class='price']/text()").extract()
        # Note: By default Item() returns dictionary object in a key value pair. So use for loop to seprate the keys and values.
        # This is the best approach. See this SO post on the same http://stackoverflow.com/questions/36025821/how-to-fix-my-scrapy-dictionary-output-format-for-csv-json
        for d, p in zip(descr, price):
            item['descr'] = d.strip()
            item['price'] = p.strip()
            yield item
