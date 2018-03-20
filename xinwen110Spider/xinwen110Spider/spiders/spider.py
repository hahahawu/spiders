from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from xinwen110Spider.spiders.get_info import get_news_info


class Xinwen110Spider(CrawlSpider):
    name = 'xinwen110'

    allowed_domains = ['xinwen110.org']

    start_urls = ['http://www.xinwen110.org/']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/a/\w+/\d+.html',
            '/a/\w+/\d{4}-\d{2}-\d{2}/\d+.html'
        ),
        allow_domains=(
            'xinwen110.org',
        ),
        deny=(
            '/e/\.*'
            'job=report',
            'job=recommend',
            'job=collect',
            'type=vote',
            'comment.php',
            'job=postnew',
        )
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/a/\.*'
        # ),
        allow_domains=(
            'xinwen110.org',
        ),
        deny=(
            '/e/\.*'
            'job=report',
            'job=recommend',
            'job=collect',
            'type=vote',
            'comment.php',
            'job=postnew',
        )
    )

    rules = (
        Rule(article_extract, follow=False, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    #
    # a_count = 0
    # f_count = 0

    def parse_article(self, response):
        sel = Selector(response)
        # self.a_count += 1
        # print('article:  ' + str(self.a_count) + '   ' + response.url)
        # news_div = sel.xpath('//td[@class="middle"]/table[@class="content"]')
        news_div = sel.xpath('//div[@class="left_list fl"]')
        if news_div:
            item = get_news_info(response)

            yield item
        else:
            raise ValueError('Page style not in list: ' + response.url)

    def parse_follow(self, response):
        sel = Selector(response)
        page_links = sel.xpath('//div[@class="page"]/a')
        if page_links:
            for href in page_links:
                if href.xpath("string(.)").extract_first() == '下一页':
                    yield Request(response.urljoin(href.xpath("./@href").extract_first()))
