import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from simple_crawler.items import simple_crawlerItem


class CraigslistSpider(scrapy.Spider):
    name = "craig"  # This name should be the same as the BOT_NAME in settings.py
    allowed_domains = ["craigslist.org"]

    def start_requests(self):
        urls = [
            'http://malaysia.craigslist.org/search/edu'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//span[@class='pl']")
        for titles in titles:
            title = titles.select("a/text()").extract()
            link = titles.select("a/@href").extract()
            print title, link
