import json
import traceback

from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wy163Spider.spiders.get_info import *
from wy163Spider.util.time_formator import *

check_value = lambda x: x if x else ''
str_format = lambda x: x.strip().replace('\u3000', '').replace('\xa0', ''). \
    replace("\"", "'").replace('\n', '').replace('\t', ' ') if x else ''


def get_comment_ids(commentIDs):
    comment_ids = []
    for comment_id in commentIDs:
        comment_id_group = comment_id.split(',')
        comment_ids.extend(comment_id_group)
    comment_ids = list(set(comment_ids))
    return comment_ids


def fill_comment_info(comment, cid, comment_IDs, article_id):
    comment_item = CommentItem()
    comment_item['article_id'] = article_id
    comment_item['comment_id'] = str(cid) + '_wy163_comment'
    comment_item['against'] = comment['against']
    comment_item['anonymous'] = comment['anonymous']
    comment_item['favCount'] = comment['favCount']
    floor = comment['buildLevel']
    comment_item['buildLevel'] = floor
    if floor == 1:
        comment_item['firstBuildLevelID'] = 0
    else:
        for each_floor in comment_IDs:
            if cid in each_floor and cid == each_floor.split(",")[floor - 1]:
                comment_item['firstBuildLevelID'] = each_floor.split(",")[0]
                break
    comment_item['content'] = str_format(comment['content'])
    comment_item['createTime'] = timeFormator(comment['createTime'])
    comment_item['ip'] = comment['ip']
    user = comment['user']
    comment_item['user_id'] = user['userId']
    comment_item['location'] = user['location']
    comment_item['shareCount'] = comment['shareCount']
    comment_item['isDel'] = comment['isDel']
    comment_item['source'] = check_value(comment.get('source'))
    comment_item['siteName'] = comment['siteName']
    comment_item['vote'] = comment['vote']

    return comment_item, user


