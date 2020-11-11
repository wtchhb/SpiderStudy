#!/usr/bin/python3
# coding: utf-8

import random

# 声明Cookies池
cookie_txts = [
    'login=flase; ASP.NET_SessionId=3tqyuiuh2auhp0swinhfyowm; Hm_lvt_9007fab6814e892d3020a64454da5a55=1605099497; codeyzgswso=49790966046bfa5f; gsw2017user=1242231%7c06549F172215EBF83CD49CFD87522B92; login=flase; wxopenid=defoaltid; gswZhanghao=1040196881%40qq.com; gswEmail=1040196881%40qq.com; wsEmail=1040196881%40qq.com; idsShiwen2017=%2c7722%2c49386%2c71137%2c; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1605099521',
]

def get_cookie():
    cookie = random.choice(cookie_txts)
    # ret = {}
    # for c in cookie.split(';'):
    #     k, v = c.split('=')
    #     ret[k] = v

    return {
        c.split('=')[0].strip(): c.split('=')[1].strip()
        for c in cookie.split(';')
    }

if __name__ == '__main__':
    print(get_cookie())