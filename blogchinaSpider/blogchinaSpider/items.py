#!/usr/bin python3
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class BlogchinaspiderItem(scrapy.Item):
#
#     pass
class BlogItem(scrapy.Item):
    bolg_key = scrapy.Field()
    blog_id = scrapy.Field()  # 博客ID
    title = scrapy.Field()  # 博客的标题
    sub_title = scrapy.Field()  # 子标题
    # author = scrapy.Field()
    blog_author_id = scrapy.Field()  # 博客的作者ID
    publish_time = scrapy.Field()  # 发表的时间
    category = scrapy.Field()  # 文章所属的类别
    read_num = scrapy.Field()  # 文章的阅读量
    comment_num = scrapy.Field()  # 文章的评论量
    hand_up_num = scrapy.Field()  # 文章的点赞量
    hand_down_num = scrapy.Field()  # 文章的点差量
    # admire_num = scrapy.Field()               # 文章赏的数量
    content = scrapy.Field()  # 文章内容
    pictures = scrapy.Field()  # 文章中的图片
    b_pictures = scrapy.Field()  # 图片的二进制表示
    # link = scrapy.Field()                     # 文章中的链接
    url = scrapy.Field()  # 文章的URL

    comment_ids = scrapy.Field()  # 文章的评论ID


class AuthorItem(scrapy.Item):
    author_key = scrapy.Field()
    author_id = scrapy.Field()  # 作者的ID
    author_name = scrapy.Field()  # 作者名
    author_blog_name = scrapy.Field()  # 作者的博客名
    introduce = scrapy.Field()  # 作者简介
    image = scrapy.Field()  # 作者的头像
    b_image = scrapy.Field()  # 作者头像的二进制
    article_num = scrapy.Field()  # 作者的文章数
    read_num = scrapy.Field()  # 作者所有文章的浏览数
    fans_num = scrapy.Field()  # 作者的粉丝数量
    focuse_num = scrapy.Field()  # 关注的用户数量

    all_article_url = scrapy.Field()  # 所有文章URL

    focuse = scrapy.Field()  # 关注用户的ID
    fans = scrapy.Field()  # 粉丝用户ID


class CommentItem(scrapy.Item):
    comment_key = scrapy.Field()
    comment_id = scrapy.Field()  # 评论的ID
    comment_user_id = scrapy.Field()  # 评论用户的ID
    comment_blog_id = scrapy.Field()  # 评论的博客ID
    comment_time = scrapy.Field()  # 评论的时间
    comment_content = scrapy.Field()  # 评论的内容
    praise_num = scrapy.Field()  # 评论的赞的数量
    praise_ids = scrapy.Field()  # 点赞的用户ID
    reply_id = scrapy.Field()  # 回复的评论的ID

    ip = scrapy.Field()  # 用户评论时的IP
    last_ip = scrapy.Field()  # 用户上次的IP


class SpecialItem(scrapy.Item):
    special_name = scrapy.Field()  # 专题名
    special_info = scrapy.Field()  # 专题信息
    special_video = scrapy.Field()  # 专题中所含的视频
    special_picture = scrapy.Field()  # 专题中所含的图片
    special_blogs = scrapy.Field()  # 专题中所含的帖子
