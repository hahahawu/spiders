from scrapy import Selector
from wy163Spider.items import *

from wy163Spider.util.time_formator import *

check_value = lambda x: x if x else ''
editor_format = lambda x: x.replace('责任编辑：', '') if x else ''
str_format = lambda x: x.strip().replace('\u3000', '').replace('\xa0', ''). \
    replace("\"", "'").replace('\n', '').replace('\t', ' ') if x else ''


def get_news_div1_info(response):
    sel = Selector(response)
    news_item = NewsItem()

    url = response.url
    # article_id
    article_id = ''.join(url.split('/')[-4::]).split('.')[0] + '_wy163_news'
    news_item['article_id'] = check_value(article_id)
    news_item['url'] = url

    # path_text & path_href
    path_xpath = '//div[@class="clearfix"]/div[@class="post_crumb"]/a'
    path_text, path_href = get_path_info(response, path_xpath)
    news_item['path_text'] = path_text
    news_item['path_href'] = path_href

    # date_time
    date_time = sel.xpath('//div[@id="epContentLeft"]/div[@class="post_time_source"]/text() '
                          '| //div[@class="ep-time-soure cDGray"]/text()').extract_first()
    news_item['date_time'] = timeFormator(check_value(date_time))

    # source
    source = sel.xpath('//*[@id="ne_article_source"]').xpath("string(.)").extract_first()
    news_item['source'] = check_value(source)

    # title
    title = sel.xpath('//div[@id="epContentLeft"]/h1/text() | //title/text()').extract_first()
    news_item['title'] = check_value(title)

    # keywords
    keywords = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['keywords'] = check_value(keywords)

    # author
    author = sel.xpath('//meta[@name="author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    # description
    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    # copyright
    copyRight = sel.xpath('//meta[@name="Copyright"]/@content').extract_first()
    news_item['copyright'] = check_value(copyRight)

    # editor
    editor = sel.xpath('//div[@class="ep-source cDGray"]/*[@class="ep-editor"]').xpath("string(.)").extract_first()
    news_item['editor'] = editor_format(editor)

    # content
    content_div = sel.xpath('//div[@id="endText"]/p').xpath("string(.)").extract()
    content = ''
    for each_p in content_div:
        content += each_p
    news_item['content'] = re.findall(u'[\u4e00-\u9fa5].+?', content)

    # picture_url
    picture_div = sel.xpath('//div[@id="endText"]/p[@class="f_center"]/img/@src | //div[@id="endText"]/div//img/@src')\
        .extract()
    picture_url_list = []
    for picture in picture_div:
        picture_url_list.append(picture)
    picture_url = ';'.join(picture_url_list)
    news_item['picture_url'] = picture_url

    # video_url
    video_div = sel.xpath('//div[@id="endText"]//div[@class="video"]/video/source/@src').extract()
    video_url_list = []
    for video in video_div:
        picture_url_list.append(video)
    video_url = ';'.join(video_url_list)
    news_item['video_url'] = video_url

    # join_count && reply_count
    # join_count = sel.xpath('//a[@class="js-tiecount js-tielink"]').xpath("string(.)").extract_first()
    # reply_count = sel.xpath('//a[@class="js-tiejoincount js-tielink"]').xpath("string(.)").extract_first()
    # news_item['join_count'] = int(join_count)
    # news_item['reply_count'] = int(reply_count)

    # 初始化comment_ids
    news_item['comment_ids'] = ''

    # 获取productKey和docId
    productKey = ''
    script_div = sel.xpath('//*[@id="post_comment_area"]/script').xpath("string(.)").extract()
    for each_script in script_div:
        if 'productKey' in each_script:
            productKey = re.findall(r'\"productKey\" : \"\w+\"', each_script)[0].split(':')[1].strip().replace('\"', '')
            break
    docId = ''.join(url.split('/')[-1]).split('.')[0]

    # print("productKey : " + str(productKey))
    # print("docId : " + str(docId))
    return {
        'productKey': productKey,
        'docId': docId,
        'news_item': news_item
    }


def get_news_div2_info(response):
    sel = Selector(response)
    news_item = NewsItem()

    url = response.url
    # article_id
    article_id = ''.join(url.split('/')[-4::]).split('.')[0] + '_wy163_news'
    news_item['article_id'] = check_value(article_id)
    news_item['url'] = url

    # path_text & path_href
    path_xpath = '//div[@class="clearfix"]/div[@class="post_crumb"]/a'
    path_text, path_href = get_path_info(response, path_xpath)
    news_item['path_text'] = path_text
    news_item['path_href'] = path_href

    # date_time
    date_time = sel.xpath('//div[@class="atc_hd"]//div[@class="ep-time-soure cDGray"]/text()').extract_first()
    news_item['date_time'] = timeFormator(date_time)

    # source
    source = sel.xpath('//div[@class="ep-time-soure cDGray"]/a').xpath("string(.)").extract_first()
    news_item['source'] = check_value(source)

    # title
    title = sel.xpath('//div[@class="atc_title"]/h1/text() | //title/text()').extract_first()
    news_item['title'] = check_value(title)

    # keywords
    keywords = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['keywords'] = check_value(keywords)

    # author
    author = sel.xpath('//meta[@name="author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    # description
    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    # copyright
    copyRight = sel.xpath('//meta[@name="Copyright"]/@content').extract_first()
    news_item['copyright'] = check_value(copyRight)

    # editor
    editor = sel.xpath('//*[@class="ep-editor"]').xpath("string(.)").extract_first()
    news_item['editor'] = editor_format(editor)

    # content
    content_div = sel.xpath('//div[@id="endText"]/p/text()').extract()
    content = ''
    for each_p in content_div:
        content += each_p
    news_item['content'] = re.findall(u'[\u4e00-\u9fa5].+?', content)

    # picture_url
    picture_div = sel.xpath('//div[@id="endText"]/p[@class="f_center"]/img/@src | //div[@id="endText"]/div//img/@src') \
        .extract()
    picture_url_list = []
    for picture in picture_div:
        picture_url_list.append(picture)
    picture_url = ';'.join(picture_url_list)
    news_item['picture_url'] = picture_url

    # video_url
    video_url = sel.xpath('//div[@id="endText"]//div[@class="video"]/video/source/@src').extract_first()
    news_item['video_url'] = video_url

    # join_count && reply_count
    # join_count = sel.xpath('//a[@class="js-tiecount js-tielink"]').xpath("string(.)").extract_first()
    # reply_count = sel.xpath('//a[@class="js-tiejoincount js-tielink"]').xpath("string(.)").extract_first()
    # news_item['join_count'] = int(join_count)
    # news_item['reply_count'] = int(reply_count)

    # 初始化comment_ids
    news_item['comment_ids'] = ''

    # 获取productKey和docId
    productKey = ''
    script_div = sel.xpath('//div[@class="sect_cmt sect"]/script').xpath("string(.)").extract()
    for each_script in script_div:
        if 'productKey' in each_script:
            productKey = re.findall(r'\"productKey\" : \"\w+\"', each_script)[0].split(':')[1].strip().replace('\"', '')
            break
    docId = ''.join(url.split('/')[-1]).split('.')[0]

    # print("productKey : " + str(productKey))
    # print("docId : " + str(docId))
    return {
        'productKey': productKey,
        'docId': docId,
        'news_item': news_item
    }


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
