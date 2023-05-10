import scrapy

class TwitterSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ['twitter.com']
    start_urls = ['']

    def start_requests(self):
        url = 'https://www.twitter.com/'
        tag = getattr(self, 'username', None)
        if tag is not None:
            url = url + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.logger.debug('callback "parse": got response %r' % response)

    def parse_item(self, response):
        item = scrapy.Item()
        item['name'] = response.xpath('.//@data-name').extract()[0]
        item['tweet_count'] = response.css('.ProfileNav-value::text').extract()[0]
        return item

