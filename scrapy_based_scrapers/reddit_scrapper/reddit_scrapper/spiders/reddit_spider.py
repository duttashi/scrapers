# -*- coding: utf-8 -*-
import scrapy

# If response code is 200, then it means the request was successfully received, understood, and accepted
# See this link for more info https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

class RedditSpiderSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['reddit']
    start_urls = ['https://www.reddit.com/r/popular/?geo_filter=MY']

    def parse(self, response):
        items = []
        for div in response.css('div.sitetable div.thing'):
            try:
                title = div.css('p.title a::text').extract_first()
                votes_div = div.css('div.score.unvoted')
                votes = votes_div.css('::attr(title)').extract_first()
                votes = votes or votes_div.css('::text').extract_first()

                items.append({'title': title, 'votes': int(votes)})
            except:
                pass

        if len(items) > 0:
            timestamp = response.meta['wayback_machine_time'].timestamp()
            return {'timestamp': timestamp, 'items': items}
