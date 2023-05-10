# Objective: curate data from the hungrygowhere page
# This spider will crawl the webpage and print the featured deals and restaurant locations
# Things TODO: find the xpath for extracting the restaurant distance and add tags featured on the webpage to itemlistings like 'discount' etc
import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from ..items import simple_crawlerItem


class hungrygoSpider(scrapy.Spider):
    name = "hungryspider"
    allowed_domains = ["http://hungrygowhere.my"]
    start_urls = ["http://deals.hungrygowhere.my/latest"]

    def parse(self, response):
        sel = Selector(response)
        # descr1 = sel.xpath("//a[@class='description']/span/text()").extract()
        descr = sel.xpath("//h2/text()").extract()
        restuarantloc = sel.xpath("//h3/text()").extract()
        restuarnt_dist = sel.xpath("//span[@class='']//text()")

        for item in descr, restuarantloc, restuarnt_dist:
            print "Deal: ", item, "\nDistance: ", restuarnt_dist
        print "\n"

        '''
        for item in descr, restuarantloc:
            print "Deal: ",item," Area:",item
            print "\n"
        '''
