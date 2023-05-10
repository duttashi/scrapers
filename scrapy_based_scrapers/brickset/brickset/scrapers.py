import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    allowed_domains = [""]
    start_urls = ['http://brickset.com/sets/year-2018']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h1 a ::text'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
            }
            #pass
        #ratings = response.xpath("//div[@class=rating")
        #print(ratings+"\n")
