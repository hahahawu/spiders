check_value = lambda x: x if x else ''
editor_format = lambda x: x.replace('责任编辑：', '').replace('责编：', '') if x else ''
str_format = lambda x: x.strip().replace('\u3000', '').replace('\xa0', ''). \
    replace("\"", "'").replace('\n', '').replace('\t', ' ') if x else ''
check_int = lambda x: x if x else 0

