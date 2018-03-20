import re

from scrapy import Selector

from ifengSpider.items import *
from ifengSpider.util.time_formator import *

from ifengSpider.util.tools import *


def get_news_div1_info(response):
    sel = Selector(response)

    news_item = NewsItem()
    url = response.url

    # article_id && url
    article_id = ''.join(url.split('/')[-2::]).split('_')[0]
    news_item['article_id'] = article_id
    news_item['article_key'] = str(article_id) + '_ifeng_article'
    news_item['url'] = url

    # path_text && path_href
    path_xpath = '//div[@class="theCurrent cDGray js_crumb"]/a'
    path_text, path_href = get_path_info(response, path_xpath)
    news_item['path_text'] = path_text
    news_item['path_href'] = path_href

    # keywords && description
    keywords = sel.xpath('//meta[@keywords]/@content').extract_first()
    news_item['keywords'] = check_value(keywords)
    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(str_format(description))

    # title
    title = sel.xpath('//*[@id="artical_topic"]/text()').extract_first()
    news_item['title'] = check_value(title)

    # source
    source = sel.xpath('//span[contains(@class,"ss03")]').xpath("string(.)").extract_first()
    news_item['source'] = check_value(source)

    # author
    author = sel.xpath('//*[@itemprop="author"]/*[@itemprop="name"]/text()').extract_first()
    news_item['author'] = check_value(author)

    # editor
    editor = sel.xpath('//div[@id="artical_sth2"]/p[@class="iphone_none"]/text() |'
                       ' //div[@id="artical_sth2"]/p[@class="zb_ph pc_none_new"]/text()').extract_first()
    news_item['editor'] = check_value(editor_format(editor))

    # date_time
    date_time = sel.xpath('//meta[@name="og:time"]/@content | //span[@itemprop="datePublished"]/text()').extract_first()
    news_item['date_time'] = timeFormator(date_time)

    # content
    content_div = sel.xpath('//div[@id="main_content"]/p').xpath("string(.)").extract()
    content = ''
    for each_p in content_div:
        content += each_p
    news_item['content'] = str_format(content)

    # picture_url
    picture_div = sel.xpath('//div[@id="main_content"]/p[@class="detailPic"]/img/@src').extract()
    picture_url_list = []
    for picture in picture_div:
        picture_url_list.append(picture)
    picture_url = ';'.join(picture_url_list)
    news_item['picture_url'] = picture_url

    # docUrl
    docUrl = ''
    script_div = sel.xpath('//head/script').xpath("string(.)").extract()
    for each_script in script_div:
        if 'commentUrl' in each_script and 'jumpToCommentView' not in each_script:
            docUrl = re.findall(r'\"commentUrl\":\".+\",', each_script)[0].split(':')[1].strip()\
                .replace('\"', '').replace(',', '')
            break
    if not docUrl or 'http' in docUrl:
        docUrl = url
    print("docUrl : "+docUrl)
    news_item['comment_ids'] = ''
    news_item['join_count'] = 0
    news_item['reply_count'] = 0

    return news_item, docUrl


def get_news_div2_info(response):
    sel = Selector(response)

    news_item = NewsItem()
    url = response.url

    # article_id && url
    article_id = ''.join(url.split('/')[-2::]).split('_')[0]
    news_item['article_id'] = article_id
    news_item['article_key'] = str(article_id) + '_ifeng_article'
    news_item['url'] = url

    # path_text && path_href
    path_xpath = '//div[@class="theCurrent cDGray js_crumb"]/a'
    path_text, path_href = get_path_info(response, path_xpath)
    news_item['path_text'] = path_text
    news_item['path_href'] = path_href

    # keywords && description
    keywords = sel.xpath('//meta[@keywords]/@content').extract_first()
    news_item['keywords'] = check_value(keywords)
    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(str_format(description))

    # title
    title = sel.xpath('//div[@class="yc_tit"]/h1/text()').extract_first()
    news_item['title'] = check_value(title)

    # source
    source = sel.xpath('//div[@class="yc_tit"]/p[1]/a').xpath("string(.)").extract_first()
    news_item['source'] = check_value(source)

    # author
    author = sel.xpath('//div[@class="yc_tit"]/p[1]/span[2]/text()').extract_first()
    news_item['author'] = check_value(author)

    # editor
    editor = sel.xpath('//p[@class="yc_zb"]/text()').extract_first()
    news_item['editor'] = check_value(editor_format(editor))

    # date_time
    date_time = sel.xpath('//div[@class="yc_tit"]/p[1]/span[1]/text()').extract_first()
    news_item['date_time'] = timeFormator(date_time)

    # content
    content_div = sel.xpath('//div[@id="yc_con_txt"]/p').xpath("string(.)").extract()
    content = ''
    for each_p in content_div:
        content += each_p
    news_item['content'] = str_format(content)

    # picture_url
    picture_div = sel.xpath('//div[@id="yc_con_txt"]/p[@class="detailPic"]/img/@src').extract()
    picture_url_list = []
    for picture in picture_div:
        picture_url_list.append(picture)
    picture_url = ';'.join(picture_url_list)
    news_item['picture_url'] = picture_url

    # docUrl
    docUrl = ''
    script_div = sel.xpath('//head/script').xpath("string(.)").extract()
    for each_script in script_div:
        if 'commentUrl' in each_script and 'jumpToCommentView' not in each_script:
            docUrl = re.findall(r'\"commentUrl\":\".+\",', each_script)[0].split(':')[1].strip()\
                .replace('\"', '').replace(',', '')
            break
    if not docUrl or 'http' in docUrl:
        docUrl = url
    print("docUrl : "+docUrl)
    news_item['comment_ids'] = ''
    news_item['join_count'] = 0
    news_item['reply_count'] = 0

    return news_item, docUrl


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
