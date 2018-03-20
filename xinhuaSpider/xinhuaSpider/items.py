# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinhuaSpiderItem(scrapy.Item):
    article_id = scrapy.Field()     # 文章ID
    url = scrapy.Field()            # 文章url
    category = scrapy.Field()       # 所属大类别
    sub_category = scrapy.Field()   # 所属小类别
    title = scrapy.Field()          # 文章标题
    summary = scrapy.Field()        # 文章摘要
    publish_time = scrapy.Field()   # 文章发布时间
    origin = scrapy.Field()         # 文章来源
    content = scrapy.Field()        # 文章内容
    # editor = scrapy.Field()         # 文章编辑

