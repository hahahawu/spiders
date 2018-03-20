#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector
import re
from xinwen110Spider.items import NewsItem

check_value = lambda x: x if x else ''
check_time = lambda x: x if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', x) else None


def get_news_info(response):
    sel = Selector(response)
    item = NewsItem()
    url = response.url

    item['url'] = url
    item['article_id'] = ''.join(url.split('/')[-3::]).split('.')[0] + '_xinwen110_news'

    # 路径
    path_xpath = '//div[@class="conbar"]/div[@class="fl"]/div[@class="connav fl"]/a'
    path_text, path_href = get_path_info(response, path_xpath)
    item['path_text'] = check_value(path_text).strip()
    item['path_href'] = check_value(path_href).strip()

    # 标题
    title = sel.xpath('//*[@id="h1title"]').xpath('string(.)').extract_first()
    item['title'] = title

    # 日期时间 & 来源 & 作者
    info_div = sel.xpath('//div[@class="fl col6"]/text()').extract_first()
    # date_time = info_div[0].xpath('string(.)').extract_first()
    # source = info_div[1].xpath('string(.)').extract_first()

    try:
        info_array = info_div.split('\u3000')
        date_time = check_time(info_array[0])
        source = info_array[1].split(':')[1].strip()
        author = info_array[2].split(':')[1].strip()
        item['date_time'] = check_value(date_time).strip()
        item['source'] = check_value(source).strip()
        item['author'] = check_value(author).strip()
    except AttributeError as e:
        print('Exception : ', str(e))
        print('info : ', str(info_div))

    # 浏览量
    # read_num = sel.xpath('//*[@id="hits"]').xpath('string(.)').extract_first()
    # comment_num = sel.xpath('//*[@id="commnetsnum"]').xpath('string(.)').extract_first()

    # item['read_num'] = check_value(read_num).strip()
    # item['comment_num'] = check_value(comment_num).strip()

    # 摘要
    summary = sel.xpath('//div[@class="summary"]').xpath('string(.)').extract_first()
    summary = summary.replace("\"", "\'")
    summary = summary.replace("“", "\'")
    item['summary'] = check_value(summary)

    # 内容
    content = sel.xpath('//*[@id="text"]').xpath('string(.)').extract_first()
    content = ''.join(re.findall(u'[\u4e00-\u9fa5].+?', content))
    content = content.replace("\"", "\'")
    content = content.replace("“", "\'")
    item['content'] = check_value(content).strip()

    # 图片
    picture_urls = sel.xpath('//*[@id="text"]//img/@src').extract()
    item['picture_url'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    return item


def get_path_info(response, path_xpath):
    sel = Selector(response)
    path_div = sel.xpath(path_xpath)

    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(check_value(path_text))
        path_href_list.append(response.urljoin(path_href))

    return '; '.join(path_text_list), '; '.join(path_href_list)
