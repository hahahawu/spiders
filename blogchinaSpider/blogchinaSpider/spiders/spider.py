#!/usr/bin python3
# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from blogchinaSpider.items import BlogItem
from blogchinaSpider.spiders.get_info import get_author_info, get_total_page, get_follow_author_list, get_article_date, \
    get_article_content, get_comment, get_author, get_article_url


class BlogChinaSpider(scrapy.Spider):
    name = 'blogchina'

    allowed_domains = ['blogchina.com']

    start_urls = ['http://tuijian.blogchina.com/list/column/flag/5']

    def parse(self, response):
        """
        :param response:
        :return:
        """
        # 爬取当前页面的所有作家
        for author_href, author_name in get_author(response):
            yield Request(url=response.urljoin(author_href),
                          callback=self.parse_author_page,
                          meta={
                              'author_name': author_name
                          })

        # 获取第二页到末页的作家列表
        page_num = get_total_page(response)
        for x in range(2, page_num + 1):
            url = 'http://tuijian.blogchina.com/list/column/flag/5/page/' + str(x)
            yield Request(url=url,
                          callback=self.parse_main_page_author)

    def parse_author_page(self, response):
        """
        爬取用户主页
        :param response:
        :return:
        """

        author_name = response.meta['author_name']
        author_item = get_author_info(response)
        author_item['author_name'] = author_name

        author_item['all_article_url'] = response.url

        # 获取所有文章的URL的参数
        article_url = 'http://post.blogchina.com/archive?user_id=' + str(author_item['author_id'])

        yield Request(url=article_url,
                      callback=self.parse_article_url,
                      meta={
                          'author_item': author_item
                      })

    def parse_article_url(self, response):
        """
        获取用户所有文章的URL，并爬取作家的信息
        :param response:
        :return:
        """
        author_item = response.meta['author_item']
        # 拼接用户所有文章的URL
        article_url = get_article_url(response)
        if article_url:
            author_item['all_article_url'] += article_url
        else:
            author_item['all_article_url'] = ''

        # 爬取作家信息
        num_ajax_url = 'http://post.blogchina.com/user/userNum?user_id=' + str(author_item['author_id'])

        yield Request(url=num_ajax_url,
                      callback=self.parse_author_num,
                      meta={
                          'author_item': author_item
                      })

    def parse_main_page_author(self, response):
        """
        爬取作家专栏页的所有作家
        :param response:
        :return:
        """
        for author_href, author_name in get_author(response):
            yield Request(url=author_href,
                          callback=self.parse_author_page,
                          meta={
                              'author_name': author_name
                          })

    def parse_author_num(self, response):
        author_item = response.meta['author_item']
        ajax_body = response.body.decode()
        # noinspection PyBroadException
        try:
            json_data = json.loads(ajax_body)
            if str(json_data['meta']['code']) == '200':
                num_data = json_data['data']['num']
                read_num = num_data['click']
                article_num = num_data['article']
                focuse_num = json_data['data']['follow']['friends']
                fans_num = json_data['data']['follow']['fans']
            else:
                read_num = '-1'
                article_num = '-1'
                focuse_num = '-1'
                fans_num = '-1'

            author_item['article_num'] = article_num
            author_item['read_num'] = read_num
            author_item['fans_num'] = fans_num
            author_item['focuse_num'] = focuse_num
        except Exception as e:
            print('Get number data error!!!' + str(e))

        # 爬取作家关注粉丝表信息
        author_item['fans'] = []
        fans_url = '/follow/' + str(author_item['author_id']) + '/fans'
        yield Request(url=response.urljoin(fans_url),
                      callback=self.parse_fans,
                      meta={
                          'author_item': author_item
                      })

        # return author_item

    def parse_fans(self, response):
        author_item = response.meta['author_item']
        result = get_follow_author_list(response)

        if result:
            follow_list, lastpagetime = result
            author_item['fans'] += follow_list
            url = '?lastpagetime=' + str(lastpagetime)
            yield Request(url=response.urljoin(url),
                          callback=self.parse_fans,
                          meta={
                              'author_item': author_item
                          })
        else:
            # 爬取关注的用户
            author_item['focuse'] = []
            url = '/follow/' + author_item['author_id'] + '/friends'
            yield Request(url=response.urljoin(url),
                          callback=self.parse_focuse,
                          meta={
                              'author_item': author_item
                          })

    def parse_focuse(self, response):
        author_item = response.meta['author_item']
        result = get_follow_author_list(response)

        if result:
            follow_list, lastpagetime = result
            author_item['focuse'] += follow_list
            url = '?lastpagetime=' + str(lastpagetime)
            yield Request(url=response.urljoin(url),
                          callback=self.parse_focuse,
                          meta={
                              'author_item': author_item
                          })
        else:
            # 作家信息爬取完毕
            yield author_item

        # 爬取文章页
        all_article_url = author_item['all_article_url']
        if int(author_item['article_num']) > 0:
            yield Request(url=response.urljoin(all_article_url),
                          callback=self.parse_article_list,
                          meta={
                              'author_id': author_item['author_id']
                          })

    def parse_article_list(self, response):
        author_id = response.meta['author_id']
        date_list = get_article_date(response)
        for date in date_list:
            # 根据date数据来获得某个月的所有文章
            date_article_url = 'http://post.blogchina.com/userdatearticle?uid=' + str(author_id) + '&date=' + str(date)
            yield Request(url=date_article_url,
                          callback=self.parse_article_json)

    def parse_article_json(self, response):
        data = response.body.decode()
        # noinspection PyBroadException
        try:
            json_data = json.loads(data)
            state = json_data['meta']['code']
            if int(state) == 200:
                data_count = json_data['data']['count']
                article_list = json_data['data']['lists']
                user_id = json_data['data']['user_id']
                date = json_data['data']['date']
                if int(data_count) > 0:
                    for article_info in article_list:
                        blog_item = BlogItem()

                        blog_item['blog_author_id'] = user_id

                        aid = article_info['aid']
                        blog_item['blog_id'] = aid
                        blog_item['blog_key'] = str(aid) + '_blogchina_blog'

                        title = article_info['title']
                        blog_item['title'] = title

                        sub_title = article_info['subtitle']
                        blog_item['sub_title'] = sub_title

                        if 'url' in article_info['pics']:
                            pictures = article_info['pics']['url']
                            blog_item['pictures'] = pictures
                        elif 'exists' in article_info['pics'] and article_info['pics']['exists'] != 'n':
                            print(article_info['pics'])
                            blog_item['pictures'] = ''

                        category = article_info['notebook_name']
                        blog_item['category'] = category

                        read_num = article_info['nums']['click']
                        blog_item['read_num'] = read_num

                        hand_up_num = article_info['nums']['support']
                        blog_item['hand_up_num'] = hand_up_num

                        comment_num = article_info['nums']['comment']
                        blog_item['comment_num'] = comment_num

                        hand_down_num = article_info['nums']['oppose']
                        blog_item['hand_down_num'] = hand_down_num

                        article_url = article_info['article_url']
                        blog_item['url'] = article_url

                        publish_time = article_info['gsh_add_time']
                        blog_item['publish_time'] = publish_time

                        yield Request(url=response.urljoin(article_url),
                                      callback=self.parse_blog_content,
                                      meta={
                                          'blog_item': blog_item
                                      })

                    if int(data_count) >= 10:
                        # 如果大于十条，继续请求后面的信息
                        next_part_url = '?uid=' + str(user_id) + '&date=' + str(date) + '&lastpagetime=' \
                                        + str(article_list[int(data_count) - 1]['add_time'])

                        yield Request(url=response.urljoin(next_part_url),
                                      callback=self.parse_article_json)

        except Exception as e:
            print('解析JSON数据失败！！！ ' + str(e))

    def parse_comment_ajax(self, response):
        blog_item = response.meta['blog_item']
        blog_id = blog_item['blog_id']
        comment_ids = []
        for comment_item in get_comment(response, blog_id):
            comment_ids.append(comment_item['comment_id'])
            yield comment_item

        blog_item['comment_ids'] = comment_ids
        yield blog_item

    def parse_blog_content(self, response):
        blog_item = response.meta['blog_item']
        article_content = get_article_content(response)
        blog_item['content'] = article_content

        article_id = blog_item['blog_id']
        comment_ajax_url = 'http://discuss5.blogchina.com/discuss/' + str(article_id)

        yield Request(url=comment_ajax_url,
                      callback=self.parse_comment_ajax,
                      meta={
                          'blog_item': blog_item
                      })
