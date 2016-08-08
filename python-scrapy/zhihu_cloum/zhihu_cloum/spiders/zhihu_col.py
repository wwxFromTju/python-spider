# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request,FormRequest
from zhihu_cloum.settings import *

class ZhihuColSpider(CrawlSpider):
    name = "zhihu_col"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        r'https://zhuanlan.zhihu.com/intelligentunit',
    )

    #def parse(self, response):
     #   pass

    def __init__(self):
        self.headers = HEADER
        self.cookies =COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, headers = self.headers, callback = self.parse_item, cookies =self.cookies)#jump to login page
    
    def parse_item(self, response):
        selector = Selector(response)
        print(selector.xpath('/*').extract())
