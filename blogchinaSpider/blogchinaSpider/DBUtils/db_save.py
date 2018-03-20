import time

from blogchinaSpider.DBUtils import MD5Utils

from hbase.ttypes import *


def gen_start_spider_info():
    """
    在爬虫开始时记录爬虫开始的时间
    :return:
    """
    now = time.time()
    spider_name = 'blogchina'
    # 让最新的行放在最前面
    row_key = gen_row_key(MD5Utils.md5_code(spider_name), str(10 ** 12 - now))

    name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
    time_column = TColumnValue(b'time', b'start_time', str(now).encode())
    column_values = [name_column, time_column]
    put = TPut(row_key, column_values)

    return row_key, put


def gen_stop_spider_info(row_key):
    """
    在爬虫结束时，记录爬虫结束的时间
    :param row_key:
    :return:
    """
    now = time.time()
    spider_name = 'blogchina'

    name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
    time_column = TColumnValue(b'time', b'stop_time', str(now).encode())
    column_values = [name_column, time_column]
    put = TPut(row_key, column_values)

    return put


def gen_blog_put(blog_item):
    """
    产生博客信息的插入数据库的数据
    :param blog_item:
    :return: rowKey
             put
    """
    blog_info_fml = b'blog_info'
    picture_fml = b'pictures'
    comment_fml = b'comments'

    author_id = blog_item['author_id']
    blog_id = blog_item['blog_id']
    row_key = gen_row_key(MD5Utils.md5_code(author_id), MD5Utils.md5_code(blog_id))

    column_values = []

    # blogInfo 列族的信息
    blog_id_column = TColumnValue(blog_info_fml, b'blog_id', str(blog_id).encode())
    column_values.append(blog_id_column)

    author_id_column = TColumnValue(blog_info_fml, b'author_id', str(blog_item['author_id']).encode())
    column_values.append(author_id_column)

    title_column = TColumnValue(blog_info_fml, b'title', blog_item['title'].encode())
    column_values.append(title_column)

    sub_title_column = TColumnValue(blog_info_fml, b'sub_title', blog_item['sub_title'].encode())
    column_values.append(sub_title_column)

    publish_time_column = TColumnValue(blog_info_fml, b'publish_time', str(blog_item['publish_time']).encode())
    column_values.append(publish_time_column)

    category_column = TColumnValue(blog_info_fml, b'category', blog_item['category'].encode())
    column_values.append(category_column)

    read_num_column = TColumnValue(blog_info_fml, b'read_num', str(blog_item['read_num']).encode())
    column_values.append(read_num_column)

    comment_num_column = TColumnValue(blog_info_fml, b'comment_num', str(blog_item['comment_num']).encode())
    column_values.append(comment_num_column)

    hand_up_num_column = TColumnValue(blog_info_fml, b'hand_up_num', str(blog_item['hand_up_num']).encode())
    column_values.append(hand_up_num_column)

    hand_down_num_column = TColumnValue(blog_info_fml, b'hand_down_num', str(blog_item['hand_down_num']).encode())
    column_values.append(hand_down_num_column)

    content_column = TColumnValue(blog_info_fml, b'content', blog_item['content'].encode())
    column_values.append(content_column)

    picture_url_column = TColumnValue(blog_info_fml, b'picture_urls', str(blog_item['pictures']).encode())
    column_values.append(picture_url_column)

    url_column = TColumnValue(blog_info_fml, b'url', str(blog_item['url']).encode())
    column_values.append(url_column)

    # picture列族的信息
    picture_num = len(blog_item['b_pictures'])
    picture_num_column = TColumnValue(picture_fml, b'picture_num', str(picture_num).encode())
    column_values.append(picture_num_column)

    for x in range(picture_num):
        column_values.append(TColumnValue(picture_fml, str(x).encode(), blog_item['b_pictures'][x]))

    # comment列族的信息
    comment_num = len(blog_item['comment_ids'])
    comment_id_column = TColumnValue(comment_fml, b'comment_num', str(comment_num).encode())
    column_values.append(comment_id_column)

    for x in range(comment_num):
        column_values.append(TColumnValue(comment_fml, str(x).encode(), str(blog_item['comment_ids'][x]).encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_author_put(author_item):
    """
    产生AuthorItem的TPut
    :param author_item:
    :return: rowKey
             TPut
    """
    author_info_fml = b'author_info'
    focuse_fml = b'focuse'
    fans_fml = b'fans'

    author_id = author_item['author_id']
    row_key = MD5Utils.md5_code(author_id).encode()

    column_values = []

    # 产生author_info列族的信息
    author_id_column = TColumnValue(author_info_fml, b'author_id', str(author_item['author_id']).encode())
    column_values.append(author_id_column)

    author_name_column = TColumnValue(author_info_fml, b'author_name', author_item['author_name'].encode())
    column_values.append(author_name_column)

    author_b_name = TColumnValue(author_info_fml, b'author_blog_name', author_item['author_blog_name'].encode())
    column_values.append(author_b_name)

    introduce_column = TColumnValue(author_info_fml, b'introduce', author_item['introduce'].encode())
    column_values.append(introduce_column)

    image_url_column = TColumnValue(author_info_fml, b'image_url', author_item['image'].encode())
    column_values.append(image_url_column)

    b_image_column = TColumnValue(author_info_fml, b'b_image', author_item['b_image'])
    column_values.append(b_image_column)

    article_num_column = TColumnValue(author_info_fml, b'article_num', str(author_item['article_num']).encode())
    column_values.append(article_num_column)

    read_num_column = TColumnValue(author_info_fml, b'read_num', str(author_item['read_num']).encode())
    column_values.append(read_num_column)

    fans_num_column = TColumnValue(author_info_fml, b'fans_num', str(author_item['fans_num']).encode())
    column_values.append(fans_num_column)

    focuse_num_column = TColumnValue(author_info_fml, b'focuse_num', str(author_item['focuse_num']).encode())
    column_values.append(focuse_num_column)

    all_article_column = TColumnValue(author_info_fml, b'all_article_url', str(author_item['all_article_url']).encode())
    column_values.append(all_article_column)

    # 产生focuse列族信息
    focuse_len = len(author_item['focuse'])
    focuse_column = TColumnValue(focuse_fml, b'focuse_num', str(focuse_len).encode())
    column_values.append(focuse_column)

    for x in range(focuse_len):
        column_values.append(TColumnValue(focuse_fml, str(x).encode(), author_item['focuse'][x].encode()))

    # 产生fans列族的信息
    fans_len = len(author_item['fans'])
    fans_column = TColumnValue(fans_fml, b'fans_num', str(fans_len).encode())
    column_values.append(fans_column)

    for x in range(focuse_len):
        column_values.append(TColumnValue(fans_fml, str(x).encode(), author_item['fans'][x].encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_comment_put(comment_item):
    comment_info_fml = b'comment_info'
    praise_info_fml = b'praise_info'

    blog_id = comment_item['comment_blog_id']
    comment_id = comment_item['comment_id']

    row_key = gen_row_key(MD5Utils.md5_code(blog_id), MD5Utils.md5_code(comment_id))

    column_values = []

    # 产生comment_info信息
    comment_id_column = TColumnValue(comment_info_fml, b'comment_id', str(comment_id).encode())
    column_values.append(comment_id_column)

    user_id_column = TColumnValue(comment_info_fml, b'comment_user_id',  str(comment_item['comment_user_id']).encode())
    column_values.append(user_id_column)

    blog_id_column = TColumnValue(comment_info_fml, b'comment_blog_id', str(comment_item['comment_blog_id']).encode())
    column_values.append(blog_id_column)

    comment_time_column = TColumnValue(comment_info_fml, b'comment_time', str(comment_item['comment_time']).encode())
    column_values.append(comment_time_column)

    content_column = TColumnValue(comment_info_fml, b'comment_content', comment_item['comment_content'].encode())
    column_values.append(content_column)

    praise_num_column = TColumnValue(comment_info_fml, b'praise_num', str(comment_item['praise_num']).encode())
    column_values.append(praise_num_column)

    replay_id_column = TColumnValue(comment_info_fml, b'replay_id', str(comment_item['replay_id']).encode())
    column_values.append(replay_id_column)

    ip_column = TColumnValue(comment_info_fml, b'ip', comment_item['ip'].encode())
    column_values.append(ip_column)

    last_ip_column = TColumnValue(comment_info_fml, b'last_ip', comment_item['last_ip'].encode())
    column_values.append(last_ip_column)

    # 产生praiseInfo列族信息
    praise_len = len(comment_item['praise_ids'])
    praise_len_column = TColumnValue(praise_info_fml, b'praise_num', str(praise_len).encode())
    column_values.append(praise_len_column)

    for x in range(praise_len):
        column_values.append(TColumnValue(praise_info_fml,
                                          str(x).encode(),
                                          str(comment_item['praise_ids'][x]).encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_row_key(*strs):
    """
    用下划线'_'拼接字符串，以产生rowKey
    :param strs:
    :return:
    """
    if not strs:
        raise ValueError('产生rowKey传递的参数不能为空!!!')

    result = ''
    for s in strs:
        result = result + s + '_'

    return result[:-1].encode()
