# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    article_key = scrapy.Field()
    article_id = scrapy.Field()             # 文章的ID
    url = scrapy.Field()                    # 文章URL
    path_text = scrapy.Field()              # 路径描述
    path_href = scrapy.Field()              # 路径链接
    keywords = scrapy.Field()               # 关键词
    title = scrapy.Field()                  # 标题
    description = scrapy.Field()            # 概要描述
    source = scrapy.Field()                 # 来源
    author = scrapy.Field()                 # 作者
    editor = scrapy.Field()                 # 编辑
    date_time = scrapy.Field()              # 发布日期
    content = scrapy.Field()                # 内容
    picture_url = scrapy.Field()            # 图片链接
    join_count = scrapy.Field()             # 参与人数
    reply_count = scrapy.Field()            # 评论条数
    comment_ids = scrapy.Field()            # 评论ID
    b_picture = scrapy.Field()              # 图片二进制
    # video_url = scrapy.Field()              # 视频链接


class CommentItem(scrapy.Item):
    comment_key = scrapy.Field()
    comment_id = scrapy.Field()             # 评论ID
    article_id = scrapy.Field()             # 文章ID
    channel_id = scrapy.Field()             # 频道ID
    client_ip = scrapy.Field()              # 用户登录IP
    create_time = scrapy.Field()            # 评论时间
    content = scrapy.Field()                # 内容
    user_id = scrapy.Field()                # 用户ID
    username = scrapy.Field()               # 用户名
    avatar_url = scrapy.Field()             # 用户头像
    ip_from = scrapy.Field()                # 用户IP来源
    parent_comment_ids = scrapy.Field()     # 如果是多楼层，且该评论不是一楼，则返回其上面的楼层ID
    uptimes = scrapy.Field()                # 该条评论获得赞的数目
    useragent = scrapy.Field()              # 用户所使用的代理


# 能获取的用户信息仅限于历史评论，暂时放弃UserItem
class UserItem(scrapy.Item):
    pass
