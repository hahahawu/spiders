from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import Selector, Request

from sxdailySpider.spiders.get_info import *


class SxdailySpider(CrawlSpider):
    name = 'sxdaily'

    allowed_domains = ['sxdaily.com.cn']

    start_urls = ['http://www.sxdaily.com.cn/']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/n/\d{4}/\d{4}/c\d+-\d+(-\d+)?.html'
        ),
        allow_domains=(
            'sxdaily.com.cn',
        ),
        deny_domains=(
            'vote.sxdaily.com.cn'
        ),
        deny=(
            '/about/.*',
            '/appfile/.*',
        )
    )

    follow_extract = LxmlLinkExtractor(
        allow=(
            '/GB/.*',
        ),
        allow_domains=(
            'sxdaily.com.cn'
        ),
        deny_domains=(
            'vote.sxdaily.com.cn'
        ),
        deny=(
            '/about/.*',
            '/appfile/.*',
        )
    )

    rules = (
        Rule(article_extract, follow=False, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    article_count = 0

    def parse_article(self, response):
        sel = Selector(response)
        news_div_1 = sel.xpath('//div[@class="container"]/div[@class="content"]')
        news_div_2 = sel.xpath('//div[@class="container"]/div[@class="article fl"]/div[@class="content fl"]')
        news_div_3 = sel.xpath('//div[@class="text width1000 clearfix"]')

        article_item = response.meta.get('article_item')
        if not article_item:
            article_item = get_meta_info(response)

        # 解析文章页面
        if news_div_1:
            article = get_news_div1_info(response)
        elif news_div_2:
            article = get_news_div2_info(response)
        elif news_div_3:
            article = get_news_div3_info(response)
        else:
            raise ValueError("Page style isn't defined : " + response.url)
        if article and article['next_page']:
            article_item['content'] += article['content']
            article_item['picture_url'] += article['picture_url']
            yield Request(response.urljoin(article['next_page_url']),
                          callback=self.parse_article,
                          meta={
                              'article_item': article_item
                          })
        else:
            article_item['picture_url'] += article['picture_url']
            article_item['content'] += article['content']
            article_item['date_time'] = article['date_time']
            article_item['editor'] = article['editor']
            article_item['author'] = article['author']
            article_item['path_text'] = article['path_text']
            article_item['path_href'] = article['path_href']

            self.article_count += 1
            print('article_count : ' + str(self.article_count))

            yield article_item

    def parse_follow(self, response):
        sel = Selector(response)

        a_list = sel.xpath('//a/@href').extract()

        for link in a_list:
            if re.match(r'/n/\d{4}/\d{4}/c\d+-\d+(-\d+).html', link):
                yield Request(
                    url=response.urljoin(link),
                    callback=self.parse_article,
                    priority=100
                )
