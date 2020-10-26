"""
http://www.meinv.hk/?cat=28
爬取美女网
-   requests
-   bs4
-   csv 存储
-   扩展  协程  asyncio
"""
import time

import requests

from utils.header import get_ua
from bs4 import BeautifulSoup, Tag

headers = {
    'User-Agent': get_ua()
}


def get(url):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        parse(resp.text)


def parse(html):
    # print(html)
    # with open('mv.html', 'w', encoding='utf-8') as f:
    #     f.write(html)

    root = BeautifulSoup(html, 'lxml')
    content_boxs = root.select('.content-box')

    for content_box in content_boxs:
        item = {}
        img: Tag = content_box.find('img')
        item['name'] = img.attrs.get('alt')
        item['cover'] = img.attrs.get('src')
        info = content_box.select('.posts-text')[0].get_text()

        try:
            _, birthday, city = [txt.strip() for txt in info.split('/')]
            item['birthday'], item['city'] = birthday[2:].strip(), city[2:].strip()
        except:
            item['birthday'], item['city'] = ('', '')
        itempipeline(item)

    # 加载下一页
    post('http://www.meinv.hk/wp-admin/admin-ajax.php')


page = 2


def post(url):
    print('-----下一页------', url)
    time.sleep(1)
    global page
    print('----加后--1----', page)
    resp = requests.post(url, data={
        'total': 24,
        'action': 'fa_load_postlist',
        'paged': page,
        'category': 28,
        'wowDelay': '0.3s'
    }, headers=headers)

    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        ret = resp.json()
        parse(ret['postlist'])

        page += 1
        print('----加后----', page)


def itempipeline(item):
    print(item)


if __name__ == '__main__':
    start_url = 'http://www.meinv.hk/?cat=28'
    get(start_url)