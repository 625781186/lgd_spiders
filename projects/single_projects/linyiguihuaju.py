# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 14:29
# @Author  : LGD
# @File    : linyiguihuaju.py
# @功能    : 爬取临沂市自然资源和规划局的工程许可证信息

import requests
from lxml import etree

url = 'http://gtj.linyi.gov.cn/sjcxy_gcghxkz.jsp?urltype=tree.TreeTempUrl&wbtreeid=2590'

headers = {
    'Host': 'gtj.linyi.gov.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

res = requests.get(url, headers=headers)
print(res.text)

html = etree.HTML(res.text)

ls = html.xpath('//table[@class="biankuang2"]/tr')
print(len(ls))