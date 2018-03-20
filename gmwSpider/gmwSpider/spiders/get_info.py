from scrapy import Selector
from gmwSpider.items import NewsItem
from gmwSpider.util.timeFormator import time_formator
import re

check_value = lambda x: x if x else ''
check_time = lambda x: x if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', x) else None
str_format = lambda x: x.strip().replace('\u3000', '').replace('\xa0', ''). \
    replace("\"", "'").replace('\n', '').replace('\t', ' ') if x else ''
editor_format = lambda x: ''.join(re.findall('\w', x)).replace('责任编辑', '') if x else ''


def get_news_div1_info(response):
    sel = Selector(response)

    next_page_div = sel.xpath('//div[@id="displaypagenum"]/center/a[@class="ptfontcon"]')

    # 获取页面内容和图片链接
    content_list = sel.xpath('//div[@id="contentMain"]//p').xpath("string(.)").extract()
    article_content = ''
    for content in content_list:
        article_content += str_format(content)
    picture_url_list = sel.xpath('//div[@id="contentMain"]/p//img/@src').extract()
    article_picture_url = ''
    for picture_url in picture_url_list:
        article_picture_url += str(response.urljoin(picture_url)) + ' ; '

    # 判断是否存在分页
    next_page_flag = False
    next_page_url = ''
    for temp_div in next_page_div:
        temp_div_str = temp_div.xpath("string(.)").extract_first()
        temp_div_href = temp_div.xpath("./@href").extract_first()
        if '下一页' in temp_div_str:
            next_page_flag = True
            next_page_url = temp_div_href
            break
    if next_page_flag:
        # 页面存在下一页按钮
        # 下一页的URL
        return {
            'next_page': True,
            'next_page_url': next_page_url,
            'content': article_content,
            'picture_url': article_picture_url
        }
    else:
        # 当前页面不存在分页，获取其它属性
        # 其它属性 ：date_time , editor , author , path_text , path_href

        date_time = sel.xpath('//span[@id="pubTime"]').xpath("string(.)").extract_first()
        date_time = check_time(time_formator(date_time))

        editor = editor_format(sel.xpath('//div[@id="contentLiability"]').xpath("string(.)").extract_first())

        source = check_value(sel.xpath('//span[@id="source"]/a').xpath("string(.)").extract_first())

        # 路径
        path_xpath = '//div[@id="contentBreadcrumbs2"]/a'
        path_text, path_href = get_path_info(response, path_xpath)

        return {
            'next_page': False,
            'content': article_content,
            'picture_url': article_picture_url,
            'date_time': date_time,
            'editor': editor,
            'source': source,
            'path_text': path_text,
            'path_href': path_href
        }


def get_news_div2_info(response):
    sel = Selector(response)

    # 获取页面内容和图片链接
    content_list = sel.xpath('//div[@id="ArticleContent"]/div[@class="ArticleContentBox"]/p') \
        .xpath("string(.)").extract()
    article_content = ''
    for content in content_list:
        article_content += str_format(content)
    picture_url_list = sel.xpath('//div[@id="ArticleContent"]/div[@class="ArticleContentBox"]//img/@src').extract()
    article_picture_url = ''
    for picture_url in picture_url_list:
        article_picture_url += str(response.urljoin(picture_url)) + ' ; '

    # 判断是否存在分页
    next_page_div = sel.xpath('//div[@id="displaypagenum"]/center/a[@class="ptfontpic"]')
    next_page_flag = False
    next_page_url = ''
    for temp_div in next_page_div:
        temp_div_str = temp_div.xpath("string(.)").extract_first()
        temp_div_href = temp_div.xpath("./@href").extract_first()
        if '下一页' in temp_div_str:
            next_page_flag = True
            next_page_url = temp_div_href
            break
    if next_page_flag:
        # 页面存在下一页按钮
        # 下一页的URL
        return {
            'next_page': True,
            'next_page_url': next_page_url,
            'content': article_content,
            'picture_url': article_picture_url
        }
    else:
        # 当前页面不存在分页，获取其它属性
        # 其它属性 ：date_time , editor , author , path_text , path_href

        date_time = sel.xpath('//span[@id="pubTime"]').xpath("string(.)").extract_first()
        date_time = check_time(time_formator(date_time))

        editor = editor_format(sel.xpath('//div[@id="Content_Liability"]').xpath("string(.)").extract_first())

        source = check_value(sel.xpath('//span[@id="source"]/a').xpath("string(.)").extract_first())

        # 路径
        path_xpath = '//div[@id="picContent-breadCrumbs2"]/a'
        path_text, path_href = get_path_info(response, path_xpath)

        return {
            'next_page': False,
            'content': article_content,
            'picture_url': article_picture_url,
            'date_time': date_time,
            'editor': editor,
            'source': source,
            'path_text': path_text,
            'path_href': path_href
        }


