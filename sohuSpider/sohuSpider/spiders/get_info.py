from scrapy import Selector

from sohuSpider.items import *
from sohuSpider.util.tools import *
from sohuSpider.util.time_formator import *


def get_news_div1_info(response):
    sel = Selector(response)
    url = response.url
    news_item = NewsItem()

    # article_id & url
    article_id = url.split('/')[-1].split('?')[0]
    news_item['article_id'] = check_value(article_id) + '_suohu_news'
    news_item['url'] = check_value(url)

    # path_text & path_href
    path_xpath = '//div[@class="location area"]//a'
    path_text, path_href = get_path_info(response, path_xpath)
    news_item['path_text'] = path_text
    news_item['path_href'] = path_href

    # keywords
    keywords = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['keywords'] = check_value(keywords)

    # description
    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = str_format(check_value(description))

    # source
    source = sel.xpath('//meta[@name="mediaid"]/@content').extract_first()
    news_item['source'] = check_value(source)

    # title
    title = sel.xpath('//title').xpath("string(.)").extract_first()
    news_item['title'] = check_value(title).split('_')[0]

    # date_time
    date_time_num = sel.xpath('//span[@id="news-time"]/@data-val').extract_first()
    news_item['date_time'] = time_transform(check_int(date_time_num))

    # content
    content_div = sel.xpath('//*[@id="mp-editor"]/p').xpath("string(.)").extract()
    content = ''
    for each_p in content_div:
        content += each_p
    news_item['content'] = str_format(content)

    # picture_url
    picture_div = sel.xpath('//*[@id="mp-editor"]/p[@class="detailPic"]/table//img/@src').extract()
    picture_url_list = []
    for picture in picture_div:
        picture_url_list.append(picture)
    picture_url = ';'.join(picture_url_list)
    news_item['picture_url'] = picture_url

    news_item['join_count'] = 0
    news_item['reply_count'] = 0
    news_item['comment_ids'] = ''

    return news_item


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
