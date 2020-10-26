#!/usr/bin/python3
#-*- coding: utf-8 -*-
import re
import json
import time

import requests
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions

from utils import header
from selenium.webdriver import Chrome

headers = {
    'User-Agent': header.get_ua()
}

chrome = Chrome(executable_path='chromedriver.exe')


def get_allcity():
    url = 'https://www.zhaopin.com/citymap'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        html = resp.text
        # with open('city.html', 'w', encoding='utf-8') as f:
        #     f.write(html)
        # print(html)

        s = re.search(r'<script>__INITIAL_STATE__=(.*?)</script>', html)
        json_data = s.groups()[0]
        data = json.loads(json_data)
        cityMapList = data['cityList']['cityMapList']  # dict
        for letter, citys in cityMapList.items():
            print(f'--------{letter}--------')
            for city in citys:
                """
                    {
                        "name": "鞍山",
                        "url": "//www.zhaopin.com/anshan/",
                        "code": "601",
                        "pinyin": "anshan"
                    }
                """
                yield city


def get_city_jobs(url):
    chrome.get(url)     # 打开城市

    # 查找警告信息的button
    # chrome.find_element_by_css_selector('.risk-warning__content button')
    # btn = chrome.find_element_by_css_selector('.risk-warning__content>button')
    # btn.click()

    # 根据class_name查询WebElement
    input_search: WebElement = chrome.find_element_by_class_name('zp-search__input')
    input_search.send_keys('Python')

    chrome.find_element_by_class_name('zp-search__btn').click()
    time.sleep(2)

    print(chrome.switch_to.active_element)

    chrome.execute_script('var q = window.document.documentElement.scrollTop=50000')
    time.sleep(0.2)
    chrome.execute_script('var q = window.document.documentElement.scrollTop=100000')
    time.sleep(0.2)

    # 等待 class_name 为"contentpile__content"div元素的出现
    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'contentpile__content')),
        '查找的元素一直没有出现'
    )

    # 判断当前查询的结果是否不存在
    nocontent = chrome.find_elements_by_class_name('contentpile__jobcontent')
    if not nocontent:
        print('当前城市未查找到Python岗位')
    else:
        # 提取查询结果
        divs = chrome.find_elements_by_class_name('contentpile__content__wrapper')
        for div in divs:
            # 每一个岗位
            job_info_url = div.find_element(By.XPATH, './/a/@href')
            print(job_info_url)


def get_city_jobs2(url):
    chrome.get(url)
    chrome.execute_script('var q = window.document.documentElement.scrollTop=3000')
    time.sleep(0.2)
    chrome.execute_script('var q = window.document.documentElement.scrollTop=5000')
    time.sleep(0.2)

    # 等待 class_name 为"contentpile__content"div元素的出现
    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'contentpile__content')),
        '查找的元素一直没有出现'
    )

    # 判断当前查询的结果是否不存在
    nocontent = chrome.find_elements_by_class_name('contentpile__jobcontent')
    if not nocontent:
        print('当前城市未查找到Python岗位')
    else:
        # 提取查询结果
        divs = chrome.find_elements_by_class_name('contentpile__content__wrapper')
        for div in divs:
            # 每一个岗位
            job_info_url = div.find_element(By.XPATH, './/a/@href')
            print(job_info_url)


if __name__ == "__main__":

    query_citys = ('北京', '广州', '上海')
    for city in get_allcity():
        """
            #   保存city城市信息
            #   请求城市下的所有Python岗位
        """
        if city['name'] in query_citys:
            print(city)
            # https://sou.zhaopin.com/?jl=530&kw=Python&kt=3
            # get_city_jobs('https:' + city['url'])
            get_city_jobs2(f'https://sou.zhaopin.com/?jl={city["code"]}&kw=Python&kt=3')
            time.sleep(5)