class Wy163Spider(CrawlSpider):
    name = 'wy163'

    allowed_domains = ['163.com']

    start_urls = ['http://news.163.com/']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/\d{2}/\d{4}/\d{2}/\w+.html',
            # '/photoview/\w+/\w+.html'
        ),
        allow_domains=(
            'news.163.com',
            'sports.163.com',
            'ent.163.com',
            # 'money.163.com',
            # 'tech.163.com',
            # 'auto.163.com',
            # 'mobile.163.com',
            # 'digi.163.com',
            'edu.163.com',
            'shanxi.news.163.com',
            # 'data.163.com',
            'war.163.com',
            'gov.163.com'
        ),
        deny=(
            '/photo.*'
        )
    )

    follow_extract = LxmlLinkExtractor(
        allow=(
        ),
        allow_domains=(
            'news.163.com',
            'sports.163.com',
            'ent.163.com',
            # 'money.163.com',
            # 'tech.163.com',
            # 'auto.163.com',
            # 'mobile.163.com',
            # 'digi.163.com',
            'edu.163.com',
            'shanxi.news.163.com',
            # 'data.163.com',
            'war.163.com',
            'gov.163.com'
        ),
        deny=(
            '/photo.*'
        )
    )

    rules = (
        Rule(article_extract, follow=False, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    article_count = 0

    def parse_article(self, response):
        sel = Selector(response)

        news_info_div1 = sel.xpath('//div[@id="epContentLeft"]')
        news_info_div2 = sel.xpath('//div[@class="atc_mian"]//div[@id="endText"]')

        if news_info_div1:
            result = get_news_div1_info(response)
        elif news_info_div2:
            result = get_news_div2_info(response)
        else:
            raise ValueError("Page style isn't defined : " + str(response.url))
        # news_item = result['news_item']
        productKey = result['productKey']
        docId = result['docId']

        # 获取评论列表
        next_url = 'http://comment.news.163.com/api/v1/products/' + str(productKey) + '/threads/' + \
                   str(docId) + '/comments/newList?offset=0&limit=40&showLevelThreshold=72&headLimit=1' \
                                '&tailLimit=2&ibc=newspc&%3Cem'
        yield Request(
            url=next_url,
            callback=self.get_comment_list,
            meta={
                'result': result,
                'curr_page': 0
            },
            priority=100
        )

    def parse_follow(self, response):
        sel = Selector(response)

        a_list = sel.xpath('//a/@href').extract()

        for link in a_list:
            if re.match(r'/\d{2}/\d{4}/\d{2}/\w+.html', link):
                yield Request(
                    url=response.urljoin(link),
                    callback=self.parse_article,
                    priority=200
                )

    def get_comment_list(self, response):
        data = response.body.decode()
        try:
            json_data = json.loads(data)
            commentIDs = json_data['commentIds']
            comments = json_data['comments']
            # comment_list_size = json_data['newListSize']

            if commentIDs:
                # 将comment_ids填入news_item
                result = response.meta['result']
                curr_page = response.meta['curr_page']
                news_item = result['news_item']
                comment_ids = get_comment_ids(commentIDs)
                news_item['comment_ids'] += ';'.join(comment_ids) + ';'
                result['news_item'] = news_item

                # 生成comment_item并开始爬取用户信息
                for comment_id in comment_ids:
                    comment = comments[comment_id + ""]
                    comment_item, user = fill_comment_info(comment, comment_id, commentIDs, news_item['article_id'])
                    yield comment_item

                    # 爬取用户信息
                    next_url = 'http://comment.api.163.com/api/v1/products/' + str(result['productKey']) \
                               + '/users/' + str(user['userId']) + '?ibc=newspc'
                    yield Request(
                        url=next_url,
                        callback=self.get_user_info,
                        priority=50,
                        meta={
                            'productKey': result['productKey'],
                        }
                    )

                # 抓取剩余的评论
                curr_page += 40
                next_url = 'http://comment.news.163.com/api/v1/products/' + str(result['productKey']) + '/threads/' + \
                           str(result['docId']) + '/comments/newList?offset=' + str(curr_page) \
                           + '&limit=40&showLevelThreshold=72&headLimit=1&tailLimit=2&ibc=newspc&%3Cem'
                yield Request(
                    url=next_url,
                    callback=self.get_comment_list,
                    meta={
                        'result': result,
                        'curr_page': curr_page
                    },
                    priority=200
                )
            else:
                result = response.meta['result']
                yield result['news_item']
        except Exception as e:
            print("解析json数据出错0 ：" + str(e))
            msg = traceback.format_exc()
            print(msg)

    def get_user_info(self, response):
        data = response.body.decode()
        try:
            json_data = json.loads(data)
            user_item = UserItem()
            user_id = json_data['userId']
            user_item['user_key'] = str(user_id) + '_wy163_user'
            user_item['user_id'] = user_id
            user_item['avatar'] = json_data['avatar']
            user_item['nickname'] = json_data['nickname']
            user_item['fans_num'] = json_data['followerCount']
            user_item['focus_num'] = json_data['followCount']
            user_item['auth_info'] = json_data['authInfo']
            user_item['create_time'] = json_data['createTime']
            user_item['fav_count'] = json_data['favCount']
            user_item['cmt_count'] = json_data['cmtCount']
            user_item['feed_count'] = json_data['feedCount']
            levelScore = json_data['levelScore']
            user_item['level'] = levelScore['level']
            user_item['score'] = levelScore['score']
            user_item['fans_ids'] = ''
            user_item['focus_ids'] = ''

            # 获取用户粉丝以及关注列表
            productKey = response.meta.get('productKey')
            if not productKey:
                productKey = re.findall(r'/products/\w+/users/', str(response.url))[0].split('/')[2]

            get_fans_url = 'http://comment.api.163.com/api/v1/products/' + str(productKey) + '/follow/user/' \
                           + str(user_id) + '/followerList?offset=0&limit=30&ibc=newspc'

            yield Request(
                url=get_fans_url,
                callback=self.get_fans_list,
                meta={
                    'user_item': user_item,
                    'curr_page': 0,
                    'productKey': productKey
                },
                priority=100
            )

        except Exception as e:
            print('解析json出错1 ：' + str(e))
            msg = traceback.format_exc()
            print(msg)

    def get_fans_list(self, response):
        data = response.body.decode()
        user_item = response.meta.get("user_item")
        curr_page = response.meta.get('curr_page')
        productKey = response.meta.get('productKey')
        try:
            json_data = json.loads(data)
            followerList = json_data.get('followerList')
            if followerList:
                fans_id = []
                for fans in followerList:
                    fans_id.append(str(fans['userId']))
                user_item['fans_ids'] += ';'.join(fans_id) + ';'
                curr_page += 40
                next_url = 'http://comment.api.163.com/api/v1/products/' + str(productKey) + '/follow/user/' + \
                           str(user_item['user_id']) + '/followerList?offset=' + str(curr_page) + '&limit=30&ibc=newspc'
                yield Request(
                    url=next_url,
                    callback=self.get_fans_list,
                    meta={
                        'user_item': user_item,
                        'curr_page': curr_page,
                        'productKey': productKey
                    },
                    priority=200
                )
            else:
                # 粉丝已经爬取完毕,开始爬取关注的用户
                get_focus_url = 'http://comment.api.163.com/api/v1/products/' + str(productKey) + '/follow/user/' \
                                + str(user_item['user_id']) + '/followList?offset=0&limit=30&ibc=newspc'
                yield Request(
                    url=get_focus_url,
                    callback=self.get_focus_list,
                    meta={
                        'user_item': user_item,
                        'curr_page': 0,
                        'productKey': productKey
                    },
                    priority=100
                )
        except Exception as e:
            print("解析json出错2 : " + str(e))
            msg = traceback.format_exc()
            print(msg)

    def get_focus_list(self, response):
        data = response.body.decode()
        user_item = response.meta.get("user_item")
        curr_page = response.meta.get('curr_page')
        productKey = response.meta.get('productKey')
        try:
            json_data = json.loads(data)
            followerList = json_data.get('followList')
            if followerList:
                focus_id = []
                for fans in followerList:
                    focus_id.append(fans['userId'])
                user_item['focus_ids'] += ';'.join(focus_id) + ';'
                curr_page += 40
                next_url = 'http://comment.api.163.com/api/v1/products/' + str(productKey) + '/follow/user/' + \
                           str(user_item['user_id']) + '/followList?offset=' + str(curr_page) + '&limit=30&ibc=newspc'
                yield Request(
                    url=next_url,
                    callback=self.get_focus_list,
                    meta={
                        'user_item': user_item,
                        'curr_page': curr_page,
                        'productKey': productKey
                    },
                    priority=200
                )
            else:
                yield user_item
        except Exception as e:
            print("解析json出错3 : " + str(e))
            msg = traceback.format_exc()
            print(msg)
