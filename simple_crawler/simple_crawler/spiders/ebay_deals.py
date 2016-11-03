# Load the required libraries
# Python ver: 2.7
# Scrapy ver: 1.2.0
# Using CrawlSpider because of the function parse_page. If want to use function parse then use BaseSpider.
# see this SO post http://stackoverflow.com/questions/5264829/why-does-scrapy-throw-an-error-for-me-when-trying-to-spider-and-parse-a-site

import scrapy
from scrapy.http import Request
# from scrapy.spiders import Rule
from scrapy.selector import Selector
from ..items import simple_crawlerItem


#from scrapy.linkextractors import LinkExtractor

class ebay_spider(scrapy.Spider):
    name = "ebay_spider"
    allowed_domains = ["http://ebay.com.my/"]
    start_urls = ["http://deals.ebay.com.my/"]

    #rules = [Rule(LinkExtractor(allow='page/*'), follow=True, callback='parse'), ]

    def parse(self, response):
        item = simple_crawlerItem()

        saletag = response.xpath("//span[@class='saleTag']/text()").extract()
        saletagalert = response.xpath("//span[@class='saleTag alert']/text()").extract()
        descr = response.xpath("//div/div/div/a/span/text()").extract()
        price = response.xpath("//div/div/div//span[@class='price']/text()").extract()

        for d, p, st, stp in zip(descr, price, saletag, saletagalert):
            item['descr'] = d.strip()
            item['price'] = p.strip()
            item['saletag'] = st.strip()
            item['saletagalert'] = stp.strip()
            yield item
