import requests

from requests import Response

from urllib.parse import urlencode

url = 'https://chengdu.anjuke.com/community/'

# 变量名后跟: 类型，好处是编程时会自动提示对象中的属性及方法
#resp: Response = requests.get(url, params={'from': 'esf_list_navigation'})

#声明函数时，参数名后跟’: 类型‘表示参数值的类型
#在函数的()后的‘-> 类型’ 表示函数返回的数据(结果)类型
#def download(url: str)-> str:
#    resp: Response = requests.get(url, params={'from': 'esf_list_navigation'})
#    if resp.status_code == 200:
#        return resp.text    #文本，resp.content 字节码
#    return '下载失败'
# url1 = 'https://chengdu.anjuke.com/community/'
# resp1 = requests.get(url1, params={'form': 'esf_list_navigation'})
# rep = ';'.join(['%s=%s' %(cookie.name, cookie.value) for cookie in resp1.cookies]) #'aQQ_ajkguid=7290271E-62EA-6336-89B4-8054801545F8;twe=2'
# rep1 = resp1.headers['Content-Type'].split("=")[-1]  #utf-8
#
#
# ret = download(url)
# print(ret)
def download(url: str)-> str:
    #resp: Response = requests(url, params={'from': 'esf_list_navigation'})
   resp: Response = requests.request('get', url, params={'from': 'esf_list_navigation'})
   if resp.status_code == 200:
       return resp.text    #文本，resp.content 字节码
   return '下载失败'

def get_douban_json():
    # url='https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&' #请求方法是post
    url = 'https://movie.douban.com/j/chart/top_list'
    data = {
        'start':1,
        'limit':20,
    }
    params = {
        'type': 5,
        'interval_id': '100:90',  # 100:90
        'action':''
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }

    # cookies = {
    #     'session_id':'',
    # }
    resp = requests.post(url, params=params, data=data, headers=headers)
    assert resp.status_code == 200
    print(resp.url)
    if 'application/json' in resp.headers['content-type']:
        #'application/json'.index(resp.headers['content-type'])   存在返回0，不存在抛出异常
        #'application/json' find(resp.headers['content-type'])     存在返回位置，不存在返回-1
        return resp.json()
    return resp.text


#ret = download(url)
ret = get_douban_json()
print(ret)


