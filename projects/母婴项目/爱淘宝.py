# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/18 19:54
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : 爱淘宝.py
# /***
 
import requests
import re
import json

url = 'https://ai.taobao.com/search/index.htm?pid=mm_26632324_6844396_107180700473&unid=&source_id=search&key=%E7%AB%A5%E8%A3%85&b=sousuo_ssk&clk1=29e4cdd161a46b0161fe9d79f22a0b0e&prepvid=200_11.24.49.55_430_1566129460476&spm=a231o.7712113%2Fg.a3342.1'

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    # 'Referer': 'https://ai.taobao.com/search/index.htm?prepvid=200_11.27.158.35_406_1566129356408&extra=&spm=a231o.7076277%2Fb.1998549605.330.39134608fLFu2N&key=%E7%AB%A5%E8%A3%85&pid=mm_26632324_6844396_107180700473&clk1=29e4cdd161a46b0161fe9d79f22a0b0e&unid=&source_id=&app_pvid=200_11.27.158.35_406_1566129356408',
}

res = requests.get(url, headers= headers, verify=False)
# print(res.text)
html = res.text.replace(' ', '')
# print(html)
pat = re.compile(r'var _pageResult = (.*?)<div class="waterfall-bg">', re.M | re.S)
ls = pat.findall(res.text)
ls = ls[0].replace(';\r\n\r\n</script>', '').replace('\r\n', '')
ls = json.loads(ls)
print(type(ls), ls)
infos = ls['result']['p4ptop']
for i in infos:
    print(i)
print(len(infos))
# for i, j in ls['result'].items():
#     print(i, j)


