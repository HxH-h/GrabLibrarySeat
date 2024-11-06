import logging
import time


def log(message):
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + message)

def get_time():
    # 获取当前时间
    now = time.localtime()

    # 格式化日期，个位数日期不输出前导零
    year = now.tm_year
    month = now.tm_mon
    day = now.tm_mday if now.tm_mday >= 10 else str(now.tm_mday)

    formatted_date = f"{year}/{month:02d}/{day}"

    return formatted_date