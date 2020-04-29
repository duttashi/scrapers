from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from simple_crawler.items import simple_crawlerItem


class blog_post_scrape(CrawlSpider):
    name = "blogpostscraper"  # give your spider a unique name because it will be used for crawling the webpages

    # allowed domain restricts the spider crawling
    allowed_domains = ["www.edumine.wordpress.com"]
    # in start_urls you have to specify the urls to crawl from
    start_urls = ["https://edumine.wordpress.com/tag/python/"]
    rules = [Rule(LinkExtractor(allow='page/*'), follow=True, callback='parse_page'), ]

    def parse_page(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("//h1[@class='entry-title']")

        items = []
        with open("itemLog.csv", "w") as f:
            for title in titles:
                item = simple_crawlerItem()
                item["post_title"] = title.xpath("//h1[@class='entry-title']//text()").extract()
                item["post_time"] = title.xpath("//time[@class='entry-date']//text()").extract()
                item["text"] = title.xpath("//p//text()").extract()
                item["link"] = title.select("a/@href").extract()

                items.append(item)

                f.write('post title: {0}\n, post_time: {1}\n, post_text: {2}\n'.format(item['post_title'],
                                                                                       item['post_time'], item['text']))
                print "#### \tTotal number of posts= ", len(items), " in category####"
