import re, time
import traceback


def timeFormator(date_time):
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', date_time):
        return date_time
    elif re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', date_time.strip().replace('\n', '').replace('  ', ' ')):
        date_time = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', date_time.strip().replace('\n', '')
                               .replace('  ', ' '))[0]
        try:
            time1 = date_time[0:19]
            timeArray = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
            dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return dt_new
        except ValueError as e:
            print('Excepion : ' + str(e))
            return '1970-01-01 00:00:00'
    elif re.match(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2}', date_time.strip().replace('\n', '')):
        date_time = re.findall(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2}', date_time.strip())[0]
        try:
            time1 = date_time[0:20]
            timeArray = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
            dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return dt_new
        except ValueError as e:
            print('Excepion : ' + str(e))
            return '1970-01-01 00:00:00'
    elif re.match(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}', date_time.strip().replace('\n', '')):
        date_time = re.findall(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}', date_time.strip())[0]
        try:
            time1 = date_time[0:17]
            timeArray = time.strptime(time1, "%Y年%m月%d日 %H:%M:%S")
            dt_new = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return dt_new
        except ValueError as e:
            print('Excepion : ' + str(e))
            return '1970-01-01 00:00:00'
    else:
        return '1970-01-01 00:00:00'


def time_transform(create_time):
    try:
        struct_time = time.gmtime(float(create_time) / 1000)
        dt_new = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        return dt_new
    except Exception as e:
        print('time transform error : ', str(create_time))
        msg = traceback.format_exc()
        print(msg)
        return ''
