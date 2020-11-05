# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response, HtmlResponse


class WanbenSpider(scrapy.Spider):
    name = 'wanben'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/finish']

    def parse(self, response):
        # scrapy.http.response.html.HtmlResponse
        print(type(response))
        # print(response.body)
