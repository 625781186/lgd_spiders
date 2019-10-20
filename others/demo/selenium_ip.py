# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 10:40
# @Author  : LGD
# @File    : selenium_ip.py
# @功能    : 为selenium设置代理ip


import requests
import json
from selenium import webdriver
import time

# 代理ipAPI
# url_get_ip = 'http://api.wandoudl.com/api/ip?app_key=e0ca7c110077909c8ef620620db92c98&pack=0&num=1&xy=2&type=2&lb=\r\n&port=4&mr=1&'
url_get_ip = 'http://api.wandoudl.com/api/ip?app_key=e0ca7c110077909c8ef620620db92c98&pack=0&num=1&xy=3&type=2&lb=\r\n&port=4&mr=1&'

headers_ip = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

ip_str = requests.get(url_get_ip, headers=headers_ip)
ip_json = json.loads(ip_str.text)
ip = str(ip_json['data'][0]['ip']) + ':' + str(ip_json['data'][0]['port'])
print(ip)

chromeOptions = webdriver.ChromeOptions()

# # 设置代理
# chromeOptions.add_extension(proxy=ip)
chromeOptions.add_argument("--proxy-server=http://{0}".format(ip))
# chromeOptions.add_argument('disable-infobars')
# chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(options=chromeOptions)

# 查看本机ip，查看代理是否起作用
# browser.get("https://detail.tmall.com/item.htm?id=586629417046")
# browser.get("https://www.baidu.com")
browser.get("39.156.66.18")
print(browser.get_cookies())
# print(browser.page_source)
time.sleep(20)
# 退出，清除浏览器缓存
browser.quit()



