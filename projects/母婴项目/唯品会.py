# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 11:02
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : 唯品会.py
# /***

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
import random

url = 'https://category.vip.com/suggest.php?keyword=%E8%BF%9E%E8%A1%A3%E8%A3%99&ff=235|12|1|1'


chrome_op = Options()
chrome_op.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_op)
# driver = webdriver.PhantomJS()
# driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
time.sleep(random.random())
for i in range(2):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(random.random() * 0.5)
time.sleep(random.random() * 3)
html = etree.HTML(driver.page_source)
# print(type(driver.page_source))
# print(html)
ls = html.xpath('//section[@id="J_searchCatList"]/div[@class="goods-list-item  c-goods  J_pro_items"]')
print(len(ls))
for i in ls:
    title = i.xpath('.//h4[@class="goods-info goods-title-info"]/a/@title')[0]
    url = i.xpath('.//h4[@class="goods-info goods-title-info"]/a/@href')[0]
    price = i.xpath('.//span[@class="title"]/text()')[0]
    print(title)
    print(price)
    print('https:' + url)
    print('==============================')
# print(html)

# headers = {
#     'Cookie': 'vip_address=%257B%2522pid%2522%253A%2522104101%2522%252C%2522cid%2522%253A%2522104101101%2522%252C%2522pname%2522%253A%2522%255Cu6cb3%255Cu5357%255Cu7701%2522%252C%2522cname%2522%253A%2522%255Cu90d1%255Cu5dde%255Cu5e02%2522%257D; vip_province=104101; vip_province_name=%E6%B2%B3%E5%8D%97%E7%9C%81; vip_city_name=%E9%83%91%E5%B7%9E%E5%B8%82; vip_city_code=104101101; vip_wh=VIP_HZ; vip_ipver=31; mars_pid=0; _smt_uid=5d515d75.554b70fa; cps=adp%3Ag1o71nr0%3A%3A%3A%3A; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0; mars_sid=dfb1dc07658b48b2976171757a38ce54; visit_id=785763904EF6A3F9B5C0A8E2D35F8EFF; _jzqco=%7C%7C%7C%7C%7C1.1580080013.1565613429237.1566183624040.1566183641563.1566183624040.1566183641563.0.0.0.5.5; mars_cid=1565613428991_b67fa8c883114989684ec32f7cd73f63',
#     'Host': 'category.vip.com',
#     'Referer': 'https://kid.vip.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
# }
#
# res = requests.get(url, headers=headers, verify=False)
# print(res.text)


# html = etree.HTML(res.text)
# ls = html.xpath('//section[@class="goods-list"]/div[@class="goods-list-item  c-goods  J_pro_items"]')
# print(len(ls))


