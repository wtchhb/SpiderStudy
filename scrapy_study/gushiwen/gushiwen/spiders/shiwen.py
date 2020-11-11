# -*- coding: utf-8 -*-
import scrapy


class ShiwenSpider(scrapy.Spider):
    name = 'shiwen'
    allowed_domains = ['gushiwen.org']
    start_urls = ['https://so.gushiwen.cn/user/collect.aspx']

    def parse(self, response):
        pass
