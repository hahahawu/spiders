import time


def timeFormat(datetime):
    # 转换成时间数组
    time1 = datetime[0:20]
    try:
        timeArray = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
    except ValueError as e:
        timeArray = time.strftime(time1, " %Y-%m-%d %H:%M:%S")
    # 转换成新的时间格式(20160505-20:28:54)
    dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return dt_new
