import json

from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from sohuSpider.spiders.get_info import *
from sohuSpider.util.time_formator import *
from sohuSpider.util.tools import *


def get_source_id(response):
    url = response.url
    source_id = url.split('/')[-1].split('_')[0]
    return source_id


def get_comment_item(comment, article_id):
    comment_item = CommentItem()
    comment_item['comment_id'] = check_value(comment['comment_id']) + '_sohu_comment'
    comment_item['article_id'] = check_value(article_id)
    comment_item['ip'] = check_value(comment['ip'])
    comment_item['create_time'] = time_transform(comment['create_time'])
    comment_item['content'] = str_format(check_value(comment['content']))
    comment_item['user_id'] = check_int(comment['user_id'])
    comment_item['nickname'] = check_value(comment['passport']['nickname'])
    comment_item['avatar_url'] = check_value(comment['passport']['img_url'])
    comment_item['ip_location'] = check_value(comment['ip_location'])

    # 如果该条评论不是一楼，则记录其上面楼层的ID
    up_floors = comment['comments']
    parent_comment_id_list = [str(floor['comment_id']) for floor in up_floors] if up_floors else []
    comment_item['parent_comment_ids'] = ';'.join(parent_comment_id_list)

    comment_item['comment_from'] = check_value(comment['from'])
    comment_item['reply_count'] = check_int(comment['reply_count'])
    comment_item['support_count'] = check_int(comment['support_count'])

    return comment_item


class SohuSpider(CrawlSpider):
    name = 'sohu'

    allowed_domains = ['sohu.com']

    start_urls = ['http://news.sohu.com']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/a/\d+_\d+'
        ),
        allow_domains=(
            'www.sohu.com',
            'news.sohu.com',
            'mil.sohu.com',
            'society.sohu.com',
            # 'mp.sohu.com',
            'sports.sohu.com',
            'yule.sohu.com'
        ),
        deny_domains=(
            'pic.news.sohu.com'
        ),
        deny=()
    )

    follow_extract = LxmlLinkExtractor(
        allow=(),
        allow_domains=(
            'www.sohu.com',
            'news.sohu.com',
            'mil.sohu.com',
            'society.sohu.com',
            # 'mp.sohu.com',
            'sports.sohu.com',
            'yule.sohu.com'
        ),
        deny_domains=(
            'pic.news.sohu.com'
        ),
        deny=()
    )

    rules = (
        Rule(article_extract, follow=False, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    def parse_article(self, response):
        sel = Selector(response)

        news_info_div1 = sel.xpath('//article[@id="mp-editor"]')

        if news_info_div1:
            news_item = get_news_div1_info(response)
        else:
            raise ValueError("Page style isn't defined : " + str(response.url))

        # 获取评论
        source_id = get_source_id(response)
        comment_url = 'http://apiv2.sohu.com/api/comment/list?page_size=100&topic_id=123456' \
                      '&page_no=1&source_id=mp_' + str(source_id)
        yield Request(
            url=comment_url,
            callback=self.get_comment_list,
            meta={
                'news_item': news_item,
                'curr_page': 1,
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
            if json_data['code'] == 200:
                jsonObject = json_data['jsonObject']
                comments = jsonObject.get('comments')
                if comments:
                    # 将comment_id填入news_item
                    temp_comment_ids = []
                    article_id = news_item['article_id']
                    for comment in comments:
                        comment_id = comment['comment_id']
                        temp_comment_ids.append(str(comment_id))
                        comment_item = get_comment_item(comment, article_id)
                        yield comment_item
                    news_item['comment_ids'] += ';'.join(temp_comment_ids) + ';'

                    curr_page = response.meta.get('curr_page')
                    curr_page += 1
                    source_id = response.url.split('_')[-1]

                    # 这里topic_id的局限性很大，暂时没找到一个比较好的获取topic_id的方法
                    next_url = 'http://apiv2.sohu.com/api/comment/list?page_size=100&topic_id=123456' \
                               '&page_no=' + str(curr_page) + '&source_id=mp_' + str(source_id)
                    yield Request(
                        url=next_url,
                        callback=self.get_comment_list,
                        meta={
                            'news_item': news_item,
                            'curr_page': curr_page,
                        },
                        priority=100
                    )
                else:
                    news_item['join_count'] = check_int(jsonObject.get('participation_sum'))
                    news_item['reply_count'] = jsonObject['cmt_sum']
                    yield news_item
        except Exception as e:
            print("解析json数据出错 ：" + str(e))
            msg = traceback.format_exc()
            print(msg)
