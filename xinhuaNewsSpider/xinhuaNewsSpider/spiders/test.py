#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule

from xinhuaNewsSpider.spiders.get_info import *


class Test(Spider):
    name = 'test'

    allowed_domains = ['people.com.cn']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://news.xinhuanet.com/asia/2016-12/29/c_129424369.htm']

    def parse(self, response):
        sel = Selector(response)
        news_1_div = sel.xpath('//div[@id="center"]/div[@id="article"] | //td/div[@id="Content"]//span[@id="content"]')
        science_div = sel.xpath('//div[@class="content"]/div[@class="c_left"]')
        news_old_div = sel.xpath('//div[@id="content"]/div[@id="article"]')
        daily_div = sel.xpath('//font[@id="Zoom"]')
        pic_div = sel.xpath('//div[@class="conW"]/div[@class="content"] | '
                            '//div[@class="detail_body"]/div[@class="content_main clearfix"] | '
                            '//*[@class="bai13"]')
        data_news_nid = sel.xpath('//div[@class="main"]/div[@class="article"]')
        global_div = sel.xpath('//body[@bgcolor]/div[@align="center"]/table[@width]')
        bj_div = sel.xpath('//div[@id="page"]/div[@id="mains"] | //div[@id="page"]/div[@id="main"]')
        mrdx_div = sel.xpath('//td[@class="fs16 bl lh30"]/div[@id="Content"]')
        politics_div = sel.xpath('//div[@class="main pagewidth"]/div[@id="content"] '
                                 '| //div[@class="c_left"]/div[@id="content"]')
        world_div = sel.xpath('//div[@id="contentblock"]/span[@id="content"]')
        asia_news_div = sel.xpath('//div[@class="ej_box"]')

        item = get_asia_news_div(response)

        return item
