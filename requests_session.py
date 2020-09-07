"""
1.下载验证码图片
2. 图片验证码的打码--获取图片上的 验证阿妈
3.登录
4.获取个人收藏信息
"""
import uuid

import requests
from lxml import etree

from utils.header import get_ua
from utils.chaojiying import rec_code

#创建一个session对象
session = requests.session()    #获取验证码接口和登录的接口必须在同一个session中请求

def download_code():
    resp = session.get('https://so.gushiwen.cn/RandCode.ashx', headers={'User-Agent': get_ua()})
    with open('code.png', 'wb') as f:
        f.write(resp.content)

def get_code_str():
    download_code()
    return rec_code('code.png')

def login():
    resp = session.post('https://so.gushiwen.cn/user/login.aspx', data={
        'email': '1040196881@qq.com',
        'pwd': 'wtc1040196881',
        'code': get_code_str()  #验证码
    })

    if resp.status_code == 200:
        collect()
    else:
        print('-'*30)
        print(resp.text)

def collect():
    resp = session.get('https://so.gushiwen.cn/user/collect.aspx')
    parse(resp.text)

def parse(html):
    root = etree.HTML(html)  # 获取html的根元素 Element
    divs = root.xpath('//div[@class="left"]/div[@class="sons"]')  # list[<Element>, ..]
    item = {}
    for div in divs:
        item['id'] = uuid.uuid4().hex
        item['name'] = div.xpath('.//p[1]//text()')
        item['author'] = ' '.join(div.xpath('.//p[2]/a/text()'))
        item['content'] = '<br>'.join(div.xpath('.//div[@class="contson"]/text()'))
        item['tags'] = ','.join(div.xpath('./div[last()]/a/text()'))



if __name__ == "__main__":
    login()
