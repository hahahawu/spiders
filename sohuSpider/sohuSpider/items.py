# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    article_id = scrapy.Field()  # 文章的ID
    url = scrapy.Field()  # 文章URL
    path_text = scrapy.Field()  # 路径描述
    path_href = scrapy.Field()  # 路径链接
    keywords = scrapy.Field()  # 关键词
    title = scrapy.Field()  # 标题
    description = scrapy.Field()  # 概要描述
    source = scrapy.Field()  # 来源
    date_time = scrapy.Field()  # 发布日期
    content = scrapy.Field()  # 内容
    picture_url = scrapy.Field()  # 图片链接
    join_count = scrapy.Field()  # 参与人数
    reply_count = scrapy.Field()  # 评论条数
    comment_ids = scrapy.Field()  # 评论ID
    b_picture = scrapy.Field()  # 图片二进制


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()  # 评论ID
    article_id = scrapy.Field()  # 文章ID
    ip = scrapy.Field()  # 用户登录IP
    create_time = scrapy.Field()  # 评论时间
    content = scrapy.Field()  # 内容
    user_id = scrapy.Field()  # 用户ID
    nickname = scrapy.Field()  # 用户名
    avatar_url = scrapy.Field()  # 用户头像
    ip_location = scrapy.Field()  # 用户IP来源
    parent_comment_ids = scrapy.Field()  # 如果是多楼层，且该评论不是一楼，则返回其上面的楼层ID
    comment_from = scrapy.Field()  # 发表该评论的设备
    reply_count = scrapy.Field()    # 回复数目
    support_count = scrapy.Field()  # 支持数
