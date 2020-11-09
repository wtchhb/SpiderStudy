# -*- coding: utf-8 -*-
import uuid

import scrapy
from scrapy.http import Response, HtmlResponse, Request
from scrapy.selector import SelectorList, Selector

from qidian.items import *


class WanbenSpider(scrapy.Spider):
    name = 'wanben'
    allowed_domains = ['www.qidian.com', 'book.qidian.com']
    start_urls = ['https://www.qidian.com/finish']

    def parse(self, response: Response):
        if response.status == 200:
            # 解析数据
            lis = response.css('.all-img-list li')  # SelectorList
            print(f'-----{len(lis)}-------')
            for li in lis:
                item = BookItem()
                item['book_id'] = uuid.uuid4().hex
                # li 对象类型是Selector , 注意：Selector没有x函数
                a = li.xpath('./div[1]/a')
                item['book_url'] = a.xpath('./@href').get()
                item['book_cover'] = a.xpath('./img/@src').get()

                item['book_name'] = li.xpath('./div[2]/h4//text()').get()
                item['author'], *item['tags'] = li.css('.author a::text').extract()
                item['summary'] = li.css('.intro::text').get()

                yield item

                # 请求小说的详情
                yield Request('https://' + item['book_url'], callback=self.parse_info, priority=1, meta={'book_id': item['book_id']})

            # 找出下一页
            next_url = response.css('.lbf-pagination-item-list').xpath('./li[last()]/a/@href').get()
            if next_url.find('javascript') == -1: # 存在下一页
                yield Request('https://' + next_url, priority=100)  # 优先级值越高，会优先下载

        # scrapy.http.response.html.HtmlResponse
        # print(type(response))
        # print(response.body)

    def parse_info(self, response: Response):
        print('-----------------解析小说的详情页面-----------------', response.meta['book_id'])
