# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    article_id = scrapy.Field()         # 文章id
    url = scrapy.Field()                # 文章URL
    path_text = scrapy.Field()          # 路径名称
    path_href = scrapy.Field()          # 路径链接
    date_time = scrapy.Field()          # 发布日期
    source = scrapy.Field()             # 来源
    title = scrapy.Field()              # 标题
    keywords = scrapy.Field()           # 关键字
    author = scrapy.Field()             # 作者
    description = scrapy.Field()        # 描述
    copyright = scrapy.Field()          # 版权
    editor = scrapy.Field()             # 编辑
    content = scrapy.Field()            # 内容
    picture_url = scrapy.Field()        # 图片链接
    video_url = scrapy.Field()          # 视频链接
    b_picture = scrapy.Field()          # 图片二进制
    comment_ids = scrapy.Field()        # 评论ID列表
    # join_count = scrapy.Field()         # 参与数
    # reply_count = scrapy.Field()        # 跟帖数
    pass


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()         # 评论ID
    against = scrapy.Field()            # 反对数
    favCount = scrapy.Field()           # 赞成数
    anonymous = scrapy.Field()          # 是否匿名
    buildLevel = scrapy.Field()         # 楼层
    firstBuildLevelID = scrapy.Field()    # 如果不是一楼，则记录该楼层第一层的评论ID
    content = scrapy.Field()            # 内容
    createTime = scrapy.Field()         # 评论时间
    ip = scrapy.Field()                 # IP地址
    user_id = scrapy.Field()            # 用户ID
    shareCount = scrapy.Field()         # 分享次数
    isDel = scrapy.Field()              # 是否删除
    source = scrapy.Field()             # 评论发表设备:手机(ph)，网站(wb)等
    siteName = scrapy.Field()             # 通过哪个网站发表的评论
    location = scrapy.Field()           # 用户发表评论时所在位置
    vote = scrapy.Field()               # 未知
    article_id = scrapy.Field()


class UserItem(scrapy.Item):
    user_key = scrapy.Field()
    user_id = scrapy.Field()            # 用户ID
    avatar = scrapy.Field()             # 用户头像
    nickname = scrapy.Field()           # 昵称
    level = scrapy.Field()              # 等级
    score = scrapy.Field()              # 积分
    fans_num = scrapy.Field()           # 粉丝数量
    focus_num = scrapy.Field()          # 关注数量
    auth_info = scrapy.Field()          # 身份信息
    create_time = scrapy.Field()        # 创建时间
    fans_ids = scrapy.Field()           # 粉丝ID列表
    focus_ids = scrapy.Field()          # 关注用户列表
    fav_count = scrapy.Field()          # 赞的数目
    cmt_count = scrapy.Field()          # 跟帖数
    feed_count = scrapy.Field()         # 未知
