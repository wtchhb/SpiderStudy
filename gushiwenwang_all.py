import requests

from lxml import etree
from utils import header


base_url = "https://so.gushiwen.cn"


def parse(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@class="right"]/div[@class="son1"]')


def get_leader(url):
    resp = requests.get(url, header={"User-Agent":header.get_ua()})
    if resp.status_code == 200:
        parse(resp.text)
    else:
        raise Exception('请求失败!')