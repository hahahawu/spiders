# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from pprint import pformat

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()     # 文章ID，从url中提取
    url = scrapy.Field()            # 文章链接
    path_text = scrapy.Field()      # 所属子目录描述
    path_href = scrapy.Field()      # 所属子目录链接
    title = scrapy.Field()          # 标题
    key_words = scrapy.Field()      # 关键字
    summary = scrapy.Field()        # 文章简介
    author = scrapy.Field()         # 作者
    date_time = scrapy.Field()      # 发布时间
    source = scrapy.Field()         # 文章来源
    content = scrapy.Field()        # 内容
    editor = scrapy.Field()         # 责任编辑
    picture_url = scrapy.Field()    # 文章中图片链接
    b_pictures = scrapy.Field()     # 图片的二进制表示

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        # return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))
        return pformat(r)

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        # return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))
        return pformat(r)

