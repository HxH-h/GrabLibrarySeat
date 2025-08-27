import requests
from constant import *

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import time
from Utils import *


# 返回含有cookie的headers
def getSession():

    options = webdriver.ChromeOptions()
    options.add_argument(rf"--user-data-dir={CONF_PATH}")

    chrome = webdriver.Edge(service=Service(CHROME_PATH), options=options)

    chrome.get(LOGIN_URL)
    # 获取用户名和密码输入框
    username = chrome.find_element(by=By.XPATH, value='//input[@id="un"]')
    password = chrome.find_element(by=By.XPATH, value='//input[@id="pd"]')
    # 填充文本
    username.send_keys(U)
    password.send_keys(P)
    # 延时
    time.sleep(1)

    login = chrome.find_element(by=By.XPATH, value='//a[@id="index_login_btn"]')
    login.click()

    while chrome.current_url != END_URL:
        time.sleep(0.5)

    cookies = chrome.get_cookies()

    headers = {
        'User-Agent': USER_AGENT,
        'Cookie': cookies[0]['name'] + '=' + cookies[0]['value']
    }
    return headers

def get_seats( day , headers):
    params = {
        'libid': 'dlut',
        'userid': USERID ,
        'mapid': KAIFAQU_THIRD,
        'starttime': day['m'],
        'endtime': day['d'] + ' 22:00',
        'number': generate_random_decimal(16)
    }
    url = get_url_with_params(URL_GETSEATLIST ,  params)
    print( url)
    resp = requests.get(url, headers=headers , verify= False).json()

    return resp
#%%

def order_seat(seats , seat_id , day , headers):
    seat = seats['seats'][seat_id - 1]['seatid']

    params = {
        'libid': 'dlut',
        'userid': USERID,
        'seatid': seat,
        'validtime': day['m'],
        'invalidtime': day['d'] + ' 22:00',
        'number': generate_random_decimal(16),
        'time': day['s'],
        'code': ''
    }
    url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
    enc_params = encrypt(url_params)
    url = URL_ORDERSEAT + '?' + enc_params

    ret = requests.post(url, headers=headers , verify= False).json()
    print(ret)

def addSeat(number , headers):

    for i in range(number):
        day = get_datetime(i)
        # 获取座位表
        seats = get_seats(day , headers)
        # 占座
        for seat_id in SEAT_ID:
            day = get_datetime(i)
            order_seat(seats , seat_id , day , headers)
            time.sleep(0.1)



if __name__ == '__main__':
    # 设置日志级别
    logging.basicConfig(level=logging.INFO)

    # 获取session
    headers = getSession()

    while not check_time(6,30):
         pass
    # 占座
    addSeat(2,headers)










