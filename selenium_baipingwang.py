#!/usr/bin/python3
# coding: utf-8
import time
import json
from urllib.parse import quote

from selenium.webdriver import Chrome
from selenium.webdriver.support import ui, expected_conditions
from selenium.webdriver.common.by import By


def start(cityName):
    url = f'https://zhaopin.baidu.com/?city={quote(cityName)}'
    chrome.get(url)

    query = chrome.find_element_by_css_selector('input[name="query"]')
    query.send_keys('Python')
    time.sleep(0.5)

    chrome.execute_script('var q = window.document.documentElement.scrollLeft=1000')
    btn = chrome.find_element_by_css_selector('.search-btn').click()
    time.sleep(0.5)

    chrome.execute_script('var q = window.document.documentElement.scrollTop=500')

    # 等待class_name 为 listitem 的div元素出现
    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'listitem')),

        'listitem的div元素没有出现'
    )

    # 获取所有岗位信息
    items = chrome.find_elements(By.CSS_SELECTOR, '.listitem>a')
    items = items[1:]  # 第一个a是广告
    for item in items:
        # 过滤当前的item是否为广告
        try:
            item.find_element(By.CLASS_NAME, 'adbar-item')
            continue
        except:
            pass

        data = item.find_element(By.TAG_NAME, 'div').get_attribute('data-click')
        info_url = json.loads(data)['url']

        # info_url = item.get_attribute('href') # 岗位详情连接
        title = item.find_element(By.CLASS_NAME, 'title').text
        salary = item.find_element(By.CSS_SELECTOR, '.salaryarea span').text

        print(info_url, title, salary)


if __name__ == '__main__':
    # chromedriver.exe  驱动程序的路径可以配置到PATH环境变量中
    chrome = Chrome(executable_path='chromedriver.exe')  # 打开浏览器
    for city in ['成都', '北京', '上海']:
        start(city)
    chrome.close()  # 关闭浏览器
