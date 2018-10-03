import scrapy
from scrapy.spiders import Spider
from simple_crawler.items import simple_crawlerItem
from scrapy.http import Request


class trivago_spider(scrapy.Spider):
    name = "myspider1"
    allowed_domains = ["www.lazada.com.my"]
    start_urls = ["http://www.lazada.com.my/shop-mobiles/?boost=3"]

    def parse(self, response):
        titles = response.xpath("//div[@class='product-card__price']")
        for title in titles:
            cost = simple_crawlerItem()
            cost["title"] = title
            yield cost
