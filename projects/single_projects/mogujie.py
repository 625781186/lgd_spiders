# -*- coding: utf-8 -*-
# @Time    : 2019/9/24 15:37
# @Author  : LGD
# @File    : mogujie.py
# @功能    : 爬取蘑菇街的裙装商品信息

# 引入内置模块或第三方模块
import requests
import time
import random



headers = {
    'referer': 'https://list.mogu.com/book/skirt/50004?acm=3.mce.1_10_1ko4w.132244.0.sEK23rCYgWO4z.pos_2-m_482172-sd_119&ptp=31.v5mL0b._head.0.QyGfCUKS',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

for i in range(1000):
    url = 'https://list.mogu.com/search?callback=jQuery21107373792688358374_1569310374911&_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop&ad=0&fcid=50004&action=skirt&acm=3.mce.1_10_1ko4w.132244.0.sEK23rCYgWO4z.pos_2-m_482172-sd_119&ptp=31.v5mL0b._head.0.QyGfCUKS&_={}'.format(1569310374912 + 1 + i)
    res = requests.get(url, headers=headers)
    print(res.text)
