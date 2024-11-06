import requests
import constant
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import Utils

# 全局存储cookie
COOKIE = ''
def getSession():
    path = 'msedgedriver.exe'

    chrome = webdriver.Edge(path)
    chrome.get(constant.LOGIN_URL)
    # 获取用户名和密码输入框
    username = chrome.find_element(by=By.XPATH, value='//input[@id="un"]')
    password = chrome.find_element(by=By.XPATH, value='//input[@id="pd"]')
    # 填充文本
    username.send_keys(constant.U)
    password.send_keys(constant.P)
    # 延时
    time.sleep(1)
    # 获取登录按钮并提交
    login = chrome.find_element(by=By.XPATH, value='//a[@id="index_login_btn"]')
    login.click()
    # 设置cookie
    cookie = chrome.get_cookie('PHPSESSID')['value']

    global COOKIE
    COOKIE = 'PHPSESSID=' + cookie
def checkSession():
    headers = {
        'User-Agent': constant.USER_AGENT,
        'Cookie': COOKIE
    }
    resp = requests.post(constant.CHECK_URL, headers=headers).json()
    ret = resp['success']
    Utils.log('CheckCookie: ' + COOKIE +" " + str(ret))
    return ret
def addSeat(date):
    # 获取addCode
    headers = {
        'User-Agent': constant.USER_AGENT,
        'Cookie': COOKIE
    }

    for seat in constant.SEATMAPPING.keys():
        data = {
            'seat_id': seat,
            'order_date': date
        }
        json_data = requests.post(constant.ADDCODE_URL, data=data, headers=headers).json()

        data = {
            'addCode': json_data['data']['addCode'],
            'method': 'addSeat'
        }
        time.sleep(0.3)
        # 返回预约结果
        ret = requests.post(constant.ADDSEAT_URL, data=data, headers=headers).json()
        print(ret)
        if ret['success']:
            Utils.log('预约座位 ' + str(constant.SEATMAPPING[seat]) +' 成功')
            return
        else:
            Utils.log('预约座位 ' + str(constant.SEATMAPPING[seat]) +' 失败 ' + ret['message'])
            # 延时
            time.sleep(0.2)




if __name__ == '__main__':
   # 设置日志级别
   Utils.logging.basicConfig(level=Utils.logging.INFO)
   # 检查session是否过期
   if not checkSession():
       constant.COOKIE = getSession()
   # 占座
   addSeat(Utils.get_time())







