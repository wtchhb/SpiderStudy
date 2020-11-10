#!/usr/bin/python3
# coding: utf-8

import pymysql
from pymysql.cursors import DictCursor


class Database():
    def __init__(self):
        self.conn = pymysql.Connect(
            host='cd-cdb-7vcnnqy0.sql.tencentcdb.com',
            port=62341,
            user='root',
            password='QCloud@123',
            db='qidian',
            charset='utf8'
        )

    def __enter__(self):
        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        return True

    def close(self):
        self.conn.close()


class BaseDao():
    def __init__(self):
        self.db = Database()

    def save(self, table_name, **item):  # **item   ==    item:dict
        sql = 'insert into %s(%s) values(%s)'
        fields = ','.join(item.keys())
        fields_paceholds = ','.join(['%%(%s)s' % key for key in item])

        with self.db as cursor:
            cursor.execute(sql % (table_name, fields, fields_paceholds), item)

            # 判断执行是否成功
            if cursor.rowcount > 0:
                return True

        return False
