# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/book/']

    rules = (
        # 所有图书分类的css样式匹配
        Rule(LinkExtractor(restrict_css='.sub-catalog'),
             follow=True),
        Rule(LinkExtractor('/book/\d+?_\d+?\.html'),
             follow=True),  # 分页的href正则匹配
        # 图书详情信息的正则匹配
        Rule(LinkExtractor('/book/\d+/'), 'parse_item', follow=False)
    )

    def parse_item(self, response):
        item = {}
        item['name'] = response.css('h1::text').get()

        # 使用ImagePipeline下载图片时，需要使用image_urls字段，是可迭代的list/tuple类型
        item['image_urls'] = response.css('.pic img::attr("src")').extract()
        # 下载图片之后，保存本地的文件位置
        item['images'] = []
        item['price'] = response.css('.num::text').get()
        table = response.css('#ct100_c1_bookleft table')
        item['author'] = table.xpath('.//tr[1]/td[2]/text()').get()
        item['publisher'] = table.xpath('.//tr[2]/td[2]/a/text()').get()

        table = response.css('.book-details>table')
        item['isbn'] = table.xpath('.//tr[1]/td[2]/text()').get()
        item['publish_date'] = table.xpath('.//tr[1]/td[4]/text()').get()
        item['page'] = table.xpath('.//tr[2]/td[4]/text()').get()

        yield item
