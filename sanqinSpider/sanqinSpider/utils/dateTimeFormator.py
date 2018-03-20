import time


def dataTimeFormator(origin_time):
    if not origin_time:
        return ''
    time1 = origin_time[0:16]
    try:
        timeArray = time.strptime(time1, "%Y-%m-%d %H:%M")
        dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return dt_new
    except ValueError:
        print('The format is wrong : '+origin_time)
        return ''
