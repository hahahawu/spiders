from scrapy.spiders import CrawlSpider,Rule
from scrapy import Request
from xinhuaSpider.items import XinhuaSpiderItem
from xinhuaSpider.spiders.getInfo import get_category, get_first_part, get_iframe_src, get_third_part, get_article, \
    get_more_news_list, get_more_next_page


class XinhuaSpider(CrawlSpider):
    name = 'xinhua'

    allowed_domains = ['xinhuanet.com',
                       'news.cn']

    start_urls = [
        "http://www.xinhuanet.com/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          callback=self.parse_home)

    # 爬取首页类别导航栏
    def parse_home(self, response):
        # encoding = response.headers.encoding
        category_list = get_category(response)
        if not category_list:
            return None

        for category, href in category_list:
            params = {
                'category': category,
                # 'third_part_right': True
            }

            yield Request(response.urljoin(href),
                          callback=self.parse_category,
                          meta=params
                          )

    # 爬取具体的类别
    def parse_category(self, response):
        category = response.meta['category']
        # third_part_right = response.meta['third_part_right']
        # 获取第一部分
        first_part = get_first_part(response)
        for first_result in first_part:
            if first_result:
                url = response.urljoin(first_result['url'])
                # 如果是文章的链接,则去解析文章页面
                if first_result['isArticle']:
                    params = {
                        'category': category,
                        'url': url,
                        'sub_category': first_result['sub_category'],
                        'title': first_result['title'],
                        'summary': first_result['summary'],
                    }

                    yield Request(url,
                                  callback=self.parse_article,
                                  meta=params)
                else:
                    # 处理frameSrc
                    link_params = {
                        'category': category,
                        'sub_category': first_result['sub_category']
                    }
                    iframe = get_iframe_src(response)
                    if iframe:
                        yield Request(response.urljoin(iframe),
                                      callback=self.parse_iframe_src,
                                      meta=link_params)
                    else:
                        yield Request(response.urljoin(first_result['url']),
                                      callback=self.parse_category,
                                      meta={
                                          'category': category,
                                          'sub_category': first_result['sub_category'],
                                          # 'third_part_right': True
                                      })
        # 获取第三部分
        third_part = get_third_part(response)
        for third_result in third_part:
            if third_result:
                third_url = response.urljoin(third_result['url'])
                if third_result['isArticle']:
                    params = {
                        'category': category,
                        'url': third_url,
                        'sub_category': third_result['sub_category'],
                        'title': third_result['title'],
                        'summary': third_result['summary'],
                    }

                    yield Request(third_url,
                                  callback=self.parse_article,
                                  meta=params)
                else:
                    link_params = {
                        'category': category,
                        'sub_category': third_result['sub_category']
                    }

                    iframe = get_iframe_src(response)
                    if iframe:
                        yield Request(response.urljoin(iframe),
                                      callback=self.parse_iframe_src,
                                      meta=link_params)
                    else:
                        yield Request(response.urljoin(third_result['url']),
                                      callback=self.parse_category,
                                      meta={
                                          'category': category,
                                          'sub_category': third_result['sub_category'],
                                          'third_part_right': False
                                      })

    # 解析文章页面
    def parse_article(self, response):
        # 获取传递的参数
        article_item = response.meta.get('article_item')
        if not article_item:
            article_item = XinhuaSpiderItem()
            article_item['content'] = ''
            article_item['category'] = response.meta['category']
            article_item['url'] = response.meta['url']
            article_item['sub_category'] = response.meta['sub_category']
            article_item['title'] = response.meta['title']
            article_item['summary'] = response.meta['summary']

        # 解析文章页面
        article = get_article(response)
        if article and article['next_page']:
            article_item['content'] += article['content']
            yield Request(response.urljoin(article['next_page_url']),
                          callback=self.parse_article,
                          meta={
                              'article_item': article_item
                          })

        else:
            article_item['article_id'] = article['article_id']
            article_item['publish_time'] = article['publish_time']
            article_item['origin'] = article['source']
            article_item['content'] += article['content']
            # article_item['editor'] = article['editor']

            yield article_item

    # 解析frameSrc
    def parse_iframe_src(self, response):
        # 接收传递的参
        category = response.meta['category']
        sub_category = response.meta['sub_category']

        article_list = get_more_news_list(response)
        for article in article_list:
            if article:
                url = response.urljoin(response.meta['url'])

                params = {
                    'category': category,
                    'sub_category': sub_category,
                    'title': response.meta['title'],
                    'summary': response.meta['summary'],
                    'url': url
                }

                yield Request(url,
                              callback=self.parse_article,
                              meta=params)

        next_page = get_more_next_page(response)
        if next_page:
            yield Request(response.urljoin(next_page),
                          callback=self.parse_iframe_src,
                          meta={
                              'category': category,
                              'sub_category': sub_category
                          })
