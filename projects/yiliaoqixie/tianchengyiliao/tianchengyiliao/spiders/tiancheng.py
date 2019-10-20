# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TianchengSpider(CrawlSpider):
    name = 'tiancheng'
    allowed_domains = ['tecenet.com']
    start_urls = ['http://www.tecenet.com/chanpin/ks-0-0-0-0.html']

    pages = LinkExtractor(restrict_xpaths='//li[@class="next"]/a')
    details = LinkExtractor(restrict_xpaths='//div[@class="cp-card cp-img-card"]/div[@class="cp-img"]/a')

    rules = [
        Rule(pages, follow=True),
        Rule(details, callback='parse_item')
    ]

    def parse_item(self, response):
        # print(response.url)
        name = response.xpath('//div[@class="product-info-title"]/h1/text()').extract()
        if name:
            name = name[0]
        else:
            try:
                name = response.xpath('//div[@class="crumb"]/text()').extract()[-1].replace(' ', '')
            except:
                return 0
        print(name)

        # name = scrapy.Field()
#     img = scrapy.Field()
#     price = scrapy.Field()
#     brand = scrapy.Field()
#     model = scrapy.Field()
#     category = scrapy.Field()
#     region = scrapy.Field()
#     department = scrapy.Field()
#     qualification_certificate = scrapy.Field()
#     info = scrapy.Field()
#     manufactor = scrapy.Field()
#     contact = scrapy.Field()
#     mail = scrapy.Field()
#     business_license = scrapy.Field()
#     business_license_of_medical_devices = scrapy.Field()
