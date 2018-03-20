import time

#只适用于本网站
def timeFormat1(time1):
    # 转换成时间数组
    time1 = time1[0:16]
    timeArray = time.strptime(time1, "%Y年%m月%d日%H:%M")
    # 转换成新的时间格式(20160505-20:28:54)
    dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return dt_new