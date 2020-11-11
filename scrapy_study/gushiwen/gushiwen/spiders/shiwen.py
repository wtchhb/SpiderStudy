# -*- coding: utf-8 -*-
import scrapy


class ShiwenSpider(scrapy.Spider):
    name = 'shiwen'
    allowed_domains = ['gushiwen.org']
    start_urls = ['http://gushiwen.org/']

    def parse(self, response):
        pass
