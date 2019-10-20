# # # -*- coding: utf-8 -*-
# # import requests
# # import random
# # import time
# # from lxml import etree
# # import json
# # import pymysql
# # # from gongsi_daili_ip import baidu_ip
# #
# # def get_info():
# #     # for a in range(1, 15):
# #     #     time.sleep(random.random())
# #     url = 'http://gtj.hg.gov.cn/col/col14207/index.html?uid=14973&pageNum=1'
# #     headers = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# #     response = requests.get(url, headers=headers)
# #     # print(response.apparent_encoding)
# #     html = response.content.decode('utf-8')
# #     print(html)
# #     h = etree.HTML(html)
# #     ls = h.xpath('//*[@id="14973"]/div/table/tbody/tr/td/table/tbody/tr')
# #     # ls.pop(0)
# #     print(len(ls))
# #     # for i in ls:
# #     #     try:
# #     #         ca_num = i.xpath('./td[1]/text()')[0]
# #     #     except:
# #     #         ca_num = ''
# #     #     try:
# #     #         ca_time = i.xpath('./td[5]/text()')[0]
# #     #     except:
# #     #         ca_time = ''
# #     #
# #     #     try:
# #     #         pro_name = i.xpath('./td[2]/text()')[0]
# #     #     except:
# #     #         pro_name = ''
# #     #
# #     #     try:
# #     #         jianshe_unit = i.xpath('./td[3]/text()')[0]
# #     #     except:
# #     #         jianshe_unit = ''
# #     #
# #     #     pro_position = ''
# #     #
# #     #     pro_guimo = ''
# #     #
# #     #     region = ''
# #     #     # 爬取时间
# #     #     spider_time = time.strftime("%Y-%m-%d", time.localtime())
# #     #     # url
# #     #     link_url = url
# #     #
# #     #     print(ca_num)
# #     #     print(ca_time)
# #     #     print(pro_name)
# #     #     print(jianshe_unit)
# #     #     print(pro_position)
# #     #     print(pro_guimo)
# #     #     print(region)
# #     #     print(spider_time)
# #     #     print(link_url)
# #     #
# #     #     strsql = "insert into hubei_xianning(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
# #     #         ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region, spider_time, link_url)
# #     #     cur.execute(strsql)
# #     #     conn.commit()
# #
# # get_info()
#
# from selenium import webdriver
# import time
# from multiprocessing import Process
# import random
# import pymysql
#
# conn = pymysql.connect(host='192.168.1.77', port=3306, user='root', password='798236031', db='gongchengguihua',)
# cur = conn.cursor()
#
#
# class Huanggang(object):
#     def __init__(self):
#         super().__init__()
#
#     def get_info(self):
#         driver = webdriver.Chrome()
#         driver.maximize_window()
#         for a in range(1, 61):
#             print('page-----------------------------', a)
#             time.sleep(random.random() * 5)
#             url = 'http://gtj.hg.gov.cn/col/col14207/index.html?uid=14973&pageNum={}'.format(a)
#             driver.get(url)
#             try:
#                 ls = driver.find_elements_by_xpath('//*[@id="14973"]/div/table/tr/td/table//tr')
#                                                  # '//*[@id="14973"]/div/table/tbody/tr/td/table/tbody/tr[3]'
#                                                   # //*[@id="14973"]/div/table/tbody/tr/td/table/tbody/tr
#                 # ls.pop(0)
#                 print(len(ls))
#
#                 for i in ls:
#                     try:
#                         ca_num = i.find_element_by_xpath('./td[1]/a').text
#                     except:
#                         ca_num = ''
#
#                     try:
#                         ca_time = i.find_element_by_xpath('./td[5]').text
#                     except:
#                         ca_time = ''
#
#                     try:
#                         pro_name = i.find_element_by_xpath('./td[3]').text
#                     except:
#                         pro_name = ''
#
#                     try:
#                         jianshe_unit = i.find_element_by_xpath('./td[2]').text
#                     except:
#                         jianshe_unit = ''
#                     try:
#                         pro_position = i.find_element_by_xpath('./td[4]').text
#                     except:
#                         pro_position = ''
#
#                     pro_guimo = ''
#
#                     region = ''
#                     # 爬取时间
#                     spider_time = time.strftime("%Y-%m-%d", time.localtime())
#                     # url
#                     link_url = url
#
#                     sql = "select * from hubei_huanggang where ca_num=%s and ca_time=%s and pro_name=%s and jianshe_unit=%s;"
#                     cur.execute(sql, [ca_num, ca_time, pro_name, jianshe_unit])
#                     num = cur.fetchall()
#                     if len(num) <= 0:
#                         sql = "insert into hubei_huanggang(id,ca_num,ca_time,pro_name,jianshe_unit,pro_position,pro_guimo,region,spider_time,link_url) VALUES (0,'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
#                             ca_num, ca_time, pro_name, jianshe_unit, pro_position, pro_guimo, region, spider_time,
#                             link_url)
#                         print(sql)
#                         cur.execute(sql)
#                         conn.commit()
#
#             except Exception as e:
#                 print(url, e)
#
#
#     def get_run(self):
#         self.get_info()
#
# if __name__ == '__main__':
#     a = Huanggang()
#     p = Process(target=a.get_run())
#     p.start()

import requests
import re
import random
import time
from lxml import etree
import json
import pymysql
# from gongsi_daili_ip import baidu_ip
from multiprocessing import Process


class Huanggang(object):
    def __init__(self):
        super().__init__()

    def get_info(self):
        # for a in range(101):
        #     print('page-------------------------', a)
            # 0*30+1   0*30+30
        url = 'http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={0}&endrecord={1}&perpage=10'.format(0*30+1, 0*30+30)
             # http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=30&perpage=10 1
             # http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=31&endrecord=60&perpage=10 4
             # http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=61&endrecord=90&perpage=10 7
             # http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=91&endrecord=120&perpage=10 9
             # http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=121&endrecord=150&perpage=10 13
             # http://gtj.hg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=151&endrecord=180&perpage=10 16

        headers = {
            'Referer': 'http://gtj.hg.gov.cn/col/col14207/index.html?uid=14973&pageNum=3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }

        data = {
            'col': '1',
            'appid': '1',
            'webid': '40',
            'path': '/',
            'columnid': '14207',
            'sourceContentType': '1',
            'unitid': '14973',
            'webname': '黄冈市自然资源和规划局',
            'permissiontype': '0',
        }

        response = requests.post(url, headers=headers, data=data)
        print(response.text)
        pat1 = re.compile(r'')
        pat = re.compile(r'target="_blank">(.*?)</ a></td>', re.M | re.S)
        res = pat.findall(response.text)
        print(res)
        # html = response.text
        #
        # pat = re.compile(r'<tr>(.*?)</tr>', re.M | re.S)
        # # pat = re.compile(r'<td align="left">(.*?)</a></td>', re.M | re.S)
        #
        # res = pat.findall(html)
        # print('----------------------------------------------------------------', res, '----------------------------------------------')
        # for i in res:
        #     print(i, '======================================================================================================================================')
        #     # a = re.compile(r'"target"="_blank">(.*?)</ a></td>', re.M | re.S)
        #     a = re.compile(r'target="_blank">(.*?)</ a></td>', re.M | re.S)
        #     # r"target"="_blank">(.*?)</ a></td>
        #     a1 = a.findall(i)
        #     print(a1)


    def get_run(self):
        self.get_info()


if __name__ == '__main__':
    a = Huanggang()
    p = Process(target=a.get_run())
    p.start()
