# Load the required libraries
# Python ver: 2.7
# Scrapy ver: 1.2.0
import scrapy

from scrapy.http import Request
import csv
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from simple_crawler.items import simple_crawlerItem


class ebay_spider(scrapy.Spider):
    name = "myspider3"
    allowed_domains = ["http://deals.ebay.com.my/"]
    start_urls = ["http://deals.ebay.com.my/"]

    def parse(self, response):
        sel = Selector(response)
        # descr1 = sel.xpath("//a[@class='description']/span/text()").extract()
        descr1 = sel.xpath("//a/span/text()").extract()
        price2 = sel.xpath("//span[@class='price']/text()").extract()
        print descr1
        print '--------'
        print price2
        print '----'

        # writing to a csv file
        mywriter = csv.writer(open("ebaytest.csv", "w"))
        head = ("Description", "Price")
        mywriter.writerows(head)
        for i in range(0, len(price2)):
            mywriter.writerows([descr1[i].encode('utf-8'),
                                price2[i]
                                ]
                               )



            ## Some notable issues
            # 1. If you are getting the userwarning: userwarning: you do not have a working installation of the service_identity module: 'no module named pyasn1_modules.rfc2459'.
            # Solution-1 : The solution to 1 is in the terminal type pip install service_identity. See this answer on SO http://stackoverflow.com/questions/24089484/python-no-module-named-service-identity
            # 2. If you getting warning scrapy.spider is deperecated then use scrapy.spiders
            # 3. If you get the error unicodeencodeerror 'ascii' codec can't encode characters in position ordinal not in range(128)
            # Solution-3: http://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
