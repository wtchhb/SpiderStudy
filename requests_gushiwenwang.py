import requests
import uuid


from lxml import etree
from utils import header

def itempipline(item):
    """保存数据"""
    print(item)

def parse(html):
    root = etree.HTML(html)  #获取html的根元素 Element
    divs = root.xpath('//div[@class="left"]/div[@class="sons"]')  #list[<Element>.....]
    item = {}
    for div in divs:
        item['id'] = uuid.uuid4().hex
        item['name'] = div.xpath('.//p[1]//text()')[0]
        item['author'] = ' '.join(div.xpath('.//p[2]/a/text()'))
        item['content'] = '<br>'.join(div.xpath('.//div[@class="contson"]/text()'))
        item['tags'] = ','.join(div.xpath('./div[last()]/a/text()'))

        itempipline(item)

def get(url):
    resp = requests.get(url, headers={'User-Agent': header.get_ua()})
    
    if resp.status_code == 200:
        parse(resp.text)

    else:
        raise Exception('请求失败!')

if __name__ == '__main__':
    get("https://www.gushiwen.org/")