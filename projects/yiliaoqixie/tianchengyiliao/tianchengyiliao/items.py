# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TianchengyiliaoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    category = scrapy.Field()
    region = scrapy.Field()
    department = scrapy.Field()
    qualification_certificate = scrapy.Field()
    info = scrapy.Field()
    manufactor = scrapy.Field()
    contact = scrapy.Field()
    mail = scrapy.Field()
    business_license = scrapy.Field()
    business_license_of_medical_devices = scrapy.Field()

