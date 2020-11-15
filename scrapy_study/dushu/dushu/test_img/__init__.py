#!/usr/bin/python3
# coding: utf-8
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Referer': 'https://www.dushu.com/'
}

resp = requests.get('https://img.dushu.com/2020/11/13/11220328447840.jpg_200.jpg',
                    headers=headers)

assert resp.status_code == 200
with open('t1.jpg', 'wb') as f:
    f.write(resp.content)