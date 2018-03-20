import time
import re


def timeFormat(datetime):
    if re.match(r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})', datetime):
        # 处理格式为 2017年10月10日 14:23:45的时间
        datetime = re.findall(r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})', datetime)[0]
        time1 = datetime[0:20]
        try:
            timeArray = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
            dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return dt_new
        except ValueError as e:
            return None
    elif re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', datetime.strip()):
        # 处理格式为 2017-10-10 14:23:45的时间
        return re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', datetime.strip())[0]
    elif re.match(r'^(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2})$', datetime):
        # 处理格式为 2017年10月10日 14:23的时间
        time1 = datetime[0:17]
        try:
            timeArray = time.strptime(time1, "%Y年%m月%d日 %H:%M")
            dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return dt_new
        except ValueError as e:
            return None
    else:
        return None
