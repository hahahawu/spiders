from scrapy import Selector
from sxdailySpider.items import NewsItem
from sxdailySpider.util.timeFormator import time_formator
import re

check_value = lambda x: x if x else ''
check_time = lambda x: x if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', x) else None
str_formator = lambda x: x.replace('\u3000', '').replace('\xa0', ''). \
    replace("\"", "'").replace('\n', '').replace('\t', ' ') if x else ''
editor_formator = lambda x: ''.join(re.findall('\w', x)).replace('责任编辑', '') if x else ''
author_formator = lambda x: ';'.join(x.replace('作者：', '').split(' ')) if x else ''


def get_news_div1_info(response):
    sel = Selector(response)

    next_page_div = sel.xpath('//div[@class="container"]/div[@class="content"]//table//a')

    # 获取页面内容和图片链接
    content_list = sel.xpath('//div[@class="container"]/div[@class="content"]/div[@id="zoom"]/p') \
        .xpath("string(.)").extract()
    article_content = ''
    for content in content_list:
        article_content += str_formator(content)
    picture_url_list = sel.xpath('//div[@class="container"]/div[@class="content"]/div[@id="zoom"]/p/img/@src') \
        .extract()
    article_picture_url = ''
    for picture_url in picture_url_list:
        article_picture_url += str(response.urljoin(picture_url)) + ';'

    # 判断是否存在分页
    temp_div = next_page_div.xpath('./img/@src').extract()
    if temp_div:
        temp_div = temp_div[-1]
    next_page_flag = True if temp_div and ('next' in temp_div) else False
    if next_page_flag:
        # 页面存在下一页按钮
        # 下一页的URL
        next_page_url = next_page_div.xpath("./@href").extract_first()

        return {
            'next_page': True,
            'next_page_url': next_page_url,
            'content': article_content,
            'picture_url': article_picture_url
        }
    else:
        # 当前页面不存在分页，获取其它属性
        # 其它属性 ：date_time , editor , author , path_text , path_href

        date_time = sel.xpath('//div[@class="container title"]/div/p').xpath("string(.)").extract_first()
        date_time = check_time(time_formator(date_time))

        editor = editor_formator(sel.xpath('//div[@class="editor"]').xpath("string(.)").extract_first())

        author = author_formator(sel.xpath('//div[@class="container title"]/p').xpath("string(.)").extract_first())

        # 路径
        path_xpath = '//div[@class="local_nav"]/a'
        path_text, path_href = get_path_info(response, path_xpath)

        return {
            'next_page': False,
            'content': article_content,
            'picture_url': article_picture_url,
            'date_time': date_time,
            'editor': editor,
            'author': author,
            'path_text': path_text,
            'path_href': path_href
        }


def get_news_div2_info(response):
    sel = Selector(response)

    next_page_div = sel.xpath('//div[@id="zoom"]/center/table//a')

    # 获取页面内容和图片链接
    content_list = sel.xpath('//div[@id="zoom"]/p').xpath("string(.)").extract()
    article_content = ''
    for content in content_list:
        article_content += str_formator(content) + '\n'
    picture_url_list = sel.xpath('//div[@id="zoom"]/p/img/@src').extract()
    article_picture_url = ''
    for picture_url in picture_url_list:
        article_picture_url += str(response.urljoin(picture_url)) + ';'

    # 判断是否存在分页
    temp_div = next_page_div.xpath('./img/@src').extract()
    if temp_div:
        temp_div = temp_div[-1]
    next_page_flag = True if temp_div and ('next' in temp_div) else False
    if next_page_flag:
        # 页面存在下一页按钮
        # 下一页的URL
        next_page_url = next_page_div.xpath("./@href").extract_first()

        return {
            'next_page': True,
            'next_page_url': next_page_url,
            'content': article_content,
            'picture_url': article_picture_url
        }
    else:
        # 当前页面不存在分页，获取其它属性
        # 其它属性 ：date_time , editor , author , path_text , path_href

        date_time = sel.xpath('//div[@class="article fl"]/div[@class="content fl"]/p')\
            .xpath("string(.)").extract_first()
        date_time = check_time(time_formator(date_time))

        editor = editor_formator(sel.xpath('//div[@class="editor"]').xpath("string(.)").extract_first())

        author = check_value(sel.xpath('//div[@class="article fl"]/div[@class="content fl"]/p/b')
                             .xpath("string(.)").extract_first().replace('  ', ''))

        # 路径
        path_xpath = '//div[@class="x_nav"]/a'
        path_text, path_href = get_path_info(response, path_xpath)

        return {
            'next_page': False,
            'content': article_content,
            'picture_url': article_picture_url,
            'date_time': date_time,
            'editor': editor,
            'author': author,
            'path_text': path_text,
            'path_href': path_href
        }


