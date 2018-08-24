# Tutorial from: http://seanmckaybeck.com/scrapy-the-basics.html
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.item import Item, Field


class RedditCrawler(CrawlSpider):
    name = "reddit-crawler"
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/learnpython/new']
    custom_settings = {
        'BOT_NAME': 'reddit-scraper',
        'DEPTH_LIMIT': 7,
        'DOWNLOAD_DELAY': 3  # wait 3 seconds
    }


def parse(self, response):
    s = Selector(response)
    next_page = s.xpath('//span[@class="nextprev"]//a/@href').extract()[0]
    if len(next_page):
        yield self.make_requests_from_url(next_page)
    posts = Selector(response).xpath('//div[@id="siteTable"]/div[@onclick="click_thing(this)"]')

    for post in posts:
        i = simple_crawlerItem()
        i['title'] = post.xpath('div[2]/p[1]/a/text()').extract()[0]
        i['url'] = post.xpath('div[2]/ul/li[1]/a/@href').extract()[0]
        i['submitted'] = post.xpath('div[2]/p[2]/time/@title').extract()[0]
        yield i
