import requests
from constant import *

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import time
import Utils

# 全局存储cookie
COOKIE = ''

headers = {
        'User-Agent': USER_AGENT,
        'Cookie': COOKIE
}
def getSession():

    path = './msedgedriver.exe'
    
    chrome = webdriver.Edge(service=Service(path))

    chrome.get(LOGIN_URL)
    # 获取用户名和密码输入框
    username = chrome.find_element(by=By.XPATH, value='//input[@id="un"]')
    password = chrome.find_element(by=By.XPATH, value='//input[@id="pd"]')
    # 填充文本
    username.send_keys(U)
    password.send_keys(P)
    # 延时
    time.sleep(1)
    # 获取登录按钮并提交
    login = chrome.find_element(by=By.XPATH, value='//a[@id="index_login_btn"]')
    login.click()
    # 设置cookie
    cookie = chrome.get_cookie('ASPSESSIONIDAQDCTBDD')['value']

    global COOKIE
    COOKIE = 'ASPSESSIONIDAQDCTBDD=' + cookie
def checkSession():
    headers = {
        'User-Agent': USER_AGENT,
        'Cookie': COOKIE
    }
    resp = requests.post(CHECK_URL, headers=headers).json()
    ret = resp['success']
    Utils.log('CheckCookie: ' + COOKIE +" " + str(ret))
    return ret
def get_seats():
    params = {
        'libid': 'dlut',
        'userid': USERID ,
        'mapid': KAIFAQU_THIRD,
        'starttime': Utils.get_datatime(),
        'endtime': Utils.get_date() + ' 22:00',
        'number': Utils.generate_random_decimal(16)
    }
    url = Utils.get_url_with_params(URL_GETSEATLIST ,  params)
    print( url)
    resp = requests.get(url, headers=headers , verify= False).json()

    return resp
seats = get_seats()
#%%

def order_seat(seat_id):
    seat = seats['seats'][seat_id - 1]['seatid']

    params = {
        'libid': 'dlut',
        'userid': USERID,
        'seatid': seat,
        'validtime': Utils.get_datatime(),
        'invalidtime': Utils.get_date() + ' 22:00',
        'number': Utils.generate_random_decimal(16),
        'time': Utils.get_datatime_second(),
        'code': ''
    }
    url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
    print(url_params)
    enc_params = Utils.encrypt(url_params)
    url = URL_ORDERSEAT + '?' + enc_params
    print(url)
    ret = requests.post(url, headers=headers , verify= False).json()
    print( ret)

order_seat(277)



if __name__ == '__main__':
   # 设置日志级别
   Utils.logging.basicConfig(level=Utils.logging.INFO)
   # while not Utils.check_time(6,30):
   #      pass
   # 检查session是否过期
   if not checkSession():
       COOKIE = getSession()

   # 占座
   #for day in Utils.get_time():
   #    addSeat(day)








