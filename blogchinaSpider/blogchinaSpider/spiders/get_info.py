#!/usr/bin python3
# -*- coding: utf-8 -*-
import json

import scrapy

from blogchinaSpider import items
from blogchinaSpider.items import CommentItem


def get_author(response):
    """
    :param response:
    :return: 作者的用户名和主页链接
    """
    author_sel = scrapy.Selector(response)
    author_list = author_sel.xpath('//ul[@class="ml"]/li')

    if not author_list:
        return None

    for author in author_list:
        author_href = author.xpath('./a/@href').extract_first()
        author_name = author.xpath('./a/text()').extract_first()

        yield author_href, author_name


# def get_author_next_page(response):
#     """
#     :param response:
#     :return:
#     """
#     pass


def get_total_page(response):
    """
    获取作家总的页数
    :param response:
    :return: page_num
    """
    page_sel = scrapy.Selector(response)
    author_num = page_sel.xpath('//input[@id="autoPageCnt"]/@value').extract_first().strip()
    page_per = page_sel.xpath('//input[@id="autoPagePer"]/@value').extract_first().strip()
    try:
        page_num = int(author_num) // int(page_per)
        return page_num + 1
    except Exception as e:
        print('Page num is error' + str(e))
        return None


def get_current_page(response):
    """
    获取当前的页码
    :param response:
    :return:
    """
    page_sel = scrapy.Selector(response)
    current_page = page_sel.xpath('//input[@id="autoPageCur"]/@value').extract_first().strip()
    try:
        return int(current_page)
    except Exception as e:
        print(str(e))
        return None


def get_author_info(response):
    """
    解析作家首页作家信息
    :param response:
    :return: AuthorItem
    """
    author_page_sel = scrapy.Selector(response)
    author_item = items.AuthorItem()
    author_id = author_page_sel.xpath('//input[@id="uid"]/@value').extract_first()
    author_item['author_id'] = author_id
    author_item['author_key'] = str(author_id) + '_blogchina_author'
    user_name = author_page_sel.xpath('//input[@id="uname"]/@value').extract_first()
    author_item['author_blog_name'] = user_name
    introduce = author_page_sel.xpath('//div[@id="con_js"]/div').xpath('string(.)').extract_first()
    author_item['introduce'] = introduce
    image = author_page_sel.xpath('//input[@id="user_small_pic"]/@value').extract_first()
    author_item['image'] = image

    # article_num = author_page_sel.xpath('//span[@id="articlenum"]/text()').extract_first()
    # author_item['article_num'] = article_num
    # read_num = author_page_sel.xpath('//span[@id="readnum"]/text()').extract_first()
    # author_item['read_num'] = read_num
    # fans_num = author_page_sel.xpath('//span[@id="fansnum"]/text()').extract_first()
    # author_item['fans_num'] = fans_num

    return author_item


def get_follow_author_list(response):
    """
    获取粉丝关注列表中的用户
    :param response:
    :return:lastpagetime, author_list
    """
    follow_sel = scrapy.Selector(response)
    author_list = follow_sel.xpath('//ul[@id="userlist"]/li').extract()
    if not author_list:
        return None

    follow_list = []
    for author in author_list:
        author_sel = scrapy.Selector(text=author)
        author_name = author_sel.xpath('//div[@class="forg-name"]/text()').extract_first()
        follow_list.append(author_name)

    lastpagetime = follow_sel.xpath('//input[@id="lastpagetime"]/@value').extract_first()

    return follow_list, lastpagetime


def get_article_url(response):
    date_ajax = response.body.decode()
    try:
        data_json = json.loads(date_ajax)
        code = data_json['meta']['code']
        if code == 200:
            data = data_json['data']
            msg_year = data['year_lists'][0]['year']
            msg_month = data['year_lists'][0]['month_lists'][0]['month']
            article_url = '/archive/' + str(msg_year) + str(msg_month) + '_1.html'

            return article_url
        else:
            return None

    except Exception as e:
        print('解析用户所有文章URL出错！！ ' + str(e))
        return None


def get_article_date(response):
    """
    获取某位作家的所有文章时间信息，以获得其所有的文章
    :param response:
    :return:
    """
    page_sel = scrapy.Selector(response)
    date_list = page_sel.xpath('//ul[@class="yearnum"]/li/dl[@class="monthnum"]/dd/div[@class="ti  mon"]/@date-data') \
        .extract()
    return date_list


def get_article_content(response):
    """
    获得文章的正文
    :param response:
    :return:
    """
    article_sel = scrapy.Selector(response)
    content = article_sel.xpath('//div[@class="article"]/div').xpath('string(.)').extract_first()

    return content


def get_comment(response, blog_id):
    """
    获取所有评论
    :param response:
    :param blog_id: 博客ID
    :return:
    """
    comment_json = response.body.decode()
    try:
        comment_data = json.loads(comment_json)
        status = comment_data['meta']['code']
        if status == 200:
            if len(comment_data['data']) > 0:
                datas = comment_data['data']
                for data in datas:
                    comment_item = CommentItem()
                    discuss_data = data['discuss']

                    comment_id = discuss_data['did']
                    comment_item['comment_id'] = comment_id
                    comment_item['comment_key'] = str(comment_id) + '_blogchina_comment'

                    comment_content = discuss_data['body']
                    comment_item['comment_content'] = comment_content

                    comment_time = discuss_data['add_time']
                    comment_item['comment_time'] = comment_time

                    comment_user_id = discuss_data['user']['user_id']
                    comment_item['comment_user_id'] = comment_user_id

                    comment_item['comment_blog_id'] = blog_id

                    praise_num = discuss_data['like']['total']
                    comment_item['praise_num'] = praise_num

                    praise_ids = discuss_data['like']['user_ids']
                    comment_item['praise_ids'] = praise_ids

                    reply_id = discuss_data['fids']
                    comment_item['reply_id'] = reply_id

                    ip = discuss_data['ip']
                    comment_item['ip'] = ip

                    last_ip = discuss_data['last_ip']
                    comment_item['last_ip'] = last_ip

                    yield comment_item

        else:
            return None
    except Exception as e:
        print(e)
        return None
