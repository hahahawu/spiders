#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib

import scrapy
from scrapy import Request
from scrapy import Selector

from xinhuaSpider.spiders.getInfo import get_third_part, get_first_part


class TestSpider(scrapy.Spider):
    name = 'test'

    start_urls = [
        # "http://news.xinhuanet.com/yuqing/2014-10/09/c_127075515_4.htm"
        # "http://news.xinhuanet.com/yuqing/2012-12/28/c_124159669_2.htm"
        # "http://news.xinhuanet.com/yuqing/2011-09/30/c_122296670.htm"
        'http://news.xinhuanet.com/yuqing/2011-09/30/c_122296670_2.htm'
    ]

    def parse(self, response):
        pass
        # # 获取最新的版式<div id='article'>
        # article_div = response.xpath('//div[@id="article"]/div[@class="article"]').extract_first()
        # # 获得<div id='contentblock'>版本的文章
        # content_block_div = response.xpath('//div[@id="contentblock"]/span[@id="content"]').extract_first()
        # # 获得<div id='content'>版本的文章
        # content_div = response.xpath('//div[@id="content"]').extract_first()
        # # 获得<div id='Content'>版本的文章
        # b_content_div = response.xpath('//div[@id="Content"]').extract_first()
        #
        # div = article_div
        # time_xpath = '//div[@class="source"]/span[@class="time"]/text()'
        # source_xpath = '//div[@class="source"]/span[@class="sourceText"]/text()'
        # next_page_xpath = '//div[@id="div_currpage"]/a[@class="nextpage"]/@href'
        # next_page_text_xpath = '//div[@id="div_currpage"]/a[@class="nextpage"]/text()'
        #
        # if content_block_div:
        #     div = content_block_div
        #     time_xpath = '//div/span[@id="pubtime"]/text()'
        #     source_xpath = '//div/span[@id="from"]/a/text()'
        # elif content_div:
        #     div = content_div
        #     time_xpath = '//div/span[@id="pubtime"]/text()'
        #     source_xpath = '//div/span[@id="source"]/text()'
        # elif b_content_div:
        #     div = b_content_div
        #     time_xpath = '//span[@id="pubtime"]/text()'
        #     source_xpath = '//table[contains(@class, "biaoti")]/tr/td/a[last()]/text()'
        #
        # if div:
        #     children_div = Selector(text=div).xpath('/*/*/*/*').extract()
        #     article = ''
        #     for child_div in children_div:
        #         if not Selector(text=child_div).xpath('//script'):
        #             article += Selector(text=child_div).xpath('string(.)').extract_first() + '\n'
        #     next_page = Selector(text=div).xpath(next_page_xpath).extract_first()
        #     next_page_text = Selector(text=div).xpath(next_page_text_xpath).extract_first()
        #     if next_page_text:
        #         next_page_text = next_page_text.strip()
        #     if next_page and next_page_text == '下一页':
        #
        #         yield {
        #             'next_page': True,
        #             'next_page_url': next_page,
        #             'content': article
        #         }
        #     else:
        #         # 获取页面的其他元素
        #         # 文章ID
        #         article_id = ''.join(response.url.split('/')[-3:]).split('.')[:1]
        #         # 文章url
        #         url = response.url
        #         # 文章发布时间
        #         publish_time = response.xpath(time_xpath).extract_first()
        #         if publish_time:
        #             publish_time = publish_time.strip('\r\n')
        #
        #         # 文章来源
        #         source = response.xpath(source_xpath).extract_first()
        #         if source:
        #             source = source.strip('\r\n')
        #
        #         yield {
        #             'next_page': False,
        #             'article_id': article_id,
        #             'url': url,
        #             'publish_time': publish_time,
        #             'source': source,
        #             'content': article
        #         }



                #################################################################################################################

                #################################################################################################################

                # # 找到要提交的表单
                # form = response.xpath('//form[@name="searchform"]').extract_first()
                # form_action = Selector(text=form).xpath('//form/@action').extract_first()
                # form_inputs = Selector(text=form).xpath('//input')
                # form_dic = {}
                # for form_input in form_inputs:
                #     name = form_input.xpath('@name').extract_first()
                #     value = form_input.xpath('@value').extract_first()
                #     form_dic[name] = value
                #
                # # 获取下页的网址
                # page_script = response.xpath('//div[@class="pageControl"]/script/text()').extract_first()
                # if page_script:
                #     # cur_page_regex = r'var +curpage *= *(\d+)'
                #     per_page_regex = r'var +perpage *= *(\d+)'
                #     record_num_regex = r'var +recordnum *= *(\d+)'
                #
                #     # p_cur_page = re.compile(cur_page_regex)
                #     p_per_page = re.compile(per_page_regex)
                #     p_record_num = re.compile(record_num_regex)
                #
                #     # g_cur_page = p_cur_page.search(page_script)
                #     g_per_page = p_per_page.search(page_script)
                #     g_record_num = p_record_num.search(page_script)
                #     page_num = 0
                #
                #     if g_per_page and g_record_num:
                #         # cur_page = int(g_cur_page.group(1))
                #         per_page = int(g_per_page.group(1))
                #         record_num = int(g_record_num.group(1))
                #         page_num = record_num // per_page + 1
                #
                #     if int(form_dic['page']) < page_num:
                #         form_dic['page'] = int(form_dic['page']) + 1
                #         form_url = form_action + '?'
                #         # for form_name in form_dic:
                #         #     form_url = form_url + form_name + '=' + str(form_dic[form_name]) + '&'
                #         url_params = urllib.parse.urlencode(form_dic)
                #         form_url += url_params
                #         url_tmp = response.urljoin(form_url[:-1])
                #
                #         return url_tmp
                #     else:
                #         return None





                # print(response.urljoin(s))
                # third_part = response.xpath('//div[@class="thirdPart"]')
                # if not third_part:
                #     return None
                #
                # if parse_l:
                #     part_l = third_part.xpath('div[@class="partL"]')
                #
                #     # 获取标题
                #     table_title_list = part_l.xpath('//div/ul[@class="showBody clearfix"]/li')
                #     if table_title_list:
                #         title_list = []
                #         for table_title in table_title_list:
                #             title_text = table_title.xpath('text()').extract_first()
                #             title_index = table_title.xpath('@data-index').extract_first()
                #             title_list.append((int(title_index), title_text))
                #
                #
                #         # 获取具体内容
                #         table_contents_list = part_l.xpath('div[@class="tabCon"]/div[@class="con"]')
                #
                #         for index, value in title_list:
                #             table_contents = table_contents_list[index - 1].xpath('div[contains(@id, "hideData")]/ul/li')
                #             for table_content in table_contents:
                #                 title = table_content.xpath('h3/a/text() | h2/a/text()').extract_first()
                #                 article_href = table_content.xpath('h3/a/@href | h2/a/@href').extract_first()
                #                 summary = table_content.xpath('p[@class="summary"]/text()').extract_first()
                #
                #                 yield {
                #                     'isArticle': True,
                #                     'sub_category': value,
                #                     'url': article_href,
                #                     'title': title,
                #                     'summary': summary
                #                 }
                #
                #             # 获取“/查看更多”中的内容 返回“查看更多”的网址
                #             more_div = table_contents_list[index - 1].xpath('ul[contains(@id, "showData")]/li/a')
                #             if more_div:
                #                 more_href = more_div.xpath('@href').extract_first()
                #
                #                 yield {
                #                     'isArticle': False,
                #                     'sub_category': value,
                #                     'href': more_href
                #                 }
                #
                #     col_list = part_l.xpath('div[@class="colList"]/div/a')
                #     if col_list:
                #         for col in col_list:
                #             col_url = col.xpath('@href').extract_first()
                #             col_text = col.xpath('string(.)').extract_first()
                #             if col_url and col_text:
                #                 yield {
                #                     'isArticle': False,
                #                     'sub_category': col_text,
                #                     'href': col_url
                #                 }
                #
                # if parse_r:
                #     part_r = third_part.xpath('div[contains(@class, "partR")]')     # 右边区域
                #     part_r_field = part_r.extract_first()
                #     part_r_div_list = Selector(text=part_r_field).xpath('//div[contains(@class, "combox")]/h2/a')
                #     for part_r_div in part_r_div_list:
                #         part_r_href = part_r_div.xpath('@href').extract_first()
                #         part_r_text = part_r_div.xpath('string(.)').extract_first()
                #
                #         if part_r_text and part_r_href:
                #             yield {
                #                 'isArticle': False,
                #                 'sub_category': part_r_text,
                #                 'href': part_r_href
                #             }
                #
                #     # 获取右边的table模块
                #     r_table_list = part_r.xpath('div[contains(@class, "tab")]/div/ul/li/a')
                #     for r_table in r_table_list:
                #         table_href = r_table.xpath('@href').extract_first()
                #         table_text = r_table.xpath('string(.)').extract_first()
                #
                #         if table_text and table_href:
                #             yield {
                #                 'isArticle': False,
                #                 'sub_category': table_text,
                #                 'href': table_href
                #             }
                #####################################################################################################################################################################

                #####################################################################################################################################################################

                # """
                #             :param response:
                #             :param parse_l:
                #             :param parse_r:
                #             :return: sub_category,
                #                      url,
                #                      title,
                #                      summary
                #             """
                # first_part = response.xpath('//div[@class="firstPart"]')
                # if not first_part:
                #     return None
                #
                # if parse_l:
                #     # 获取partL
                #     part_l = first_part.xpath('div[@class="partL"]')  # 左边区域
                #
                #     if part_l:
                #         # 获取图片区的新闻
                #         sub_category = 'rollPic'
                #         pic_part_list = part_l.xpath('div[@class="device"]//div[@class="swiper-slide"]')
                #         for pic_part in pic_part_list:
                #             article_href = pic_part.xpath('a/@href').extract_first()
                #             img_src = pic_part.xpath('a/img/@src').extract_first()
                #             title = pic_part.xpath('a/img/@alt').extract_first()
                #
                #             yield {
                #                 'isArticle': True,
                #                 'sub_category': sub_category,
                #                 'url': article_href,
                #                 'title': title,
                #                 'summary': response.urljoin(img_src)
                #             }
                #
                #         # 获取otherPart
                #         sub_category_list = part_l.xpath("div/h3/a | div/h2/a")
                #         for sub_category in sub_category_list:
                #             text = sub_category.xpath('string(.)').extract_first()
                #             href = sub_category.xpath('@href').extract_first()
                #
                #             yield {
                #                 'isArticle': False,
                #                 'sub_category': text,
                #                 'url': href
                #             }
                #
                #         # firstPart 左边的下方栏目
                #         sub_li_list = part_l.xpath('//div[@class="tab"]/div[@class="tab_title"]/ul/li/a')
                #         for sub_li in sub_li_list:
                #             li_text = sub_li.xpath('string(.)').extract_first()
                #             li_href = sub_li.xpath('@href').extract_first()
                #
                #             yield {
                #                 'isArticle': False,
                #                 'sub_category': li_text,
                #                 'url': li_href
                #             }
                #
                # if parse_r:
                #     # 获取partR
                #     # url 和summary为空
                #     part_r = first_part.xpath('div[contains(@class, "partR")]')  # 右边区域
                #     if part_r:
                #         sub_category_list = part_r.xpath("div/h3/a | div/h2/a")
                #         for sub_category in sub_category_list:
                #             text = sub_category.xpath('string(.)').extract_first()
                #             href = sub_category.xpath('@href').extract_first()
                #
                #             yield {
                #                 'isArticle': False,
                #                 'sub_category': text,
                #                 'href': href
                #             }
                # if not part_l and not parse_r:
                #     return None
