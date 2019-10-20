# -*- coding: utf-8 -*-
import requests
import random
import time
from lxml import etree
import json
# import demjson
import pymysql
# from gongsi_daili_ip import baidu_ip



def get_url():
    url = 'http://api.fsmap.com.cn/GTGHService/home/SearchData'
    data = {
        'strWhere': '%2C%2C%2C',
        'action': 'ydgh',
        'area': '',
        'pageIndex': '1',
        'pageSize': '15'
    }
    response = requests.post(url, data=data)
    html = response.text
    print(html)
    datas_json = json.loads(html)
    print(datas_json)
    print(type(datas_json))
    datas = json.loads(datas_json['datas'])
    for i in datas:
        link = i['4']
        # 'http://api.fsmap.com.cn/GTGHService/ViewCase/ydghxkz/1c890ad1-6d81-4925-b6f4-0b9e09cff55e'
        print(link)


get_url()