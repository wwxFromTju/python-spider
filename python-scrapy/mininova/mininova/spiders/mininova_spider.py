from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mininova.items import MininovaItem

class MininovaSpider(CrawlSpider):

    name = 'mininova'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org/today']
    rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def __init__(self, *args, **kwargs):
        super(MininovaSpider, self).__init__(*args, **kwargs)
        print('args', args)
        print('kwargs', kwargs)
    
    def parse_torrent(self, response):
        torrent = MininovaItem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("//h1/text()").extract()
        torrent['description'] = response.xpath("//div[@id='description']").extract()
        torrent['size'] = response.xpath("//div[@id='info-left']/p[2]/text()[2]").extract()
        return torrent
