import logging
import random
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote

# 打印日志
def log(message):
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + message)

# 生成随机数
def generate_random_decimal(decimal_places):

    # 生成0到1之间的随机数
    random_num = random.random()

    # 保留指定的小数位数
    # 使用round函数进行四舍五入
    result = round(random_num, decimal_places)

    return result

def get_datetime(offset_days: int = 0) -> dict:
    target_time = datetime.now() + timedelta(days=offset_days)
    ret = {
        's': target_time.strftime('%Y-%m-%d %H:%M:%S'),
        'm': target_time.strftime('%Y-%m-%d %H:%M'),
        'd': target_time.strftime('%Y-%m-%d')
    }
    return ret


# 自定义拼接参数
def custom_quote(s, safe='/', encoding=None, errors=None):
    return quote(s, safe=safe + ':', encoding=encoding, errors=errors)
def get_url_with_params(url , params):
    return url + "?" + urlencode(params, quote_via=custom_quote)

# 检查时间
def check_time(hour: int, minute: int = 0):
    now = time.localtime()
    current_hour = now.tm_hour
    current_minute = now.tm_min
    # 先比较小时，再比较分钟
    if current_hour > hour or (current_hour == hour and current_minute >= minute):
        return True
    else:
        return False


# 编码
def encrypt(text: str, key: str = "wx3cba883abac619bb") -> str:
    t = ["", "g", "h", "i"]
    result = []
    n = 0
    for ch in text:
        r = ord(ch) + 2
        if n >= len(key):
            n = 0
        r += ord(key[n])
        o = hex(r)[2:]  # 去掉 "0x"
        if len(o) < 4:
            o = t[4 - len(o)] + o
        result.append(o.lower())
        n += 1
    return "".join(result)

# 解码
def decrypt(cipher: str, key: str = "wx3cba883abac619bb") -> str:
    # 先把补位替换回来
    cipher = cipher.replace("g", "000").replace("h", "00").replace("i", "0")
    result = []
    a = 0
    for n in range(0, len(cipher), 4):
        s = cipher[n:n+4]
        r = int(s, 16)
        if a >= len(key):
            a = 0
        r -= ord(key[a])
        result.append(chr(r - 2))
        a += 1
    return "".join(result)

