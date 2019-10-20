# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 15:46
# @Author  : LGD
# @File    : stations_infos.py
# @功能    : 获取最新的车站编号信息


import requests
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9110'
html_text = requests.get(url).text

# 去掉文本总最后多余的两个符号，并以@符号进行分割，第一项不是有用的信息
infos = html_text[:-2].split("@")[1:]
stations = {}
for info in infos:
    station_list = info.split("|")
    # 将车站的代码作为键,汉字，全拼，简拼作为值
    stations[station_list[2]] = {'cn': station_list[1], 'qp': station_list[3], 'jp': station_list[4]}
for k, v in stations.items():
    print(k, v)
