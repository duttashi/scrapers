# So officially this will be my first attempt to crawling.
# Keep things simple for now. Create a crawler to crawl reddit website on data science
# Objective: gather all the posts, posted by, time stamp and votes

import scrapy
from scrapy.spiders import Spider
from simple_crawler.items import simple_crawlerItem
from scrapy.http import Request


class reddit_spider(scrapy.Spider):
    name = "myspider2"
    allowed_domains = ["www.reddit.com"]
    start_urls = ["https://www.reddit.com/r/datascience/"]

    def parse(self, response):
        post_title = response.xpath("//div/p[@class='title']")
        for title in post_title:
            post_t = simple_crawlerItem()
            post_t["title"] = title.extract()
            yield post_t
        post_timestamp = response.xpath("//p/time[@class='live-timestamp']")
        for time_stamp in post_timestamp:
            post_ts = simple_crawlerItem()
            post_ts["live_timestamp"] = time_stamp.extract()
            yield post_ts


'''
TODO:
1. go to next page and next
'''

'''
Xpaths:
//div/p[@class="title"]|//p/time[@class="live-timestamp"]
//div/p[@class="title"]|//p/time[@class="live-timestamp"]|//p[@class="tagline"]
//div/p[@class="title"]|//p/time[@class="live-timestamp"]|//p[@class="tagline"]|//a[@class="bylink comments may-blank"]
//div/p[@class="title"]|//p/time[@class="live-timestamp"]|//p[@class="tagline"]|//a[@class="bylink comments may-blank"]//div[@class="score dislikes"]


'''
