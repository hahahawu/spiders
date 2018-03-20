import time
import re


def time_formator(date_time):
    # 2017年11月14日16:25
    date_time1 = re.findall(r'\d{4}年\d{2}月\d{2}日\d{2}:\d{2}', date_time.strip())
    if date_time:
        date_time = date_time1[0]
        try:
            time1 = date_time[0:16]
            timeArray = time.strptime(time1, "%Y年%m月%d日%H:%M")
            dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return dt_new
        except ValueError as e:
            print('Excepion : ' + str(e))
            return ''
    else:
        raise ValueError('Wrong time format : ', str(date_time))
