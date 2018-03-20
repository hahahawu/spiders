# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from sohuSpider.settings import TB_NEWS, TB_COMMENT
from sohuSpider.items import *


def generate_insert_sql(item, table):
    sql = 'INSERT INTO ' + table + '('
    tb_fields = ''
    tb_values = ''
    for tb_f in item:
        tb_fields = tb_fields + tb_f + ', '
        tb_values = tb_values + '"' + str(item[tb_f]) + '", '

    return sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'


class SaveToMysqlPipeline(object):
    def __init__(self, mysql_uri, mysql_user_name, mysql_password, mysql_db):
        self.mysql_uri = mysql_uri
        self.mysql_user_name = mysql_user_name
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_HOST'),
            mysql_user_name=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWD'),
            mysql_db=crawler.settings.get('MYSQL_DBNAME')
        )

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            self.mysql_uri,
            self.mysql_user_name,
            self.mysql_password,
            self.mysql_db,
            charset='utf8'
        )

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        cursor = self.connect.cursor()

        if isinstance(item, NewsItem):
            print("News!!!")
            sql = generate_insert_sql(item, TB_NEWS)
        elif isinstance(item, CommentItem):
            print("Comment!!!")
            sql = generate_insert_sql(item, TB_COMMENT)
        else:
            raise ValueError("Wrong Type of item : ", item)
        if sql:
            try:
                print('Sql : ' + sql)
                cursor.execute(sql)
            except Exception as e:  # 方法一：捕获所有异常
                # 如果发生异常，则回滚
                print(sql)
                print("发生异常", str(e))

        self.connect.commit()

        cursor.close()
        return item


class PrintTest(object):
    def process_item(self, item, spider):
        print(item)
        return item

