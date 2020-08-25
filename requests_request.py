import requests

from requests import Response


url = 'https://chengdu.anjuke.com/community/'

# 变量名后跟: 类型，好处是编程时会自动提示对象中的属性及方法
#resp: Response = requests.get(url, params={'from': 'esf_list_navigation'})

#声明函数时，参数名后跟’: 类型‘表示参数值的类型
#在函数的()后的‘-> 类型’ 表示函数返回的数据(结果)类型
def download(url: str)-> str:
    resp: Response = requests.get(url, params={'from': 'esf_list_navigation'})
    if resp.status_code == 200:
        return resp.text    #文本，resp.content 字节码
    return '下载失败'
url1 = 'https://chengdu.anjuke.com/community/'
resp1 = requests.get(url1, params={'form': 'esf_list_navigation'})
rep = ';'.join(['%s=%s' %(cookie.name, cookie.value) for cookie in resp1.cookies]) #'aQQ_ajkguid=7290271E-62EA-6336-89B4-8054801545F8;twe=2'


ret = download(url)
print(ret)

