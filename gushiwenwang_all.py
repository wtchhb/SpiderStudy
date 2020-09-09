import requests

from lxml import etree
from utils import header


base_url = "https://so.gushiwen.cn"


def parse_head_url(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@class="right"]/div[@class="son1"]')
    for div in divs:
        urls = div.xpath('./child::a/@href')

    print(urls[1:5])

    for url in urls[1:5]:
        print(url)

    return urls[1:5]


def get_leader(url):
    resp = requests.get(url,
                        headers={'User-Agent': header.get_ua()}
                        )
    if resp.status_code == 200:
        parse_head_url(resp.text)
    else:
        raise Exception('请求失败!')

def parse(html):
    pass



if __name__ == "__main__":
    get_leader('https://www.gushiwen.org/')