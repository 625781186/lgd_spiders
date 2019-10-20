# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 21:38
# @Author  : LGD
# @File    : jingdong_1.py
# @功能    : 获取京东评论

import time
import requests

# 蘑菇代理的隧道订单
appKey = "Z1ZxZGZvZzVoSFI2aU1aNTo1M2xNQXZjdlRvbFBZTjV1"

# 蘑菇隧道代理服务器地址
ip_port = 'secondtransfer.moguproxy.com:9001'

# 代理协议
proxy = {"https": "https://" + ip_port}


headers = {
    'Proxy-Authorization': 'Basic ' + appKey,
    'Referer': 'https://item.jd.com/100006808184.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

for i in range(100):
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv5721&productId=100006808184&score=0&sortType=5&page={0}&pageSize=10&isShadowSku=0&fold=1'.format(i)
    try:
        res = requests.get(url, headers=headers, proxies=proxy, verify=False)
        print(res.text)

    except Exception as e:
        print(e)
    print('==========', i)
    time.sleep(1)