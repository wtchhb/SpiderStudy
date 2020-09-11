import requests
import uuid
import time
import pymysql
import os
import codecs
import re

from lxml import etree
from csv import DictWriter

from utils import header
from dao import Connection_spider

conn = Connection_spider()
base_url = 'http://www.hydcd.com/cy/'

def itempipeline(item):
    """保存数据"""
    print(item)
    # 字段字符串： id,name,pinyin,explain,content
    # values占位字符串： %(id)s, %(name)s, %(author)s, %(content)s,%(tags)s
    sql = 'insert into chengyugushi(%s) values(%s)'
    fields = ','.join(item.keys())
    value_placeholds = ','.join(['%%(%s)s' % key for key in item])


    with conn as c:
        # sql_all = sql % (fields, value_placeholds)
        # print(sql_all)
        # c.execute(sql_all, item)
        try:
            c.execute("insert into chengyugushi values('%s', '%s', '%s', '%s', '%s')" % (item['id'], item['name'], item['pinyin'], item['explain'], item['content']))
        except Exception:
            pass


has_header = os.path.exists('cehngyugushi.csv')  # 是否第一次写入csv的头
header_fields = ('id', 'name', 'pinyin', 'explain', 'content')


def itempipeline4csv(item):
    global has_header
    with open('cehngyugushi.csv', 'a', encoding='utf-8') as f:
        writer = DictWriter(f, fieldnames=header_fields)
        if not has_header:
            writer.writeheader()  # 写入第一行的标题
            has_header = True

        writer.writerow(item)  # 写入数据

def parse_old_url(html):
    root = etree.HTML(html)
    divs = root.xpath('//td[@valign="top"]/div[@align="left"]')
    # div = divs[1]
    urls = divs[1].xpath('//li//a/@href')
    get(urls)
    print(urls)

def get_old_url(url):
    resp = requests.get(url,
                        headers={'User-Agent' : header.get_ua(), 'Connection': 'close'}
                        )
    if resp.status_code == 200:
        parse_old_url(resp.text)
    else:
        raise Exception('请求失败')

def parse(html):
    root = etree.HTML(html, parser=etree.HTMLParser(encoding='gb2312'))
    divs = root.xpath('//td[@valign="top"]/div[@align="left"]')
    item = {}
    for div in divs[:-1]:
        item['id'] = uuid.uuid4().hex
        # try:
        #     item['name'] = re.sub('\W+', ' ', div.xpath('child::font[2]/text()')[0]).split(" ")[2]
        # except Exception:
        #     item['name'] = div.xpath('child::font[2]/text()')[0].split('：')[1]
        try:
            item['name'] = re.sub('\W+', ' ', div.xpath('child::font[2]/text()')[0]).split(" ")[2]
        except Exception:
            print('请求错误')
            continue
        # item['pinyin'] = div.xpath('//font[2]/p[1]/text()')[0].split("：")[1].split("\r")[0]
        item['pinyin'] = ' '.join(re.sub('\W+', ' ', div.xpath('//font[2]/p/text()')[0]).split(" ")[2:-1])
        # item['explain'] = (((divs[0].xpath('//font[2]/p[2]/text()')[0]).split("：")[-1]).split("\r")[0].split(' ')[-1])
        item['explain'] = ','.join(re.sub('\W+', ' ', div.xpath('//font[2]/p[2]/text()')[0]).split(" ")[2:])
        item['content'] = re.sub('\W+', ' ', ''.join(div.xpath('//p/font/text()')[::]))
        # content = (((div.xpath('//p/font/text()')[0]).split("\u3000")[2]).split("\r"))[0]
        # try:
        #     item['content'] = ''.join((((div.xpath('//p/font/text()')[0]).split("\u3000")[2]).split("\r"))[0])
        # except Exception:
        #     try:
        #         item['content'] = ''.join((div.xpath('//p//span/text()')[0]).split("\u3000")[2].split('\r')[0])
        #     except Exception:
        #         item['content'] = ''.join(divs[1].xpath('//p/font/text()'))
        # itempipeline4csv(item)
        print(item['id'], item['name'], item['pinyin'], item['explain'], item['content'])
        itempipeline(item)



def get(urls):
    for url in urls:
        resp = requests.get(base_url + url,
                            headers={'User-Agent': header.get_ua()}
                            )
        resp.encoding = "gb2312"
        if resp.status_code == 200:
            parse(resp.text)
        else:
            raise Exception('请求失败')


if __name__ == "__main__":
    get_old_url('http://www.hydcd.com/cy/chengyugushi.htm')



