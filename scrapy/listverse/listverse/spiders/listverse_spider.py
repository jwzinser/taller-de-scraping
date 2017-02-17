from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from listverse.items import ListVerseItem
from time import time
import csv
import re
import string
import sys
import json


class ListVerseSpider(CrawlSpider):
    name = 'lv_crawler'
    allowed_domains = ["http://listverse.com/","listverse.com"]
    start_urls =['http://listverse.com/']
    rules = [
            Rule(LinkExtractor(allow=[r'.*listverse.com/\d+/\d+/\d+/*']), callback='parse_articles'),
            Rule(LinkExtractor(allow=[r'.*listverse.*']), callback='parse_paginacion',follow=True),
        ]
    def parse_paginacion(self,response):
        item = ListVerseItem()
        item['paginacion'] = response.url
        #yield item

    def parse_articles(self, response):
        #item = ListVerseItem()
        item = {}
        item['titulo'] = response.xpath('//h1/text()').extract()[0].encode('utf-8')
        item['url'] = response.url
        item['category'] = response.xpath('//section[@class="new the-article"]/article/a[@class="title-category"]/text()').extract()[0]

        item['author'] = response.xpath('//article/p/span[@class="author"]/a/text()').extract()[0]
        item['time'] = response.xpath('//article/p/time/text()').extract()[0]

        #item['body_list'] = response.xpath('//article/p/text()').extract()
        #item['title_list'] = response.xpath('//article/h2/text()').extract()

        with open('/Users/juanzinser/Documents/MCC/gran_escala/taller-de-scraping/scrapy/listverse/data/'+item['titulo']+'.json', 'w') as fp:
            json.dump(item, fp)

        yield item