def get_news_div3_info(response):
    sel = Selector(response)

    # 获取页面内容和图片链接
    content_list = sel.xpath('//div[@id="container"]/div[@id="cont_left"]/p').xpath("string(.)").extract()
    article_content = ''
    for content in content_list:
        article_content += str_format(content)
    picture_url_list = sel.xpath('//div[@id="container"]/div[@id="cont_left"]/p//img/@src').extract()
    article_picture_url = ''
    for picture_url in picture_url_list:
        article_picture_url += str(response.urljoin(picture_url)) + ' ; '

    # 判断是否存在分页
    next_page_div = sel.xpath('//div[@id="displaypagenum"]/center/a[@class="ptfontpic"]')
    next_page_flag = False
    next_page_url = ''
    for temp_div in next_page_div:
        temp_div_str = temp_div.xpath("string(.)").extract_first()
        temp_div_href = temp_div.xpath("./@href").extract_first()
        if '下一页' in temp_div_str:
            next_page_flag = True
            next_page_url = temp_div_href
            break
    if next_page_flag:
        # 页面存在下一页按钮
        # 下一页的URL
        return {
            'next_page': True,
            'next_page_url': next_page_url,
            'content': article_content,
            'picture_url': article_picture_url
        }
    else:
        # 当前页面不存在分页，获取其它属性
        # 其它属性 ：date_time , editor , author , path_text , path_href

        date_time = sel.xpath('//span[@id="pubTime"]').xpath("string(.)").extract_first()
        date_time = check_time(time_formator(date_time))

        editor = editor_format(sel.xpath('//div[@id="Content_Liability"]').xpath("string(.)").extract_first())

        source = check_value(sel.xpath('//span[@id="source"]/a').xpath("string(.)").extract_first())

        # 路径
        path_xpath = '//div[@id="picContent-breadCrumbs2"]/a'
        path_text, path_href = get_path_info(response, path_xpath)

        return {
            'next_page': False,
            'content': article_content,
            'picture_url': article_picture_url,
            'date_time': date_time,
            'editor': editor,
            'source': source,
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
    article_id = ''.join(url.split('/')[-3:]).split('.')[0].replace('content', 'c') + '_gmdaily_news'
    item['article_id'] = check_value(article_id)

    # title
    # title = ''.join(sel.xpath('//title').xpath("string(.)").extract_first().split('_')[:-1])
    title = sel.xpath('//*[@id="articleTitle"] | //*[@class="picContentHeading"]').xpath("string(.)").extract_first()
    item['title'] = check_value(str_format(title))

    # summary
    summary = sel.xpath('//meta[@name="description"]/@content').extract_first()
    item['summary'] = check_value(str_format(summary))

    # author
    author = sel.xpath('//meta[@name="author"]/@content').extract_first()
    item['author'] = check_value(str_format(author))

    # key_words
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = check_value(str_format(key_words))

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

    return '; '.join(path_text_list[1::]), '; '.join(path_href_list[1::])
