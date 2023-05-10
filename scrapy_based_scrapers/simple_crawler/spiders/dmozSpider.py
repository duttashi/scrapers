import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from simple_crawler.items import simple_crawlerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class dmozSpider(scrapy.Spider):
    name = "dmozspider"
    allowed_domains = ["http://dmoz.org"]
    start_urls = ["http://www.dmoz.org/",
                  "http://www.dmoz.org/Arts/Awards/Golden_Globe_Awards/"
                  ]

    rules = (
        Rule(LinkExtractor(allow='sub-cat'))

    )

    def parse(self, response):
        sel = Selector(response)
        # descr1 = sel.xpath("//a[@class='description']/span/text()").extract()
        descr = sel.xpath("//h2/a/text()").extract()
        print descr
        yield Request(callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        descr = sel.xpath("//div[@class='site-title']/text()").extract()
        print descr
