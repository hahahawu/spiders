# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from pprint import pformat

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()     # 文章ID
    url = scrapy.Field()    # URL
    path_text = scrapy.Field()
    path_href = scrapy.Field()
    title = scrapy.Field()      # 标题
    date_time = scrapy.Field()  # 发布时间
    source = scrapy.Field()     # 来源
    author = scrapy.Field()   # 作者
    # read_num = scrapy.Field()   # 浏览量
    # comment_num = scrapy.Field()    # 评论数量
    content = scrapy.Field()        # 内容
    picture_url = scrapy.Field()    # 图片地址
    b_pictures = scrapy.Field()
    summary = scrapy.Field()       # 摘要

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



