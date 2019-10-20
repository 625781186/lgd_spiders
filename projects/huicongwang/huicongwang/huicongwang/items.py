# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HuicongwangItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    total_num = scrapy.Field()
    period_dispatch = scrapy.Field()
    freight = scrapy.Field()
    ordering_information = scrapy.Field()
    detail_info = scrapy.Field()
    Manufactor = scrapy.Field()
    contact_num = scrapy.Field()
    Contact_person = scrapy.Field()

