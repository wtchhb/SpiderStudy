import requests

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}

def get_all():
    url = 'http://www.hydcd.com/cy/gushi/0340ly.htm'
    resp = requests.get(url, headers=headers)
    resp.encoding = "gb2312"
    if resp.status_code == 200:
        html = resp.text
        print(html)



if __name__ == "__main__":
    get_all()