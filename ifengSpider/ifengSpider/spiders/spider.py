import re, json
import traceback

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from ifengSpider.spiders.get_info import *
from ifengSpider.util.tools import *


def get_comment_item(comment):
    comment_item = CommentItem()
    comment_item['comment_id'] = comment['comment_id']
    comment_item['comment_key'] = str(comment['comment_id']) + '_ifeng_comment'
    comment_item['article_id'] = comment['article_id']
    comment_item['channel_id'] = check_int(comment['channel_id'])
    comment_item['client_ip'] = check_value(comment['client_ip'])
    comment_item['create_time'] = check_value(comment['comment_date']+':00')
    comment_item['content'] = str_format(comment['comment_contents'])
    comment_item['user_id'] = check_int(comment['user_id'])
    comment_item['username'] = check_value(comment['uname'])
    comment_item['avatar_url'] = check_value(comment['faceurl'])
    comment_item['ip_from'] = check_value(comment['ip_from'])
    comment_item['uptimes'] = check_int(comment['uptimes'])
    comment_item['useragent'] = check_value(comment.get('useragent'))
    comment_item['parent_comment_ids'] = ''
    parent_comment_ids = []
    for parent_node in comment['parent']:
        parent_comment_ids.append(parent_node['comment_id'])
    comment_item['parent_comment_ids'] += ';'.join(parent_comment_ids) + ';'
    return comment_item


class IfengSpider(CrawlSpider):
    name = 'ifeng'

    allowed_domains = ['ifeng.com']

    start_urls = ['http://www.ifeng.com']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/a/\d{8}/\d+_\d+.shtml'
        ),
        allow_domains=(
            'news.ifeng.com',
            'culture.ifeng.com',
            'guoxue.ifeng.com',
            'sports.ifeng.com',
            'ent.ifeng.com',
            'sn.ifeng.com'
        ),
        deny_domains=(),
        deny=()
    )

    follow_extract = LxmlLinkExtractor(
        allow=(),
        allow_domains=(
            'news.ifeng.com',
            'culture.ifeng.com',
            'guoxue.ifeng.com',
            'sports.ifeng.com',
            'ent.ifeng.com',
            'sn.ifeng.com'
        ),
        deny_domains=(),
        deny=()
    )

    rules = (
        Rule(article_extract, follow=False, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    def parse_article(self, response):
        sel = Selector(response)

        news_info_div1 = sel.xpath('//div[@id="artical"]')
        news_info_div2 = sel.xpath('//div[@id="yc_con_txt"]')

        if news_info_div1:
            news_item, docUrl = get_news_div1_info(response)
        elif news_info_div2:
            news_item, docUrl = get_news_div2_info(response)
        else:
            raise ValueError('Page style isn\'t defined : ' + str(response.url))

        # 获取评论
        comment_url = 'http://comment.ifeng.com/get.php?orderby=uptimes&docUrl=' + str(docUrl) + '&format=json&job' \
                      '=1&p=1&pageSize=20 '
        yield Request(
            url=comment_url,
            callback=self.get_comment_list,
            meta={
                'news_item': news_item,
                'curr_page': 1,
                'docUrl': docUrl,
            },
            priority=100
        )

    def parse_follow(self, response):
        pass

    def get_comment_list(self, response):
        data = response.body.decode()
        news_item = response.meta.get('news_item')
        try:
            json_data = json.loads(data)
            comments = json_data['comments']

            if comments:
                # 将comment_id填入news_item
                temp_comment_ids = []
                for comment in comments:
                    comment_id = comment['comment_id']
                    temp_comment_ids.append(comment_id)
                    comment_item = get_comment_item(comment)
                    yield comment_item
                news_item['comment_ids'] += ';'.join(temp_comment_ids) + ';'

                curr_page = response.meta.get('curr_page')
                curr_page += 1
                docUrl = response.meta.get('docUrl')
                next_url = 'http://comment.ifeng.com/get.php?orderby=uptimes&docUrl=' + str(docUrl) \
                           + '&format=json&job=1&p='+str(curr_page)+'&pageSize=20 '
                yield Request(
                    url=next_url,
                    callback=self.get_comment_list,
                    meta={
                        'news_item': news_item,
                        'curr_page': curr_page,
                        'docUrl': docUrl,
                    },
                    priority=100
                )
            else:
                news_item['join_count'] = json_data['join_count']
                news_item['reply_count'] = json_data['count']
                yield news_item
        except Exception as e:
            print("解析json数据出错 ：" + str(e))
            msg = traceback.format_exc()
            print(msg)
