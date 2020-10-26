import  requests
from utils import header

headers = {
    'User-Agent': header.get_ua()
}

def get_allcity():
    url = 'https://www.zhaopin.com/citymap'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        html = resp.text
        with open('city.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(html)


if __name__ == "__main__":
    get_allcity()