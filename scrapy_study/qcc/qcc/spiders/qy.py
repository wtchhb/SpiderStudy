# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QySpider(CrawlSpider):
    name = 'qy'
    allowed_domains = ['qcc.com']
    start_urls = ['https://www.qcc.com/g_AH.html']

    rules = (
        Rule(LinkExtractor(allow=r'g_{A-Z}{2,}\.html',
                           deny=r'g_[A-Z]{2,}_\d+\.html',),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='.pagination'),
             callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        item = {}

        trs = response.css('.m_srchList tr')
        for tr in trs:
            item['cover'] = tr.xpath('./td[1]/img/@src').get()
            item['name'] = tr.xpath('./td[2]/a[1]/text()').get()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return item
