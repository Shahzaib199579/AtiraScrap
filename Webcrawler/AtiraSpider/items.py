# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AtiraspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    buildingName = scrapy.Field()
    roomName = scrapy.Field()
    price = scrapy.Field()
    capacity = scrapy.Field()
    roomFeatures = scrapy.Field()
    location = scrapy.Field()
