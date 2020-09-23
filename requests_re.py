"""
基于正则re模块接续数据
"""

import re
import os

import requests

from utils.header import get_ua

base_url = 'http://sc.chinaz.com/tupian/'
url = f'{base_url}shuaigetupian.html'
headers = {
    'User-Agent': get_ua()
}

if os.path.exists('mn.html'):
    with open('mn.html', encoding='utf-8') as f:
        html = f.read()
else:
    resp = requests.get(url, headers=headers)
    print(resp.encoding)    # ISO-8859-1
    resp.encoding='utf-8'   # 可以修改响应的状态码
    assert resp.status_code == 200
    html = resp.text
    with open('mn.html', 'w', encoding=resp.encoding) as f:
        f.write(html)

# print(html)
# [\u4e00-\u9fa5]   匹配中文字符
compile = re.compile(r'<img src2="(.*?)" alt="(.*?)">')
compile2 = re.compile(r'<img alt="(.*?)" src="(.*?)">')
images = compile.findall(html)   #返回list
if len(images) == 0:
    images = compile2.findall(html)
print(len(images), images, sep='\n')

next_url = re.findall(r'<b>24</b></a><a href="(.*?)" class="nextpage">', html, re.S)
print(base_url + next_url[0])