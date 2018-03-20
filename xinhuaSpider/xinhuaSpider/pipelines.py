# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymysql
from xinhuaSpider.settings import TB_NEWS
from xinhuaSpider.dateTimeFormator import timeFormat


def generate_insert_sql(item):
    sql = 'INSERT INTO ' + TB_NEWS + '('
    tb_fields = ''
    tb_values = ''
    for tb_f in item:
        tb_fields = tb_fields + tb_f + ', '
        tb_values = tb_values + '"' + str(item[tb_f]) + '", '

    return sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'


class XinhuaspiderPipeline(object):
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
        # print(item)
        '''
            content出去空白符并连接字符串
            publish_time格式化
            id去除中括号
        '''
        item['content'] = ''.join(re.findall(u'[\u4e00-\u9fa5].+?', item['content']))
        item['publish_time'] = timeFormat(item['publish_time'])
        item['article_id'] = item['article_id'][0]
        sql = generate_insert_sql(item)
        if sql:
            try:
                print('Sql : ' + sql)
                cursor.execute(sql)
            except Exception as e:  # 方法一：捕获所有异常
                # 如果发生异常，则回滚
                print("发生异常", str(e))
                print(sql)

        self.connect.commit()
        cursor.close()
        return item