def get_news_div3_info(response):
    sel = Selector(response)

    next_page_div = sel.xpath('//div[@class="text width1000 clearfix"]/center//table//a')

    # 获取页面内容和图片链接
    content_list = sel.xpath('//div[@class="text width1000 clearfix"]/p').xpath("string(.)").extract()
    article_content = ''
    for content in content_list:
        article_content += str_formator(content) + '\n'
    picture_url_list = sel.xpath('//div[@class="text width1000 clearfix"]/dl[@class="clearfix"]//img/@src').extract()
    article_picture_url = ''
    for picture_url in picture_url_list:
        article_picture_url += str(response.urljoin(picture_url)) + ';'

    # 判断是否存在分页
    temp_div = next_page_div.xpath('./img/@src').extract()[-1]
    next_page_flag = True if temp_div and ('next' in temp_div) else False
    if next_page_flag:
        # 页面存在下一页按钮
        # 下一页的URL
        next_page_url = next_page_div.xpath("./@href").extract_first()

        return {
            'next_page': True,
            'next_page_url': next_page_url,
            'content': article_content,
            'picture_url': article_picture_url
        }
    else:
        # 当前页面不存在分页，获取其它属性
        # 其它属性 ：date_time , editor , author , path_text , path_href

        date_time = sel.xpath('//div[@class="text width1000 clearfix"]/h3').xpath("string(.)").extract_first()
        date_time = check_time(time_formator(date_time))

        editor = editor_formator(sel.xpath('//div[@class="editor"]').xpath("string(.)").extract_first())

        author = author_formator(sel.xpath('//div[@class="text width1000 clearfix"]/h3/b')
                                 .xpath("string(.)").extract_first())

        # 路径
        path_xpath = '//h6[@class="margin10 width980 clear"]/a'
        path_text, path_href = get_path_info(response, path_xpath)

        return {
            'next_page': False,
            'content': article_content,
            'picture_url': article_picture_url,
            'date_time': date_time,
            'editor': editor,
            'author': author,
            'path_text': path_text,
            'path_href': path_href
        }


def get_meta_info(response):
    """
    :param response:
    :return: 包含基本信息的一个NewITem
    处理分页情况，在首次爬取页面就获取分页全部页面的基本信息
    基本信息：url , article_id , title , content = '' , summary , source , key_words , picture_url = ''
    """
    sel = Selector(response)
    item = NewsItem()

    # url && article_id
    url = response.url
    item['url'] = check_value(url)
    article_id = ''.join(url.split('/')[-3:]).split('.')[0] + '_sxdaily_news'
    item['article_id'] = check_value(article_id)

    # title
    title = ''.join(sel.xpath('//title').xpath("string(.)").extract_first().split('_')[:-1])
    item['title'] = check_value(str_formator(title))

    # summary
    summary = sel.xpath('//meta[@name="description"]/@content').extract_first()
    item['summary'] = check_value(str_formator(summary))

    # source
    source = sel.xpath('//meta[@name="source"]/@content').extract_first()
    item['source'] = check_value(str_formator(source))

    # key_words
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = check_value(str_formator(key_words))

    # content && picture_url
    item['content'] = ''
    item['picture_url'] = ''

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
