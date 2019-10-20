# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/18 19:38
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : selenium233.py
# /***


from selenium import webdriver

import time, random
import pymysql

url = 'https://g.hongshu.com/content/93416/13903995.html'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
infos = driver.find_elements_by_xpath('//div[@class="rdtext"]/p')
# print(infos)
for i in infos:
    print(i)


