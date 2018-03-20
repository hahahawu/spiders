# #!/usr/bin python3
# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from thrift import Thrift
#
# from blogchinaSpider.DBUtils.db_save import *
# from hbase import THBaseService
# from hbase.ttypes import *
# from thrift.transport import TSocket
# from thrift.transport import TTransport
# from thrift.protocol import TCompactProtocol
#
#
# from scrapy import Request
# from scrapy.pipelines.images import ImagesPipeline
#
# from blogchinaSpider.items import BlogItem, AuthorItem, CommentItem
#
#
# class SaveHBasePipeline(object):
#     def __init__(self, settings):
#         self.DB_URI = settings['HBASE_URI']
#         self.DB_PORT = settings['HBASE_PORT']
#         self.TB_INFO = settings['TB_INFO'].encode()
#         self.TB_AUTHOR = settings['TB_AUTHOR'].encode()
#         self.TB_BLOG = settings['TB_BLOG'].encode()
#         self.TB_COMMENT = settings['TB_COMMENT'].encode()
#
#         # 连接数据库表
#         socket = TSocket.TSocket(self.DB_URI, self.DB_PORT)
#         self.transport = TTransport.TFramedTransport(socket)
#         protocol = TCompactProtocol.TCompactProtocol(self.transport)
#         self.client = THBaseService.Client(protocol)
#
#         self.transport.open()
#         # 将爬虫开始的信息存入数据库
#         self.spider_info_row_key, start_put = gen_start_spider_info()
#         self.client.put(self.TB_INFO, start_put)
#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.spider.settings
#         return cls(settings=settings)
#
#     def close_spider(self, spider):
#         # 存储爬虫结束的信息
#         stop_put = gen_stop_spider_info(self.spider_info_row_key)
#         try:
#             self.client.put(self.TB_INFO, stop_put)
#         except:
#             self.transport.close()
#             self.transport.open()
#             self.client.put(self.TB_INFO, stop_put)
#         self.transport.close()
#
#     def process_item(self, item, spider):
#         if isinstance(item, BlogItem):
#             _, item_put = gen_blog_put(item)
#             try:
#                 self.client.put(self.TB_BLOG, item_put)
#             except:
#                 self.transport.close()
#                 self.transport.open()
#                 self.client.put(self.TB_BLOG, item_put)
#         elif isinstance(item, AuthorItem):
#             _, item_put = gen_author_put(item)
#             try:
#                 self.client.put(self.TB_AUTHOR, item_put)
#             except:
#                 self.transport.close()
#                 self.transport.open()
#                 self.client.put(self.TB_AUTHOR, item_put)
#         elif isinstance(item, CommentItem):
#             _, item_put = gen_comment_put(item)
#             try:
#                 self.client.put(self.TB_COMMENT, item_put)
#             except:
#                 self.transport.close()
#                 self.transport.open()
#                 self.client.put(self.TB_COMMENT, item_put)
#
#         return item
#
#
# class ImageSavePipeline(ImagesPipeline):
#     @classmethod
#     def from_settings(cls, settings):
#         global store_uri
#         store_uri = settings['IMAGES_STORE']
#         return cls(store_uri, settings=settings)
#
#     def get_media_requests(self, item, info):
#         if isinstance(item, BlogItem):
#             for image_url in item['pictures']:
#                 yield Request(image_url)
#
#         if isinstance(item, AuthorItem):
#             if item['image']:
#                 yield Request(item['image'])
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#
#         # 将图片转化为二进制形式
#         if isinstance(item, BlogItem):
#             item['b_pictures'] = []
#             for image_path in image_paths:
#                 try:
#                     fin = open(store_uri + image_path, mode='br')
#                     img = fin.read()
#                     item['b_pictures'].append(img)
#                     fin.close()
#                 except IOError as e:
#                     print(e)
#
#         elif isinstance(item, AuthorItem):
#             item['b_image'] = b''
#             try:
#                 fin = open(store_uri + image_paths[0], mode='br')
#                 img = fin.read()
#                 item['b_image'] = img
#                 fin.close()
#             except IOError as e:
#                 print(e)
#
#         return item
import pymysql
from blogchinaSpider.settings import TB_AUTHOR, TB_COMMENT, TB_BLOG
from blogchinaSpider.items import BlogItem, AuthorItem, CommentItem


def generate_insert_sql(item, table_name):
    sql = 'INSERT INTO ' + table_name + '('
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
        # print(item)
        if isinstance(item, BlogItem):
            print('blog!!!')
            sql = generate_insert_sql(item, TB_BLOG)
        elif isinstance(item, AuthorItem):
            print('author!!!')
            sql = generate_insert_sql(item, TB_AUTHOR)
        elif isinstance(item, CommentItem):
            print('comment!!!')
            sql = generate_insert_sql(item, TB_COMMENT)
        else:
            raise ValueError('Wrong item object.')
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
