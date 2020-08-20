import requests

from lxml import etree
from utils import header


def parse(html):
    root = etree.HTML(html)  #获取html的根元素


def get(url):
    resp = requests.get(url, headers={'User-Agent': header.get_ua()})
    
    if resp.status_code == 200:
        parse(resp.text)

    else:
        raise Exception('请求失败!')