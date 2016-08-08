# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from douban250.items import Douban250Item

class Douban250movie2Spider(CrawlSpider):
    name = "douban250movie2"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['https://movie.douban.com/top250']
    rules=[
            Rule(LinkExtractor(allow=['\?start=\d+.*'])),
            Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),'parse_item')
            ]

    def parse_item(self, response):
        sel = response
#        print(sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract())
        item = Douban250Item()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//*[@id="info"]/span[3]/span[2]/a/text()').extract()
        return item

