"""
基于requests库封装操作ElasticSearch搜索引擎的函数（SDK）
"""

import requests

from urllib.parse import quote

INDEX_HOST = '106.55.56.16'
INDEX_PORT = 80


class ESIndex():
    """ES的索引库类"""
    def __init__(self, index_name, doc_type):
        self.index_name = index_name
        self.doc_type = doc_type

    def create(self):   #创建索引库
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}'
        json_data = {
            "settings": {
                "number_of_shards": 5,      # 主分片数量（默认一个索引被分配5个主分片）
                "number_of_replicas": 1     # 复制分片的数量（每个主分片都有1个复制分片）
            }
        }
        resp = requests.put(url, json=json_data)
        if resp.status_code == 200:
            print('索引创建成功')
            print(resp.json())

    def delete(self):   #删除索引库
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}'
        resp = requests.delete(url)
        if resp.status_code == 200:
            print('delete index ok')

    def add_doc(self, item: dict):
        # 向库中增加文档
        # 格式：/_index/_type/_id
        # 自增ID接口：/foods/text
        # 自定义ID接口：/foods/text/1
        doc_id = item.pop('id', None)
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/{self.doc_type}'
        if doc_id:
            url += str(doc_id)

        resp = requests.post(url, json=item)
        if resp.status_code == 200:
            print(f'{url} 文档增加成功！')

    def remove(self, doc_id):
        # 删除文档
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/{self.doc_type}/{doc_id}'
        resp = requests.delete(url)
        if resp.status_code == 200:
            print(f'delete {url} ok')

    def update_doc(self, item: dict):
        # 更新文档
        doc_id = item.pop('id')
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/{self.doc_type}/{doc_id}'
        resp = requests.put(url, json=item)
        assert resp.status_code == 200
        print(f'{url} update ok')

    def query(self, wd=None):
        # 查询
        # 空搜索
        #   /_search
        # 分页查询
        #   size:结果数，默认10
        #   from:跳过开始的结果数，默认0
        #       GET /_search?size=5
        #       GET /_search?size=5&from=5
        # 查询字符串（DSL---》结构化查询语句）
        #   查询字符串方式，将参数拼接到URL中
        #   JSON格式的请求体
        #       GET /_all/text/_search?q=nqme:蒸
        #       GET /_all/text/_search?q=name:蒸+name:john+price:1.5
        q = quote(wd) if wd else ''
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/_search?size=100'
        if q:
            url += f'&q={q}'
        resp = requests.get(url)
        datas = []
        if resp.status_code == 200:
            ret = resp.json()
            hits = ret['hits']['hits']
            if hits:
                for item in hits:
                    data = item['_source']
                    data['id'] = item['_id']

                    datas.append(data)
        return datas

if __name__ == '__main__':
    index = ESIndex('gushiwen', 'tuijian')
    index.create()
    # index.add_doc({
    #     'id': 1,
    #     'name': 'disen',
    #     'price': 19.5
    # })
    # index.add_doc({
    #     'id': 2,
    #     'name': 'jack',
    #     'price': 10
    # })
    print(index.query())