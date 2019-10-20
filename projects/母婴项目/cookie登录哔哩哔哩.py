# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 19:41
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : cookie登录哔哩哔哩.py
# /***

import time
import random
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.bilibili.com/'

# bsource=seo_baidu;
# _uuid=3E728CD7-1BE8-6086-48E0-E2C58BD0581907895infoc;
# buvid3=A9FC794F-DAD1-417A-9F7F-322A19D6C10D155807infoc;
# LIVE_BUVID=AUTO6515663879122776;
# sid=iirpj10b;
# DedeUserID=240400161;
# DedeUserID__ckMd5=42eef4d47f9889ac;
# SESSDATA=9d2f2fd2%2C1568979984%2C7840fc81;
# bili_jct=0241d3469667b3b2c96a63e97f7dd89c

# bsource=seo_baidu;
# _uuid=3E728CD7-1BE8-6086-48E0-E2C58BD0581907895infoc;
# buvid3=A9FC794F-DAD1-417A-9F7F-322A19D6C10D155807infoc;
# LIVE_BUVID=AUTO6515663879122776;
# sid=iirpj10b

# _uuid=3E728CD7-1BE8-6086-48E0-E2C58BD0581907895infoc; buvid3=A9FC794F-DAD1-417A-9F7F-322A19D6C10D155807infoc; LIVE_BUVID=AUTO6515663879122776; sid=iirpj10b; DedeUserID=240400161; DedeUserID__ckMd5=42eef4d47f9889ac; SESSDATA=e78f658e%2C1568980502%2C25d56381; bili_jct=c3bfc08982579a015abd38b1fd68d60d

cookies = {
    '_uuid': '3E728CD7-1BE8-6086-48E0-E2C58BD0581907895infoc',
    'buvid3': 'A9FC794F-DAD1-417A-9F7F-322A19D6C10D155807infoc',
    'LIVE_BUVID':'AUTO6515663879122776',
    'sid': 'iirpj10b',
    'DedeUserID': '240400161',
    'DedeUserID__ckMd5': '42eef4d47f9889ac',
    'SESSDATA': 'e78f658e%2C1568980502%2C25d56381',
    'bili_jct': 'c3bfc08982579a015abd38b1fd68d60d',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Cookie': '_uuid=3E728CD7-1BE8-6086-48E0-E2C58BD0581907895infoc; buvid3=A9FC794F-DAD1-417A-9F7F-322A19D6C10D155807infoc; LIVE_BUVID=AUTO6515663879122776; sid=iirpj10b; DedeUserID=240400161; DedeUserID__ckMd5=42eef4d47f9889ac; SESSDATA=e78f658e%2C1568980502%2C25d56381; bili_jct=c3bfc08982579a015abd38b1fd68d60d; UM_distinctid=16cb420eb88229-08b445638d53fc-7373e61-15f900-16cb420eb891ab; CNZZDATA2724999=cnzz_eid%3D707668139-1566386485-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1566386485',

# 'Host': 'www.bilibili.com',
}

res = requests.get('https://space.bilibili.com/240400161', headers=headers, verify=False)
print(res.text)

# driver = webdriver.Chrome()
# driver.get(url)
# cookies = driver.get_cookies()
# driver.delete_all_cookies()

# for i, j in cookies.items():
#     print(i, j)
#     driver.add_cookie({'name': i, 'value': j})
# coo = driver.get_cookies()
# driver.get(url)
# for k in coo:
#     print(k)



 


