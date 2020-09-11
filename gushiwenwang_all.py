import requests
import time

from lxml import etree
from utils import header


base_url = "https://so.gushiwen.cn"


def parse_head_url(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@class="right"]/div[@class="son1"]')
    for div in divs:
        urls = div.xpath('./child::a/@href')
        get(urls[1:5])
        # print(urls[1:5])

    # for url in urls:
    #     test = get(url)
    #     print(test)

        # resp_con = requests.get(url,
        #                         headers={'User-Agent': header.get_ua()}
        #                         )
        # if resp_con.status_code == 200:
        #     parse(resp_con.text)
        # else:
        #     raise Exception('请求失败!')
    # print(urls[1:5])

    # for url in urls[1:5]:
    #     print(url)

def get_leader(url):
    resp = requests.get(url,
                        headers={'User-Agent': header.get_ua()}
                        )
    if resp.status_code == 200:
        parse_head_url(resp.text)
    else:
        raise Exception('请求失败!')

def parse(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@class="left"]/div[@class="sons"]')
    for div in divs:

        name = div.xpath('.//p[1]//text()')
        author = ' '.join(div.xpath('.//p[2]//text()'))
        content = div.xpath('.//div[@class="contson"]/text()')
        tag = ','.join(div.xpath('./div[last()]/a/text()'))

        print(name, author, content, tag)

    next_url = [base_url + root.xpath('//a[@class="amore"]/@href')[0]]
    print(next_url)
    time.sleep(0.5)
    try:
        get(next_url)
    except Exception:
        pass

def get(urls):
    for url in urls:
        resp = requests.get(url,
                            headers={'User-Agent':header.get_ua()}
                            )
        if resp.status_code == 200:
            parse(resp.text)
        else:
            raise Exception('请求失败')

if __name__ == "__main__":
    get_leader('https://www.gushiwen.cn')