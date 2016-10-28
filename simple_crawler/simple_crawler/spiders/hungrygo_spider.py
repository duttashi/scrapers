# Objective: curate data from the hungrygowhere page
# This spider will crawl the webpage and print the featured deals and restaurant locations
# Things TODO: find the xpath for extracting the restaurant distance and add tags featured on the webpage to itemlistings like 'discount' etc
import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from simple_crawler.items import simple_crawlerItem


class hungrygoSpider(scrapy.Spider):
    name = "hungryspider"
    allowed_domains = ["http://hungrygowhere.my"]
    start_urls = ["http://deals.hungrygowhere.my/hotdeals/"]

    def parse(self, response):
        sel = Selector(response)
        # descr1 = sel.xpath("//a[@class='description']/span/text()").extract()
        descr = sel.xpath("//h2/text()").extract()
        restuarantloc = sel.xpath("//h3/text()").extract()

        for item in descr:
            print "Deal: ", item
        for loc in restuarantloc:
            print "Area: ", loc
        print "\n"

        '''
        for item in descr, restuarantloc:
            print "Deal: ",item," Area:",item
            print "\n"
        '''
